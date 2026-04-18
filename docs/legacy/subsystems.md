# Subsystems Guide

## What is a Subsystem?

**Think of it like a better Singleton:** If you're familiar with the Singleton pattern (a class with only one instance globally accessible), subsystems are similar but with superpowers. Unlike traditional singletons, subsystems are managed by Unreal Engine itself, which handles their creation, destruction, and initialization order automatically. You get global accessibility without the typical singleton headaches.

In Unreal Engine, a **subsystem** is a specialized class that provides automatic lifetime management and initialization ordering. Subsystems are designed to encapsulate specific functionality and maintain state throughout their lifetime scope.

**Key Benefits:**

- **Automatic Lifecycle Management**: Subsystems are automatically initialized and deinitialized by Unreal Engine
- **Dependency Management**: You can specify dependencies between subsystems to ensure proper initialization order
- **Global Access**: Easy to access from anywhere in your project without needing direct references
- **Separation of Concerns**: Each subsystem handles a specific domain of functionality

**Types of Subsystems:**

- `UGameInstanceSubsystem` - Lives for the entire game instance (persists across level transitions)
- `UWorldSubsystem` - Lives for a specific world/level
- `ULocalPlayerSubsystem` - Lives for a specific local player
- Others: Editor, Engine, etc.

In this project, we use **GameInstanceSubsystems** because our AI conversation features need to persist across the entire game session.

---

## The 5 Subsystems in Our Project

Our project uses the following subsystems to manage AI conversations:

1. **WebSocketSubsystem** - Low-level WebSocket communication
2. **OpenAiApiSubsystem** - OpenAI Realtime API integration
3. **AudioInputSubsystem** - Microphone audio capture and processing
4. **AIToolInterpreterSubsystem** - AI function call interpretation
5. **AIConversationOrchestratorSubsystem** - Coordination layer

---

## Subsystem Responsibilities

### WebSocketSubsystem
**Purpose**: Manages low-level WebSocket connections for real-time bidirectional communication.

**Responsibilities:**

- Establishing and maintaining WebSocket connections
- Sending and receiving raw messages
- Handling connection lifecycle (connect, disconnect, errors)
- Broadcasting connection events

**Key Methods:**

- `IsConnected()` - Check connection status
- `SendMessage(const FString& Message)` - Send raw messages

**Events:**

- `OnConnected` - Fired when connection is established
- `OnMessageReceived` - Fired when a message arrives
- `OnConnectionError` - Fired on connection errors
- `OnClosed` - Fired when connection closes

### OpenAiApiSubsystem
**Purpose**: Manages communication with OpenAI's Realtime API via WebSocket.

**Responsibilities:**

- Sending audio input to OpenAI
- Receiving and parsing OpenAI responses (audio, text, function calls)
- Managing conversation sessions and configuration
- Creating conversation items
- Detecting speech start/stop events

**Key Methods:**

- `SendAudioInputToAI(const FString& AudioChunkBase64)` - Send audio to AI
- `CreateConversationItem(const TSharedPtr<FJsonObject>& ItemObject)` - Add conversation items
- `UpdateSessionConfiguration(const TSharedPtr<FJsonObject>& SessionObject)` - Update AI settings

**Events:**

- `OnResponseAudioDeltaReceived` - AI audio response chunks (base64 PCM16)
- `OnResponseTranscriptDeltaReceived` - AI text transcript chunks
- `OnFunctionCallReceived` - AI function call requests
- `OnInputSpeechStarted` - User started speaking
- `OnInputSpeechStopped` - User stopped speaking
- `OnNewResponse` - New AI response created

**Dependencies:**

- `WebSocketSubsystem` - For underlying WebSocket communication

### AudioInputSubsystem
**Purpose**: Captures and processes audio from the microphone for AI consumption.

**Responsibilities:**

- Capturing audio from the default microphone
- Downsampling audio to 24kHz mono (required by OpenAI)
- Converting audio to PCM16 format
- Encoding audio as base64 strings
- Broadcasting processed audio chunks

**Key Methods:**

- `StartCapturing()` - Begin capturing audio
- `StopCapturing()` - Stop capturing audio

**Events:**

- `OnAudioChunkCaptured` - Processed audio chunk ready (base64 PCM16)
- `OnAudioCaptureStarted` - Capture has begun
- `OnAudioCaptureStopped` - Capture has ended

**Technical Details:**

- Input: Any format from microphone
- Output: 24kHz mono PCM16, base64-encoded
- Processing: Downsampling, channel mixing, format conversion

### AIToolInterpreterSubsystem
**Purpose**: Interprets and executes AI function calls (tool calls) from OpenAI.

**Responsibilities:**

