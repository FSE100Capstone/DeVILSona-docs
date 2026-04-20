# Deployment and Launch Guide

This page explains the two supported deployment methods for the project:

1. **Android APK deployment to Meta Quest headset**
2. **Windows desktop executable launch through Meta Quest Link**

It also explains how to install and launch each version.

---

## Overview

The project supports two main deployment workflows:

- **Android / Meta Quest deployment**
  - The project is packaged as an **APK** for direct installation onto the headset
  - Depending on build size, this may also include one or more **OBB** files
  - This version runs directly on the headset without requiring a PC connection after installation

- **Windows desktop deployment through Meta Quest Link**
  - The project is packaged as a **Windows executable**
  - The headset must be connected to the PC through **Meta Quest Link**
  - The desktop application is launched from the PC and viewed through the headset

These two workflows are used for different purposes. The Android build is used for direct on-device deployment, while the Windows desktop build is useful for running the full desktop version through a PC-connected headset.

---

## Prerequisites for Meta Quest Android Deployment

Before installing an APK to the headset, the following must be true:

- A **Meta Developer account** must be created and linked to the Meta account used on the headset
- **Developer Mode** must be enabled for the headset
- The headset must be connected to the PC by USB
- The required **USB permission prompts inside the headset must be accepted**

### Important Note

Enabling **Developer Mode** by itself is **not enough**.

When the headset is connected by USB, the user must also accept the permission prompts that appear inside the headset, such as:

- **USB data access**
- **USB debugging / allow USB debugging**

If those prompts are not accepted, Android install methods such as the generated Unreal install script or SideQuest will fail even if Developer Mode is already enabled.

---

## Deployment Type 1: Android APK for Meta Quest

### Purpose

This deployment method installs the application directly onto the Meta Quest headset. It is used when the experience should run natively on the headset without relying on a PC at runtime.

### Typical Output Files

An Android deployment may produce:

- `.apk`
- `.obb`
- additional `.obb` files in larger builds

Common examples:

- `FSE100Capstone-Android-Shipping-arm64.apk`
- `main.1.com.YourCompany.FSE100Capstone.obb`

---

## Option A: Install Using Unreal's Generated Install Script

If the packaged Android output includes an install script such as:

- `Install_FSE100Capstone-Android-Shipping-arm64.bat`

this is usually the easiest installation method.

### Requirements

Before running the install script:

- Developer Mode must be enabled
- The headset must be connected by USB
- The user must accept the USB permission prompts inside the headset

### Steps

1. Connect the Meta Quest headset to the PC with a USB cable.
2. Put on the headset.
3. Accept any prompts related to:
   - **USB data access**
   - **USB debugging**
4. On the PC, open the packaged Android build folder.
5. Double-click the generated install script.
6. Wait for the script to:
   - install the APK
   - copy the required OBB file(s)
7. When the install window closes, the application should be installed on the headset.

### Important Note

If the USB permission prompts were not accepted inside the headset, the install script may fail even if the headset is already in Developer Mode.

### Launching After Install

1. Put on the headset.
2. Open **Library**.
3. Open **Unknown Sources**.
4. Select the installed application.
5. Launch it from the headset.

---

## Option B: Install Using SideQuest

SideQuest can also be used to install the Android build onto the headset.

### Requirements

- SideQuest installed on the PC
- A **Meta Developer account**
- Developer Mode enabled on the headset
- Headset connected by USB
- USB permission prompts accepted inside the headset

### Important Note

SideQuest installation will not work correctly if the headset is connected but the user did not accept the required USB prompts in the headset.

### Install the APK

1. Open **SideQuest** on the PC.
2. Confirm the headset is connected.
3. Drag the main `.apk` file into the SideQuest window.

Use the main APK, not any helper APK such as an `AFS_` file.

Example:

- Use: `FSE100Capstone-Android-Shipping-arm64.apk`
- Do not use: `AFS_FSE100Capstone-Android-Shipping-arm64.apk`

### Install the OBB

If the build includes an OBB file, it must be placed in the correct folder on the headset.

### OBB Folder Format

