# Hardware Provisioning, Sideloading & DeVILStarter Setup

!!! info "Audience"
    IT Administrators responsible for provisioning Meta Quest headsets and deploying the DeVILSona application.

This page covers the complete process for setting up Meta Quest headsets for enterprise use and deploying (sideloading) the DeVILSona APK.

---

## Meta Quest Provisioning

### Developer Mode vs. Standard Mode

By default, Meta Quest headsets are locked to only install applications from the **Meta Horizon Store**. Since DeVILSona is a custom institutional application and not published to the store, it must be installed via **sideloading**—transferring the APK directly from a computer using ADB (Android Debug Bridge).

**Developer Mode** must be enabled on each headset to allow sideloading.

### Enabling Developer Mode

**Prerequisites:**

- A Meta developer account (free at [https://developer.oculus.com](https://developer.oculus.com))
- The Meta Horizon mobile app installed on your phone
- The headset paired with your Meta account in the Meta Horizon app

**Steps:**

1. Open the **Meta Horizon app** on your phone
2. Tap on your **headset** in the Devices tab
3. Navigate to **Settings → Developer Mode**
4. Toggle **Developer Mode: ON**
5. On the headset, you may need to confirm by clicking **"Allow Developer Features"** in a prompt that appears in the headset

**Verify Developer Mode is active:**
Connect the headset to a PC via USB-C and run:
```powershell
adb devices
```
If Developer Mode is on, the headset will appear in the list (you may need to confirm the fingerprint inside the headset the first time):
```
List of devices attached
1WMHXXXXXX    device
```
If the device shows as `unauthorized`, put on the headset and accept the "Allow USB Debugging" popup.

### MDM and Enterprise Management Considerations

For larger deployments (10+ headsets across an IT department), consider:

**Meta Quest for Business (formerly Meta for Business):**

- Provides enterprise management features including over-the-air app deployment, device management dashboards, and kiosk mode
- Requires purchasing a **Meta Quest for Business** subscription per device
- Enables deployment of custom APKs without enabling Developer Mode per device

**Alternative MDM Solutions:**

- **ArborXR**, **Manage XR**, or **Headjack** are third-party Mobile Device Management solutions that support Meta Quest
- These allow remote APK deployment, device monitoring, and usage analytics

For a small-scale FSE100 deployment (typically 4–8 headsets), manual Developer Mode + ADB sideloading per the instructions below is the most practical approach.

---

## Sideloading the DeVILSona APK

### Prerequisites

Before sideloading, ensure you have:

| Requirement | Details |
|-------------|---------|
| **ADB installed** | Part of Android Platform Tools: [https://developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools) |
| **USB-C cable** (data-capable) | Not all USB-C cables support data transfer—use the cable that came with the headset or a quality data cable |
| **DeVILSona APK file** | Build output from Unreal Engine packaging (see [Developer Guide: UE5 Implementation](../developer-guide/ue5-implementation.md) for build instructions) |
| **Developer Mode enabled** | Per Section 1.2 above |
| **Windows 10/11 PC** | macOS cannot build Quest APKs; all sideloading should be done from Windows |

### Installing ADB

**Option A: Android Platform Tools (Lightweight)**

1. Download from: [https://developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools)
2. Extract to a permanent location (e.g., `C:\platform-tools\`)
3. Add to your system PATH:
   - Open **System Properties → Environment Variables → System Variables → Path**
   - Add `C:\platform-tools\`
4. Verify: Open PowerShell and run `adb --version`

**Option B: SideQuest (Recommended for Non-Developers)**
[SideQuest](https://sidequestvr.com) is a free desktop application that simplifies the sideloading process with a graphical interface. It automatically handles ADB under the hood.

1. Download SideQuest Desktop from [https://sidequestvr.com/setup-howto](https://sidequestvr.com/setup-howto)
2. Install and launch SideQuest
3. Connect the headset via USB-C

### Sideloading via ADB (Command Line)

**Step 1: Connect the headset**
```powershell
# Connect headset to PC via USB-C, then:
adb devices
# Should show: <serial>    device
```

**Step 2: Install the APK**
```powershell
adb install -r "C:\path\to\DeVILSona-Shipping.apk"
```

The `-r` flag allows reinstalling over an existing version. Installation typically takes 30–120 seconds depending on APK size.

**Expected output:**
```
Performing Streamed Install
Success
```

**Step 3: Verify installation**
```powershell
adb shell pm list packages | findstr "fse100"
```
You should see the package name listed (e.g., `package:com.fse100.devilsona`).

### Sideloading via SideQuest (GUI Method)

1. Open SideQuest and confirm the headset shows as **Connected (green circle)**
2. Click **"Install APK file from folder on computer"** (the folder icon in the top toolbar)
3. Navigate to and select the DeVILSona APK file
4. SideQuest will install the APK and show a success notification

### Which APK File to Select

The Unreal Engine build process for Android generates **multiple APK files** in the build output directory:
```
<Project>/Saved/StagedBuilds/Android_ASTC/
```

You will see files like:

- `FSE100Capstone-arm64-Shipping.apk` (smaller, ~50–100MB)
- `FSE100Capstone-arm64-Shipping_universal.apk` or a larger combined file

!!! warning "Always install the LARGEST APK file."
    The smaller APK is incomplete and requires a separate OBB (additional data) file to function. The large APK packages all game content inside it, making deployment and management simpler.

!!! tip "Learn More"
    If you'd like to learn more, you can read our more fine-grained technical documentation on the full Android packaging process, including SDK/NDK version requirements, environment variables, and troubleshooting at [UE5 Build Guide (Android APK)](../legacy/build-android-apk.md).

### Launching the Installed Application

After installation, the app will appear in the headset's App Library under **"Unknown Sources"** (a separate tab).

On the Meta Quest:

1. Navigate to **App Library** (grid icon at bottom of home screen)
2. Tap the **Unknown Sources** tab
3. Find and launch **"FSE100 Capstone"** (or whatever label was set in the UE5 project)

### Batch Sideloading Multiple Headsets

To sideload to multiple headsets simultaneously using ADB:

```powershell
# Get list of connected devices
$devices = adb devices | Select-String "device$" | ForEach-Object { ($_ -split "\s+")[0] }

# Install on each device
foreach ($device in $devices) {
    Write-Host "Installing on $device..."
    adb -s $device install -r "C:\path\to\DeVILSona.apk"
}
```

!!! note
    Note: You can connect multiple headsets to a USB hub, but each headset needs Developer Mode enabled and the USB debugging fingerprint accepted individually.

---

## DeVILStarter Configuration & Installation

### What DeVILStarter Requires

Before DeVILStarter can start or stop infrastructure, the host Windows machine needs:

| Requirement | Details |
|-------------|---------|
| **AWS CLI v2** | Download from [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/) |
| **Terraform** | Download from [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install) |
| **AWS IAM Credentials** | Access Key ID + Secret Access Key with sufficient permissions |
| **Internet Access** | HTTPS outbound to `*.amazonaws.com` |

### Configuring AWS Credentials

Run the following in PowerShell to configure credentials:
```powershell
aws configure
```

Provide:
```
AWS Access Key ID: <provided by project admin or your AWS IAM user>
AWS Secret Access Key: <provided by project admin>
Default region name: us-east-2
Default output format: json
```

Credentials are stored in `~\\.aws\\credentials`. DeVILStarter reads them automatically from this location.

**Required IAM Permissions:**
The IAM user/role running DeVILStarter needs permissions to manage the following AWS services:

- `apigateway:*`
- `lambda:*`
- `dynamodb:*`
- `iam:*` (for creating Lambda execution roles)

The simplest approach for a development/educational deployment is attaching the **AdministratorAccess** managed policy to the IAM user, accepting that this is not least-privilege. For stricter environments, craft a custom IAM policy limited to the above services in `us-east-2`.

### Installing Terraform

1. Download the Terraform binary for Windows from [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)
2. Extract the `terraform.exe` to a directory (e.g., `C:\terraform\`)
3. Add that directory to your system PATH (same process as ADB in Section 2.2)
4. Verify: `terraform --version`

### Installing and Running DeVILStarter

1. Obtain the DeVILStarter installer or executable from the DeVILSona project repository
2. Run the installer (or the executable directly if it's a portable build)
3. Launch DeVILStarter

On the first launch, DeVILStarter will look for the `DeVILSona-infra` Terraform configuration directory. Confirm the path is correct in DeVILStarter's settings if prompted.

### Verifying DeVILStarter Works

1. Click **"Start Infrastructure"**
2. Watch the log output. You should see Terraform messages like:
   ```
   Terraform has been successfully initialized!
   Plan: 8 to add, 0 to change, 0 to destroy.
   Apply complete! Resources: 8 added, 0 changed, 0 destroyed.
   ```
3. The status indicator should turn **green**
4. To confirm the API is live, use a REST client (like [curl](https://curl.se/) or [Postman](https://www.postman.com/)) to test the endpoint:
   ```powershell
   curl -X POST https://<id>.execute-api.us-east-2.amazonaws.com/login `
     -H "Content-Type: application/json" `
     -d '{"StudentID": 999, "SessionID": "test"}'
   ```
   You should receive a 200 response with `{"ok":true,"exists":false,"sessions":[]}`.

---

## Sideloading Checklist

Before each deployment cycle, verify:

- [ ] Developer Mode enabled on all headsets
- [ ] ADB or SideQuest installed on deployment PC
- [ ] Correct (largest) APK file identified in build output
- [ ] All headsets show as `device` in `adb devices`
- [ ] APK installed and launchable on each headset
- [ ] App appears under "Unknown Sources" in App Library
- [ ] Wi-Fi configured on each headset (correct SSID + password)
- [ ] AWS credentials configured on DeVILStarter machine
- [ ] Terraform installed and in PATH
- [ ] DeVILStarter tested: infrastructure start → green status → infrastructure stop

---

➡️ **Next:** [Network Configuration](network-configuration.md)
