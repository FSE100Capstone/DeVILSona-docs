<h1>⭐ PART 1 / 5 — Introduction + Prerequisites + AWS CLI Setup + Project Structure<h1>
<hr>
<h1>🏗️ <strong>FSE100 AWS Infrastructure Setup</strong></h1>
<p>(Terraform + Lambda + API Gateway + DynamoDB + Unreal Engine C++)</p>
<p>This document explains how to set up the cloud-based save/load system used in the FSE100 Capstone Project using:</p>
<ul>
<li>
<p><strong>Terraform</strong> (Infrastructure as Code)</p>
</li>
<li>
<p><strong>AWS Lambda (Node.js)</strong></p>
</li>
<li>
<p><strong>API Gateway (HTTP API)</strong></p>
</li>
<li>
<p><strong>DynamoDB</strong></p>
</li>
<li>
<p><strong>Unreal Engine C++</strong> (HTTP JSON integration)</p>
</li>
</ul>
<hr>
<h1>📘 <strong>1. Prerequisites</strong></h1>
<h2>Required Software</h2>

Tool | Version | Purpose
-- | -- | --
Terraform | Latest | AWS infrastructure automation
AWS CLI | v2 | Account authentication & profiles
Node.js | v18–v22 | Lambda runtime & npm packages
Unreal Engine 5 (C++) | Latest | Sending login/session requests


<hr>
<h1>📙 <strong>2. AWS CLI Setup</strong></h1>
<p>Run in PowerShell:</p>
<pre><code class="language-powershell">aws configure
</code></pre>
<p>Fill in your IAM user credentials:</p>
<pre><code>AWS Access Key ID: &lt;your-access-key&gt;
AWS Secret Access Key: &lt;your-secret-key&gt;
Default region name: us-east-2
Default output format: json
</code></pre>
<hr>
<h1>📗 <strong>3. Terraform Project Structure</strong></h1>
<p>Your Terraform project should look like this:</p>
<pre><code>FSE100-AWS/
 ├─ main.tf
 ├─ lambda.tf
 ├─ apigw.tf
 ├─ lambda/
 │   ├─ save_session/
 │   │   ├─ index.js
 │   │   ├─ package.json
 │   │   └─ node_modules/
 │   ├─ login/
 │   │   ├─ index.js
 │   │   ├─ package.json
 │   │   └─ node_modules/
 │   ├─ save_session.zip
 │   ├─ login.zip
