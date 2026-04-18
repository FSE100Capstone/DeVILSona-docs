# Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`ACarPawnBase`](#class_a_car_pawn_base) | 
`class `[`AIntervieweeActor`](#class_a_interviewee_actor) | [AIntervieweeActor](#class_a_interviewee_actor)
`class `[`FSE100Capstone`](#class_f_s_e100_capstone) | 
`class `[`UAIConversationOrchestratorSubsystem`](#class_u_a_i_conversation_orchestrator_subsystem) | [UAIConversationOrchestratorSubsystem](#class_u_a_i_conversation_orchestrator_subsystem)
`class `[`UAIToolInterpreterSubsystem`](#class_u_a_i_tool_interpreter_subsystem) | [UAIToolInterpreterSubsystem](#class_u_a_i_tool_interpreter_subsystem)
`class `[`UAudioInputSubsystem`](#class_u_audio_input_subsystem) | [UAudioInputSubsystem](#class_u_audio_input_subsystem)
`class `[`UAudioProcessingSubsystem`](#class_u_audio_processing_subsystem) | 
`class `[`UMyUnrealEdEngine`](#class_u_my_unreal_ed_engine) | 
`class `[`UOpenAiApiSubsystem`](#class_u_open_ai_api_subsystem) | [UOpenAiApiSubsystem](#class_u_open_ai_api_subsystem)
`class `[`UWebSocketSubsystem`](#class_u_web_socket_subsystem) | [UWebSocketSubsystem](#class_u_web_socket_subsystem)

# class `ACarPawnBase` 

```
class ACarPawnBase
  : public APawn
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`ACarPawnBase`](#class_a_car_pawn_base_1a38499c55e35177e538d0f1a962bbba64)`()` | 
`public virtual void `[`Tick`](#class_a_car_pawn_base_1ac6cb636db1dc16c0d45109cf4489584e)`(float DeltaTime)` | 
`public virtual void `[`SetupPlayerInputComponent`](#class_a_car_pawn_base_1afecdc76469c59359a6b2e5027714e31f)`(class UInputComponent * PlayerInputComponent)` | 
`public void `[`Look`](#class_a_car_pawn_base_1ac9ca5028ffb78fdbda19d30d9e7854bd)`(const FInputActionValue & Value)` | 
`public void `[`DisableLook`](#class_a_car_pawn_base_1a9b26f985ed205c69312c074733ee6469)`(const FInputActionValue & Value)` | 
`public void `[`EnableLook`](#class_a_car_pawn_base_1a2de3f7c97e2056293243367951066201)`(const FInputActionValue & Value)` | 
`protected class UInputAction * `[`LookAction`](#class_a_car_pawn_base_1a15b8d8f3a4e02c965752ce7c4db433e4) | 
`protected class UInputAction * `[`LookHoldAction`](#class_a_car_pawn_base_1a2b1917f2fa2086266e67136954f01ea0) | 
`protected bool `[`bLookEnabled`](#class_a_car_pawn_base_1ac6590257b24a408b7d6df357a6cca954) | 
`protected class UCameraComponent * `[`DriverCamera`](#class_a_car_pawn_base_1af09fe8ba1e0d5049e370ed232ccce411) | 
`protected class USceneComponent * `[`Root`](#class_a_car_pawn_base_1a8d833505a0b622a59c7f3f3502d4172c) | 
`protected UInputMappingContext * `[`DefaultMappingContext`](#class_a_car_pawn_base_1a3cb2f9e97f55d3f6eed432af9c1e2f6c) | 
`protected virtual void `[`BeginPlay`](#class_a_car_pawn_base_1a6194455b6d27f4efe211c07100240e0c)`()` | 
`protected virtual void `[`NotifyControllerChanged`](#class_a_car_pawn_base_1a9b2e3a7344a5e16073d3bf282d8083b9)`()` | 

## Members

#### `public  `[`ACarPawnBase`](#class_a_car_pawn_base_1a38499c55e35177e538d0f1a962bbba64)`()` 

#### `public virtual void `[`Tick`](#class_a_car_pawn_base_1ac6cb636db1dc16c0d45109cf4489584e)`(float DeltaTime)` 

#### `public virtual void `[`SetupPlayerInputComponent`](#class_a_car_pawn_base_1afecdc76469c59359a6b2e5027714e31f)`(class UInputComponent * PlayerInputComponent)` 

#### `public void `[`Look`](#class_a_car_pawn_base_1ac9ca5028ffb78fdbda19d30d9e7854bd)`(const FInputActionValue & Value)` 

#### `public void `[`DisableLook`](#class_a_car_pawn_base_1a9b26f985ed205c69312c074733ee6469)`(const FInputActionValue & Value)` 

#### `public void `[`EnableLook`](#class_a_car_pawn_base_1a2de3f7c97e2056293243367951066201)`(const FInputActionValue & Value)` 

#### `protected class UInputAction * `[`LookAction`](#class_a_car_pawn_base_1a15b8d8f3a4e02c965752ce7c4db433e4) 

#### `protected class UInputAction * `[`LookHoldAction`](#class_a_car_pawn_base_1a2b1917f2fa2086266e67136954f01ea0) 

#### `protected bool `[`bLookEnabled`](#class_a_car_pawn_base_1ac6590257b24a408b7d6df357a6cca954) 

#### `protected class UCameraComponent * `[`DriverCamera`](#class_a_car_pawn_base_1af09fe8ba1e0d5049e370ed232ccce411) 

#### `protected class USceneComponent * `[`Root`](#class_a_car_pawn_base_1a8d833505a0b622a59c7f3f3502d4172c) 

#### `protected UInputMappingContext * `[`DefaultMappingContext`](#class_a_car_pawn_base_1a3cb2f9e97f55d3f6eed432af9c1e2f6c) 

#### `protected virtual void `[`BeginPlay`](#class_a_car_pawn_base_1a6194455b6d27f4efe211c07100240e0c)`()` 

#### `protected virtual void `[`NotifyControllerChanged`](#class_a_car_pawn_base_1a9b2e3a7344a5e16073d3bf282d8083b9)`()` 

# class `AIntervieweeActor` 

```
class AIntervieweeActor
  : public AActor
```  

[AIntervieweeActor](#class_a_interviewee_actor)

A class representing an interviewee actor in the game. This actor handles audio responses, subtitles, and interactions with AI subsystems.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public FOnSubtitleUpdated `[`OnSubtitleUpdated`](#class_a_interviewee_actor_1a85bbf008605943706bf4b33617a44a6d) | Delegate triggered when subtitles are updated.
`public FOnResponseTranscriptDeltaReceived `[`OnTranscriptDeltaReceived`](#class_a_interviewee_actor_1ad588c29f9e2e3189a789fd6a9c389e0b) | Delegate triggered when a transcript delta is received.
`public FOnInputSpeechStarted `[`OnInputSpeechStarted`](#class_a_interviewee_actor_1a5f44f7dcaf227c5f4c666e0df6683e0f) | Delegate triggered when input speech starts.
`public FOnTalkingStarted `[`OnTalkingStarted`](#class_a_interviewee_actor_1adba856f968b28f6660a06d6fb4bf4fa7) | Delegate triggered when talking starts.
`public FOnTalkingStopped `[`OnTalkingStopped`](#class_a_interviewee_actor_1a8f34ba5ad3249438f0450f78bf75303e) | Delegate triggered when talking stops.
`public FOnSetEmotion `[`OnSetEmotion`](#class_a_interviewee_actor_1a80ad69e69ebaa3f987d6af39a93a9aba) | Delegate triggered to set the emotion of the actor.
`public USoundWaveProcedural * `[`AIResponseSoundWave`](#class_a_interviewee_actor_1ac3293fa9ce48e39112ee8056c26ae2f9) | Sound wave used for AI responses.
`public UAudioComponent * `[`AudioComponent`](#class_a_interviewee_actor_1ae1b1682047f68f2dbc8a855bbfe99bb8) | Audio component used to play audio responses.
`public  `[`AIntervieweeActor`](#class_a_interviewee_actor_1ae361e3c3ad77da41f40b6eeb7e3cf7b0)`()` | 
`public virtual void `[`Tick`](#class_a_interviewee_actor_1af038a718ec81e69de3caa305e9c08d40)`(float DeltaTime)` | 
`protected virtual void `[`BeginPlay`](#class_a_interviewee_actor_1a93ec6eaec458956d596477434fada7e4)`()` | 

## Members

#### `public FOnSubtitleUpdated `[`OnSubtitleUpdated`](#class_a_interviewee_actor_1a85bbf008605943706bf4b33617a44a6d) 

Delegate triggered when subtitles are updated.

#### `public FOnResponseTranscriptDeltaReceived `[`OnTranscriptDeltaReceived`](#class_a_interviewee_actor_1ad588c29f9e2e3189a789fd6a9c389e0b) 

Delegate triggered when a transcript delta is received.

#### `public FOnInputSpeechStarted `[`OnInputSpeechStarted`](#class_a_interviewee_actor_1a5f44f7dcaf227c5f4c666e0df6683e0f) 

Delegate triggered when input speech starts.

#### `public FOnTalkingStarted `[`OnTalkingStarted`](#class_a_interviewee_actor_1adba856f968b28f6660a06d6fb4bf4fa7) 

Delegate triggered when talking starts.

#### `public FOnTalkingStopped `[`OnTalkingStopped`](#class_a_interviewee_actor_1a8f34ba5ad3249438f0450f78bf75303e) 

Delegate triggered when talking stops.

#### `public FOnSetEmotion `[`OnSetEmotion`](#class_a_interviewee_actor_1a80ad69e69ebaa3f987d6af39a93a9aba) 

Delegate triggered to set the emotion of the actor.

#### `public USoundWaveProcedural * `[`AIResponseSoundWave`](#class_a_interviewee_actor_1ac3293fa9ce48e39112ee8056c26ae2f9) 

Sound wave used for AI responses.

#### `public UAudioComponent * `[`AudioComponent`](#class_a_interviewee_actor_1ae1b1682047f68f2dbc8a855bbfe99bb8) 

Audio component used to play audio responses.

#### `public  `[`AIntervieweeActor`](#class_a_interviewee_actor_1ae361e3c3ad77da41f40b6eeb7e3cf7b0)`()` 

#### `public virtual void `[`Tick`](#class_a_interviewee_actor_1af038a718ec81e69de3caa305e9c08d40)`(float DeltaTime)` 

#### `protected virtual void `[`BeginPlay`](#class_a_interviewee_actor_1a93ec6eaec458956d596477434fada7e4)`()` 

# class `FSE100Capstone` 

```
class FSE100Capstone
  : public ModuleRules
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public inline  `[`FSE100Capstone`](#class_f_s_e100_capstone_1af35522fb289190d5367245f73b7578f5)`(ReadOnlyTargetRules Target)` | 

## Members

#### `public inline  `[`FSE100Capstone`](#class_f_s_e100_capstone_1af35522fb289190d5367245f73b7578f5)`(ReadOnlyTargetRules Target)` 

# class `UAIConversationOrchestratorSubsystem` 

```
class UAIConversationOrchestratorSubsystem
  : public UGameInstanceSubsystem
```  

[UAIConversationOrchestratorSubsystem](#class_u_a_i_conversation_orchestrator_subsystem)

A game instance subsystem that orchestrates AI conversations by coordinating between audio input and OpenAI API subsystems. This subsystem manages the flow of audio data from capture to processing by the AI system.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public virtual void `[`Initialize`](#class_u_a_i_conversation_orchestrator_subsystem_1aa7c4a39a60d580741eeab81c3e020a11)`(FSubsystemCollectionBase & Collection)` | Initializes the subsystem and sets up necessary dependencies. 
`public virtual void `[`Deinitialize`](#class_u_a_i_conversation_orchestrator_subsystem_1a02ff56dd71b40ebdfdc0a86306e7ee2b)`()` | Cleans up the subsystem and releases resources.

## Members

#### `public virtual void `[`Initialize`](#class_u_a_i_conversation_orchestrator_subsystem_1aa7c4a39a60d580741eeab81c3e020a11)`(FSubsystemCollectionBase & Collection)` 

Initializes the subsystem and sets up necessary dependencies. 
#### Parameters
* `Collection` The collection of subsystems being initialized.

#### `public virtual void `[`Deinitialize`](#class_u_a_i_conversation_orchestrator_subsystem_1a02ff56dd71b40ebdfdc0a86306e7ee2b)`()` 

Cleans up the subsystem and releases resources.

# class `UAIToolInterpreterSubsystem` 

```
class UAIToolInterpreterSubsystem
  : public UGameInstanceSubsystem
```  

[UAIToolInterpreterSubsystem](#class_u_a_i_tool_interpreter_subsystem)

A game instance subsystem that interprets and executes AI tool calls from the OpenAI API. This subsystem listens for function calls from the AI and handles them accordingly, such as updating emotions or other game state based on AI decisions.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public FOnSetEmotion `[`OnSetEmotion`](#class_u_a_i_tool_interpreter_subsystem_1a34330b788d008dd33388e16a7d5056dd) | Delegate triggered when the AI requests an emotion change. Broadcasts the emotion string to be applied to relevant actors.
`public virtual void `[`Initialize`](#class_u_a_i_tool_interpreter_subsystem_1abef39226afecb301cac60216664b671a)`(FSubsystemCollectionBase & Collection)` | Initializes the subsystem and sets up connections to other subsystems. 
`public virtual void `[`Deinitialize`](#class_u_a_i_tool_interpreter_subsystem_1a1717b6d2bf8fd88554a717da3ac1e5e3)`()` | Cleans up the subsystem and releases resources.

## Members

#### `public FOnSetEmotion `[`OnSetEmotion`](#class_u_a_i_tool_interpreter_subsystem_1a34330b788d008dd33388e16a7d5056dd) 

Delegate triggered when the AI requests an emotion change. Broadcasts the emotion string to be applied to relevant actors.

#### `public virtual void `[`Initialize`](#class_u_a_i_tool_interpreter_subsystem_1abef39226afecb301cac60216664b671a)`(FSubsystemCollectionBase & Collection)` 

Initializes the subsystem and sets up connections to other subsystems. 
#### Parameters
* `Collection` The collection of subsystems being initialized.

#### `public virtual void `[`Deinitialize`](#class_u_a_i_tool_interpreter_subsystem_1a1717b6d2bf8fd88554a717da3ac1e5e3)`()` 

Cleans up the subsystem and releases resources.

# class `UAudioInputSubsystem` 

```
class UAudioInputSubsystem
  : public UGameInstanceSubsystem
```  

[UAudioInputSubsystem](#class_u_audio_input_subsystem)

A game instance subsystem that manages audio input capture from the microphone. This subsystem captures audio in real-time, processes it (downsamples to 24kHz mono and converts to PCM16 format), and broadcasts the audio chunks as base64-encoded strings for consumption by AI systems or other audio processing pipelines.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public FOnAudioCaptureStarted `[`OnAudioCaptureStarted`](#class_u_audio_input_subsystem_1a7dd7fa7db2766977a4b6a5aa7743fe9e) | Delegate triggered when audio capture has started successfully.
`public FOnAudioCaptureStopped `[`OnAudioCaptureStopped`](#class_u_audio_input_subsystem_1aed7b770f94ca4e3208d0acaf5ca9910a) | Delegate triggered when audio capture has stopped.
`public FOnAudioChunkCaptured `[`OnAudioChunkCaptured`](#class_u_audio_input_subsystem_1aee5619a8bc4f8b7a73ba8da768e610e9) | Delegate triggered when a new audio chunk has been captured and processed. The audio chunk is provided as a base64-encoded PCM16 string.
`public virtual void `[`Initialize`](#class_u_audio_input_subsystem_1a46732eaeb65f04fe726e02b8b452bcde)`(FSubsystemCollectionBase & Collection)` | Initializes the subsystem and sets up audio capture components. 
`public virtual void `[`Deinitialize`](#class_u_audio_input_subsystem_1a2590fb6120d1b9869fcdbf710a8ab7b6)`()` | Cleans up the subsystem, stops any active capture, and releases resources.
`public void `[`StartCapturing`](#class_u_audio_input_subsystem_1ab0cfe7164942fc6420d6925f89235b33)`()` | Starts capturing audio from the default microphone device. Triggers OnAudioCaptureStarted delegate when capture begins.
`public void `[`StopCapturing`](#class_u_audio_input_subsystem_1ab436fea43a8ef2a69796adbc01516d3b)`()` | Stops capturing audio from the microphone. Triggers OnAudioCaptureStopped delegate when capture ends.

## Members

#### `public FOnAudioCaptureStarted `[`OnAudioCaptureStarted`](#class_u_audio_input_subsystem_1a7dd7fa7db2766977a4b6a5aa7743fe9e) 

Delegate triggered when audio capture has started successfully.

#### `public FOnAudioCaptureStopped `[`OnAudioCaptureStopped`](#class_u_audio_input_subsystem_1aed7b770f94ca4e3208d0acaf5ca9910a) 

Delegate triggered when audio capture has stopped.

#### `public FOnAudioChunkCaptured `[`OnAudioChunkCaptured`](#class_u_audio_input_subsystem_1aee5619a8bc4f8b7a73ba8da768e610e9) 

Delegate triggered when a new audio chunk has been captured and processed. The audio chunk is provided as a base64-encoded PCM16 string.

#### `public virtual void `[`Initialize`](#class_u_audio_input_subsystem_1a46732eaeb65f04fe726e02b8b452bcde)`(FSubsystemCollectionBase & Collection)` 

Initializes the subsystem and sets up audio capture components. 
#### Parameters
* `Collection` The collection of subsystems being initialized.

#### `public virtual void `[`Deinitialize`](#class_u_audio_input_subsystem_1a2590fb6120d1b9869fcdbf710a8ab7b6)`()` 

Cleans up the subsystem, stops any active capture, and releases resources.

#### `public void `[`StartCapturing`](#class_u_audio_input_subsystem_1ab0cfe7164942fc6420d6925f89235b33)`()` 

Starts capturing audio from the default microphone device. Triggers OnAudioCaptureStarted delegate when capture begins.

#### `public void `[`StopCapturing`](#class_u_audio_input_subsystem_1ab436fea43a8ef2a69796adbc01516d3b)`()` 

Stops capturing audio from the microphone. Triggers OnAudioCaptureStopped delegate when capture ends.

# class `UAudioProcessingSubsystem` 

```
class UAudioProcessingSubsystem
  : public UGameInstanceSubsystem
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public virtual void `[`Initialize`](#class_u_audio_processing_subsystem_1a8a91a7178f4bc26e5ec973e49086f8df)`(FSubsystemCollectionBase & Collection)` | 
`public virtual void `[`Deinitialize`](#class_u_audio_processing_subsystem_1a6ca1cfd3f81861a0e749d0aed5b72d13)`()` | 

## Members

#### `public virtual void `[`Initialize`](#class_u_audio_processing_subsystem_1a8a91a7178f4bc26e5ec973e49086f8df)`(FSubsystemCollectionBase & Collection)` 

#### `public virtual void `[`Deinitialize`](#class_u_audio_processing_subsystem_1a6ca1cfd3f81861a0e749d0aed5b72d13)`()` 

# class `UMyUnrealEdEngine` 

```
class UMyUnrealEdEngine
  : public UUnrealEdEngine
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public virtual void `[`Init`](#class_u_my_unreal_ed_engine_1a027819011220a9d93f8297be638e827d)`(IEngineLoop * InEngineLoop)` | 

## Members

#### `public virtual void `[`Init`](#class_u_my_unreal_ed_engine_1a027819011220a9d93f8297be638e827d)`(IEngineLoop * InEngineLoop)` 

# class `UOpenAiApiSubsystem` 

```
class UOpenAiApiSubsystem
  : public UGameInstanceSubsystem
```  

[UOpenAiApiSubsystem](#class_u_open_ai_api_subsystem)

A game instance subsystem that manages real-time communication with OpenAI's Realtime API via WebSocket. This subsystem handles bidirectional streaming of audio and text data, processes AI responses including audio deltas and transcripts, and manages function calls from the AI. It supports session configuration updates and conversation item creation.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public FOnConnected `[`OnConnected`](#class_u_open_ai_api_subsystem_1a89affdd6e9dc46f4bfa7f5d712a377c1) | Delegate triggered when successfully connected to the OpenAI WebSocket API.
`public FOnResponseAudioDeltaReceived `[`OnResponseAudioDeltaReceived`](#class_u_open_ai_api_subsystem_1a9cb5376ec922e5d04a5dc94d1a2f37b8) | Delegate triggered when an audio response delta is received from OpenAI. Audio data is provided as base64-encoded PCM16 chunks.
`public FOnResponseTranscriptDeltaReceived `[`OnResponseTranscriptDeltaReceived`](#class_u_open_ai_api_subsystem_1ab756a3143733fb6e5a95175a2c77f005) | Delegate triggered when a transcript response delta is received from OpenAI. Text data is provided as string chunks representing the AI's spoken response.
`public FOnInputSpeechStarted `[`OnInputSpeechStarted`](#class_u_open_ai_api_subsystem_1a2675fb510a5a7f36d19a49dccb49119b) | Delegate triggered when the AI detects that user input speech has started.
`public FOnInputSpeechStopped `[`OnInputSpeechStopped`](#class_u_open_ai_api_subsystem_1a4cb2813a76790c9f98aa7edaae616eb5) | Delegate triggered when the AI detects that user input speech has stopped.
`public FOnNewResponse `[`OnNewResponse`](#class_u_open_ai_api_subsystem_1ad0ffa6b66b04a73e14a331369b45d25a) | Delegate triggered when a new AI response has been created and is ready to process.
`public FOnFunctionCallReceived `[`OnFunctionCallReceived`](#class_u_open_ai_api_subsystem_1ace490639abcd3d5c62b74b52897e9f68) | Delegate triggered when the AI requests a function call. Contains a JSON object with function name and arguments.
`public virtual void `[`Initialize`](#class_u_open_ai_api_subsystem_1a5426a20acb002550b0530fbbf7220314)`(FSubsystemCollectionBase & Collection)` | Initializes the subsystem and sets up WebSocket connections. 
`public virtual void `[`Deinitialize`](#class_u_open_ai_api_subsystem_1a5319f937ed470094dc12e1a7eb92bf35)`()` | Cleans up the subsystem, closes WebSocket connections, and releases resources.
`public void `[`SendAudioInputToAI`](#class_u_open_ai_api_subsystem_1aaa7121109a2ce6e5eea6009e260b9905)`(const FString & AudioChunkBase64)` | Sends audio input data to the OpenAI API for processing. 
`public void `[`CreateConversationItem`](#class_u_open_ai_api_subsystem_1a330bbf0a40f512e0fb6f11be93eec436)`(const TSharedPtr< FJsonObject > & ItemObject)` | Creates a new conversation item in the OpenAI session. Used to inject messages, function call results, or other conversation elements. 
`public void `[`UpdateSessionConfiguration`](#class_u_open_ai_api_subsystem_1abda828dc121262f71c3130080301ecc2)`(const TSharedPtr< FJsonObject > & SessionObject)` | Updates the OpenAI session configuration. Can be used to change settings like tools, instructions, etc. 
`public void `[`SendRawWebSocketMessage`](#class_u_open_ai_api_subsystem_1aa55bf270cca8ca7325b9445176f3b0f4)`(const FString & PayloadString)` | Sends a raw JSON message through the WebSocket connection. 

## Members

#### `public FOnConnected `[`OnConnected`](#class_u_open_ai_api_subsystem_1a89affdd6e9dc46f4bfa7f5d712a377c1) 

Delegate triggered when successfully connected to the OpenAI WebSocket API.

#### `public FOnResponseAudioDeltaReceived `[`OnResponseAudioDeltaReceived`](#class_u_open_ai_api_subsystem_1a9cb5376ec922e5d04a5dc94d1a2f37b8) 

Delegate triggered when an audio response delta is received from OpenAI. Audio data is provided as base64-encoded PCM16 chunks.

#### `public FOnResponseTranscriptDeltaReceived `[`OnResponseTranscriptDeltaReceived`](#class_u_open_ai_api_subsystem_1ab756a3143733fb6e5a95175a2c77f005) 

Delegate triggered when a transcript response delta is received from OpenAI. Text data is provided as string chunks representing the AI's spoken response.

#### `public FOnInputSpeechStarted `[`OnInputSpeechStarted`](#class_u_open_ai_api_subsystem_1a2675fb510a5a7f36d19a49dccb49119b) 

Delegate triggered when the AI detects that user input speech has started.

#### `public FOnInputSpeechStopped `[`OnInputSpeechStopped`](#class_u_open_ai_api_subsystem_1a4cb2813a76790c9f98aa7edaae616eb5) 

Delegate triggered when the AI detects that user input speech has stopped.

#### `public FOnNewResponse `[`OnNewResponse`](#class_u_open_ai_api_subsystem_1ad0ffa6b66b04a73e14a331369b45d25a) 

Delegate triggered when a new AI response has been created and is ready to process.

#### `public FOnFunctionCallReceived `[`OnFunctionCallReceived`](#class_u_open_ai_api_subsystem_1ace490639abcd3d5c62b74b52897e9f68) 

Delegate triggered when the AI requests a function call. Contains a JSON object with function name and arguments.

#### `public virtual void `[`Initialize`](#class_u_open_ai_api_subsystem_1a5426a20acb002550b0530fbbf7220314)`(FSubsystemCollectionBase & Collection)` 

Initializes the subsystem and sets up WebSocket connections. 
#### Parameters
* `Collection` - The collection of subsystems being initialized.

#### `public virtual void `[`Deinitialize`](#class_u_open_ai_api_subsystem_1a5319f937ed470094dc12e1a7eb92bf35)`()` 

Cleans up the subsystem, closes WebSocket connections, and releases resources.

#### `public void `[`SendAudioInputToAI`](#class_u_open_ai_api_subsystem_1aaa7121109a2ce6e5eea6009e260b9905)`(const FString & AudioChunkBase64)` 

Sends audio input data to the OpenAI API for processing. 
#### Parameters
* `AudioChunkBase64` - Base64-encoded audio chunk (PCM16 format, 24kHz mono).

#### `public void `[`CreateConversationItem`](#class_u_open_ai_api_subsystem_1a330bbf0a40f512e0fb6f11be93eec436)`(const TSharedPtr< FJsonObject > & ItemObject)` 

Creates a new conversation item in the OpenAI session. Used to inject messages, function call results, or other conversation elements. 
#### Parameters
* `ItemObject` - JSON object representing the conversation item.

#### `public void `[`UpdateSessionConfiguration`](#class_u_open_ai_api_subsystem_1abda828dc121262f71c3130080301ecc2)`(const TSharedPtr< FJsonObject > & SessionObject)` 

Updates the OpenAI session configuration. Can be used to change settings like tools, instructions, etc. 
#### Parameters
* `SessionObject` - JSON object containing the session configuration parameters.

#### `public void `[`SendRawWebSocketMessage`](#class_u_open_ai_api_subsystem_1aa55bf270cca8ca7325b9445176f3b0f4)`(const FString & PayloadString)` 

Sends a raw JSON message through the WebSocket connection. 
#### Parameters
* `PayloadString` - JSON string payload to send to the OpenAI API.

# class `UWebSocketSubsystem` 

```
class UWebSocketSubsystem
  : public UGameInstanceSubsystem
```  

[UWebSocketSubsystem](#class_u_web_socket_subsystem)

A game instance subsystem that manages WebSocket connections for real-time bidirectional communication with external services. This subsystem handles connection lifecycle, message sending/receiving, and error handling.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public FOnConnected `[`OnConnected`](#class_u_web_socket_subsystem_1a4a3b226fd80631beeb07ec717b51609e) | Delegate triggered when the WebSocket connection is successfully established.
`public FOnConnectionError `[`OnConnectionError`](#class_u_web_socket_subsystem_1a9cf4fa7b598d81b0bc4044029ff44e0d) | Delegate triggered when a connection error occurs. Provides the error message for debugging and user feedback.
`public FOnMessageReceived `[`OnMessageReceived`](#class_u_web_socket_subsystem_1a73ce4e6689c0c3e54c9db784dccefc67) | Delegate triggered when a message is received from the WebSocket server. Messages are provided as string data (typically JSON).
`public FOnClosed `[`OnClosed`](#class_u_web_socket_subsystem_1a5a37f49e91c94cd75594fec95612dcba) | Delegate triggered when the WebSocket connection is closed. Provides status code, reason, and whether the closure was clean.
`public virtual void `[`Initialize`](#class_u_web_socket_subsystem_1a7a2a93145e2e17cb5c2b7a3ff3dcc9a1)`(FSubsystemCollectionBase & Collection)` | Initializes the subsystem and sets up the WebSocket connection. 
`public virtual void `[`Deinitialize`](#class_u_web_socket_subsystem_1a8dd52f1106648ffec4345a4b62671ec9)`()` | Cleans up the subsystem, closes the WebSocket connection, and releases resources.
`public bool `[`IsConnected`](#class_u_web_socket_subsystem_1af0c510330d462257e3146dbbaa4588f3)`()` | Checks if the WebSocket is currently connected. 
`public void `[`SendMessage`](#class_u_web_socket_subsystem_1a24ced5cdbe6f2c05de3009e4034586d4)`(const FString & Message)` | Sends a message through the WebSocket connection. 

## Members

#### `public FOnConnected `[`OnConnected`](#class_u_web_socket_subsystem_1a4a3b226fd80631beeb07ec717b51609e) 

Delegate triggered when the WebSocket connection is successfully established.

#### `public FOnConnectionError `[`OnConnectionError`](#class_u_web_socket_subsystem_1a9cf4fa7b598d81b0bc4044029ff44e0d) 

Delegate triggered when a connection error occurs. Provides the error message for debugging and user feedback.

#### `public FOnMessageReceived `[`OnMessageReceived`](#class_u_web_socket_subsystem_1a73ce4e6689c0c3e54c9db784dccefc67) 

Delegate triggered when a message is received from the WebSocket server. Messages are provided as string data (typically JSON).

#### `public FOnClosed `[`OnClosed`](#class_u_web_socket_subsystem_1a5a37f49e91c94cd75594fec95612dcba) 

Delegate triggered when the WebSocket connection is closed. Provides status code, reason, and whether the closure was clean.

#### `public virtual void `[`Initialize`](#class_u_web_socket_subsystem_1a7a2a93145e2e17cb5c2b7a3ff3dcc9a1)`(FSubsystemCollectionBase & Collection)` 

Initializes the subsystem and sets up the WebSocket connection. 
#### Parameters
* `Collection` The collection of subsystems being initialized.

#### `public virtual void `[`Deinitialize`](#class_u_web_socket_subsystem_1a8dd52f1106648ffec4345a4b62671ec9)`()` 

Cleans up the subsystem, closes the WebSocket connection, and releases resources.

#### `public bool `[`IsConnected`](#class_u_web_socket_subsystem_1af0c510330d462257e3146dbbaa4588f3)`()` 

Checks if the WebSocket is currently connected. 
#### Returns
True if connected, false otherwise.

#### `public void `[`SendMessage`](#class_u_web_socket_subsystem_1a24ced5cdbe6f2c05de3009e4034586d4)`(const FString & Message)` 

Sends a message through the WebSocket connection. 
#### Parameters
* `Message` The message string to send (typically JSON).

Generated by [Moxygen](https://sourcey.com/moxygen)