# Backend & Cloud Operations

!!! info "Audience"
    Technical Administrators monitoring and maintaining the DeVILSona AWS infrastructure.

This page explains how to navigate the AWS Console to verify the health of the DeVILSona backend, check DynamoDB data, verify Lambda execution, and handle Terraform state issues.

---

## Navigating the AWS Console

### Login & Region Selection

1. Log in to the AWS Console: [https://console.aws.amazon.com](https://console.aws.amazon.com)
2. In the top-right region selector, ensure you are in **US East (Ohio) — us-east-2**

!!! warning
    DeVILSona's infrastructure is deployed to `us-east-2`. If you are viewing another region, you will not see any resources.

### Finding DeVILSona Resources

| Resource | Service | Name/Identifier |
|----------|---------|-----------------|
| REST API | **API Gateway** | `FSE100-Session-API` |
| Save Lambda | **Lambda** | `FSE100_SaveSession` |
| Login Lambda | **Lambda** | `FSE100_Login` |
| Session database | **DynamoDB** | `StudentSessions` |
| IAM execution role | **IAM → Roles** | `FSE100_Lambda_ExecutionRole` |

Use the AWS **Resource Groups** feature or simply navigate directly to each service via the console navigation.

---

## Monitoring DynamoDB

### Accessing the StudentSessions Table

1. In the AWS Console, navigate to **DynamoDB → Tables**
2. Click on **`StudentSessions`**
3. Click **"Explore table items"** to view stored data

### Verifying the Table Schema

Confirm the table has the correct key schema:

| Key | Role | Type |
|-----|------|------|
| `StudentID` | Partition Key | Number |
| `SessionID` | Sort Key | String |

!!! warning "Note on Schema Discrepancy"
    The `AWS-Save-System.md` legacy documentation describes the sort key as `"SessionKey"` (a compound string like `"0001#Mike#1"`), while the `AWS-Terraform.md` configuration uses `"SessionID"` as a simple string. The Terraform-deployed schema (`SessionID` as sort key) is the authoritative schema for the current deployment. Verify which schema is active before troubleshooting login issues.

### Checking Table Health Metrics

From the table detail page:

1. Click the **"Monitor"** tab
2. Review:
   - **Read/Write capacity consumed:** Should show spikes during class sessions and be near zero otherwise
   - **Throttled requests:** Any value above 0 indicates the table was overwhelmed—this is unlikely with PAY_PER_REQUEST billing mode but possible during extreme bursts
   - **Item count:** Tracks how many session records exist

### Querying Specific Student Records

To look up a specific student's data (e.g., to debug a "progress not loading" issue):

1. In **Explore table items**, click **"Query"**
2. Set `StudentID` (Partition Key) = the student's ASUID (as a Number)
3. Click **Run**

If the student has any saved sessions, their records will appear. If no records appear, either:

- The student hasn't logged in and created a save yet
- The ASUID entered is incorrect
- The save operation failed (check Lambda logs)

### Manually Editing or Deleting Records

For recovery purposes (e.g., a student's progress got corrupted), you can manually edit or delete DynamoDB items:

1. Find the item in **Explore table items**
2. Click the item to open it
3. Click **"Edit item"** to modify field values, or **"Delete item"** to remove it

!!! warning
    Only modify data as a last resort. Always communicate with the student and their instructor before changing their session progress.

### Billing Mode

The table uses **PAY_PER_REQUEST** billing:

- No pre-provisioned capacity needed
- Cost scales linearly with actual reads/writes
- For typical FSE100 use (dozens of students per semester), costs are negligible (cents per month)

---

## Verifying Lambda Execution

### Accessing Lambda Functions

1. Navigate to **Lambda → Functions** in the AWS Console
2. You should see `FSE100_SaveSession` and `FSE100_Login`
3. Click either function to view its configuration

### Checking Lambda Configuration

For each Lambda function, verify:

| Setting | Expected Value |
|---------|---------------|
| **Runtime** | `Node.js 22.x` |
| **Handler** | `index.handler` |
| **Timeout** | Default (3s) — sufficient for DynamoDB operations |
| **Execution Role** | `FSE100_Lambda_ExecutionRole` |
| **Environment Variables** | `TABLE_NAME = StudentSessions`, `STAGE = dev` |

### Checking Lambda Execution Logs (CloudWatch)

Lambda automatically logs to **CloudWatch Logs**.

1. In the Lambda function detail page, click the **"Monitor"** tab
2. Click **"View CloudWatch logs"**
3. You will see a log group named `/aws/lambda/FSE100_SaveSession` or `/aws/lambda/FSE100_Login`
4. Click on a recent **Log Stream** (streams are grouped by Lambda container instance + time)

**Reading the logs:**

Each Lambda invocation produces a log entry. The Node.js functions use `console.log()` extensively, so you will see:

For a login request:
```
=== Login event ===
{"body":"{\"StudentID\":1234567890,\"SessionID\":\"0001\"}", ...}
```

For a save request:
```
=== SaveSession event ===
{"body":"{\"StudentID\":1234567890,...}", ...}
```

If a request fails, the logs will show the error with a stack trace.

### Lambda Metrics

In the **Monitor** tab, review:

- **Invocations:** Number of times the function was called
- **Duration:** Execution time per invocation (should be well under 1 second for normal DynamoDB operations)
- **Error count:** Any non-zero value indicates failures—drill into CloudWatch logs for details
- **Throttles:** Occurs if Lambda concurrency limits are hit (unlikely at this usage scale)

### Testing Lambda Directly

You can manually invoke a Lambda function for testing without needing to go through the headset:

1. In Lambda function detail, click the **"Test"** tab
2. Create a new test event with a sample JSON body:
```json
{
  "body": "{\"StudentID\": 9999, \"SessionID\": \"test\"}"
}
```
3. Click **"Test"** and view the response

A successful login response looks like:
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"ok\":true,\"exists\":false,\"sessions\":[]}"
}
```

---

## API Gateway Health Check

### Verifying API Routes

1. Navigate to **API Gateway** in the AWS Console
2. Click on **`FSE100-Session-API`**
3. Under **Routes**, verify:
   - `POST /session` is configured and integrated with `FSE100_SaveSession`
   - `POST /login` is configured and integrated with `FSE100_Login`
   
4. Click on a route to view its integration and check the Lambda ARN is correct

### Obtaining the API URL

1. In API Gateway → click the API name → **Stages**
2. The **`$default`** stage URL is the base URL for all requests
3. Full URLs:
   - Save: `<base_url>/session`
   - Login: `<base_url>/login`

### Testing the API Endpoint Directly

From any terminal with internet access:
```powershell
# Test login endpoint (should return 200 with exists: false for a new student)
curl -X POST https://<id>.execute-api.us-east-2.amazonaws.com/login `
  -H "Content-Type: application/json" `
  -d '{"StudentID": 9999, "SessionID": "test"}'
```

---

## Understanding Terraform State Alignment

### What Is Terraform State?

Terraform maintains a **state file** (`terraform.tfstate`) that records the mapping between the configuration files you wrote and the actual AWS resources that were created. Every `terraform apply` updates this file.

### State File Location

The state file is stored **locally** on the machine running DeVILStarter, in the `DeVILSona-infra` Terraform project directory.

!!! warning "This is a critical single point of failure."
    If the state file is on one machine and that machine is replaced, is lost, or the state file is accidentally deleted, Terraform loses awareness of the currently deployed infrastructure.

### What Happens If State Is Out of Sync

If the state file does not match the real AWS resources (e.g., state file was lost, or AWS resources were manually changed in the console), the following problems can occur:

| Scenario | Symptoms | Risk |
|----------|----------|------|
| State file lost but resources still running | `terraform plan` shows "8 to add" even though they already exist. Running `apply` will fail due to duplicate resource names. | Medium |
| Resource manually deleted in AWS but state shows it as existing | `terraform plan` shows the resource as "needs no changes." `terraform apply` will try to reference the deleted resource and may error. | Medium |
| State file corrupted | Various Terraform errors; may require manual remediation. | High |

### Recovering from Lost State

If the state file is lost but AWS resources are still running:

1. **Do not run `terraform apply` yet.**
2. Instead, use `terraform import` to bring existing resources into the state file:
```bash
# Example: import the DynamoDB table
terraform import aws_dynamodb_table.student_sessions StudentSessions

# Example: import the API
terraform import aws_apigatewayv2_api.session_api <api-id-from-aws-console>
```
3. Repeat for each resource. This is tedious but recoverable.

4. **Alternatively:** Run `terraform destroy` to tear down all resources (if the API ID is known, or manually delete resources in the AWS Console), then run `terraform apply` fresh.

### Preventing State Loss — Recommended Best Practice

For production hardiness, migrate the state file to **AWS S3 + DynamoDB remote state**:

```hcl
# In main.tf, add a backend configuration:
terraform {
  backend "s3" {
    bucket         = "devilsona-terraform-state"
    key            = "infra/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

This stores the state file in S3 (durable, versioned) and uses DynamoDB for state locking (prevents simultaneous runs). This is a recommended future improvement—see [Known Issues & Roadmap](../developer-guide/known-issues-roadmap.md).

---

## Cost Estimation

For reference, the typical monthly cost for this infrastructure at FSE100 scale:

| Service | Estimated Monthly Cost |
|---------|----------------------|
| Lambda (millions of free requests included) | ~$0.00 |
| API Gateway | ~$0.01–$0.10 (based on ~1,000–10,000 requests/semester) |
| DynamoDB (PAY_PER_REQUEST) | ~$0.01–$0.25 (a few hundred items, minimal reads) |
| CloudWatch Logs | ~$0.01–$0.05 |
| **Total (while running)** | **< $0.50/month** |
| **When torn down (destroy)** | **$0.00** |

!!! note
    The biggest cost lever is ensuring DeVILStarter's "Stop Infrastructure" is run after each class session. Leaving the infrastructure running 24/7 for a month costs less than $1 regardless, making this a very economical system.

---

➡️ **Next:** [Logging & Incident Response](logging-incident-response.md)
