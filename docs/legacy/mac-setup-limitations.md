# Mac Setup (Apple Silicon + OVRLipSync)

This project uses the OVRLipSync plugin, which is compiled for x86_64 (Intel) only.  
Because of this, Unreal Engine must be built and run in x86_64 mode on Apple Silicon Macs.

---

# 🚨 Critical Rule

Unreal MUST run in x86_64 mode for this project.

- ARM (default Mac mode) will cause:
  - module load failures
  - linker errors
  - missing plugin symbols

---

# 🧱 Initial Setup (First Time Only)

## Clean the Project

From your project root directory, run:

```bash
rm -rf Binaries Intermediate DerivedDataCache
```

---

## Generate Xcode Project Files (x86)

```bash
arch -x86_64 /Users/Shared/Epic\ Games/UE_5.6/Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh \
-project="/path/to/FSE100Capstone.uproject" \
-game
```

---

## Build the Project (x86)

```bash
arch -x86_64 /Users/Shared/Epic\ Games/UE_5.6/Engine/Build/BatchFiles/Mac/Build.sh \
FSE100CapstoneEditor Mac Development \
-architecture=x86_64 \
"/path/to/FSE100Capstone.uproject"
```

Wait until you see:

```
BUILD SUCCESSFUL
```

---

# 🚀 Running the Project (REQUIRED EVERY TIME)

⚠️ The project MUST be opened using Terminal every time.

```bash
arch -x86_64 /Users/Shared/Epic\ Games/UE_5.6/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor \
"/path/to/FSE100Capstone.uproject"
```

Opening the project any other way will launch Unreal in ARM mode and cause module load failures.

---

# ❌ DO NOT DO THE FOLLOWING

- Do NOT double-click the `.uproject`
- Do NOT open from Epic Launcher
- Do NOT build using Xcode
- Do NOT allow Unreal to rebuild modules automatically

These will launch Unreal in ARM mode and break the build.

---

# 🔄 Rebuilding After Code Changes

If you:

- pull new C++ changes
- modify plugin code
- get a “Missing Modules” error

Run:

```bash
rm -rf Binaries Intermediate DerivedDataCache

arch -x86_64 /Users/Shared/Epic\ Games/UE_5.6/Engine/Build/BatchFiles/Mac/Build.sh \
FSE100CapstoneEditor Mac Development \
-architecture=x86_64 \
"/path/to/FSE100Capstone.uproject"
```

Then launch again using the run command above.

---

# 📌 Notes

- This limitation only applies to Mac (Apple Silicon)
- Windows builds are unaffected
- This is required due to OVRLipSync being x86_64-only

# Mac Setup (General Requirements)

This section covers macOS-specific setup required to run Unreal Engine, Git, and AI integrations for this project.

---

# 🧰 Xcode Installation (Required)

Unreal Engine requires a specific version of Xcode.  
The App Store version may NOT be compatible.

## Required Version

Xcode 16

Download from:
https://developer.apple.com/download/all/?q=xcode%2016

---

## Setup

After installing, set command line tools:

```bash
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

Verify:

```bash
xcode-select -p
```

---

# 🧰 Git Setup (Required for Unreal Git Plugin)

## Install Git

```bash
git --version
```

If not installed:
https://git-scm.com/install/mac

---

## Install Git LFS

```bash
brew install git-lfs
git lfs install
```

Required for Unreal assets (.uasset, .umap).

---

## Install Git Credential Manager

```bash
brew install --cask git-credential-manager
```

⚠️ Only required once per machine.

---

## ⚠️ Git LFS Permission Issue (Mac)

In some cases, Git LFS may fail due to missing execute permissions on the bundled binary.

### Error Example

If you see the following error in the Unreal output log:

```
LogSourceControl: Error: env: ../../../../../../<project-path>/Plugins/UEGitPlugin/git-lfs-mac-amd64: Permission denied
```

---

### Fix

1. Navigate to the plugin directory in Terminal:

```bash
cd "<path-to-project>/Plugins/UEGitPlugin"
```

2. Grant execute permissions:

```bash
chmod +x git-lfs-mac-amd64
```

---

# 🔐 macOS Security & Permissions

macOS blocks microphone access by default. This must be enabled for voice input.

---

## 🎤 Microphone Access (Required)

Enable access for:

- UnrealEditor-Mac-DebugGame

### Steps:

1. Open:
   System Settings → Privacy & Security → Microphone

2. Enable:
   UnrealEditor-Mac-DebugGame

Without this:

- voice input will not work
- OpenAI audio input will fail

---

# 🔑 OpenAI API Key Setup (Mac)

The OpenAI API key must be configured as an environment variable.

This project requires the following variable name:

```
CAPSTONE_PROJECT_OPENAI_API_KEY
```

---

# Option 1: Permanent Setup (Recommended)

This method ensures the API key is available every time you open a terminal or run Unreal.

## Identify your shell

Run:

```bash
echo $SHELL
```

- If it returns `/bin/zsh` → use `.zshrc`
- If it returns `/bin/bash` → use `.bash_profile`

---

## Open your shell configuration file

### For Zsh:
```bash
nano ~/.zshrc
```

### For Bash:
```bash
nano ~/.bash_profile
```

---

## Add the API key

Add this line at the bottom of the file:

```bash
export CAPSTONE_PROJECT_OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

---

## Save and exit

- Press `Ctrl + O`, then `Enter`
- Press `Ctrl + X`

---

## Apply changes

### For Zsh:
```bash
source ~/.zshrc
```

### For Bash:
```bash
source ~/.bash_profile
```

---

# Option 2: Temporary Setup

Use this if you only need the key for the current terminal session.

```bash
export CAPSTONE_PROJECT_OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

⚠️ This will be lost when the terminal is closed.

---

# 🔍 Verify Setup

Run:

```bash
echo $CAPSTONE_PROJECT_OPENAI_API_KEY
```

If set correctly, this will output your API key.

---

# ⚠️ Important Notes

- The variable name must be exactly:
  ```
  CAPSTONE_PROJECT_OPENAI_API_KEY
  ```

- This must match the name used in the project code

- Unreal Engine must be launched from an environment where this variable is available  
  (this is already satisfied when launching via the required terminal command)

- If the variable is not set, Unreal will log:
  ```
  CAPSTONE_PROJECT_OPENAI_API_KEY environment variable is not set
  ```

---

# 📌 Notes

- These steps apply only to macOS
- Windows setup differs (environment variables are set through System settings)
- Missing any of these steps may result in:
  - build failures
  - Git integration not working
  - voice input not functioning

# 🥽 VR Testing Limitations on Mac (Meta Quest)

macOS does NOT support direct VR testing with Meta Quest using Unreal Engine.

---

## 🚫 Meta Quest Link (Not Supported on Mac)

Meta Quest Link (USB or Air Link) is not supported on macOS.

This means:

- You cannot use "VR Preview" in Unreal Engine on Mac
- You cannot connect a Quest headset for live testing from the Editor

---

## 🚫 Meta XR Simulator (Not Supported on Mac)

The Meta XR Simulator is not available on macOS.

This means:

- You cannot simulate VR interactions within Unreal on Mac
- You cannot test motion controllers or headset movement locally

---

## ✅ Supported Workflows

### Option 1 — Use a Windows Machine (Recommended)

For full VR testing:

- Use a Windows machine with Meta Quest Link enabled
- Run Unreal Engine VR Preview
- Test interactions, UI, and performance in real time

---

### Option 2 — Package and Deploy to Headset

If a Windows machine is not available:

1. Package the project for Android (Quest)
2. Install the build directly onto the headset
3. Test within the standalone environment

---

## ⚠️ Important Notes

- Mac can still be used for:
  - development
  - Blueprint work
  - C++ implementation
  - UI and interaction setup

- However, ALL real-time VR testing must be done using:
  - Windows + Quest Link  
  - or packaged builds on the headset

---

## 📌 Summary

macOS is not suitable for real-time VR testing with Meta Quest.

A Windows machine or packaged headset build is required for validating VR functionality.