# Unreal Engine 5 Implementation

!!! info "Audience"
    Developers working directly with the UE5 codebase. Read [The AI Pipeline](ai-pipeline.md) first if you haven't already—this page maps conceptual pipeline layers to concrete UE5 implementations.

---

## C++ vs. Blueprints: The Project Standard

Before reading any further, understand this decision that governs every feature you build:

### The Rule: C++ for Logic, Blueprints for Configuration

| Use C++ For | Use Blueprints For |
|-------------|-------------------|
| All subsystems and game instance logic | Character animation graphs (ABP_) |
| Performance-critical game code (audio processing, WebSocket, HTTP) | UI widgets (WB_ prefix) |
| Data structures exposed to Blueprints (`USTRUCT`, `UFUNCTION`) | Level designer-controlled behavior |
| Anything that binds to C++ delegates | Prototype/quick-iteration work |
| Plugin code and extensions | Asset referencing and content wiring |

**Why this matters:** The AI pipeline processes audio data at 24kHz on every microphone capture tick. Performing this in Blueprint would cause significant frame stalls. Blueprint execution is single-threaded and significantly slower than compiled C++ for tight loops.

### Unreal C++ Naming Conventions Used in This Project

| Prefix | Meaning | Example |
|--------|---------|---------|
| `U` | `UObject`-derived class | `UOpenAiApiSubsystem` |
| `A` | `AActor`-derived class | `AIntervieweeActor` |
| `F` | Plain struct (no heap allocation) | `FStudentSessionData` |
| `E` | Enum | `EDecompressionType` |
| `I` | Interface | `IHttpRequest` |
| `T` | Template class | `TArray`, `TSharedPtr` |

---

## GameInstance Subsystem Architecture

!!! note
    If you haven't read [The AI Pipeline (Conceptual)](ai-pipeline.md), do that now. This section maps those concepts to their UE5 C++ equivalents.

### Why GameInstance Subsystems?

A `UGameInstance` persists for the **entire session**—it is created when the game starts and destroyed when it ends. It survives level transitions, which is essential for an AI conversation that can span multiple maps (lobby → interview room → etc.).

`UGameInstanceSubsystem` classes are a UE5 design pattern that:

- Are automatically instantiated by the engine at GameInstance creation time
- Are destroyed automatically when the GameInstance is destroyed
- Can declare `InitializeDependency<Type>()` to enforce initialization order
- Are globally accessible via `GetGameInstance()->GetSubsystem<T>()`

This avoids the Singleton trap (no manual lifecycle management) while preserving global accessibility.

### The Five Subsystems: Mapping Concepts to Code

#### `UAudioInputSubsystem` — The Capture Layer

**Header:** `Source/FSE100Capstone/Subsystems/AudioInputSubsystem.h`

```cpp
UCLASS()
class UAudioInputSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable)
    void StartCapturing();

    UFUNCTION(BlueprintCallable)
    void StopCapturing();

    // Fired when a new base64 PCM16 audio chunk is ready
    UPROPERTY(BlueprintAssignable)
    FOnAudioChunkCaptured OnAudioChunkCaptured;

    UPROPERTY(BlueprintAssignable)
    FOnAudioCaptureStarted OnAudioCaptureStarted;

    UPROPERTY(BlueprintAssignable)
    FOnAudioCaptureStopped OnAudioCaptureStopped;
};
```

**Internal Processing Pipeline:**

1. `StartCapturing()` opens the default microphone via UE5's Audio Capture component
2. The capture callback fires with raw PCM float data at the platform's native sample rate
3. The subsystem downsamples the buffer to 24kHz (simple decimation or polyphase resample)
4. Converts float samples to int16: `int16 sample = (int16)(floatSample * 32767.0f)`
5. Encodes the byte array as base64: `FBase64::Encode(ByteArray, Base64String)`
6. Broadcasts `OnAudioChunkCaptured(Base64String)`

**Important:** The microphone is **stopped** when the AI begins speaking (to prevent the AI from hearing its own output and creating a feedback loop) and **restarted** when the AI finishes speaking.

---

#### `UWebSocketSubsystem` — The Transport Layer

**Header:** `Source/FSE100Capstone/Subsystems/WebSocketSubsystem.h`