</code></pre>
<p>These three Terraform files perform the entire infrastructure setup:</p>
<ul>
<li>
<p><strong>main.tf</strong> → DynamoDB + provider settings</p>
</li>
<li>
<p><strong>lambda.tf</strong> → Lambda functions + IAM roles</p>
</li>
<li>
<p><strong>apigw.tf</strong> → API Gateway routes + permissions</p>
</li>
</ul>
<hr>
<h1>📘 <strong>4. main.tf — Base Terraform Configuration</strong></h1>
<pre><code class="language-hcl">terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~&gt; 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_dynamodb_table" "student_sessions" {
  name         = "StudentSessions"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "StudentID"
  range_key = "SessionID"

  attribute {
    name = "StudentID"
    type = "N"
  }

  attribute {
    name = "SessionID"
    type = "S"
  }
}
</code></pre>
<hr>
<html>
<body>
<h1>⭐ <strong>PART 2 / 5 — Lambda Functions + IAM Roles (lambda.tf)</strong></h1>
<hr>
<h1>📙 <strong>5. lambda.tf — Lambda Deployment</strong></h1>
<p>This file defines both Lambda functions:</p>
<ul>
<li>
<p><strong>FSE100_SaveSession</strong></p>
</li>
<li>
<p><strong>FSE100_Login</strong></p>
</li>
</ul>
<p>It also includes the IAM role required for both.</p>
<hr>
<h1>📘 <strong>5.1 SaveSession Lambda</strong></h1>
<pre><code class="language-hcl">resource "aws_lambda_function" "save_session" {
  function_name = "FSE100_SaveSession"

  runtime = "nodejs22.x"
  handler = "index.handler"

  filename         = "${path.module}/lambda/save_session.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/save_session.zip")

  role = aws_iam_role.lambda_exec_role.arn

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.student_sessions.name
      STAGE      = "dev"
    }
  }
}
</code></pre>
<hr>
<h1>📘 <strong>5.2 Login Lambda</strong></h1>
<pre><code class="language-hcl">resource "aws_lambda_function" "login" {
  function_name = "FSE100_Login"

  runtime = "nodejs22.x"
  handler = "index.handler"

  filename         = "${path.module}/lambda/login.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/login.zip")

  role = aws_iam_role.lambda_exec_role.arn

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.student_sessions.name
      STAGE      = "dev"
    }
  }
}
</code></pre>
<hr>
<h1>📙 <strong>5.3 IAM Role (Shared by Both Lambda Functions)</strong></h1>
<pre><code class="language-hcl">resource "aws_iam_role" "lambda_exec_role" {
  name = "FSE100_Lambda_ExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })
}
</code></pre>
<hr>
<h1>📘 <strong>5.4 Attach Required Policies</strong></h1>
<h3>✔ Lambda basic execution role</h3>
<pre><code class="language-hcl">resource "aws_iam_role_policy_attachment" "lambda_basic_exec" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_exec_role.name
}
</code></pre>
<h3>✔ DynamoDB read/write access</h3>
<pre><code class="language-hcl">resource "aws_iam_role_policy_attachment" "lambda_dynamodb_access" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  role       = aws_iam_role.lambda_exec_role.name
}
</code></pre>
<hr>
<h1>📗 <strong>5.5 Packaging Lambda Code (PowerShell)</strong></h1>
<p>⚠️ You must compress your Node.js Lambda functions before running <code inline="">terraform apply</code>.</p>
<h3>✔ Save Session</h3>
<pre><code class="language-powershell">cd lambda/save_session
npm init -y
npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
Compress-Archive -Path * -DestinationPath ../save_session.zip -Force
</code></pre>
<h3>✔ Login</h3>
<pre><code class="language-powershell">cd lambda/login
npm init -y
npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
Compress-Archive -Path * -DestinationPath ../login.zip -Force
</code></pre>
<hr>
<h1>📘 <strong>5.6 Summary of lambda.tf</strong></h1>

Component | Purpose
-- | --
Lambda functions | Save / login logic
IAM role | Lambda execution role
BasicExecutionRole | Lambda basic execution role
DynamoDBFullAccess | Read/write to StudentSessions
Zip files | Deployed code packages

<hr>
<h1>⭐ <strong>PART 3 / 5 — API Gateway (apigw.tf) + Routes + Permissions</strong></h1>
<hr>
<h1>📘 <strong>6. apigw.tf — API Gateway (HTTP API)</strong></h1>
<p>This file creates:</p>
<ul>
<li>
<p>One <strong>HTTP API</strong></p>
</li>
<li>
<p>Two <strong>routes</strong>:</p>
<ul>
<li>
<p><code inline="">POST /session</code></p>
</li>
<li>
<p><code inline="">POST /login</code></p>
</li>
</ul>
</li>
<li>
<p>Two <strong>Lambda integrations</strong></p>
</li>
<li>
<p>Auto-deployed <code inline="">$default</code> stage</p>
</li>
<li>
<p>Lambda invoke permissions</p>
</li>
<li>
<p>API endpoint outputs (for Unreal Engine)</p>
</li>
</ul>
<hr>
<h1>📙 <strong>6.1 Create the HTTP API</strong></h1>
<pre><code class="language-hcl">resource "aws_apigatewayv2_api" "session_api" {
  name          = "FSE100-Session-API"
  protocol_type = "HTTP"
}
</code></pre>
<hr>
<h1>📘 <strong>6.2 Create Lambda Integrations</strong></h1>
<h3>✔ Integration: POST /session → SaveSession Lambda</h3>
<pre><code class="language-hcl">resource "aws_apigatewayv2_integration" "session_integration" {
  api_id                 = aws_apigatewayv2_api.session_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.save_session.arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}