- Listening for function call events from OpenAI
- Parsing function call arguments
- Executing appropriate game logic based on function calls
- Updating AI tool configuration dynamically
- Managing available tools/functions

**Key Methods:**

- `UpdateAIToolChoice(const FString& ToolChoice)` - Configure available tools

**Events:**

- `OnSetEmotion` - Emotion change requested by AI

**Supported Functions:**

- `set_emotion` - Changes the interviewee's emotional state

**Dependencies:**

- `OpenAiApiSubsystem` - Listens to function call events

### AIConversationOrchestratorSubsystem
**Purpose**: Orchestrates the flow of data between audio input and the AI system.

**Responsibilities:**

- Connecting AudioInputSubsystem to OpenAiApiSubsystem
- Acting as a coordination layer
- Routing audio data to the AI

**Key Logic:**
```cpp
AudioInput → Orchestrator → OpenAI API
```

**Dependencies:**

- `AudioInputSubsystem` - Source of audio data
- `OpenAiApiSubsystem` - Destination for audio data

## How the Subsystems Interact

The subsystems work together in a layered architecture:

### Data Flow Example: User Speaks to AI

1. **User speaks** → `AudioInputSubsystem` captures microphone audio
2. **Audio processing** → `AudioInputSubsystem` downsamples to 24kHz mono PCM16, base64-encodes
3. **Event broadcast** → `OnAudioChunkCaptured` fires with base64 audio
4. **Orchestration** → `AIConversationOrchestratorSubsystem` receives the event
5. **Forward to AI** → Orchestrator calls `OpenAiApiSubsystem::SendAudioInputToAI()`
6. **Network send** → `OpenAiApiSubsystem` formats message and calls `WebSocketSubsystem::SendMessage()`
7. **WebSocket** → `WebSocketSubsystem` sends data to OpenAI servers

### Data Flow Example: AI Responds

1. **Network receive** → `WebSocketSubsystem` receives message from OpenAI
2. **Event broadcast** → `OnMessageReceived` fires with JSON message
3. **Parse response** → `OpenAiApiSubsystem` parses the JSON
4. **Route data** → Based on response type:
   - Audio delta → `OnResponseAudioDeltaReceived` fires
   - Transcript delta → `OnResponseTranscriptDeltaReceived` fires
   - Function call → `OnFunctionCallReceived` fires
5. **Function execution** → `AIToolInterpreterSubsystem` handles function calls
6. **Game logic** → `OnSetEmotion` fires → `IntervieweeActor` updates emotion

---

## I'm Gonna Make a New C++ Class! How Can I...

### Reference a Subsystem

To get a reference to a subsystem from any class, use the `GetGameInstance()->GetSubsystem<T>()` pattern:

```cpp
// In your header (.h file)
#include "Subsystems/OpenAiApiSubsystem.h"

class AMyActor : public AActor
{
    GENERATED_BODY()

private:
    UPROPERTY()
    UOpenAiApiSubsystem* OpenAiApiSubsystem;
};
```

```cpp
// In your source (.cpp file)
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    
    // Get the subsystem from the game instance
    OpenAiApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>();
    
    // Always check for null!
    if (OpenAiApiSubsystem)
    {
        UE_LOG(LogTemp, Display, TEXT("Got OpenAI subsystem!"));
    }
}
```

**Important Notes:**

- Always store subsystems as `UPROPERTY()` to prevent garbage collection
- Always null-check before using
- Use `GetWorld()->GetGameInstance()->GetSubsystem<T>()` if you don't inherit from AActor
- Subsystems are only available after the game instance is initialized

---

### Call a Subsystem's Method

Once you have a reference, calling methods is straightforward:

```cpp
void AMyActor::SendAudioToAI()
{
    if (!OpenAiApiSubsystem)
    {
        UE_LOG(LogTemp, Error, TEXT("OpenAiApiSubsystem is null!"));
        return;
    }
    
    // Call a method
    FString AudioData = TEXT("base64EncodedAudioData...");
    OpenAiApiSubsystem->SendAudioInputToAI(AudioData);
    
    // Create a conversation item
    TSharedPtr<FJsonObject> Item = MakeShared<FJsonObject>();
    Item->SetStringField(TEXT("type"), TEXT("message"));
    Item->SetStringField(TEXT("role"), TEXT("user"));
    OpenAiApiSubsystem->CreateConversationItem(Item);
}
```

**Example: Starting Audio Capture**
```cpp
void AMyCharacter::StartListening()
{
    UAudioInputSubsystem* AudioInputSubsystem = 
        GetGameInstance()->GetSubsystem<UAudioInputSubsystem>();
    
    if (AudioInputSubsystem)
    {
        AudioInputSubsystem->StartCapturing();
        UE_LOG(LogTemp, Display, TEXT("Started capturing audio"));
    }
}
```