```text
/Android/obb/<package.name>/

Example:
/Android/obb/com.YourCompany.FSE100Capstone/

## Steps

1. In SideQuest, open the headset file browser.
2. Navigate to:
   - `Android`
   - `obb`
3. Create the package folder if it does not already exist.
4. Copy the `.obb` file into that folder.

### Example final location

`/Android/obb/com.YourCompany.FSE100Capstone/main.1.com.YourCompany.FSE100Capstone.obb`

## Launching After Install

1. Put on the headset.
2. Open **Library**.
3. Open **Unknown Sources**.
4. Select the installed application.
5. Launch it from the headset.

## Post-Install Audio Checks

After installing the APK, verify the headset audio and microphone settings before testing AI voice input.

### Check That the Microphone Is Not Muted

Make sure the headset microphone is not muted before launching the application.

### Check App Microphone Permission

In the headset, go to:

**Settings → Privacy → Installed Apps → FSE100 → Permission for Mic**

Make sure microphone permission is enabled for the application.

### Important Note

Even if the APK installs correctly, AI voice input will not work if:

- the headset microphone is muted
- the application does not have microphone permission enabled in headset settings

---

## Deployment Type 2: Windows Desktop Executable Through Meta Quest Link

### Purpose

This deployment method runs the Windows build on a desktop PC while the headset is connected through **Meta Quest Link**. The application runs on the PC, and the headset acts as the VR display/output device.

This is different from the Android build because the application is not running natively on the headset.

### Requirements

Before launching the desktop build:

- Meta Quest headset connected to the PC by USB
- Meta Quest Link / Meta Horizon Link installed and working
- Headset in Quest Link mode
- The Windows build packaged successfully
- A desktop executable available, such as:
  - `FSE100Capstone.exe`

## Launching the Desktop Build

1. Connect the headset to the PC using a USB cable.
2. Put on the headset.
3. Make sure **Quest Link** / **Meta Horizon Link** is active.
4. Confirm the headset is currently in Link mode.
5. On the PC, open the packaged Windows build folder.
6. Double-click the application `.exe` file.
7. Wait for the application to launch.
8. Use the headset controllers to interact with the application.

### Notes

- The headset must remain connected to the PC while using the desktop build.
- This version is launched from the desktop, not from **Unknown Sources** on the headset.
- If the headset is not in Link mode, the executable may launch on the desktop monitor without entering the headset properly.

---

## Recommended Usage

### Use the Android APK build when:

- the experience should run directly on the headset
- you are testing native headset deployment
- you need to validate actual Android / Quest behavior

### Use the Windows desktop executable when:

- you want to run the PC version in VR
- the headset is connected through Meta Quest Link
- you want to use desktop rendering/features instead of native Android deployment

---

## Common Installation Notes

- A Meta Developer account is required in order to enable Developer Mode
- Developer Mode alone is not enough for USB installation workflows
- The user must also accept the required USB prompts inside the headset
- Always use the main packaged APK for headset installation
- If an OBB is generated, it must be copied to the correct package-name folder on the headset
- If an install script is provided by Unreal, it is usually the simplest Android installation method
- For the desktop build, the headset must already be connected through Meta Quest Link before launching the `.exe`

---

## Troubleshooting

### Install Script or SideQuest Cannot Install to Headset

Check the following:

- Developer Mode is enabled
- the Meta account has a linked Meta Developer account
- the headset is connected by USB
- the USB permission prompts inside the headset were accepted

If the USB prompts were not accepted, both the generated install script and SideQuest may fail.

### APK Installed but App Does Not Launch Correctly

Possible causes include:

- OBB file missing
- OBB copied to the wrong folder
- package name folder mismatch
- incomplete install

Check that the OBB is stored in the correct path under:

`/Android/obb/<package.name>/`

### App Not Found on Headset

If the APK was installed successfully, the app should appear under:

- **Library**
- **Unknown Sources**

If it does not appear there, the install may not have completed correctly.

### Desktop Executable Does Not Open in Headset

Check that:

- the headset is connected by USB
- Meta Quest Link is active
- the headset is currently in Link mode
- the `.exe` was launched after Link was already active

---

## Summary

The project supports two deployment methods:

### Android APK deployment

- install directly to the headset
- launch from **Unknown Sources**
- can be installed using Unreal's install script or SideQuest

### Windows desktop deployment

- connect headset through Meta Quest Link
- launch the packaged `.exe` on the PC
- use headset controllers for interaction