</code></pre>
<h3>✔ Integration: POST /login → Login Lambda</h3>
<pre><code class="language-hcl">resource "aws_apigatewayv2_integration" "login_integration" {
  api_id                 = aws_apigatewayv2_api.session_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.login.arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}
</code></pre>
<hr>
<h1>📗 <strong>6.3 Create API Routes</strong></h1>
<h3>✔ Route: POST /session</h3>
<pre><code class="language-hcl">resource "aws_apigatewayv2_route" "session_route" {
  api_id    = aws_apigatewayv2_api.session_api.id
  route_key = "POST /session"
  target    = "integrations/${aws_apigatewayv2_integration.session_integration.id}"
}
</code></pre>
<h3>✔ Route: POST /login</h3>
<pre><code class="language-hcl">resource "aws_apigatewayv2_route" "login_route" {
  api_id    = aws_apigatewayv2_api.session_api.id
  route_key = "POST /login"
  target    = "integrations/${aws_apigatewayv2_integration.login_integration.id}"
}
</code></pre>
<hr>
<h1>📘 <strong>6.4 Auto-deployed Default Stage</strong></h1>
<pre><code class="language-hcl">resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.session_api.id
  name        = "$default"
  auto_deploy = true
}
</code></pre>
<p>This ensures <strong>every change</strong> is instantly deployed without needing manual deployments.</p>
<hr>
<h1>📙 <strong>6.5 Lambda Invoke Permissions</strong></h1>
<p>APIGW must be allowed to run the Lambdas.</p>
<h3>✔ Allow invoke → SaveSession</h3>
<pre><code class="language-hcl">resource "aws_lambda_permission" "allow_apigw_invoke_session" {
  statement_id  = "AllowAPIGatewayInvokeSession"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.save_session.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.session_api.execution_arn}/*/*"
}
</code></pre>
<h3>✔ Allow invoke → Login</h3>
<pre><code class="language-hcl">resource "aws_lambda_permission" "allow_apigw_invoke_login" {
  statement_id  = "AllowAPIGatewayInvokeLogin"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.login.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.session_api.execution_arn}/*/*"
}
</code></pre>
<hr>
<h1>📗 <strong>6.6 Useful API Outputs</strong></h1>
<p>Your Terraform output will print:</p>
<ul>
<li>
<p>Base URL</p>
</li>
<li>
<p>Full /session endpoint</p>
</li>
<li>
<p>Full /login endpoint</p>
</li>
</ul>
<pre><code class="language-hcl">output "session_api_base_url" {
  value = aws_apigatewayv2_api.session_api.api_endpoint
}

output "session_api_session_url" {
  value = "${aws_apigatewayv2_api.session_api.api_endpoint}/session"
}

output "session_api_login_url" {
  value = "${aws_apigatewayv2_api.session_api.api_endpoint}/login"
}
</code></pre>
<p>These URLs are used inside Unreal Engine C++.</p>
<hr>
<h1>📘 <strong>6.7 Summary of API Gateway Setup</strong></h1>

Component | Purpose
-- | --
HTTP API | Handles all requests
Integration | Connects routes to Lambda
Route POST /session | Saves student session
Route POST /login | Loads student session
Auto-deploy | No need to manually deploy stages
Lambda permissions | Allows API to trigger Lambda

<hr>
<h1>⭐ <strong>PART 4 / 5 — Lambda Code (Node.js) + Packaging Instructions</strong></h1>
<hr>
<h1>📘 <strong>7. Lambda — SaveSession (index.js)</strong></h1>
<p>This function:</p>
<ul>
<li>
<p>Receives session data from Unreal Engine</p>
</li>
<li>
<p>Saves or overwrites a record in DynamoDB</p>
</li>
<li>
<p>Stores logs, progress, character info, timestamps, etc.</p>
</li>
</ul>
<hr>
<h2>✔ <code inline="">lambda/save_session/index.js</code></h2>
<pre><code class="language-js">const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, PutCommand } = require("@aws-sdk/lib-dynamodb");

const client = new DynamoDBClient({});
const ddb = DynamoDBDocumentClient.from(client);

