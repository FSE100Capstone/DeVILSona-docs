# Meta Quest Link Setup and Unreal Engine VR Preview Guide

This guide explains how to set up a Meta Quest headset for Unreal Engine development using **Meta Horizon Link**. It includes the required account setup, mobile and desktop apps, developer mode, USB connection, OpenXR configuration, and how to use **VR Preview** in Unreal Engine.

## Official References

- [Meta Quest Link Requirements](https://www.meta.com/help/quest/140991407990979/)
- [Meta Quest Link and Unreal Instructions](https://developers.meta.com/horizon/documentation/unreal/unreal-link/)

---

## Overview

Meta Quest Link allows a Meta Quest headset to function as a PC VR headset so Unreal Engine projects can be tested directly from the editor using **VR Preview**. This is much faster than packaging and installing a full APK every time you want to test a change.

---

## Requirements

Before starting, make sure you have:

- A compatible **Meta Quest headset**
  - Meta Quest 3S
  - Meta Quest 3
  - Meta Quest 2
  - Meta Quest Pro
- A compatible **Windows PC**
- A **Meta account**
- A **Meta Developer account**
- The **Meta Horizon mobile app**
- The **Meta Horizon Link desktop app**
- **Unreal Engine** installed on the development PC
- A **USB-C cable** that supports data transfer
  - A wired USB connection is recommended for setup and development because it is generally more stable than wireless

---

## Part 1: Create or Confirm a Meta Developer Account

A **Meta Developer account** is required for Link-based app development workflows.

### Steps

1. Sign in with your Meta account.
2. Create or confirm access to a **Meta Developer account**.
3. Use the same account for the headset, mobile app, and desktop Link app.

---

## Part 2: Install the Meta Horizon Mobile App

The mobile app is required for headset setup and enabling Developer Mode.

### Steps

1. Install the **Meta Horizon mobile app** on your phone.
2. Sign in with your Meta account.
3. Turn on the headset.
4. Pair the headset to the mobile app if it is not already paired.
5. Confirm the headset appears in the app under connected devices.

---

## Part 3: Enable Developer Mode

Developer Mode must be enabled for development workflows such as USB debugging and Unreal Engine testing.

### Steps

1. Open the **Meta Horizon mobile app**.
2. Select your connected headset.
3. Open the headset settings.
4. Find **Developer Mode**.
5. Turn **Developer Mode** **On**.
6. Restart the headset if prompted.

---

## Part 4: Install Meta Horizon Link on Desktop

The desktop Link application is required for connecting the headset to the PC for Unreal Engine VR Preview.

### Steps

1. Download and install **Meta Horizon Link** on the Windows development machine.
2. Sign in using the same Meta account used on the headset and mobile app.
3. Open the app and allow it to finish setup or updates.

---

## Part 5: Configure Meta Horizon Link for Development

These settings should be configured before using Unreal Engine with Link.

### Activate OpenXR Runtime

1. Open the **Meta Horizon Link** app on the desktop.
2. Go to **Settings > General**.
3. Next to **OpenXR Runtime**, select **Set Meta Horizon Link as active**.
4. Once active, the option becomes grayed out.

### Toggle Developer Runtime Features

1. In the **Meta Horizon Link** app, go to **Settings > Developer**.
2. Turn **Developer Runtime Features** **On**.

### Optional Feature Toggles

If your project needs specific runtime features over Link, return to **Settings > Developer** and enable them there. Depending on the project, these can include features such as:

- Passthrough over Meta Horizon Link
- Eye tracking over Meta Horizon Link
- Natural Facial Expressions over Meta Horizon Link

If you enable new runtime features while Unreal Engine is already open, restart the editor before testing.

---

## Part 6: Connect the Headset to the PC

A wired connection is the recommended development workflow.

### USB Connection Steps

1. Connect the headset to the PC with a **USB-C data cable**.
2. Put on the headset.
3. Accept any prompts for:
   - **USB data access**
   - **USB debugging**
4. Open the **Meta Horizon Link** desktop app.
5. Confirm the headset appears under **Devices**.

### Test the Cable Connection

In the **Meta Horizon Link** app:

1. Go to **Devices**.
2. Select the connected headset.
3. Select **Device Setup**.
4. Choose **Link Cable**.
5. Select **Continue**.
6. On the cable check page, select **Test Connection**.
7. Confirm the result shows a compatible connection.

If the connection is weak or incompatible, try a different USB-C cable.

---

## Part 7: Enable Quest Link on the Headset

### Steps in the Headset

1. Put on the headset.
2. Open **Settings**.
3. Go to **System**.
4. Find **Quest Link**.
5. Turn **Quest Link** on.
6. Select **Launch Quest Link**.

This should move the headset into the PC VR / Link environment.

---

## Part 8: Use Meta Quest Link with Unreal Engine

Once the headset is connected and Link is active, Unreal Engine can use the headset directly.

### Steps

1. Open the Unreal Engine project on the development PC.
2. Wait for the project to finish loading.
3. Open the level you want to test.
4. Make sure the headset is connected through **Meta Horizon Link** and currently in Link mode.
5. In Unreal Engine, click **Play** and choose **VR Preview**.

### Expected Behavior

- The Unreal scene should launch directly to the headset.
- The headset should switch from the Link interface into the Unreal project.
- Tracking data from the headset and controllers should be available in the editor session.

---

## Part 9: Recommended Development Workflow

A common workflow during development is:

1. Connect the headset by USB.
2. Open **Meta Horizon Link**.
3. Confirm the headset is connected.
4. Launch **Quest Link** from the headset.
5. Open the Unreal project.
6. Make your changes.
7. Use **VR Preview** to test quickly.
8. Stop the preview.
9. Repeat as needed.

This workflow is much faster than packaging an APK after every change.

---

## Part 10: Preview Platform Notes in Unreal

Unreal Engine supports previewing platform-specific rendering settings.

### Notes

- In Unreal, preview platform options are available under **Settings > Preview Platform**.
- Quest uses **Vulkan** rendering.
- Link can support both **OpenGL** and **Vulkan** during development workflows.

This can be useful when checking how a project may behave under Quest-targeted rendering.

---

## Part 11: Optional Development Convenience

### Disable the Proximity Sensor

If the headset keeps sleeping when you remove it during development, the proximity sensor can be disabled temporarily using **Meta Quest Developer Hub (MQDH)**.

### Steps

1. Connect the headset to the development PC.
2. Open **MQDH**.
3. Go to **Device Manager**.
4. Select the headset.
5. Under **Device Actions**, find **Proximity Sensor**.
6. Toggle it to disable the proximity sensor temporarily.

This is useful during long testing sessions.

---

## Important Notes

- Link helps reduce iteration time, but it is **not identical** to running a packaged APK directly on the headset.
- Visual appearance and performance can differ between **VR Preview over Link** and a packaged Android build.
- Final validation should still be done with an actual headset build installed on the device.

---

## Troubleshooting

## Common VR Preview Black Screen Issue

It is common for **VR Preview** to launch to a black screen the first time, especially if another play mode such as **Selected Viewport** was used immediately before it. This can also happen occasionally even without switching play modes.

In most cases, this does not mean the headset or project is broken.

### Recommended Fix

1. Press **Esc** to exit the failed VR Preview session.
2. Launch **VR Preview** again.

The second launch will often load correctly.

## Headset Does Not Show Up in Meta Horizon Link

- Confirm the USB cable supports data transfer, not just charging
- Try a different USB port
- Reconnect the cable
- Restart the headset
- Restart the Meta Horizon Link app

## VR Preview Does Not Launch Correctly

- Make sure the headset is already connected and in **Quest Link** mode
- Make sure **Meta Horizon Link** is open before launching **VR Preview**
- Restart Unreal Engine after changing Link developer features
- Confirm **Meta Horizon Link** is set as the active **OpenXR Runtime**

## USB Debugging Prompt Does Not Appear

- Reconnect the headset
- Confirm **Developer Mode** is enabled in the mobile app
- Check for prompts inside the headset

## Performance or Connection Quality Is Poor

- Use a different USB-C cable
- Run the **Test Connection** option in the Link app
- Prefer wired USB for development
- Close unnecessary background applications on the PC

---

## Summary

To use Meta Quest Link with Unreal Engine:

1. Create or confirm a **Meta Developer account**
2. Install the **Meta Horizon mobile app**
3. Pair the headset
4. Enable **Developer Mode**
5. Install **Meta Horizon Link** on the desktop PC
6. Set **Meta Horizon Link** as the active **OpenXR Runtime**
7. Turn on **Developer Runtime Features**
8. Connect the headset by **USB-C**
9. Enable and launch **Quest Link**
10. Open Unreal Engine and use **VR Preview**

This is the primary workflow for fast VR iteration during development.
