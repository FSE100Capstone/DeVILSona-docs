# Logging & Incident Response

!!! info "Audience"
    Technical Administrators diagnosing failures in the DeVILSona system.

This page documents how to access logs from each component of the DeVILSona system and provides an escalation path for resolving system failures.

---

## Meta Quest Crash Logs (Android Logcat via ADB)

When the DeVILSona app crashes or behaves unexpectedly on the headset, the most valuable diagnostic tool is **Android Logcat**—the real-time log stream from the Android OS.

### Prerequisites

- ADB installed and in PATH (see [Hardware Provisioning & Sideloading](hardware-provisioning.md))
- Headset connected via USB-C in Developer Mode
- `adb devices` shows the headset as `device` (not `unauthorized`)

### Capturing Real-Time Logs

Open PowerShell and run:
```powershell
adb logcat
```

This streams all logs from the headset. The output is extremely verbose—filter it to DeVILSona-specific logs:

```powershell
# Filter for the game's log tag (UE5 uses "LogTemp" and named tags)
adb logcat -s LogTemp:V UE4:V UE:V

# Or filter for just errors
adb logcat "*:E"

# Or capture everything to a file for later analysis
adb logcat > C:\Logs\devilsona_session.txt
```

### Understanding Log Output

Unreal Engine logs through Android Logcat with these tags:

| Tag | Meaning |
|-----|---------|
| `LogTemp` | General project logs from `UE_LOG(LogTemp, ...)` |
| `UE4` | Unreal Engine core messages |
| `LogOnline` | Network/online subsystem messages |
| `LogHttp` | HTTP requests (AWS API calls) |

**Looking for AWS save/load issues:**
```
[AWS] Status: 200
[AWS] Save Response 200: {"message":"Save successful",...}
[AWS-Login] Status: 200, Body: {"ok":true,"exists":true,...}
```

**Common error patterns:**
```
[AWS] Save API URL is not set!
→ The app was not given the AWS endpoint URL at startup.
  Verify the URL is correctly set in the UE5 GameInstance Blueprint.

[AWS] SaveSession failed
→ HTTP request failed. Check Wi-Fi connectivity and API Gateway status.

[AWS-Login] Login API URL is not set!
→ Same as above for the login endpoint.

OpenAI WebSocket: Connection closed with code 1006
→ WebSocket connection dropped. Check network quality and firewall rules.

CAPSTONE_PROJECT_OPENAI_API_KEY environment variable is not set
→ The OpenAI API key was not found. This environment variable must be
  set at build time (Windows) or passed via the launcher.
```

### Pulling a Crash Log

If the app crashed and you need the crash report:
```powershell
# Pull the entire log buffer (includes recent crash info)
adb logcat -d > crash_log.txt

# Or pull UE5's dedicated crash log files from device storage
adb pull /sdcard/UE4Game/FSE100Capstone/ C:\Logs\ue4_logs\
```

The pulled directory from `/sdcard/UE4Game/FSE100Capstone/` will contain:

- `Logs/` — Unreal Engine log files from each session
- `Saved/` — Additional saved data including crash reports if crash reporter is enabled

### Capturing Logs While Reproducing an Issue

For intermittent issues (e.g., "AI stops responding after 5 minutes"), the best approach is to capture logs during the exact failure:

1. Clear the log buffer before starting:
   ```powershell
   adb logcat -c
   ```
2. Start capturing to a file:
   ```powershell
   adb logcat > C:\Logs\reproduction_$(Get-Date -Format "yyyyMMdd_HHmmss").txt
   ```
3. Reproduce the issue in the headset
4. Stop logging (Ctrl+C) and share the file with the development team

---

## DeVILStarter Local Log Files

**DeVILStarter** streams Terraform's stdout/stderr output directly to its UI panel. This output is also written to log files for persistent diagnostics.

### Log File Location

Log files are stored in DeVILStarter's application data directory. Depending on the installation:

