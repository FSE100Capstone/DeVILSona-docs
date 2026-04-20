# UE5 Android APK Build Guide (MetaHuman Variant)

This page documents the full Android APK build workflow used for the **MetaHuman / Lip Sync / Meta XR** version of the project. Unlike the standard Android build path, this version required additional Android setup, plugin configuration, project setting changes, Meta XR validation, and repeated cleanup/rebuild attempts before a successful APK + OBB build was produced.

This guide is ordered from the **initial Android setup** through the **MetaHuman-specific changes** and finally the **cook / package / install workflow**.

## Related References

- [Advanced Setup and Troubleshooting Guide for Using Android SDK (UE 5.6)](https://dev.epicgames.com/documentation/unreal-engine/advanced-setup-and-troubleshooting-guide-for-using-android-sdk?application_version=5.6)
- [Set Up Android SDK, NDK, and Android Studio Using Turnkey for Unreal Engine (UE 5.6)](https://dev.epicgames.com/documentation/unreal-engine/set-up-android-sdk-ndk-and-android-studio-using-turnkey-for-unreal-engine?application_version=5.6)

---

## Overview

This workflow was used to build the **MetaHuman-enabled Android APK** version of the project for direct installation onto Meta Quest hardware. Compared to the standard Android build flow, this version required:

- Android support to be installed for UE 5.6
- Android Studio and the correct SDK / NDK configuration
- Turnkey setup / verification
- additional Android project settings
- Meta XR project setup validation
- stricter plugin configuration
- repeated cleanup between failed package attempts

This build path also preserves a **separate OBB file** instead of packaging all game data inside the APK.

---

## Part 1: Install Android Support for Unreal Engine 5.6

Before opening the project in Unreal Engine, make sure Android support is installed for the engine version being used.

### Steps

1. Open **Epic Games Launcher**.
2. Go to **Library**.
3. Find **Unreal Engine 5.6**.
4. Click the dropdown / options menu for that engine version.
5. Open **Options**.
6. Make sure **Android** is checked under **Target Platforms**.
7. Apply the changes if needed.

---

## Part 2: Install Android Studio

Install the Android Studio version referenced in Epic’s UE 5.6 Android setup documentation:

- **Android Studio Koala Feature Drop | 2024.1.2 Patch 1**
- **September 17, 2024**

This is the version Epic explicitly calls out in the advanced Android SDK setup guide.

---

## Part 3: Install Android SDK / NDK Components

After installing Android Studio:

1. Open **Android Studio**.
2. Open **SDK Manager**.
3. Install the required Android SDK components.
4. Install the required Android command-line tools.
5. Install the NDK version used by this project:

- `NDK 26.1.10909125`

This MetaHuman build specifically used `NDK 26.1.10909125`.

---

## Part 4: Run Turnkey / Verify Android Setup in Unreal

Epic’s recommended UE 5.6 workflow is to use Unreal’s Android setup / Turnkey flow first.

### Steps

1. Open the project in **Unreal Engine 5.6**.
2. Go to **Platforms → Android**.
3. If available, run the Android setup / install flow from Unreal.
4. Let Unreal verify or install the Android dependencies it can manage automatically.

If the project still has Android toolchain issues after this, continue with the manual verification and troubleshooting steps below.

---

## Part 5: Update SDK / NDK / Java Paths

Once Android Studio and the correct NDK are installed, update the SDK / NDK paths both on the machine and in Unreal.

### Environment / System Paths

Update the relevant environment variable paths on the machine so they point to the correct Android SDK / NDK locations.

### Unreal Engine Paths

Go to:

**Platforms → Android SDK**

and confirm the paths point to the correct installed locations.

This build specifically required updating the paths so they pointed to:

- the correct Android SDK
- `NDK 26.1.10909125`
- the correct Java location

---

## Part 6: Configure Android in the Project

Go to:

**Project Settings → Platforms → Android**

If a red banner appears saying the project is not configured for Android:

- click **Configure Now**

This must be completed before continuing.

---

## Part 7: Configure Android Project Settings

Go to:

**Project Settings → Platforms → Android**

Apply the following settings.

### SDK Version Settings

- Set **Minimum SDK Version** to `31`
- Set **Target SDK Version** to `34`

### APK / OBB Settings

- Turn **off** **Package game data inside .apk**
  - this preserves a separate `.obb` file
- Leave these enabled:
  - **Allow large OBB files**
  - **Allow patch OBB file**
  - **Allow overflow OBB files**

### Texture Format Settings

Under **Multi Texture Format**:

- disable **ETC2**
- disable **DXT**
- leave only **ASTC** enabled

### Build Architecture Settings

Under **Build**:

- enable **Support arm64 [aka arm64-v8a]**
- disable **Support x86_64 [aka x64]**

### Android Permission Settings

Make sure the following are enabled exactly:

- `android.permission.INTERNET`
- `android.permission.RECORD_AUDIO`
- **Add permissions to support Voice chat (RECORD_AUDIO)**
- **Request permission at startup for Voice chat (RECORD_AUDIO)**

---

## Part 8: Configure Packaging Settings

Go to:

**Project Settings → Project → Packaging**

Make sure:

- **Create compressed cooked packages** is enabled

---

## Part 9: Configure Meta XR Project Settings

Go to:

**Project Settings → Meta XR**

Then:

1. Run **MetaXR Project Setup Tool**
2. Click **Apply All** for all rules

This step was required for the Meta XR portion of the project configuration.

---

## Part 10: Configure Plugins for the MetaHuman Variant

This build required a more restrictive plugin setup than the standard Android workflow.

### Meta XR Plugin

Place the **MetaXR** plugin in:

`Engine/Plugins/Marketplace`

and remove it from the project plugins folder if it exists there.

### MetaHuman Plugins

Disable all MetaHuman plugins **except**:

- **MetaHuman Creator**
- **MetaHuman SDK**
- **MetaHuman Core Tech**
- **MetaHuman Animator**

This reduced conflicts and matched the final working MetaHuman APK configuration.

---

## Part 11: MetaHuman-Specific Build Notes

Compared to the standard Android build workflow, this MetaHuman version required:

- the correct NDK version
- more careful plugin selection
- Meta XR rule validation
- ASTC-only texture output
- separate OBB packaging
- more cleanup and retry cycles after failed package attempts

---

## Part 12: Cook the Project First

Before attempting a full package, do a clean Android cook first.

Go to:

**Platforms → Android**

Then run **Cook Project**.

### Goal

The goal is to get a clean cook before attempting a full package.

### What to Fix

During the cook:

- resolve **red errors**
- warnings can usually be left alone unless they are clearly blocking packaging

---

## Part 13: Package the Project

Once the cook is clean:

1. Go to **Platforms → Android**
2. Run **Package Project**

---

## Part 14: If Packaging Still Fails After a Clean Cook

Even if the cook completed successfully, packaging may still surface additional cook/package errors.

If that happens:

1. Resolve the new blocking errors.
2. Close Unreal Engine.
3. Delete:
   - `DerivedDataCache`
   - `Saved/StagedBuilds`
   - `Intermediate/Android`
4. Open **Visual Studio**.
5. Build the project in Visual Studio.
6. Launch Unreal Engine from Visual Studio once the build completes.
7. Try packaging again.

This process may need to be repeated multiple times.

---

## Part 15: Reality of the MetaHuman Android Build Process

This build process was not consistently one-pass successful. In practice, it often required:

- fixing one group of errors
- cleaning intermediate folders
- rebuilding
- reopening in Visual Studio
- trying again

In other words:

1. Fix the blocking errors
2. Clean the Android / intermediate output
3. Rebuild
4. Try again
5. Cross your fingers

---

## Part 16: Successful Output

When successful, the build produced:

- main Android APK
- separate OBB file
- Unreal-generated install script

Because **Package game data inside .apk** was disabled, the build preserved a separate `.obb` file rather than forcing everything into the APK.

---

## Part 17: Installing the Successful Build to the Headset

After the MetaHuman Android build succeeded, the APK was installed using the generated Unreal install script rather than SideQuest.

### Method Used

Run the generated file from the packaged Android output folder:

- `Install_FSE100Capstone-Android-Shipping-arm64.bat`

### Why This Was Useful

This method handled:

- APK installation
- OBB placement
- direct headset installation over USB

### Requirements

For the install script to work:

- the headset must be connected to the PC by USB
- **Developer Mode** must already be enabled
- the USB prompts inside the headset must be accepted, including:
  - USB data access
  - USB debugging

---

## Part 18: Recommended Summary Workflow

1. Install Android support for UE 5.6 through **Epic Games Launcher**
2. Install **Android Studio Koala Feature Drop | 2024.1.2 Patch 1**
3. Install the required Android SDK components
4. Install **NDK 26.1.10909125**
5. Run Unreal’s Android setup / Turnkey flow first
6. Update machine environment paths and Unreal Android SDK paths
7. Open the project and configure Android if the red banner appears
8. Configure Android settings:
   - separate OBB
   - ASTC only
   - Min SDK 31
   - Target SDK 34
   - arm64 only
   - required audio / internet permissions
9. Enable compressed cooked packages
10. Move **MetaXR** plugin to `Engine/Plugins/Marketplace`
11. Disable all unnecessary MetaHuman plugins
12. Run **MetaXR Project Setup Tool** and apply all rules
13. Cook Android first
14. Resolve blocking cook errors
15. Package Android
16. If packaging still fails:
   - close Unreal
   - delete `DerivedDataCache`
   - delete `Saved/StagedBuilds`
   - delete `Intermediate/Android`
   - rebuild in Visual Studio
   - reopen from Visual Studio
   - try again
17. Once successful, use the generated **Install** `.bat` file to install to the headset

---

## Notes

This MetaHuman Android build flow should be treated as a troubleshooting-heavy workflow rather than a guaranteed one-pass packaging path. The baseline Android environment must be configured first, and the MetaHuman-specific changes should then be layered on top of that setup.
