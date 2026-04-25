# Welcome to the DeVILSona Wiki

**DeVILSona** is an immersive Virtual Reality simulation designed to transform how undergraduate engineering students engage with design thinking. Instead of reading static paper personas, students put on a Meta Quest headset and hold **real-time, unscripted voice conversations** with AI-driven characters—learning directly from the people their designs are meant to serve.

This wiki is the comprehensive knowledge base for everyone involved in the DeVILSona ecosystem, organized into three distinct sections for three very different audiences.

---

## 🗺️ Choose Your Guide

### 🎓 Educator & Sponsor Guide
*For instructors and project sponsors who run DeVILSona sessions in the classroom.*

| Page | Description |
|------|-------------|
| [Welcome to DeVILSona](educator-guide/welcome.md) | What DeVILSona is, its educational goals, and the role of AI |
| [Classroom Setup & Hardware](educator-guide/classroom-setup.md) | Physical space setup, headset management, charging & sanitation |
| [Running a Session](educator-guide/running-a-session.md) | Step-by-step guide for launching and running a class session |
| [Student Safety & Privacy](educator-guide/safety-privacy.md) | AI content guardrails, data privacy, VR sickness protocols |
| [Troubleshooting for Educators](educator-guide/troubleshooting.md) | Quick-fix guide for common classroom problems |
| [Project Resources and Deliverables](educator-guide/project-resources-and-deliverables.md) | Centralized links to major project resources, research materials, design artifacts, and non-code deliverables created during the DeVILSona capstone (Fall 2025/Spring 2026) |

---

### 🖥️ Technical Administrator Guide
*For IT staff and technical administrators managing deployment and infrastructure.*

| Page | Description |
|------|-------------|
| [System & Architecture Overview](admin-guide/system-architecture.md) | End-to-end topology of the VR client, cloud backend, and launcher |
| [Hardware Provisioning & Sideloading](admin-guide/hardware-provisioning.md) | Developer Mode setup, ADB deployment, DeVILStarter configuration |
| [Network Configuration](admin-guide/network-configuration.md) | Whitelisting OpenAI and AWS endpoints, bandwidth requirements |
| [Backend & Cloud Operations](admin-guide/backend-cloud.md) | AWS Console navigation, DynamoDB & Lambda monitoring |
| [Logging & Incident Response](admin-guide/logging-incident-response.md) | Pulling crash logs, reading error outputs, escalation paths |

---

### 👨‍💻 Developer Knowledge Base
*For incoming capstone development teams taking over the codebase.*

| Page | Description |
|------|-------------|
| [Developer Onboarding & Environment Setup](developer-guide/onboarding.md) | Prerequisites, repo cloning, local env setup, first compile |
| [Core Architecture Deep Dive](developer-guide/core-architecture.md) | Full-stack system diagram and data flow between all components |
| [The AI Pipeline](developer-guide/ai-pipeline.md) | Conceptual walkthrough of the entire AI conversation lifecycle |
| [Unreal Engine 5 Implementation](developer-guide/ue5-implementation.md) | Subsystems, VR mechanics, MetaHuman integration, save system |
| [Infrastructure & Cloud (Terraform & AWS)](developer-guide/infrastructure-cloud.md) | AWS architecture, Terraform provisioning, DeVILStarter deep dive |
| [Contribution Guidelines](developer-guide/contribution-guidelines.md) | Git flow, commit standards, PR process, code style, QA checklist |
| [Known Issues & Roadmap](developer-guide/known-issues-roadmap.md) | Technical debt inventory, DeVILSpectator handoff, roadmap |
| [Independent Learning Paths](developer-guide/learning-paths.md) | Curated curriculum with external resources for every technology |
| [Scenario 2: Driving to a Job Interview](developer-guide/driving-scenario-overview.md) | Blueprint architecture, level flow, core actors, interactions, and implementation details for the driving scenario |

---

### 📘 Student Guide
*For student end users of the VR experience.*