---

### Bind to a Subsystem's Event

Subsystems expose delegates (events) that you can bind to. There are two types:

#### Dynamic Delegates (BlueprintAssignable)
These use `AddDynamic` and require a `UFUNCTION()`:

```cpp
// In your header (.h file)
class AMyActor : public AActor
{
    GENERATED_BODY()

private:
    UPROPERTY()
    UOpenAiApiSubsystem* OpenAiApiSubsystem;
    
    // Must be a UFUNCTION for dynamic delegates
    UFUNCTION()
    void HandleTranscriptReceived(const FString& TranscriptDelta);
    
    UFUNCTION()
    void HandleInputSpeechStarted();
};
```

```cpp
// In your source (.cpp file)
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    
    OpenAiApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>();
    
    if (OpenAiApiSubsystem)
    {
        // Bind to dynamic delegates using AddDynamic
        OpenAiApiSubsystem->OnResponseTranscriptDeltaReceived.AddDynamic(
            this, 
            &AMyActor::HandleTranscriptReceived
        );
        
        OpenAiApiSubsystem->OnInputSpeechStarted.AddDynamic(
            this,
            &AMyActor::HandleInputSpeechStarted
        );
    }
}

void AMyActor::HandleTranscriptReceived(const FString& TranscriptDelta)
{
    UE_LOG(LogTemp, Display, TEXT("AI said: %s"), *TranscriptDelta);
}

void AMyActor::HandleInputSpeechStarted()
{
    UE_LOG(LogTemp, Display, TEXT("User started speaking"));
}
```

#### Regular Multicast Delegates
These use `AddRaw`, `AddUObject`, or `AddLambda`:

```cpp
// For FOnFunctionCallReceived (non-dynamic delegate)
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    
    OpenAiApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>();
    
    if (OpenAiApiSubsystem)
    {
        // Bind using AddUObject for regular delegates
        OpenAiApiSubsystem->OnFunctionCallReceived.AddUObject(
            this,
            &AMyActor::HandleFunctionCall
        );
        
        // Or use a lambda
        OpenAiApiSubsystem->OnFunctionCallReceived.AddLambda(
            [this](const TSharedPtr<FJsonObject>& FunctionCall)
            {
                UE_LOG(LogTemp, Display, TEXT("Function call received!"));
            }
        );
    }
}

void AMyActor::HandleFunctionCall(const TSharedPtr<FJsonObject>& FunctionCall)
{
    // Process the function call
    FString FunctionName;
    if (FunctionCall->TryGetStringField(TEXT("name"), FunctionName))
    {
        UE_LOG(LogTemp, Display, TEXT("Function: %s"), *FunctionName);
    }
}
```

#### Don't Forget to Unbind!
Always unbind delegates when your object is destroyed to prevent crashes:

```cpp
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (OpenAiApiSubsystem)
    {
        OpenAiApiSubsystem->OnResponseTranscriptDeltaReceived.RemoveDynamic(
            this,
            &AMyActor::HandleTranscriptReceived
        );
        
        OpenAiApiSubsystem->OnInputSpeechStarted.RemoveDynamic(
            this,
            &AMyActor::HandleInputSpeechStarted
        );
        
        OpenAiApiSubsystem->OnFunctionCallReceived.RemoveAll(this);
    }
    
    Super::EndPlay(EndPlayReason);
}
```

---

## Complete Example: Custom AI Listener Actor

Here's a complete example showing all three patterns:

**MyAIListener.h**
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Subsystems/OpenAiApiSubsystem.h"
#include "Subsystems/AudioInputSubsystem.h"
#include "MyAIListener.generated.h"

UCLASS()
class FSE100CAPSTONE_API AMyAIListener : public AActor
{
    GENERATED_BODY()
    
public:
    AMyAIListener();
    
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
    
    // Public method to start/stop listening
    UFUNCTION(BlueprintCallable)
    void StartListening();
    
    UFUNCTION(BlueprintCallable)
    void StopListening();

private:
    // Subsystem references
    UPROPERTY()
    UOpenAiApiSubsystem* OpenAiApiSubsystem;
    
    UPROPERTY()
    UAudioInputSubsystem* AudioInputSubsystem;
    
    // Event handlers (must be UFUNCTION for dynamic delegates)
    UFUNCTION()
    void HandleAITranscript(const FString& TranscriptDelta);
    
    UFUNCTION()
    void HandleSpeechStarted();
    
    UFUNCTION()
    void HandleSpeechStopped();
    
    // Full transcript accumulator
    FString FullTranscript;
};
```

**MyAIListener.cpp**
```cpp
#include "MyAIListener.h"