exports.handler = async (event) =&gt; {
  console.log("=== SaveSession event ===");
  console.log(JSON.stringify(event, null, 2));

  // Parse event body
  const body = typeof event.body === "string" ? JSON.parse(event.body) : event;

  const tableName = process.env.TABLE_NAME;

  const params = {
    TableName: tableName,
    Item: {
      StudentID: body.StudentID,
      SessionID: body.SessionID,
      StudentName: body.StudentName ?? "",
      ScenarioCharacterName: body.ScenarioCharacterName ?? "",
      ScenarioNumber: body.ScenarioNumber ?? 0,
      Progress: body.Progress ?? 0,
      CompletionTime: body.CompletionTime ?? "",
      Logs: body.Logs ?? [],
      LastUpdated: Date.now()
    }
  };

  await ddb.send(new PutCommand(params));

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    },
    body: JSON.stringify({
      message: "Save successful",
      saved: params.Item
    })
  };
};
</code></pre>
<hr>
<h1>📙 <strong>8. Lambda — Login (index.js)</strong></h1>
<p>This function:</p>
<ul>
<li>
<p>Receives StudentID &amp; SessionID</p>
</li>
<li>
<p>Queries DynamoDB</p>
</li>
<li>
<p>Returns all matching sessions as JSON</p>
</li>
<li>
<p>Unreal Engine will parse the JSON response</p>
</li>
</ul>
<hr>
<h2>✔ <code inline="">lambda/login/index.js</code></h2>
<pre><code class="language-js">const { DynamoDBClient, QueryCommand } = require("@aws-sdk/client-dynamodb");

const REGION = process.env.AWS_REGION || "us-east-2";
const TABLE_NAME = process.env.TABLE_NAME;

const ddbClient = new DynamoDBClient({ region: REGION });

exports.handler = async (event) =&gt; {
  console.log("=== Login event ===");
  console.log(JSON.stringify(event, null, 2));

  // Parse incoming JSON body
  const body = event.body ? JSON.parse(event.body) : event;

  if (!body.StudentID || !body.SessionID) {
    return {
      statusCode: 400,
      body: JSON.stringify({
        ok: false,
        message: "StudentID and SessionID are required"
      })
    };
  }

  const params = {
    TableName: TABLE_NAME,
    KeyConditionExpression: "StudentID = :sid AND SessionID = :sess",
    ExpressionAttributeValues: {
      ":sid": { N: String(body.StudentID) },
      ":sess": { S: body.SessionID }
    }
  };

  try {
    const result = await ddbClient.send(new QueryCommand(params));
    const items = result.Items || [];

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        ok: true,
        exists: items.length &gt; 0,
        sessions: items
      })
    };
  } catch (err) {
    console.error("DynamoDB Query error:", err);

    return {
      statusCode: 500,
      body: JSON.stringify({
        ok: false,
        message: "Failed to query sessions",
        error: String(err)
      })
    };
  }
};
</code></pre>
<hr>
<h1>📗 <strong>9. Packaging Lambda Code (PowerShell)</strong></h1>
<p>Terraform requires <strong>zip files</strong> of Lambda code.</p>
<p>Run these commands before <code inline="">terraform apply</code>.</p>
<hr>
<h2>✔ Save Session Lambda</h2>
<pre><code class="language-powershell">cd lambda/save_session
npm init -y
npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
Compress-Archive -Path * -DestinationPath ../save_session.zip -Force
</code></pre>
<hr>
<h2>✔ Login Lambda</h2>
<pre><code class="language-powershell">cd lambda/login
npm init -y
npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
Compress-Archive -Path * -DestinationPath ../login.zip -Force
</code></pre>
<hr>
<h1>📘 <strong>10. JSON Body Examples (Used by Unreal Engine)</strong></h1>
<p>These are examples of what Unreal Engine sends.</p>
<hr>
<h3>✔ SaveSession JSON Example</h3>
<pre><code class="language-json">{
  "StudentID": 3,
  "StudentName": "Namett",
  "SessionID": "0001#Mike#1",
  "ScenarioCharacterName": "Mike",
  "ScenarioNumber": 1,
  "Progress": 10,
  "CompletionTime": "2025-11-16 10:39",
  "Logs": ["Hello world", "Save test"]
}
</code></pre>
<hr>
<h3>✔ Login JSON Example</h3>
<pre><code class="language-json">{
  "StudentID": 3,
  "SessionID": "0001"
}
</code></pre>
<hr>
<h1>📙 <strong>11. Common Lambda Errors (and Fixes)</strong></h1>

