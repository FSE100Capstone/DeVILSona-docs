# Independent Learning Paths & Technology Stack

!!! info "Audience"
    Incoming developers who want to build competency in specific parts of the DeVILSona tech stack.
    
    This page provides a curated, opinionated curriculum for each major technology area. Don't try to learn everything at once—identify the components you'll be working on and focus there first.

---

## How to Use This Guide

1. **Identify your role:** Will you primarily work on the UE5 client, the cloud backend, or the web launcher?
2. **Start with fundamentals:** Each section has beginner resources before advanced ones. Don't skip them.
3. **Build something small first:** Theory without practice is useless. Each section contains a suggested mini-project to solidify your learning.
4. **Ask for code review:** Your capstone teammates are the best resource for DeVILSona-specific patterns. Read the existing source code alongside these resources.

---

## Part 1: Unreal Engine 5 VR Client & AI Interactions

### 🎮 1.1 Unreal Engine 5 — Core Concepts

**Why it matters:** Understanding UE5's architecture (actors, components, GameInstance lifecycle) is mandatory before touching anything else.

**Resources:**

- 📖 [Official UE5 Documentation — Programming Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-in-unreal-engine) — Start here. The Actor lifecycle, GameInstance, and GameMode sections are critical.
- 🎬 [Unreal Online Learning — Unreal Engine 5 Kickstart](https://dev.epicgames.com/community/learning/courses/e4Z/unreal-engine-5-kickstart-for-developers/rRW/unreal-engine-introduction-to-unreal-engine-5) — Free official course, excellent for getting oriented
- 🎬 [Alex Forsythe — How Unreal Engine C++ Works (YouTube)](https://www.youtube.com/c/AlexForsythe) — Best free resource for understanding UObject, GC, and UE-specific C++ patterns
- 📖 [Unreal Slackers Discord](https://discord.gg/unreal-slackers) — The most active UE5 developer community; invaluable for getting unstuck

**Suggested Mini-Project:** Create a new Actor class in C++ that subscribes to a `FTimerHandle` and spawns a debug print every 2 seconds. This confirms you understand the Actor lifecycle and UE-flavored C++.

**Key Topics for This Project:**

- GameInstance vs. GameMode vs. Actor lifecycle
- The role of `BeginPlay()`, `Tick()`, and `EndPlay()`
- How level loading affects persistent objects
- Understanding Output Log and using `UE_LOG()`

---

### ⚙️ 1.2 C++ (Unreal-Specific)

**Why it matters:** The entire AI pipeline is C++. You cannot meaningfully contribute to the core systems without it.

**Resources:**

- 📖 [Epic's Unreal C++ Coding Standard](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine) — The style guide you must follow
- 📖 [UObject, Object Creation, and Garbage Collection](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-uproperties) — Understanding `UPROPERTY` and GC is critical for avoiding crashes
- 📖 [Unreal Engine Delegates](https://dev.epicgames.com/documentation/en-us/unreal-engine/delegates-and-lamba-functions-in-unreal-engine) — The event system used throughout the AI pipeline
- 🎬 [Ben UI — Unreal C++ Series (YouTube)](https://www.youtube.com/@BenUI) — Excellent practical tutorials on real UE5 C++ patterns
- 📖 [Unreal Engine Subsystems Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine) — Directly relevant to DeVILSona's architecture

**Suggested Mini-Project:** Create a `UGameInstanceSubsystem` that stores a "message of the day" string, exposes a `GetMessage()` UFUNCTION, and allows a Blueprint to read it. This validates you understand the subsystem pattern used throughout the codebase.

**Common Pitfalls:**

- Forgetting `UPROPERTY()` on `UObject*` pointers → garbage collection crash
- Not unbinding delegates in `EndPlay()` → crash after Actor is destroyed
- Using `new` / `delete` instead of `NewObject<>()` → memory management chaos
- Calling subsystem methods in constructor (subsystems aren't available yet)

---

### 🥽 1.3 Virtual Reality (VR) Fundamentals

**Why it matters:** VR has unique constraints around rendering performance, stereo geometry, and user comfort that don't exist in flat-screen games.

**Resources:**

- 📖 [Meta Quest Developer Documentation](https://developer.oculus.com/documentation/unreal/unreal-develop-overview/) — The canonical reference for Quest development in UE5
- 📖 [UE5 VR Best Practices](https://dev.epicgames.com/documentation/en-us/unreal-engine/vr-performance-and-profiling-in-unreal-engine) — Performance profiling guide specific to VR
- 🎬 [VR Performance Crash Course (Unreal Online Learning)](https://dev.epicgames.com/community/learning/courses/jYQ/unreal-engine-vr-performance-tips) — Why 72fps is non-negotiable and how to achieve it
- 📖 [VR Template Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/vr-template-in-unreal-engine) — UE5's built-in VR template explains common patterns

**Key Concepts:**

- Fixed Foveated Rendering and why it's essential on standalone hardware
- Single-pass stereo rendering (Mobile Multi-View)
- Why draw calls and overdraw matter much more in VR than PC games
- Tracking origin and floor vs. eye level tracking
- Guardian/boundary system

---

### 📱 1.4 Meta XR SDK

**Why it matters:** The project uses the Meta XR Plugin, not the generic OpenXR plugin. Meta-specific APIs enable Quest-specific features.

**Resources:**

- 📖 [Meta XR Plugin for Unreal Engine — Official Docs](https://developer.oculus.com/documentation/unreal/unreal-engine-integration/) — The primary reference
- 📖 [Meta Quest Developer Hub](https://developer.oculus.com/documentation/unity/ts-odh/) — The profiling and deployment tool for Quest
- 🎬 [Meta Horizon Worlds — Unreal Tutorials (official YouTube)](https://www.youtube.com/@MetaQuestDevelopers) — Meta's official development channel

**Key Features Used in This Project:**

- `MetaXRControllerInput` — Quest controller input handling
- Foveated rendering settings
- Android packaging configuration for Quest

---

### 🤖 1.5 OpenAI Realtime API

**Why it matters:** The Realtime API is the most complex external dependency in this project. Misunderstanding its behavior causes subtle, hard-to-debug issues.

**Resources:**

- 📖 [OpenAI Realtime API Documentation](https://platform.openai.com/docs/guides/realtime) — **Read this completely before touching the AI subsystems.** The event reference is essential.
- 📖 [OpenAI Realtime API Reference (Event Catalog)](https://platform.openai.com/docs/api-reference/realtime-commands) — Every event the server sends and the client can send
- 🎬 [Building with the OpenAI Realtime API (OpenAI DevDay 2024 YouTube)](https://www.youtube.com/watch?v=z3lzqc4i_EQ) — Conceptual walkthrough of the API
- 📖 [OpenAI Cookbook — Realtime Examples](https://cookbook.openai.com/examples/realtime) — Practical code examples (JavaScript/Python; adapt the concepts to C++)

**Key Concepts for DeVILSona:**

- Server-side Voice Activity Detection (VAD) — why you don't control speech boundaries
- Audio format requirements — the strict 24kHz PCM16 mono base64 format
- Session configuration vs. conversation item creation
- Tool calling schema and the function call lifecycle

---

### 🔌 1.6 WebSockets

**Why it matters:** Understanding WebSocket fundamentals prevents you from treating the OpenAI connection like HTTP.

**Resources:**

- 📖 [MDN WebSockets Guide](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) — Excellent conceptual introduction
- 📖 [RFC 6455 (WebSocket Protocol)](https://datatracker.ietf.org/doc/html/rfc6455) — The protocol spec; read Section 1–5 for the concepts
- 📖 [UE5 WebSocket Module Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/WebSockets) — The specific UE5 API used in `WebSocketSubsystem`

**Key Concepts:**

- The HTTP Upgrade handshake
- Full-duplex communication (both sides can send simultaneously)
- Connection lifecycle events: `OnConnected`, `OnMessage`, `OnClosed`, `OnError`
- Why idle connections can be closed by firewalls/load balancers (keep-alive pings)

---

## Part 2: Cloud Infrastructure & Backend

### ☁️ 2.1 AWS DynamoDB

**Why it matters:** Student session data lives here. Understanding DynamoDB's data model prevents schema mistakes.

**Resources:**

- 📖 [AWS DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) — Start with the "Core components" and "Working with items" sections
- 🎬 [DynamoDB Crash Course (Fireship — YouTube)](https://www.youtube.com/watch?v=2k2GINpO308) — 10-minute introduction to NoSQL thinking
- 🎬 [DynamoDB: From Beginner to Pro (Alex DeBrie)](https://www.youtube.com/watch?v=W3oxBqCCVJM) — Deep dive into data modeling patterns
- 📖 [The DynamoDB Book (Alex DeBrie)](https://www.dynamodbbook.com/) — The definitive resource; expensive but excellent

**Key Concepts for DeVILSona:**

- Partition key + sort key design (StudentID + SessionID)
- `PutItem` (upsert) vs. `UpdateItem` (partial update)
- NoSQL modeling constraints: you can only query on primary keys or GSIs
- `begins_with` in KeyConditionExpression — used by the Login Lambda

---

### 🌐 2.2 AWS API Gateway

**Why it matters:** API Gateway is the public-facing endpoint that the headset talks to. Understanding it helps debug 4xx and 5xx errors.

**Resources:**

- 📖 [API Gateway HTTP API Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html) — DeVILSona uses HTTP API (V2), not REST API (V1)
- 📖 [API Gateway Payload Format Version 2.0](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html) — Understanding how Lambda receives the event object
- 🎬 [AWS API Gateway Tutorial (Traversy Media)](https://www.youtube.com/watch?v=BXUnkSkZx4A) — Practical video walkthrough

---

### ⚡ 2.3 AWS Lambda

**Why it matters:** The save/load logic runs here. Understanding Lambda execution context helps optimize cold starts and debug errors.

**Resources:**

- 📖 [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) — Execution model, cold starts, environment variables
- 📖 [AWS SDK for JavaScript V3 — DynamoDB Document Client](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/Package/-aws-sdk-lib-dynamodb/) — The exact SDK used in the Lambda functions
- 🎬 [AWS Lambda Tutorial (TechWorld with Nana)](https://www.youtube.com/watch?v=eOBq__h4OJ4) — Clear overview of serverless computing concepts

---

### 🏗️ 2.4 Terraform

**Why it matters:** All AWS resources are managed through Terraform. You cannot safely modify the infrastructure without understanding it.

**Resources:**

- 📖 [Terraform Official Documentation](https://developer.hashicorp.com/terraform/docs) — The most comprehensive reference
- 🎬 [Terraform Course for Beginners (freeCodeCamp)](https://www.youtube.com/watch?v=SLB_c_ayRMo) — 2-hour comprehensive free course
- 📖 [Terraform AWS Provider Registry](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) — Reference for all AWS resource types used in DeVILSona
- 🎬 [Terraform Associate Exam Prep (TechWorld with Nana)](https://www.youtube.com/watch?v=7xngnjfIlK4) — Thorough but practical; worth watching even if not taking the exam

**Key Concepts for DeVILSona:**

- `terraform plan` vs. `terraform apply` vs. `terraform destroy`
- `terraform output` — retrieving values like API endpoint URLs
- Dependency graph — how Terraform knows to create the DynamoDB table before the Lambda that references it
- The `source_code_hash` trick for detecting Lambda code changes

---

## Part 3: Web-Based Apps (DeVILStarter & DeVILSpectator)

### ⚛️ 3.1 React

**Why it matters:** DeVILStarter's UI is React. DeVILSpectator (when completed) is also React.

**Resources:**

- 📖 [React Official Documentation](https://react.dev) — The new official docs are excellent; use these, not the old ones
- 🎬 [React Full Course (David Gray — freeCodeCamp)](https://www.youtube.com/watch?v=RVFAyFWO4go) — 9-hour comprehensive free course
- 📖 [Wails Documentation](https://wails.io/docs/introduction) — Specific to DeVILStarter's architecture
- 🎬 [Building Desktop Apps with Wails (YouTube)](https://www.youtube.com/watch?v=3WADqJj0E2g) — Introduction to the Wails framework

**Key Concepts for DeVILStarter:**

- `useState` and `useEffect` hooks for managing UI state
- Event handling from the Go backend (`EventsOn` from `@wailsapp/runtime`)
- Async/await for calling Go functions

---

### 📘 3.2 TypeScript

**Why it matters:** All web code is written in strict TypeScript. Type safety prevents an entire class of runtime bugs.

**Resources:**

- 📖 [TypeScript Official Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — Comprehensive official documentation
- 🎬 [TypeScript Tutorial (Net Ninja)](https://www.youtube.com/playlist?list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI) — Beginner-friendly video series
- 📖 [TypeScript Deep Dive (Basarat Ali Syed)](https://basarat.gitbook.io/typescript/) — Free online book; excellent for developers coming from JavaScript

---

## Part 4: Version Control & Deployment Tooling

### 🗂️ 4.1 Git & Git LFS

**Why it matters:** Large binary assets (UE5 `.uasset` files) are stored in Git LFS. Without understanding this, you will corrupt the repository.

**Resources:**

- 📖 [Git LFS Official Documentation](https://git-lfs.github.com/) — Essential reading before touching the UE5 repository
- 🎬 [Git LFS Tutorial (GitHub)](https://www.youtube.com/watch?v=uLR1RNqJ1Mw) — Visual explanation of how LFS works
- 📖 [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials) — Excellent written guides for intermediate Git concepts (rebasing, cherry-picking, conflict resolution)
- 🎬 [Git Rebase vs Merge (The Coding Train)](https://www.youtube.com/watch?v=CRlGDDprdOQ) — Understanding why this project prefers rebase

**Common LFS Mistakes:**

- Cloning without LFS installed → all binary files are just text pointers
- Forgetting to run `git lfs track "*.uasset"` before adding a new binary file type
- Editing binary files in a non-LFS environment → corrupts the pointer

---

### 📲 4.2 ADB (Android Debug Bridge) & SideQuest

**Why it matters:** Getting your build onto the Quest headset requires ADB knowledge.

**Resources:**

- 📖 [Android ADB Documentation](https://developer.android.com/tools/adb) — Official ADB command reference
- 📖 [SideQuest Setup Guide](https://sidequestvr.com/setup-howto) — The easiest way to sideload for non-developers
- 🎬 [Meta Quest Developer Mode & Sideloading Tutorial (YouTube)](https://www.youtube.com/watch?v=FZnYlKGtLGU) — Step-by-step visual walkthrough

**Essential ADB Commands for DeVILSona:**
```powershell
adb devices                          # List connected devices
adb install -r <path/to/app.apk>     # Install/update the APK
adb logcat -s LogTemp                # View UE5 game logs in real time
adb logcat -c                        # Clear the log buffer
adb pull /sdcard/UE4Game/ .          # Pull all game logs to local directory
adb shell pm list packages | findstr "fse100"  # Verify app is installed
```
