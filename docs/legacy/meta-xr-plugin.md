
# 🥽 Meta XR Plugin – Unreal Engine Integration Guide

This document explains how to install and configure the **Meta XR Plugin** for Unreal Engine 5.  
It also compares the plugin to the default **OpenXR Plugin**, and provides full setup steps for both **Windows** and **macOS**.

---

# Overview

**Meta XR Plugin** is Meta's official integration for Unreal Engine.  
Unlike the generic OpenXR plugin, Meta XR provides:

- Full optimization for Quest devices (Quest 1, 2, 3, Pro)
- Native hand tracking
- Passthrough & Mixed Reality support
- Scene Understanding (Scene Mesh)
- Spatial Anchors
- Better standalone VR performance
- Meta-specific rendering & tracking improvements

If you are building VR for **Meta Quest standalone**,  
**Meta XR Plugin is strongly recommended over OpenXR**.

---

# Why Meta XR Plugin is Better Than OpenXR

| Feature | OpenXR Plugin | Meta XR Plugin | Notes |
|--------|----------------|----------------|-------|
| Quest standalone optimization | ⚠️ Basic | ✅ Full | Better FPS + stability |
| Hand tracking support | Limited | **Full** | Joint tracking, gestures |
| Passthrough (MR) | Very limited | **Full Passthrough API** | Essential for MR |
| Scene Understanding | ❌ No | **Yes** | Scene mesh + anchors |
| Mixed Reality depth blending | ❌ No | **Yes** | MR compositing |
| Spatial anchors | ❌ No | **Yes** | Persistent room positions |
| Controller haptics | Basic | **Advanced** | Meta haptic feedback modes |
| Standalone performance | Moderate | **Optimized** | Foveated rendering pathway |

### Summary
**Meta XR = Maximum performance, full Quest features & MR support**  
**OpenXR = Works everywhere but limited on Quest**

---

# Installation Guide (Windows + macOS)

This section explains the correct way to install the Meta XR Integration Package from Meta’s official website.

---

# Windows Installation

## ✔ Step 1. Disable OpenXR Plugin
1. Open Unreal Engine
2. Go to: **Edit → Plugins**
3. Search for **OpenXR**
4. Disable all:
   - `OpenXR`
   - `OpenXR Input`
   - Any related OpenXR extensions
5. Restart Unreal Engine

---

## ✔ Step 2. Download Meta XR Integration

Download the official plugin from Meta:  
👉 **https://developers.meta.com/horizon/downloads/package/unreal-engine-5-integration**

Download the `.zip` package for UE5.

---

## ✔ Step 3. Install the Plugin

1. Navigate to your UE installation location:

```

UE5 Installation Folder/Engine/Plugins/Marketplace/

```

Example:
```

C:/Program Files/Epic Games/UE_5.5/Engine/Plugins/Marketplace/

```

2. If **Marketplace** folder does not exist → **create it manually**
3. Unzip the downloaded Meta XR package
4. Move the extracted folder into:

```

Engine/Plugins/Marketplace/

```

5. Restart Unreal Engine

You should now see **Meta XR** plugins in the Plugin Manager.

---

# macOS Installation

macOS cannot build Android APK,  
but it can still edit, test, and run Meta XR preview via streaming.

## ✔ Step 1. Disable OpenXR Plugin
Same as Windows:

- Go to **Edit → Plugins**
- Disable all OpenXR-related plugins
- Restart Unreal Engine

---

## ✔ Step 2. Locate Unreal Engine on macOS

Unreal is installed here:

```

/Users/Shared/Epic Games/UE_5.x/

```

Example:
```

/Users/Shared/Epic Games/UE_5.3/Engine/Plugins/

```

---

## ✔ Step 3. Install Meta XR Plugin

1. Download from Meta:  
   https://developers.meta.com/horizon/downloads/package/unreal-engine-5-integration

2. Unzip it  
3. Move the extracted folder to:

```

/Users/Shared/Epic Games/UE_5.x/Engine/Plugins/Marketplace/

```

Create **Marketplace** manually if missing.

4. Restart Unreal Engine

---

# Plugin Verification

In Unreal:

**Edit → Plugins → search “Meta”**

You should see:

- Meta XR
- Meta XR HMD
- Meta XR Utilities
- Meta XR Hands / Hand Tracking
- Meta XR Passthrough
- Meta XR Scene / Spatial / Anchors

Enable what you need → Restart UE

---

# Unreal Engine Project Configuration

Once installed, the following project settings are required.

---

## ✔ 4.1 XR and HMD Settings

### Enable Meta XR Support:
```

Project Settings → XR → Meta XR

```

### Disable OpenXR completely:
```

Plugins → OpenXR → Disable

```

(Optional but recommended to avoid conflicts)

---

## ✔ 4.2 Android & Packaging Settings (Windows only)

Go to:

```

Project Settings → Platforms → Android

```

Set:

- SDK API Level: **33+**
- Enable `Support Vulkan`
- Disable `OpenGL` (if using Vulkan only)
- Accept Android SDK licenses

---

## ✔ 4.3 Rendering Optimization

Recommended Meta XR settings:

- ✔ Enable **Late Latching**
- ✔ Enable **Fixed Foveated Rendering**
- ✔ Enable **Mobile Multi-View**
- ✔ Anti-Aliasing: **TSR** or **FXAA** for performance

---

# Input & Interaction Setup

## Controller Input

Use Meta XR input classes:

```

MetaXRControllerInput

```

DO NOT use:

- OpenXR Input
- OculusInput (deprecated)

---

## Hand Tracking Setup

Enable in:

```

Project Settings → Meta XR → Hand Tracking

```

Blueprint components:

- `MetaXRHandComponent`
- `MetaXRHandTrackingSubsystem`

Provides:

- Joint poses  
- Pinch gestures  
- Hand mesh tracking  
- Tracking confidence  

---

# Passthrough & MR Features

Meta XR Plugin unlocks all MR tools:

### Available MR Features

- ✔ Passthrough API (color camera feed)
- ✔ Scene Understanding (mesh reconstruction)
- ✔ Plane detection
- ✔ Spatial anchors
- ✔ Depth-based MR composition
- ✔ Boundary & guardian APIs

To enable:

```

Project Settings → Meta XR → Passthrough

```

---

# Packaging & Deployment

## Windows Build (APK)

1. Connect Quest via USB (Developer Mode ON)
2. Build from:
```

Platform: Android → Development/Shipping

```
3. Package → Install using:
- Unreal’s built-in installer
- Or **Meta Quest Developer Hub** (recommended)

---

## macOS Build Notes

- macOS **cannot** produce Android APKs  
- You must:
- Build on Windows, OR
- Use remote build system (GitHub Actions, CI/CD)

macOS is still fine for:

- Asset creation
- Blueprint systems
- UI development
- Gameplay programming
- VR preview (via Link/AirLink)

---

# Troubleshooting

### ❗ Black screen on headset  
- OpenXR is still enabled → disable it
- Meta XR HMD plugin missing → enable it

### ❗ Tracking origin floating too high/low  
Set:
```

XR Origin = Floor Level

```

### ❗ MR not working  
Ensure:

- Passthrough is enabled
- Vulkan is enabled
- Hand tracking is enabled (if used)

### ❗ Build error on macOS  
macOS cannot build Android → build on Windows

---

# Summary

**Meta XR Plugin is the recommended solution for Meta Quest development.**

Benefits:

- Better performance than OpenXR
- Quest-specific rendering optimizations
- Hand tracking, passthrough, scene understanding
- MR depth & anchor support
- Native platform tools and improved tracking stability

For any VR or MR project targeting Quest standalone,  
**Meta XR Plugin is the correct and optimized choice.**

---

# End of Document
```