AMyAIListener::AMyAIListener()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AMyAIListener::BeginPlay()
{
    Super::BeginPlay();
    
    // 1. Get subsystem references
    OpenAiApiSubsystem = GetGameInstance()->GetSubsystem<UOpenAiApiSubsystem>();
    AudioInputSubsystem = GetGameInstance()->GetSubsystem<UAudioInputSubsystem>();
    
    // 2. Bind to subsystem events
    if (OpenAiApiSubsystem)
    {
        OpenAiApiSubsystem->OnResponseTranscriptDeltaReceived.AddDynamic(
            this,
            &AMyAIListener::HandleAITranscript
        );
        
        OpenAiApiSubsystem->OnInputSpeechStarted.AddDynamic(
            this,
            &AMyAIListener::HandleSpeechStarted
        );
        
        OpenAiApiSubsystem->OnInputSpeechStopped.AddDynamic(
            this,
            &AMyAIListener::HandleSpeechStopped
        );
    }
}

void AMyAIListener::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    // 3. Always unbind to prevent crashes
    if (OpenAiApiSubsystem)
    {
        OpenAiApiSubsystem->OnResponseTranscriptDeltaReceived.RemoveDynamic(
            this,
            &AMyAIListener::HandleAITranscript
        );
        
        OpenAiApiSubsystem->OnInputSpeechStarted.RemoveDynamic(
            this,
            &AMyAIListener::HandleSpeechStarted
        );
        
        OpenAiApiSubsystem->OnInputSpeechStopped.RemoveDynamic(
            this,
            &AMyAIListener::HandleSpeechStopped
        );
    }
    
    Super::EndPlay(EndPlayReason);
}

void AMyAIListener::StartListening()
{
    // 4. Call subsystem methods
    if (AudioInputSubsystem)
    {
        AudioInputSubsystem->StartCapturing();
        UE_LOG(LogTemp, Display, TEXT("Started listening..."));
    }
}

void AMyAIListener::StopListening()
{
    if (AudioInputSubsystem)
    {
        AudioInputSubsystem->StopCapturing();
        UE_LOG(LogTemp, Display, TEXT("Stopped listening."));
    }
}

void AMyAIListener::HandleAITranscript(const FString& TranscriptDelta)
{
    // Accumulate the transcript
    FullTranscript += TranscriptDelta;
    UE_LOG(LogTemp, Display, TEXT("AI: %s"), *TranscriptDelta);
}

void AMyAIListener::HandleSpeechStarted()
{
    UE_LOG(LogTemp, Display, TEXT("User started speaking"));
    FullTranscript.Empty(); // Clear previous transcript
}

void AMyAIListener::HandleSpeechStopped()
{
    UE_LOG(LogTemp, Display, TEXT("User stopped speaking"));
    UE_LOG(LogTemp, Display, TEXT("Full AI response: %s"), *FullTranscript);
}
```

---

## Best Practices

1. **Always null-check subsystems** before using them
2. **Store subsystems as UPROPERTY()** to prevent garbage collection
3. **Unbind delegates in EndPlay()** or BeginDestroy() to prevent crashes
4. **Use the right delegate binding**:
   - `AddDynamic()` for dynamic multicast delegates (requires `UFUNCTION()`)
   - `AddUObject()` for regular delegates
   - `AddLambda()` for inline handlers
5. **Initialize subsystems in BeginPlay()** not in the constructor
6. **Use InitializeDependency()** when creating subsystems that depend on other subsystems
7. **Log errors** when subsystems are unexpectedly null to help debugging

---

## Troubleshooting

**Problem: Subsystem is null**

- Make sure the game instance is initialized (don't call in constructor)
- Check that the subsystem class is properly set up with `UCLASS()`
- Verify you're using `GetGameInstance()` not `GetWorld()`

**Problem: Event not firing**

- Verify you bound with `AddDynamic()` or `AddUObject()`
- Check that the handler function signature matches exactly
- Ensure handler is marked `UFUNCTION()` for dynamic delegates
- Make sure you didn't unbind accidentally

**Problem: Crash when object is destroyed**

- You forgot to unbind delegates in `EndPlay()`
- Always call `RemoveDynamic()` or `RemoveAll(this)` before destruction

---

## Summary

Subsystems in this project provide a clean, modular architecture for AI conversation features:

- **WebSocketSubsystem**: Raw network communication
- **OpenAiApiSubsystem**: AI protocol and response handling  
- **AudioInputSubsystem**: Audio capture and processing
- **AIToolInterpreterSubsystem**: Function call execution
- **AIConversationOrchestratorSubsystem**: Coordination

They work together in layers, from low-level WebSocket up to high-level AI interactions, with events flowing through the system to notify interested parties of state changes and data updates.