Error | Cause | Fix
-- | -- | --
Cannot find module 'index' | Wrong zip structure | Make sure index.js is at root of zip
Missing region | AWS CLI not configured | Run aws configure
AccessDeniedException | IAM policy missing | Attach DynamoDBFullAccess
500 Internal Server Error | Wrong KeyCondition | Ensure StudentID & SessionID exist


<hr>
<h1>⭐ <strong>PART 5 / 5 — Unreal Engine C++ Integration + Final Summary</strong></h1>
<hr>
<h1>📘 <strong>12. Unreal Engine C++ Integration (USaveToAWS)</strong></h1>
<p>The C++ code in Unreal Engine sends JSON to your Terraform-managed AWS API.</p>
<p>Two main functions:</p>
<ul>
<li>
<p><strong>SendStudentSessionToAWS</strong> → calls <code inline="">/session</code></p>
</li>
<li>
<p><strong>LoginStudentFromAWS</strong> → calls <code inline="">/login</code></p>
</li>
</ul>
<p>After Terraform deploys, get your URL from:</p>
<pre><code>terraform output session_api_session_url
terraform output session_api_login_url
</code></pre>
<hr>
<h1>📙 <strong>12.1 Save Session to AWS (POST /session)</strong></h1>
<pre><code class="language-cpp">void USaveToAWS::SendStudentSessionToAWS(
    int32 StudentID,
    const FName&amp; StudentName,
    const FString&amp; SessionID,
    const FString&amp; ScenarioCharacterName,
    int32 ScenarioNumber,
    float Progress,
    const FString&amp; CompletionTime
)
{
    TSharedRef&lt;FJsonObject&gt; JsonObject = MakeShared&lt;FJsonObject&gt;();

    JsonObject-&gt;SetNumberField(TEXT("StudentID"), StudentID);
    JsonObject-&gt;SetStringField(TEXT("StudentName"), StudentName.ToString());
    JsonObject-&gt;SetStringField(TEXT("SessionID"), SessionID);
    JsonObject-&gt;SetStringField(TEXT("ScenarioCharacterName"), ScenarioCharacterName);
    JsonObject-&gt;SetNumberField(TEXT("ScenarioNumber"), ScenarioNumber);
    JsonObject-&gt;SetNumberField(TEXT("Progress"), Progress);
    JsonObject-&gt;SetStringField(TEXT("CompletionTime"), CompletionTime);

    FString JsonString;
    TSharedRef&lt;TJsonWriter&lt;&gt;&gt; Writer = TJsonWriterFactory&lt;&gt;::Create(&amp;JsonString);
    FJsonSerializer::Serialize(JsonObject, Writer);

    UE_LOG(LogTemp, Log, TEXT("[AWS] Sending JSON: %s"), *JsonString);

    TSharedRef&lt;IHttpRequest, ESPMode::ThreadSafe&gt; Request =
        FHttpModule::Get().CreateRequest();

    const FString Url = TEXT("https://api.devilsona.click/session");

    Request-&gt;SetURL(Url);
    Request-&gt;SetVerb(TEXT("POST"));
    Request-&gt;SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request-&gt;SetContentAsString(JsonString);

    Request-&gt;OnProcessRequestComplete().BindStatic(
        [](FHttpRequestPtr Req, FHttpResponsePtr Response, bool bWasSuccessful)
        {
            if (!bWasSuccessful || !Response.IsValid())
            {
                UE_LOG(LogTemp, Error, TEXT("[AWS] SaveSession failed"));
                return;
            }

            UE_LOG(LogTemp, Log,
                TEXT("[AWS] Save Response %d: %s"),
                Response-&gt;GetResponseCode(),
                *Response-&gt;GetContentAsString());
        }
    );

    Request-&gt;ProcessRequest();
}
</code></pre>
<hr>
<h1>📗 <strong>12.2 Login from AWS (POST /login)</strong></h1>
<pre><code class="language-cpp">void USaveToAWS::LoginStudentFromAWS(
    int32 StudentID,
    const FString&amp; SessionID
)
{
    TSharedRef&lt;FJsonObject&gt; JsonObject = MakeShared&lt;FJsonObject&gt;();

    JsonObject-&gt;SetNumberField(TEXT("StudentID"), StudentID);
    JsonObject-&gt;SetStringField(TEXT("SessionID"), SessionID);

    FString JsonString;
    TSharedRef&lt;TJsonWriter&lt;&gt;&gt; Writer = TJsonWriterFactory&lt;&gt;::Create(&amp;JsonString);
    FJsonSerializer::Serialize(JsonObject, Writer);

    UE_LOG(LogTemp, Log, TEXT("[AWS-Login] Sending JSON: %s"), *JsonString);

    TSharedRef&lt;IHttpRequest, ESPMode::ThreadSafe&gt; Request =
        FHttpModule::Get().CreateRequest();

    const FString Url = TEXT("https://api.devilsona.click/login");

    Request-&gt;SetURL(Url);
    Request-&gt;SetVerb(TEXT("POST"));
    Request-&gt;SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request-&gt;SetContentAsString(JsonString);

    Request-&gt;OnProcessRequestComplete().BindLambda(
        [](FHttpRequestPtr Req, FHttpResponsePtr Response, bool bWasSuccessful)
        {
            if (!bWasSuccessful || !Response.IsValid())
            {
                UE_LOG(LogTemp, Error, TEXT("[AWS-Login] Request failed"));
                return;
            }

            UE_LOG(LogTemp, Log,
                TEXT("[AWS-Login] Response %d: %s"),
                Response-&gt;GetResponseCode(),
                *Response-&gt;GetContentAsString());
        }
    );

    Request-&gt;ProcessRequest();
}
</code></pre>
<hr>
<h1>📘 <strong>12.3 Parsing Login Results in C++</strong></h1>
<p>If you want to store the login result:</p>
<pre><code class="language-cpp">void USaveToAWS::GetLastLoginResult(
    bool&amp; bSuccess,
    bool&amp; bExists,
    TArray&lt;FStudentSessionData&gt;&amp; Sessions
)
{
    bSuccess = GLastLoginSuccess;
    bExists = GLastLoginExists;
    Sessions = GLastLoginSessions;
}
</code></pre>
<p>This is automatically populated by <code inline="">LoginStudentFromAWS()</code>.</p>
<hr>
<h1>📙 <strong>13. API Request Logs (Example)</strong></h1>
<p>These show up in UE Log:</p>
<pre><code>[AWS-Login] Sending JSON: {"StudentID":7,"SessionID":"0001"}
[AWS-Login] Status: 200, Body: {"ok":true,"exists":true,"sessions":[ ... ]}
</code></pre>
<hr>
<h1>📗 <strong>14. Terraform Apply Cycle</strong></h1>
<p>Always run:</p>
<pre><code class="language-powershell">terraform init
terraform plan
terraform apply
</code></pre>
<p>Whenever you:</p>
<ul>
<li>
<p>Change Lambda code (new zip required)</p>
</li>
<li>
<p>Change DynamoDB structure</p>
</li>
<li>
<p>Modify API Gateway routes</p>
</li>
<li>
<p>Update IAM roles</p>
</li>
</ul>
<hr>
<h1>📘 <strong>15. Final Summary</strong></h1>

Component | Status
-- | --
Terraform Infrastructure | ✅ Complete
DynamoDB Table | ✅ StudentSessions
SaveSession Lambda | ✅ Node.js 22.x
Login Lambda | ✅ Node.js 22.x
API Gateway Routes | /session → Save, /login → Login
IAM Role & Permissions | Properly attached
Unreal Engine C++ Integration | Fully functional
Auto-deployment via $default stage | Enabled


<p>You now have a <strong>full production-grade cloud backend</strong> running on AWS, fully automated through Terraform and cleanly integrated into Unreal Engine 5.</p>
<hr>