| Page | Description |
|------|-------------|
| [Game User Guide](user-guide/game-guide.md) | Comprehensive guide to DeVILSona, covering basic controls, account creation, AI interview system, and scenario progression |
| [Scenario 1 User Guide: Morning Routine](user-guide/scenario1-morningroutine.md) | End-to-end guide for Scenario 1, including waking up, taking a shower, equipping the prosthetic arm, and other early interactions |
| [Scenario 2 User Guide: Driving to a Job Interview](user-guide/scenario2-drivingtoajobinterview.md) | End-to-end guide for Scenario 2, including controls, objective flow, player positioning, and important usage notes |
| [Troubleshooting Interview Audio and Microphone Issues](user-guide/interview-issues.md) | Troubleshooting steps for microphone input, permissions, and missing AI dialogue during interview interactions |
| [Troubleshooting Navigation Issues](user-guide/navigation-issues.md) | Troubleshooting steps for teleport disorientation, reset orientation, positioning problems, and general VR navigation comfort |
| [Troubleshooting Scenario 1 Issues](user-guide/scenario1-issues.md) | Troubleshooting steps for common issues in Scenario 1, such as the shower dial, equipping the prosthetic arm, and hand visibility |

---

## 📦 Project Ecosystem at a Glance

| Repository | Tech Stack | Purpose |
|-----------|------------|---------|
| **DeVILSona** | Unreal Engine 5 (C++ & Blueprints), OpenAI Realtime API, MetaXR | The VR simulation application itself |
| **DeVILSona-infra** | Terraform, AWS (Lambda, API Gateway, DynamoDB) | Cloud backend for session persistence |
| **DeVILStarter** | Wails (Go), React/TypeScript/Vite | Desktop launcher for infrastructure provisioning |
| **DeVILSona.wiki** | GitHub Wiki Markdown | This documentation repository |

!!! note "Note"
    A companion web app called **DeVILSpectator** (React/TypeScript) exists in an unfinished state. It is documented under [Known Issues & Roadmap](developer-guide/known-issues-roadmap.md) as a future development target.

---

## 📁 Legacy Documentation

The pages below are **fine-grained technical documents** covering specific subsystems and tooling in depth. Readers looking to go beyond the high-level guides above can consult these for deeper technical understanding.

| Page | Description |
|------|-------------|
| [AWS Save System](legacy/aws-save-system.md) | DynamoDB save-data integration and schema |
| [AWS & Terraform](legacy/aws-terraform.md) | Full Terraform config walkthrough for the cloud backend |
| [Auto-generated API Documentation](legacy/api-documentation.md) | Auto-generated API reference for all subsystems |
| [Mac Setup & Limitations](legacy/mac-setup-limitations.md) | OVRLipSync, VR, and AI integration notes on macOS |
| [MetaQuest Link Setup and Use](legacy/metaquest-link-setup-and-use.md) | Meta Horizon mobile app, developer mode, Meta Horizon Link desktop setup, OpenXR activation, and Unreal Engine VR Preview workflow |
| [Meta XR Plugin](legacy/meta-xr-plugin.md) | Meta XR SDK plugin setup and configuration |
| [MetaHuman Creator](legacy/metahuman-creator.md) | MetaHuman pipeline, blendshapes, and animation notes |
| [Oculus LipSync Plugin](legacy/oculus-lipsync.md) | OVRLipSync integration, viseme mapping, and troubleshooting |
| [Save System](legacy/save-system.md) | Local UE5 save-game system design |
| [Subsystems](legacy/subsystems.md) | Overview of all UE5 GameInstanceSubsystems |
| [UE5 Build Guide (Android APK)](legacy/build-android-apk.md) | Packaging the project as a Meta Quest APK |
| [UE5 Build Guide (Windows Shipping)](legacy/build-windows-shipping.md) | Packaging the project as a Windows Shipping build |
| [UE5 Android APK Build Guide (MetaHuman Variant)](legacy/build-android-apk-metahuman.md) | Additional setup and troubleshooting required to package the MetaHuman / Meta XR Android APK build |
| [Deployment and Launch Guide](legacy/deployment-and-launch-guide.md) | Android APK installation to Meta Quest, OBB placement, SideQuest/install script workflow, and Windows desktop launch through Meta Quest Link |

---

*Last updated: April 2026 | FSE100 Capstone Project*