```cpp
UCLASS()
class UWebSocketSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable)
    bool IsConnected() const;

    UFUNCTION(BlueprintCallable)
    void SendMessage(const FString& Message);

    // Connection lifecycle events
    UPROPERTY(BlueprintAssignable)
    FSimpleMulticastDelegate OnConnected;

    UPROPERTY(BlueprintAssignable)
    FOnWebSocketMessageReceived OnMessageReceived;

    UPROPERTY(BlueprintAssignable)
    FOnWebSocketError OnConnectionError;

    UPROPERTY(BlueprintAssignable)
    FSimpleMulticastDelegate OnClosed;

private:
    TSharedPtr<IWebSocket> WebSocket;
};
```

**Connection Setup:**
```cpp
void UWebSocketSubsystem::Connect(const FString& Url, const FString& ApiKey)
{
    // Create WebSocket with required headers
    TMap<FString, FString> Headers;
    Headers.Add(TEXT("Authorization"), FString::Printf(TEXT("Bearer %s"), *ApiKey));
    Headers.Add(TEXT("OpenAI-Beta"), TEXT("realtime=v1"));

    WebSocket = FWebSocketsModule::Get().CreateWebSocket(Url, TEXT(""), Headers);

    WebSocket->OnConnected().AddUObject(this, &UWebSocketSubsystem::HandleConnected);
    WebSocket->OnMessage().AddUObject(this, &UWebSocketSubsystem::HandleMessageReceived);
    WebSocket->OnConnectionError().AddUObject(this, &UWebSocketSubsystem::HandleError);
    WebSocket->OnClosed().AddUObject(this, &UWebSocketSubsystem::HandleClosed);

    WebSocket->Connect();
}
```

---

#### `UOpenAiApiSubsystem` — The Protocol Layer

**Header:** `Source/FSE100Capstone/Subsystems/OpenAiApiSubsystem.h`

This subsystem depends on `WebSocketSubsystem` (declared via `InitializeDependency`).

**Key Methods:**
```cpp
// Send a chunk of audio to OpenAI
void SendAudioInputToAI(const FString& AudioChunkBase64);

// Add a message to the conversation history (e.g., inject context)
void CreateConversationItem(const TSharedPtr<FJsonObject>& ItemObject);

// Reconfigure the AI session (persona, tools, voice)
void UpdateSessionConfiguration(const TSharedPtr<FJsonObject>& SessionObject);
```

**Key Events (what downstream systems listen to):**
```cpp
// AI audio response (base64 PCM16 chunk)
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnResponseAudioDelta, const FString&, AudioDelta);
UPROPERTY(BlueprintAssignable)
FOnResponseAudioDelta OnResponseAudioDeltaReceived;

// AI text transcript (partial, streams in)
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTranscriptDelta, const FString&, Text);
UPROPERTY(BlueprintAssignable)
FOnTranscriptDelta OnResponseTranscriptDeltaReceived;

// AI requests a function call
DECLARE_MULTICAST_DELEGATE_OneParam(FOnFunctionCallReceived, const TSharedPtr<FJsonObject>&);
FOnFunctionCallReceived OnFunctionCallReceived;

// Speech detection events
UPROPERTY(BlueprintAssignable)
FSimpleMulticastDelegate OnInputSpeechStarted;

UPROPERTY(BlueprintAssignable)
FSimpleMulticastDelegate OnInputSpeechStopped;
```

**JSON Parsing Logic:**
The subsystem's `WebSocketSubsystem::OnMessageReceived` handler parses incoming JSON and routes by `type` field:

```cpp
void UOpenAiApiSubsystem::HandleMessageReceived(const FString& RawJson)
{
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(RawJson);
    
    if (!FJsonSerializer::Deserialize(Reader, JsonObject)) return;
    
    FString Type;
    JsonObject->TryGetStringField(TEXT("type"), Type);
    
    if (Type == TEXT("response.audio.delta"))
    {
        FString Delta;
        JsonObject->TryGetStringField(TEXT("delta"), Delta);
        OnResponseAudioDeltaReceived.Broadcast(Delta);
    }
    else if (Type == TEXT("response.audio_transcript.delta"))
    {
        FString Delta;
        JsonObject->TryGetStringField(TEXT("delta"), Delta);
        OnResponseTranscriptDeltaReceived.Broadcast(Delta);
    }
    else if (Type == TEXT("response.function_call_arguments.done"))
    {
        OnFunctionCallReceived.Broadcast(JsonObject);
    }
    else if (Type == TEXT("input_audio_buffer.speech_started"))
    {
        OnInputSpeechStarted.Broadcast();
    }
    else if (Type == TEXT("input_audio_buffer.speech_stopped"))
    {
        OnInputSpeechStopped.Broadcast();
    }
}
```

