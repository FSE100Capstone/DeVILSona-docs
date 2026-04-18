# Developer Onboarding & Environment Setup

!!! info "Audience"
    Incoming capstone developers setting up their local development environment for the first time.

Welcome to the DeVILSona project. This guide will walk you through every step required to get from zero to a working development environment. Read this page in full before starting—the order of operations matters.

---

## Hardware & Software Prerequisites

### Minimum Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 64-bit | Windows 11 64-bit |
| **CPU** | Intel Core i7 (8th gen) / AMD Ryzen 7 | Intel Core i9 / AMD Ryzen 9 |
| **RAM** | 32 GB | 64 GB |
| **GPU** | NVIDIA GTX 1080 / AMD RX 5700 XT | NVIDIA RTX 3080+ |
| **Storage** | 200 GB free SSD space | 500 GB NVMe SSD |
| **Meta Quest headset** | Quest 2 (for VR testing) | Quest 3 |

!!! warning "macOS Warning"
    macOS developers face significant limitations on this project. The OVRLipSync plugin is compiled for x86_64 only, requiring Unreal Engine to run in Rosetta 2 emulation mode on Apple Silicon Macs. You **cannot** build Android APKs on macOS. See [Mac-Specific Limitations](#mac-specific-limitations) at the end of this page for complete details if you must use a Mac.

### Required Software

Install the following in this order:

**1. Visual Studio 2022 (Community or Professional)**

- Download: [https://visualstudio.microsoft.com/vs/](https://visualstudio.microsoft.com/vs/)
- During installation, select these workloads:
    - ✅ **Desktop development with C++**
    - ✅ **Game development with C++**
- Under "Individual components", also install:
    - ✅ **Windows 10/11 SDK (latest version)**
    - ✅ **.NET 8.0 Runtime**

**2. Unreal Engine 5.6+**

- Install the **Epic Games Launcher**: [https://www.epicgames.com/store/en-US/download](https://www.epicgames.com/store/en-US/download)
- In the launcher, navigate to **Unreal Engine → Library**
- Install **Unreal Engine 5.6** (or the latest 5.x version)
- Installation size: ~60–80 GB

**3. Git**

- Download: [https://git-scm.com/download/win](https://git-scm.com/download/win)
- During installation, select:
    - ✅ "Git from the command line and also from 3rd-party software"
    - ✅ "Use bundled OpenSSH"

**4. Git LFS (Git Large File Storage)**

```powershell
# Install Git LFS
git lfs install
```
!!! warning "This is critical."
    Unreal Engine projects store binary assets (`.uasset`, `.umap`, textures, etc.) in Git LFS. Without it, you will clone a repository with broken placeholder files instead of actual assets.

**5. Android Studio Koala 2024.1.2 (for Android/Quest builds)**

- Download the specific version: [https://developer.android.com/studio/archive](https://developer.android.com/studio/archive)
- After installing, in the Android SDK Manager, ensure these are installed:
    - Android SDK Platform 34 (Target SDK)
    - Android SDK Platform 35 (Recommended SDK)
    - NDK version **r27c** (29.0.13113456) — **use this exact version**
    - Android Build Tools 35.0.1

**6. AWS CLI v2**

- Download: [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)
- Verify: `aws --version`

**7. Terraform**

- Download: [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)
- Add to PATH; verify: `terraform --version`

**8. Node.js v20+ (for Lambda function development)**

- Download: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
- Verify: `node --version`

---

## GitHub Access & Repository Cloning

### Getting Repository Access

The DeVILSona project spans multiple GitHub repositories. Request access to:

| Repository | Purpose |
|-----------|---------|
| `FSE100Capstone/DeVILSona` | Main UE5 VR project |
| `FSE100Capstone/DeVILSona-infra` | Terraform/AWS infrastructure |
| `FSE100Capstone/DeVILStarter` | Desktop launcher (Wails/Go/React) |
| `FSE100Capstone/DeVILSona.wiki` | This wiki |

Contact the project lead or faculty advisor to be added as a collaborator on each repository.

### SSH Key Setup (Recommended)

Using SSH for Git avoids needing to enter credentials with every push/pull.

```powershell
# Generate an SSH key (use your university email)
ssh-keygen -t ed25519 -C "your@asu.edu"

# Start the SSH agent
Get-Service -Name ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent

# Add your key to the agent
ssh-add ~/.ssh/id_ed25519

# Copy your public key to clipboard
Get-Content ~/.ssh/id_ed25519.pub | clip
```

Then go to GitHub → Profile Settings → SSH and GPG keys → New SSH Key, and paste the key.

Test the connection:
```powershell
ssh -T git@github.com
# Expected: Hi <username>! You've successfully authenticated...
```

### Personal Access Token (PAT) — Alternative

If working in an environment where SSH is not supported:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a token with `repo` scope
3. Use this token as your password when Git prompts for credentials

### Cloning the Main Repository

```powershell
# Clone with SSH (recommended)
git clone git@github.com:FSE100Capstone/DeVILSona.git

# Or with HTTPS + PAT
git clone https://github.com/FSE100Capstone/DeVILSona.git
```

After cloning, verify that Git LFS pulled the actual assets:
```powershell
cd DeVILSona
git lfs pull
# This may take several minutes on first clone - it downloads all binary assets
```

Check that assets look correct (not empty placeholder files):
```powershell
# A real .uasset should be >1KB; an LFS pointer is ~200 bytes
Get-ChildItem -Recurse -Filter "*.uasset" | Where-Object { $_.Length -lt 500 } | Select-Object Name, Length
# In a healthy repo, this should return no results (or very few small ones)
```

### Repository Directory Structure

After cloning, the main UE5 project structure is:
```
DeVILSona/
├── .git/
├── .gitattributes          ← Git LFS tracking patterns (DO NOT MODIFY)
├── .gitignore
├── Config/                 ← UE5 project configuration files
├── Content/                ← All UE5 assets (.uasset, .umap files)
│   ├── MetaHumans/         ← AI character assets
│   ├── Blueprints/
│   └── Levels/
├── Plugins/                ← Third-party plugins (OVRLipSync, etc.)
│   └── OVRLipSync/
├── Source/                 ← C++ source code
│   └── FSE100Capstone/
│       ├── Subsystems/     ← AI subsystem classes
│       ├── Actors/         ← Game actor classes (IntervieweeActor, etc.)
│       └── ...
├── FSE100Capstone.uproject ← Project file (open this to launch UE5)
└── Saved/                  ← Generated at runtime, not committed
```

---

## Local Environment Setup

### OpenAI API Key Configuration

The project needs an OpenAI API key to power the AI conversations. This key is loaded from an **environment variable** for security—it is never hardcoded in the source code.

**Variable name:** `CAPSTONE_PROJECT_OPENAI_API_KEY`

**Setting it on Windows (Permanent):**

1. Open **System Properties → Advanced → Environment Variables**
2. Under **System variables**, click **New**
3. Variable name: `CAPSTONE_PROJECT_OPENAI_API_KEY`
4. Variable value: `sk-proj-...` (your full API key)
5. Click OK, then restart any open terminals/editors

**Verify it's set:**
```powershell
echo $env:CAPSTONE_PROJECT_OPENAI_API_KEY
# Should print your API key
```

!!! warning
    Obtain the API key from the project lead or your faculty advisor. Do not generate your own key for production use without authorization.

### AWS Credentials Configuration

```powershell
aws configure
# Enter the access key, secret key, region (us-east-2), and format (json)
```

Credentials are used by:

- The Terraform infrastructure management (DeVILStarter / DeVILSona-infra)
- The AWS CLI for debugging DynamoDB

### Generating Unreal Engine Project Files

Before opening the project in Visual Studio, you must generate the Unreal Engine project files:

1. Navigate to the project directory in File Explorer
2. Right-click `FSE100Capstone.uproject`
3. Select **"Generate Visual Studio project files"**

This creates `FSE100Capstone.sln` which Visual Studio needs to compile the C++ code.

!!! note
    If you don't see this context menu option, ensure Unreal Engine is installed via the Epic Games Launcher and properly registered with Windows.

### First Compilation

**Option A: Open in Unreal Engine (Compiles automatically)**

1. Double-click `FSE100Capstone.uproject`
2. Unreal Engine will open and attempt to compile the C++ code automatically
3. On first compile, this takes **10–30 minutes** depending on your CPU
4. If compilation fails, check Visual Studio is installed with the correct workloads

**Option B: Compile from Visual Studio**

1. Open `FSE100Capstone.sln` in Visual Studio 2022
2. Set the solution configuration to **Development Editor** and platform to **Win64**
3. Right-click `FSE100Capstone` project in Solution Explorer → **Build**

!!! tip "Learn More"
    If you'd like to learn more about packaging the project for distribution, you can read our more fine-grained technical documentation on Windows Shipping builds at [UE5 Build Guide (Windows Shipping)](../legacy/build-windows-shipping.md) and Android APK builds at [UE5 Build Guide (Android APK)](../legacy/build-android-apk.md).

### OVRLipSync Plugin Verification

After compiling, verify the OVRLipSync plugin loaded correctly:

1. In the Unreal Engine Editor, go to **Edit → Plugins**
2. Search for **"OVR"** or **"Lip Sync"**
3. Ensure **OVRLipSync** shows as **Enabled** (not greyed out)

If the plugin is missing or fails to load:

1. Check the `Plugins/OVRLipSync/` directory exists and contains actual files (not LFS pointers)
2. Run `git lfs pull` and check again
3. For UE 5.6 compatibility, the plugin requires a minor source code fix—see instructions in the legacy [Oculus-LipSync-Plugin](../legacy/oculus-lipsync.md) documentation

---

## Mac-Specific Limitations

!!! note
    This section applies only to developers using Apple Silicon (M-series) Macs.

### The OVRLipSync x86_64 Constraint

The OVRLipSync plugin ships as a pre-compiled binary for **x86_64 (Intel) architecture only**. Apple Silicon Macs run an ARM64 architecture natively. This means:

- If you open the project normally (ARM64 mode), Unreal Engine **cannot load the OVRLipSync plugin** and will fail with module load errors
- The workaround is to run Unreal Engine in **Rosetta 2 (x86_64 emulation) mode**
- This requires building and running Unreal Engine from the x86_64 binary, not the ARM binary

### Required Xcode Version

Install **Xcode 16** (not the App Store version):

- Download from: [https://developer.apple.com/download/all/?q=xcode%2016](https://developer.apple.com/download/all/?q=xcode%2016)

After installation:
```bash
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
xcode-select -p  # Verify path
```

### First-Time Build on Mac (x86_64 mode)

```bash
# Clean the project first
rm -rf Binaries Intermediate DerivedDataCache

# Generate project files in x86 mode
arch -x86_64 /Users/Shared/Epic\ Games/UE_5.6/Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh \
  -project="/path/to/FSE100Capstone.uproject" \
  -game

# Build in x86 mode
arch -x86_64 /Users/Shared/Epic\ Games/UE_5.6/Engine/Build/BatchFiles/Mac/Build.sh \
  FSE100CapstoneEditor Mac Development \
  -architecture=x86_64 \
  "/path/to/FSE100Capstone.uproject"
```

### Opening the Project on Mac (EVERY TIME)

!!! warning
    You MUST open the project via Terminal every single time. Never double-click the .uproject file on Mac.

```bash
arch -x86_64 /Users/Shared/Epic\ Games/UE_5.6/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor \
  "/path/to/FSE100Capstone.uproject"
```

**DO NOT:**

- Double-click the `.uproject` file
- Open from the Epic Games Launcher
- Allow Unreal to rebuild modules automatically (click "No" if prompted)

### Mac Microphone Access

Before the AI voice input will work:

1. **System Settings → Privacy & Security → Microphone**
2. Enable access for **UnrealEditor-Mac-DebugGame**

### VR Testing on Mac

**Mac cannot perform real-time VR testing with Meta Quest.** Meta Quest Link (USB) and Meta Quest Air Link are not supported on macOS. Mac developers should use Mac for:

- C++ coding and Blueprint editing
- UI development
- General gameplay programming

For VR testing, use a Windows workstation or package directly to the headset (Android APK build is not possible on Mac either—this requires a Windows machine).

!!! tip "Learn More"
    If you'd like to learn more, you can read our more fine-grained technical documentation on macOS setup including Xcode configuration, Git LFS permissions, OpenAI API key setup, and VR testing limitations at [Mac Setup & Limitations](../legacy/mac-setup-limitations.md).

---

## Next Steps

With your environment set up, continue to understand the system architecture:

➡️ **[Core Architecture Deep Dive](core-architecture.md)**
