# Contribution Guidelines

!!! info "Audience"
    All developers contributing code to any DeVILSona repository.

These guidelines exist to ensure that the codebase remains healthy, understandable, and maintainable for future capstone teams. Please read this page in full before submitting your first pull request.

---

## Git Flow & Branching Strategy

This project uses a **simplified Git Flow** strategy with three branch types:

### Branch Naming Conventions

| Branch Type | Format | Example |
|------------|--------|---------|
| **Feature** | `feature/<short-description>` | `feature/add-emotion-blend-states` |
| **Bugfix** | `bugfix/<short-description>` | `bugfix/fix-websocket-reconnect` |
| **Hotfix** (on prod) | `hotfix/<short-description>` | `hotfix/fix-login-crash-on-quest3` |
| **Release** | `release/<semester>` | `release/spring-2027` |

Rules:

- Use **lowercase** with hyphens only (no underscores, no spaces, no special chars)
- Keep descriptions **concise** (2–4 words): describe what the branch does, not how
- **Never commit directly to `main`**—all changes come through pull requests

### Workflow

```
main (protected)
│
├── feature/add-new-persona ← Your development happens here
│   ├── commit: "Add Maria persona system prompt"
│   ├── commit: "Add emotion transitions for frustration state"
│   └── commit: "Add unit test for PersonaConfig parsing"
│       → Pull Request → Review → Squash Merge to main
│
├── bugfix/fix-lipsync-timer-leak
│   └── ...
│
└── hotfix/critical-crash-fix
    └── ...
```

### Keeping Your Branch Up to Date

Always rebase your feature branch on `main` before opening a PR:

```bash
# While on your feature branch:
git fetch origin
git rebase origin/main

# If conflicts: resolve them, then:
git rebase --continue
```

!!! note
    Prefer **rebase** over **merge** to keep the git history linear and readable.

---

## Commit Message Standards

Well-written commit messages are the most powerful form of documentation in a fast-moving codebase. Every commit must follow this format:

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**`<type>`** must be one of:
| Type | When to Use |
|------|-------------|
| `feat` | A new feature or capability |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `refactor` | Code restructuring without behavior change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build system changes, dependency updates |
| `style` | Formatting, whitespace (no logic change) |

**`<scope>`** is the component affected. Examples for this project:

- `audio` — AudioInputSubsystem or audio processing
- `websocket` — WebSocketSubsystem or connection management
- `ai-api` — OpenAiApiSubsystem or AI protocol
- `tools` — AIToolInterpreterSubsystem or function calls
- `orch` — AIConversationOrchestratorSubsystem
- `lipsync` — OVRLipSync integration or IntervieweeActor
- `ui` — Any UI widget (WB_ assets)
- `save` — SaveGame system or SaveToAWS
- `infra` — Terraform or AWS configuration
- `starter` — DeVILStarter application

**`<subject>`** rules:

- Imperative mood: "Add X", "Fix Y", "Remove Z" (not "Added" or "Fixes")
- Maximum 72 characters
- No period at the end
- Lowercase

### Good vs. Bad Commit Messages

❌ **Bad:**
```
fixed stuff
Update files
changes to save system
wip
```

✅ **Good:**
```
fix(audio): prevent feedback loop by stopping mic during AI playback

When the AI begins speaking, the microphone input was not being 
stopped, causing the AI to hear its own audio output and triggering
spurious speech detection events. This fix calls StopCapturing() 
on OnInputSpeechStarted and StartCapturing() on HandleAudioFinished.

Closes #42
```

### Atomic Commits

Each commit should represent **one logical change**. Avoid:

- Commits that fix a bug AND add an unrelated feature
- Commits that combine debugging changes with production code
- Commits that contain `console.log` or `UE_LOG` calls added during debugging

---

## Pull Request Guidelines

### Before Opening a PR

- [ ] Your branch is rebased on the latest `main`
- [ ] All editor-flagged compilation warnings are resolved
- [ ] You've tested your changes in PIE (Play In Editor) mode
- [ ] You've tested on a physical Meta Quest headset if your change affects VR behavior
- [ ] Code has been reviewed by yourself (read through every changed line)
- [ ] Commit history is clean (no merge commits, no "WIP" commits)

### PR Title Format

Use the same format as commit messages:
```
feat(ai-api): add streaming reconnection on dropped WebSocket
fix(lipsync): resolve mouth freeze after AI response ends
```

### PR Description Template

```markdown
## Summary
A brief description of what this PR does and why.

## Changes
- Added XYZ to improve ABC
- Fixed DEF by changing GHI

## Testing
- [ ] Tested in PIE (Play In Editor)
- [ ] Tested on Meta Quest headset
- [ ] Tested the affected subsystem in isolation
- [ ] Verified no regressions in [specific feature]

## Related Issues
Closes #<issue_number>
```

### Review Process

- **At least one team member must review** before merging
- Reviewers should look for: correctness, code style adherence, null safety, and delegate unbinding
- Use **inline comments** for specific line-level feedback
- Use the **"Changes Requested"** status if blocking issues are found
- **Squash and merge** into main to keep history clean (squash all PR commits into one)

### What Reviewers Should Check for C++ Code