---

#### `UAIToolInterpreterSubsystem` — The Interpretation Layer

**Header:** `Source/FSE100Capstone/Subsystems/AIToolInterpreterSubsystem.h`

Depends on `OpenAiApiSubsystem` (bound in `Initialize`).

```cpp
UCLASS()
class UAIToolInterpreterSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    // Called to reconfigure what tools the AI can use
    UFUNCTION(BlueprintCallable)
    void UpdateAIToolChoice(const FString& ToolChoice);

    // Fired when the AI requests an emotion change
    UPROPERTY(BlueprintAssignable)
    FOnSetEmotion OnSetEmotion;

private:
    UPROPERTY()
    UOpenAiApiSubsystem* OpenAiApiSubsystem;

    void HandleFunctionCall(const TSharedPtr<FJsonObject>& FunctionCall);
};
```

**Initialize binds to the OpenAI subsystem:**
```cpp
void UAIToolInterpreterSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    // Ensure OpenAiApiSubsystem is initialized first
    Collection.InitializeDependency<UOpenAiApiSubsystem>();
    Super::Initialize(Collection);

    OpenAiApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>();
    if (OpenAiApiSubsystem)
    {
        OpenAiApiSubsystem->OnFunctionCallReceived.AddUObject(
            this, &UAIToolInterpreterSubsystem::HandleFunctionCall);
    }
}

void UAIToolInterpreterSubsystem::HandleFunctionCall(const TSharedPtr<FJsonObject>& FunctionCall)
{
    FString FunctionName;
    FunctionCall->TryGetStringField(TEXT("name"), FunctionName);

    if (FunctionName == TEXT("set_emotion"))
    {
        FString ArgumentsStr;
        FunctionCall->TryGetStringField(TEXT("arguments"), ArgumentsStr);
        
        TSharedPtr<FJsonObject> Args;
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ArgumentsStr);
        FJsonSerializer::Deserialize(Reader, Args);
        
        FString Emotion;
        if (Args && Args->TryGetStringField(TEXT("emotion"), Emotion))
        {
            OnSetEmotion.Broadcast(Emotion);
        }
    }
}
```

---

#### `UAIConversationOrchestratorSubsystem` — The Coordination Layer

The simplest subsystem—its sole responsibility is routing data between the audio input and AI API:

```cpp
void UAIConversationOrchestratorSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Collection.InitializeDependency<UAudioInputSubsystem>();
    Collection.InitializeDependency<UOpenAiApiSubsystem>();
    Super::Initialize(Collection);

    AudioInputSubsystem = GetGameInstance()->GetSubsystem<UAudioInputSubsystem>();
    OpenAiApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>();

    if (AudioInputSubsystem && OpenAiApiSubsystem)
    {
        // Wire audio capture output directly to AI input
        AudioInputSubsystem->OnAudioChunkCaptured.AddDynamic(
            this, &UAIConversationOrchestratorSubsystem::HandleAudioChunk);
    }
}

void UAIConversationOrchestratorSubsystem::HandleAudioChunk(const FString& Base64Audio)
{
    if (OpenAiApiSubsystem)
    {
        OpenAiApiSubsystem->SendAudioInputToAI(Base64Audio);
    }
}
```

### Accessing Subsystems From Other C++ Classes

```cpp
// In any Actor or Component's BeginPlay:
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    
    // Get any subsystem (always null-check the result)
    UOpenAiApiSubsystem* ApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>();
    if (ApiSubsystem)
    {
        // Bind to events using AddDynamic (for BlueprintAssignable delegates)
        ApiSubsystem->OnResponseTranscriptDeltaReceived.AddDynamic(
            this, &AMyActor::HandleTranscript);
        
        // Or AddUObject for non-dynamic delegates
        ApiSubsystem->OnFunctionCallReceived.AddUObject(
            this, &AMyActor::HandleFunctionCall);
    }
}

// Always unbind in EndPlay to prevent dangling delegate crashes:
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (UOpenAiApiSubsystem* ApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>())
    {
        ApiSubsystem->OnResponseTranscriptDeltaReceived.RemoveDynamic(this, &AMyActor::HandleTranscript);
        ApiSubsystem->OnFunctionCallReceived.RemoveAll(this);
    }
    Super::EndPlay(EndPlayReason);
}
```

