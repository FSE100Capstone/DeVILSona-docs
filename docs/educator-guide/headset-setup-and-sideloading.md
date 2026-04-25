# Headset Setup & Sideloading

!!! info "Audience"
    Educators performing the one-time setup to prepare Meta Quest headsets for running DeVILSona.

This page walks you through the initial setup process for each Meta Quest headset, including enabling the required developer settings, installing the DeVILSona app, and preparing the DeVILStarter launcher on your laptop. **You only need to do this once per headset** — after the initial setup, headsets are ready for repeated classroom use.

---

## Step 1: Enable Developer Mode on Each Headset

By default, Meta Quest headsets can only install apps from the official Meta store. Since DeVILSona is a custom application, you need to enable **Developer Mode** to allow installation of apps from other sources (called "sideloading").

### Prerequisites

- A **Meta developer account** (free — sign up at [https://developer.oculus.com](https://developer.oculus.com))
- The **Meta Horizon mobile app** installed on your phone ([iOS](https://apps.apple.com/app/meta-horizon/id1366478176) / [Android](https://play.google.com/store/apps/details?id=com.oculus.twilight))
- The headset **paired** with your Meta account in the Meta Horizon app

### Steps

1. Open the **Meta Horizon** app on your phone
2. Tap on your **headset** in the Devices tab
3. Navigate to **Settings → Developer Mode**
4. Toggle **Developer Mode: ON**
5. Put on the headset — if prompted, click **"Allow Developer Features"** to confirm

!!! note
    You only need to do this once per headset. Developer Mode stays enabled until you manually turn it off.

---

## Step 2: Install SideQuest on Your Computer

**SideQuest** is a free desktop application that makes it easy to install apps onto your Meta Quest headset without needing command-line tools. It provides a simple drag-and-drop interface for managing VR applications.

### Download and Install

1. Go to [https://sidequestvr.com/setup-howto](https://sidequestvr.com/setup-howto)
2. Download the **SideQuest Advanced Installer** for Windows
3. Run the installer and follow the on-screen prompts
4. Launch SideQuest after installation completes

!!! tip "Official SideQuest Documentation"
    For detailed installation instructions and troubleshooting, refer to the official SideQuest setup guide: [SideQuest Setup How-To](https://sidequestvr.com/setup-howto)

---

## Step 3: Install the DeVILSona App on Each Headset

### Connect the Headset

1. Use a **USB-C data cable** to connect the Meta Quest headset to your computer

    !!! warning
        Not all USB-C cables support data transfer — some only charge. Use the cable that came with your headset, or a cable you know works for data.

2. **Put on the headset** and look for a popup asking **"Allow USB Debugging?"** — select **Allow** (and optionally check "Always allow from this computer")
3. In SideQuest, check the **connection indicator** in the top-left corner:
    - 🟢 **Green** = Connected and ready
    - 🔴 **Red** = Not detected — try a different USB cable or USB port

### Install the APK

1. In SideQuest, click the **"Install APK file from folder on computer"** button (the folder icon with a down arrow in the top toolbar)
2. Navigate to the DeVILSona APK file on your computer and select it
3. SideQuest will install the app and show a **success notification** when complete

!!! warning "Which APK File to Select"
    When you build or receive the DeVILSona APK, you may see multiple APK files in the output folder. **Always install the LARGEST APK file.** The smaller APK is incomplete and will not work properly on its own. The large APK packages all game content inside it.

### Verify the Installation

1. Put on the headset
2. Open the **App Library** (the grid icon at the bottom of the home screen)
3. Tap the **"Unknown Sources"** tab (sideloaded apps appear here, not in the main list)
4. You should see **"FSE100Capstone"** (or similar) listed
5. Tap to launch it and verify the login screen appears

### Installing on Multiple Headsets

Repeat the connect → install → verify process for each headset. With SideQuest, you can only install to **one headset at a time** via USB.

!!! tip "Batch Installation Tip"
    If you have a USB hub, you can connect multiple headsets at once — but SideQuest will only detect one at a time. Disconnect and reconnect headsets one by one to install sequentially. The installation itself takes about 1–2 minutes per headset.

---

## Step 4: Set Up DeVILStarter (First Time Only)

**DeVILStarter** is the desktop application you use before each class session to start and stop the cloud backend. Setting it up for the first time takes about 5 minutes.

### Download DeVILStarter

1. On your **Windows laptop**, navigate to the [DeVILStarter GitHub Releases page](https://github.com/FSE100Capstone/DeVILStarter/releases/latest)
2. Click on **"DeVILStarter.exe"** to download the application
3. Save it to a convenient location (e.g., your Desktop or Documents folder)

### First Launch

1. Double-click **DeVILStarter.exe** to launch it
2. DeVILStarter will initialize and check for required dependencies
3. If prompted to log into your **ASU account**, follow the on-screen instructions — DeVILStarter uses your ASU credentials to access the AWS cloud backend

!!! note
    DeVILStarter handles all the cloud configuration automatically. You do not need to install any additional tools (like Terraform or the AWS CLI) — they are bundled with the application.

### Verify It Works

1. Click the **power slider** to start the cloud infrastructure
2. If prompted, log into your ASU account and confirm the matching code
3. Wait for the status to show **"Infrastructure deployed"** (typically 2–5 minutes on first run)
4. Click the power slider again to **stop** the infrastructure
5. Wait for the status to show **"Infrastructure stopped"**

If this works, your setup is complete. For day-of session instructions, see [Running a Session](running-a-session.md).

---

## Setup Checklist

Before your first classroom session, verify all of the following:

- [ ] Developer Mode enabled on **all** headsets
- [ ] SideQuest installed on your Windows computer
- [ ] DeVILSona APK installed on **all** headsets (appears under "Unknown Sources")
- [ ] DeVILSona app launches successfully on each headset (login screen visible)
- [ ] Wi-Fi configured on each headset (correct SSID and password)
- [ ] DeVILStarter downloaded and tested on your Windows laptop
- [ ] DeVILStarter successfully starts and stops the cloud infrastructure

---

➡️ **Next:** [Network Requirements](network-requirements.md)