```
# Standard Windows App Data location:
%APPDATA%\DeVILStarter\logs\

# Or relative to the executable:
<DeVILStarter install directory>\logs\
```

!!! note
    Check the DeVILStarter settings panel for the exact log directory if unsure.

### Understanding DeVILStarter Logs

Log files are named by date/time. Each file contains the captured Terraform output from that session. Key patterns to look for:

**Successful Infrastructure Start:**
```
Terraform has been successfully initialized!
Plan: 8 to add, 0 to change, 0 to destroy.
aws_dynamodb_table.student_sessions: Creating...
aws_dynamodb_table.student_sessions: Creation complete after 7s
aws_lambda_function.save_session: Creating...
...
Apply complete! Resources: 8 added, 0 changed, 0 destroyed.

Outputs:
session_api_session_url = "https://abcd1234.execute-api.us-east-2.amazonaws.com/session"
session_api_login_url = "https://abcd1234.execute-api.us-east-2.amazonaws.com/login"
```

**Common Terraform Errors:**

| Error Message | Cause | Resolution |
|--------------|-------|------------|
| `Error: No valid credential sources found` | AWS credentials not configured | Run `aws configure` on the machine |
| `Error: error creating Lambda Function: ResourceConflictException` | Lambda already exists (state mismatch) | Run `terraform destroy` then `terraform apply` |
| `Error: InvalidSignatureException` | System time is out of sync | Sync system clock: `w32tm /resync` |
| `Error: UnauthorizedClientException` | IAM permissions insufficient | Verify the IAM user has required permissions |
| `Error: zip file not found` | Lambda code not packaged | Run the Lambda packaging PowerShell commands (see [Infrastructure & Cloud](../developer-guide/infrastructure-cloud.md)) |

### Checking AWS Credential Status

If DeVILStarter fails due to credentials:
```powershell
# Verify credentials are configured
aws sts get-caller-identity

# Expected output:
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/devilsona-admin"
}

# If you get an error, reconfigure:
aws configure
```

---

## Escalation Path

When logging and basic troubleshooting are insufficient, use the following escalation path:

### Level 1: Educator Self-Service
- Follow [Educator Troubleshooting Guide](../educator-guide/troubleshooting.md)
- Restart the app, check Wi-Fi, restart the headset

### Level 2: Technical Administrator
- Use ADB to pull crash logs from the headset
- Check DynamoDB for missing or corrupted student records
- Restart DeVILStarter and re-deploy infrastructure if needed

### Level 3: Developer Team
Escalate to the capstone development team when:

- The app crashes every time on launch (likely a build or configuration issue)
- Lambda functions consistently error despite correct credentials and network
- The Terraform configuration needs to be updated (new endpoints, schema changes)
- A new APK build is needed (e.g., bug fix or new feature)

When escalating to the developer team, provide:

1. **ADB logcat capture** from when the issue occurred
2. **DeVILStarter log file** from the session
3. **Exact steps to reproduce** the issue
4. **Headset model and firmware version** (from Settings → About in the headset)
5. **Network environment description** (campus Wi-Fi, name, any known restrictions)

---

## Quick Diagnostic Checklist

When something isn't working:

```
1. HEAD CHECK:
   [ ] Is DeVILStarter running and showing Green/Ready status?
   [ ] Is the headset connected to Wi-Fi (correct SSID)?
   [ ] Is the app launched and on the login screen?

2. NETWORK CHECK:
   [ ] Can the headset reach the internet? (try Meta Browser → google.com)
   [ ] Is WebSocket traffic allowed? (test with wscat from same SSID laptop)

3. BACKEND CHECK:
   [ ] DynamoDB table accessible (check from AWS Console)?

4. CLIENT CHECK:
   [ ] ADB logcat showing normal AWS save/login messages?
   [ ] Any error messages in adb logcat -s LogTemp?

5. ESCALATE if:
   [ ] All above look normal but issue persists
   [ ] App crashes on launch
   [ ] Terraform fails with unknown errors
```
