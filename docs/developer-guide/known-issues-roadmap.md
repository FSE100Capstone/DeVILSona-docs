# Current Known Issues, Technical Debt & Roadmap

!!! info "Audience"
    Incoming developers who need to understand what was left unfinished and where to focus future development.
    
    ⚠️ **This page is critical reading.** Do not start feature work until you understand the technical debt landscape. Building on a weak foundation compounds problems exponentially.

---

## Unfinished Work & Technical Debt

### WebSocket Reconnection Logic

**Severity:** High  
**Status:** Not implemented

**Problem:** If the WebSocket connection to OpenAI drops mid-conversation (due to network interruptions, server-side timeouts, or idle timeouts), the current system has **no automatic reconnection logic**. The conversation simply stalls. The student must exit and relaunch the app.

**Why This Matters:** University Wi-Fi is inherently unreliable. A dropped connection during a class session forces a hard restart, losing the student's conversational context.

**Required Solution:**

- Detect `OnClosed` and `OnConnectionError` events from `WebSocketSubsystem`
- Implement exponential backoff reconnection (try after 1s, 2s, 4s, 8s...)
- On reconnection, re-send the session configuration (`session.update`) to restore the AI persona
- Consider storing conversation context client-side to enable conversation continuity across reconnects

**Complexity:** Medium — the subsystem structure accommodates this well; it requires state management around the reconnection cycle.

---

### Terraform Remote State

**Severity:** Medium  
**Status:** Not implemented — using local state

**Problem:** Terraform state is stored **locally** on the machine running DeVILStarter. If this machine is replaced, the state file is lost, or multiple people need to manage infrastructure simultaneously, the state will fall out of sync.

**Required Solution:**
Migrate to S3 + DynamoDB remote state:

```hcl
terraform {
  backend "s3" {
    bucket         = "devilsona-terraform-state"
    key            = "infra/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

This requires creating the S3 bucket and DynamoDB lock table once manually (bootstrapping), then running `terraform init -migrate-state`.

**Complexity:** Low-Medium — well-documented Terraform pattern; the main effort is bootstrapping the remote backend.

---

### OpenAI API Key Management

**Severity:** Medium  
**Status:** Loaded from environment variable at runtime

**Problem:** The OpenAI API key is read from an environment variable (`CAPSTONE_PROJECT_OPENAI_API_KEY`) at runtime. On Android (Meta Quest), environment variables are set at build time or passed through Unreal's packaging configuration. This means the API key is **baked into the packaged APK**.

**Risks:**

- If the APK is extracted or decompiled, the API key could be exposed
- Rotating the key requires a full rebuild and redeployment

**Required Solution:**

- Move API key provisioning to the AWS backend: the headset authenticates with the backend, and the backend issues a short-lived session token or proxies the OpenAI connection
- Alternatively, use AWS Secrets Manager to store the key and retrieve it at session start via a Lambda function

**Complexity:** High — requires significant architectural changes to the authentication flow.

---

### No Conversation Persistence / Replay Feature

**Severity:** Low (current course requirements met)  
**Status:** Not implemented

**Problem:** Conversation transcripts are not saved anywhere persistent. Instructors and researchers cannot review what students said or how the AI responded. Students cannot review their conversation after the session.

**Required Solution:**

- Store conversation transcript deltas in DynamoDB alongside session progress
- Add a `Transcript` field to the `StudentSessions` table
- Build a simple review interface (this is where DeVILSpectator comes in)

**Complexity:** Medium — the transcript data is already flowing through `OnResponseTranscriptDeltaReceived`; persisting it requires additional save logic and UI.

---

### No Multi-Headset Coordination

**Severity:** Low (single-headset per session works)  
**Status:** Not implemented

**Problem:** There is no mechanism for multiple headsets to participate in a shared session, or for an instructor to monitor multiple headsets simultaneously from a single dashboard.

---

### Error Handling in SaveToAWS

**Severity:** Medium  
**Status:** Partial implementation

**Problem:** When AWS HTTP requests fail (network error, Lambda error, DynamoDB error), the current implementation logs an error and silently continues. There is no:

- Retry logic for transient failures
- User-facing notification of failed saves
- Queuing mechanism to retry failed saves when connectivity is restored

**Required Solution:**

- Implement a local save queue for failed AWS operations
- Retry with exponential backoff
- Show a non-intrusive indicator in the UI when a save fails

---

## DeVILSpectator (Web Application) Handoff

**DeVILSpectator** is an **unfinished** web application intended to serve as an instructor dashboard. It was started by the current capstone team but not completed. Its vision is:

- Real-time view of active student sessions (which character they're talking to, how far into the scenario)
- Conversation transcript display (live or post-session replay)
- Student progress analytics (scenario completion rates, time-per-scenario)

### Current State of the Repository

**Tech Stack:**

- React 18 + TypeScript
- Vite build toolchain
- Material UI (MUI) component library
- React Router for navigation

**What Exists:**

- Project scaffolding (Vite + React + TypeScript configuration)
- Basic project structure with placeholder components
- MUI theme configuration
- No actual backend integration
- No authentication system

**What Is Missing:**

- Authentication (how does an instructor log in?)
- WebSocket or polling-based live session monitoring
- Connection to the AWS backend (DynamoDB queries, API Gateway integration)
- Any completed UI screens beyond skeleton components
- Deployment configuration

### Recommended Starting Point for Next Team

1. **Define the authentication model first:** Who can access DeVILSpectator? Should it use ASU SSO (SAML/OIDC), a simple admin password, or something else? This decision affects all subsequent architecture.

2. **Create a read-only API endpoint in DeVILSona-infra:** Add a Terraform-managed Lambda + API Gateway route for querying session data (e.g., `GET /sessions?instructorId=XYZ`). This gives DeVILSpectator a backend to call.

3. **Build the session list view first:** A simple table showing active students, their progress, and current character is the highest-value feature. Build this before attempting any real-time updates.

4. **Add real-time updates second:** WebSocket-based updates from the backend (using API Gateway's WebSocket APIs) would enable live dashboard updates. This is a significant architectural addition.

### Key Files in DeVILSpectator

```
DeVILSpectator/
├── package.json           ← Dependencies (React, MUI, etc.)
├── vite.config.ts         ← Build configuration
├── tsconfig.json          ← TypeScript strict mode enabled
├── src/
│   ├── App.tsx            ← Root component with routing
│   ├── theme.ts           ← MUI theme customization
│   ├── components/        ← Placeholder components (incomplete)
│   └── pages/             ← Route-level components (incomplete)
```

---

## Recommended Roadmap for Next Capstone Team

The following are suggested milestones, ordered by impact and feasibility:

### 🚀 Milestone 1: Stability & Hardening (Weeks 1–3)
*Goal: Make the existing system reliable enough to run without issues during a full semester.*

- [ ] **Implement WebSocket reconnection** (see Section 1.1) — eliminates the most common classroom disruption
- [ ] **Migrate Terraform state to S3** (see Section 1.2) — prevents infrastructure management catastrophes
- [ ] **Add retry logic to SaveToAWS** (see Section 1.6) — ensures no student progress is silently lost
- [ ] **Run full regression testing** on a physical Quest headset in a simulated classroom environment

### 📊 Milestone 2: Instructor Tooling (Weeks 4–8)
*Goal: Give instructors visibility into what students are experiencing.*

- [ ] **Design and build DeVILSpectator session list view** — show active sessions and progress
- [ ] **Add read-only API endpoint** in DeVILSona-infra for instructor data queries
- [ ] **Implement basic authentication** for DeVILSpectator (even a simple shared-secret approach is better than nothing)
- [ ] **Add transcript saving** to DynamoDB — captures conversation history for post-session review

### 🎭 Milestone 3: Content Expansion (Weeks 6–12)
*Goal: Add new characters and scenarios to expand the educational value.*

- [ ] **Add 2–3 new AI personas** relevant to different engineering design domains
- [ ] **Refine existing persona prompts** based on student feedback from the first semester
- [ ] **Expand `set_emotion` function** to support a wider range of nuanced emotional states with corresponding animation states
- [ ] **Add a scenario selection menu** so students can choose which character to interview

### 🔒 Milestone 4: Security Hardening (Weeks 10+)
*Goal: Address the API key exposure risk before any broader deployment.*

- [ ] **Move OpenAI API key out of the APK** — proxy OpenAI connections through the AWS backend
- [ ] **Apply least-privilege IAM** — replace `AmazonDynamoDBFullAccess` with a scoped custom policy
- [ ] **Audit DynamoDB for FERPA compliance** — document data retention policy

---

## Known Bugs

| Bug | Severity | Component | Description |
|-----|----------|-----------|-------------|
| Mouth freeze after long pauses | Low | LipSync / IntervieweeActor | If the AI pauses mid-response, the mouth can freeze in an open position. FInterpTo idle speeds may need further tuning. |
| Login screen keyboard contrast | Low | UI / WB_Login | The VR keyboard can be difficult to see on bright backgrounds in some lighting conditions |
| Session load delay without feedback | Medium | SaveToAWS / BP_GameInstance | The UI shows no loading indicator while waiting for the AWS login response |
| WebSocket idle disconnect | High | WebSocketSubsystem | Long pauses in speech (>60s) can cause the OpenAI WebSocket to close silently |