1. **UPROPERTY() on all UObject pointers** — prevents garbage collection crashes
2. **Null checks before subsystem access** — subsystems can theoretically fail to initialize
3. **Delegate unbinding in EndPlay()** — the #1 source of crashes in this codebase
4. **No raw pointers to UObjects** — always use `TWeakObjectPtr` if storing a reference you don't own
5. **Thread safety of async operations** — HTTP callbacks run on a non-game thread; use `AsyncTask(ENamedThreads::GameThread, ...)` to touch UObjects

---

## Code Style Standards

### Unreal Engine C++ Style

This project follows the **Unreal Engine Coding Standard** ([Epic's official guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine)) with these specifics:

**Naming:**
```cpp
// Classes: PascalCase with UE prefix
class UMySubsystem : public UGameInstanceSubsystem {}

// Functions: PascalCase, verb-first
void SendAudioInputToAI(const FString& Audio);
bool IsConnected() const;

// Variables: PascalCase for UPROPERTY, camelCase for local
UPROPERTY()
UOpenAiApiSubsystem* OpenAiApiSubsystem;  // member

FString localVariableName;              // local

// Constants: Macro-style uppercase or constexpr
constexpr int32 kLipSyncFrameSize = 240;
```

**Formatting:**

- Indent with **tabs** (Unreal standard), not spaces
- Opening braces on the **same line** for functions, new line for class declarations
- Maximum line length: **120 characters**

**Comments:**
```cpp
// Single-line comments for inline explanation

/**

 * Multi-line documentation comment for functions.
 * Explain the WHY, not just the WHAT.
 * 
 * @param AudioChunkBase64  The base64-encoded PCM16 audio chunk to send
 */
void SendAudioInputToAI(const FString& AudioChunkBase64);
```

### Blueprint Naming Conventions

| Asset Type | Prefix | Example |
|-----------|--------|---------|
| Blueprint Class | `BP_` | `BP_IntervieweeCharacter` |
| Widget Blueprint | `WB_` | `WB_LoginScreen` |
| Animation Blueprint | `ABP_` | `ABP_Face_PostProcess` |
| SaveGame | `SG_` | `SG_SaveData` |
| Material | `M_` | `M_SkinMaterial` |
| Material Instance | `MI_` | `MI_CharacterSkin` |
| Texture | `T_` | `T_FaceAlbedo` |
| Static Mesh | `SM_` | `SM_ChairProp` |
| Skeletal Mesh | `SKM_` | `SKM_CharacterBody` |

### TypeScript Style (DeVILStarter / DeVILSpectator)

- **Strict TypeScript** — `strict: true` in tsconfig. No `any` types.
- **Functional React components** only (no class components)
- **Named exports** for all components
- Component filenames: **PascalCase** (`InfrastructurePanel.tsx`)
- Utility/hook filenames: **camelCase** (`useTerraformLogs.ts`)
- Interfaces over type aliases for object shapes

```typescript
// ✅ Good
interface TerraformStatus {
    isRunning: boolean;
    lastDeployedAt: Date | null;
    apiUrls: {
        sessionUrl: string;
        loginUrl: string;
    } | null;
}

// ❌ Bad
type stuff = any;
```

### Terraform / HCL Style

```hcl
# Resource names: snake_case, descriptive
resource "aws_lambda_function" "save_session" {
  # Attribute names: snake_case (standard HCL)
  function_name = "FSE100_SaveSession"
  
  # Group related attributes together
  runtime = "nodejs22.x"
  handler = "index.handler"
  
  # Separate unrelated attribute groups with a blank line
  filename         = "${path.module}/lambda/save_session.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/save_session.zip")
}
```

---

## QA & Testing Checklist

Before submitting any PR that touches gameplay code:

### PIE (Play In Editor) Test

Run the game from the UE5 Editor using **Play In Editor → Simulate**:

- [ ] App launches without compile errors or assertion failures
- [ ] Login screen displays correctly
- [ ] Entering test ASUID + SessionID and clicking login completes without crash
- [ ] The AI character appears in the scene
- [ ] Microphone capture starts (look for `[Audio] Capture started` in Output Log)
- [ ] Speaking produces audio chunks in the Output Log (`[Audio] Sending chunk...`)
- [ ] AI responds (look for `[AI] Audio delta received` or similar in Output Log)
- [ ] Character mouth animates during AI speech
- [ ] Session saves without error (`[AWS] Save Response 200` in Output Log)
- [ ] Session loads correctly on a second login with the same ASUID + SessionID

### Physical Headset Test (for VR-specific changes)

- [ ] Build and install APK to the Meta Quest
- [ ] App launches from Unknown Sources without crashing
- [ ] Guardian system sets up correctly
- [ ] Head tracking and controller tracking function
- [ ] Audio plays through the headset speakers at correct volume
- [ ] Microphone input works (voice triggers AI response)
- [ ] Framerate is stable (check with Meta Quest Developer Hub)

### AWS Integration Test

- [ ] DeVILStarter successfully starts infrastructure (green status)
- [ ] API endpoints respond correctly (curl test both `/session` and `/login`)
- [ ] Session save from the game creates a new DynamoDB item
- [ ] Session load retrieves the previously saved item
- [ ] DeVILStarter successfully destroys infrastructure (infrastructure offline)

---

➡️ **Next:** [Known Issues & Roadmap](known-issues-roadmap.md)