!!! tip "Learn More"
    If you'd like to learn more, you can read our more fine-grained technical documentation on subsystem architecture, including complete code examples for referencing, calling, and binding to subsystem events, at [Subsystems](../legacy/subsystems.md).

---

## VR Mechanics & Meta XR Integration

### Why Meta XR Plugin, Not OpenXR

The project uses the **Meta XR Plugin** instead of the default OpenXR plugin for the following concrete reasons:

| Feature | OpenXR | Meta XR Plugin |
|---------|--------|---------------|
| Standalone Quest rendering optimization | Basic | Full (Fixed Foveated Rendering, Late Latching) |
| Hand tracking | Limited | Full joint tracking |
| Input mapping | Generic | Quest-optimized |
| Passthrough API | Very limited | Full color passthrough |
| Performance | Moderate | Best for Quest hardware |

### Installing the Meta XR Plugin

1. **Disable OpenXR first:** Edit → Plugins → Search "OpenXR" → Disable all OpenXR plugins → Restart
2. Download from Meta: [https://developers.meta.com/horizon/downloads/package/unreal-engine-5-integration](https://developers.meta.com/horizon/downloads/package/unreal-engine-5-integration)
3. Unzip to: `<UE5 Install Path>/Engine/Plugins/Marketplace/` (create Marketplace folder if missing)
4. Restart Unreal Engine → Edit → Plugins → Search "Meta XR" → Enable desired plugins

!!! tip "Learn More"
    If you'd like to learn more, you can read our more fine-grained technical documentation on Meta XR Plugin installation, OpenXR comparison, input/hand tracking setup, passthrough/MR features, and packaging at [Meta XR Plugin](../legacy/meta-xr-plugin.md).

### Required Project Settings for VR

```
Project Settings → XR → Meta XR
  ✅ Enable Meta XR Support

Project Settings → Engine → Rendering  
  ✅ Mobile Multi-View (required for stereo VR rendering on Quest)
  ✅ Forward Shading (better VR performance than Deferred)

Project Settings → Platforms → Android
  ✅ Package Game Data Inside APK
  SDK API Level: 33+
  Enable Support Vulkan: ✅
```

### Recommended Rendering Optimizations

```
Project Settings → Meta XR (or Project Settings → VR)
  ✅ Enable Late Latching    — Reduces perceived head-tracking latency
  ✅ Fixed Foveated Rendering — Renders edges of view at lower resolution
  ✅ Mobile Multi-View        — Single-pass stereo rendering (major perf win)
  Anti-Aliasing: FXAA (lower cost than TAA/TSR on mobile GPU)
```

---

## MetaHuman Integration

### MetaHuman Plugin Requirements

Enable in Edit → Plugins:

- ✅ **MetaHuman Creator**
- ✅ **MetaHuman Animator**
- ✅ **MetaHuman Core Tech**
- ✅ **MetaHuman SDK**

### Creating a New MetaHuman Character

1. Content Drawer → Right-click → MetaHuman → MetaHuman Character
2. Double-click the created asset to launch the MetaHuman Creator editor
3. Customize face, hair, skin, body, clothing, accessories
4. Click **Create Full Rig** when customization is complete
!!! warning
    Once rigged, editing is locked. To re-edit: Unrig → Edit → Create Full Rig again

5. After rigging, click **Download Texture Source** → Select 2K Resolution
6. Click **Assembly** → Configure:
   - Assembly Type: **UE Cine (Complete)**
   - Optimization: **Medium** (critical for VR framerate)
   - Root Directory: Choose your project's Content directory

### VR Optimization Settings for the Generated Blueprint

Open the generated MetaHuman Blueprint and apply these settings:

**Face Component:**
```
Visibility Based Anim Tick Option → Always Tick Pose and Refresh Bones
(Ensures face continues updating in VR even when the camera is looking away)
```

**Body Component:**
```
Visibility Based Anim Tick Option → Always Tick Pose
```

**Hair Component:**
```
Use Cards → True    (Hair card simulation is much cheaper than strand sim in VR)
LOD Bias → 1        (Start at lower LOD for performance)
```

**LODSync Component:**
```
Num LODs → 8       (More LOD levels = smoother performance transitions)
```

**Body Mesh:**
```
Cast Shadow → True
Cast Contact Shadow → False  (Contact shadows are expensive and barely visible in VR)
```

!!! tip "Learn More"
    If you'd like to learn more, you can read our more fine-grained technical documentation on MetaHuman Creator setup, including plugin installation, character customization, rigging, texture downloads, assembly settings, and VR optimization at [MetaHuman Creator](../legacy/metahuman-creator.md).

### The Face Animation Post-Process Blueprint

All lip sync curves must be applied through:
```
MetaHumans/Common/Face/ABP_Face_PostProcess
```

This Animation Blueprint is the engine for facial deformation. **Do not modify this file directly**—instead, modify it through the curve map approach described in [The AI Pipeline](ai-pipeline.md) Section 5.

Key setup in `ABP_Face_PostProcess`:

1. Add a **ModifyCurve** node in the AnimGraph, placed immediately before `AnimNode_RigLogic`
2. Set ModifyCurve's **Apply Mode** to `Add` and **Alpha** to `1.0`
3. In the EventGraph's `EventBlueprintUpdateAnimation`:
   - Get `IntervieweeActorRef` from parent actor
   - Call `GetCurrentVisemes()` (C++ UFUNCTION) → 15-element float array
   - Call `GetCurrentLoudness()` → normalized 0-1 float
   - Apply viseme multipliers
   - Apply FInterpTo smoothing
   - Write to `LipSyncCurves` map
   - Clear and rebuild the map → fed to ModifyCurve node

!!! tip "Learn More"
    If you'd like to learn more, you can read our more fine-grained technical documentation on the OVRLipSync plugin, including installation, UE5.6 compatibility fixes, streaming architecture, viseme-to-curve mappings, multiplier values, and smoothing parameters at [Oculus LipSync Plugin](../legacy/oculus-lipsync.md).

---

## Internal Save System (`BP_GameInstance`)

The internal (local) save system handles **on-device** session persistence using UE5's `SaveGame` object system. This is separate from the **remote** (AWS) save system; the two work in tandem.

### Two SaveGame Objects

```
SG_LocalGameSetting
├── LastUserID: String  (format: "ASUID_SessionID", e.g., "1234567890_0001")
│   └── Used to auto-fill login UI on next launch

SG_SaveData  (one per ASUID+SessionID pair)
├── ASUID: Int
├── StudentName: String
├── SessionID: Int
└── ScenarioProgress: Array<FScenarioProgressStruct>
    └── {CharacterName, ScenarioNumber, Progress (float), LastSaveTime}
```

### Initialization Flow

When the game starts, `VRGameMode.BeginPlay()` calls `BP_GameInstance.Initial()`:

```
Initial():

1. Try to load SG_LocalGameSetting from slot "LocalSettings"
   ├── If not found: create new SG_LocalGameSetting, save it
   └── If found: read LastUserID

2. Parse LastUserID → extract ASUID and SessionID
3. Try to load SG_SaveData from slot formatted as "ASUID_SessionID"
   ├── If found: game is ready; auto-fill login UI with known values
   └── If not found: Login UI opens with empty fields
```

### Login Flow

```
User enters ASUID + SessionID → presses Login:

1. BP_GameInstance.Login(ASUID, StudentName, SessionID)
2. Construct slot name: ASUID + "_" + SessionID
3. Load SG_SaveData from that slot
   ├── Exists → load data → proceed to game
   └── Not exists → show warning popup "No save data found"

User presses "New Save":

1. WB_Save_New widget opens
2. User enters ASUID, StudentName, SessionID
3. BP_GameInstance creates new SG_SaveData
4. Updates SG_LocalGameSetting.LastUserID = ASUID + "_" + SessionID
5. Saves both objects to disk
6. Proceeds to game
```

### AWS Sync Integration

The local save tracks progress as the student plays. At checkpoint moments (scenario start, scenario completion), `BP_GameInstance` also calls `USaveToAWS::SendStudentSessionToAWS()` to sync with the remote database. On login, `USaveToAWS::LoginStudentFromAWS()` retrieves cloud data; if cloud data is more recent than local data, it takes precedence.

!!! tip "Learn More"
    If you'd like to learn more, you can read our more fine-grained technical documentation on the local save system, including `SG_LocalGameSetting`, `SG_SaveData`, the login/new-save UI flow, and SessionID policies at [Save System](../legacy/save-system.md).

---

➡️ **Next:** [Infrastructure & Cloud](infrastructure-cloud.md)
