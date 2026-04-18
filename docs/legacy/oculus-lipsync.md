# MetaHuman Lip Sync Setup (OVRLipSync)

## Overview

This system enables real-time lip synchronization for MetaHuman characters using the Oculus **OVRLipSync** plugin.

OVRLipSync analyzes incoming audio waveform data (PCM samples) and converts it into **viseme weights**.  
These viseme weights represent the probability that a specific mouth shape is being spoken at a given moment.

The system works in the following stages:

1. Audio Input  
2. OVRLipSync phoneme analysis  
3. Viseme weights returned  
4. Animation Blueprint processing  
5. ModifyCurve node applies curves  
6. RigLogic evaluates facial deformation

The result is **real-time MetaHuman mouth animation synchronized to speech audio**.

---

# What Are Visemes?

A **viseme** represents the visual mouth shape associated with one or more phonemes.

Example groupings:

| Phoneme | Viseme | Example |
|---|---|---|
P/B/M | PP | pop |
F/V | FF | five |
TH | TH | think |
D/T/N | DD | dog |
A | AA | father |

OVRLipSync outputs **15 values**:

| Index | Viseme |
|---|---|
0 | Silence |
1 | PP |
2 | FF |
3 | TH |
4 | DD |
5 | KK |
6 | CH |
7 | SS |
8 | NN |
9 | RR |
10 | AA |
11 | E |
12 | IH |
13 | OH |
14 | OU |

---

# Requirements

- Unreal Engine **5.6+**
- Windows only

⚠️ The Oculus LipSync plugin **does not function on macOS**.

---

# Plugin Installation

Download:

https://github.com/Shiyatzu/OculusLipsyncPlugin-UE5

Copy only:

```
OVRLipSync
```

into:

```
ProjectRoot/Plugins/
```

---

# UE5.6 Compatibility Fixes

## Fix include

Change:

```cpp
#include "Voice/Public/VoiceModule.h"
```

to

```cpp
#include "VoiceModule.h"
```

---

## Add dependency

Edit:

```
OVRLipSync.Build.cs
```

Add:

```cpp
"Voice"
```

---

## Fix decompression type

Change:

```cpp
SoundWave->DecompressionType = DTYPE_RealTime;
```

to

```cpp
SoundWave->DecompressionType = EDecompressionType::DTYPE_RealTime;
```

---

# Project Code Integration

Lip sync logic is implemented in:

```
IntervieweeActor.h
IntervieweeActor.cpp
```

These handle:

- audio streaming
- PCM buffering
- viseme extraction
- loudness calculation
- blueprint access

---

# OVRLipSync Streaming Architecture

OpenAI responses are streamed as **small base64 encoded audio packets ("audio deltas")**.

These packets arrive **faster than the audio actually plays** through the Unreal `SoundWaveProcedural`.

If lip sync were calculated only when packets arrive, the following problem occurs:

- streaming packets stop arriving once the full response is received
- however the SoundWave still contains **buffered audio that continues playing**
- lip sync processing stops early
- the character’s mouth stops moving while the audio is still playing

This is why the system separates responsibilities into **two functions**:

| Function | Responsibility |
|--------|--------|
HandleAudioDeltaReceived | receives and stores streamed audio packets |
ProcessLipSyncFrames | continuously analyzes buffered audio for lip sync |

Instead of processing lip sync immediately when packets arrive, decoded PCM samples are stored in a persistent buffer:

```
PlaybackPCMBuffer
```

A repeating timer then calls `ProcessLipSyncFrames()` every **10 milliseconds** to analyze audio frames while playback continues.

This ensures lip sync continues **even after streaming packets stop arriving**.

---

# BeginPlay()

BeginPlay initializes the lip sync system.

### Create OVRLipSync context

```cpp
LipSyncContext = MakeShared<UOVRLipSyncContextWrapper>(
 ovrLipSyncContextProvider_Enhanced,
 24000,
 4096
);
```

Parameters:

| Parameter | Meaning |
|---|---|
Enhanced | higher accuracy phoneme detection |
24000 | audio sample rate |
4096 | internal buffer |

---

### Initialize viseme array

```cpp
CurrentVisemes.SetNum(15);
```

OVRLipSync outputs **15 viseme values** representing detected mouth shapes.

---

### Create procedural sound wave

```cpp
AIResponseSoundWave = NewObject<USoundWaveProcedural>();
```

This sound wave is used to **play streamed AI speech audio in real time**.

---

# HandleAudioDeltaReceived()

This function runs whenever OpenAI sends a new **audio delta packet**.

The audio arrives as **base64 encoded PCM samples**.

### Responsibilities

This function handles **stream processing and buffering**, but does **not perform lip sync analysis**.

---

### Decode base64

```cpp
FBase64::Decode(AudioDelta, AudioData);
```

Converts the base64 audio packet into raw audio bytes.

---

### Queue audio for playback

```cpp
AIResponseSoundWave->QueueAudio(AudioData.GetData(), AudioData.Num());
```

This sends the decoded audio to the procedural SoundWave so it can play through the character's dialogue audio component.

---

### Convert to PCM

```cpp
int16* PCM = reinterpret_cast<int16*>(AudioData.GetData());
```

The raw audio bytes are interpreted as **16-bit PCM samples**, which is the format required by OVRLipSync.

---

### Append to playback buffer

```cpp
PlaybackPCMBuffer.Append(PCM, SampleCount);
```

PCM samples are stored in a persistent buffer so they can be analyzed later.

This buffer accumulates streaming audio packets and acts as the **source for lip sync frame processing**.

---

### Compute loudness

```
Loudness = sqrt(sum(sample²) / sampleCount)
```

The loudness value is normalized to **0–1** and is used later by the animation blueprint to scale **jaw-driven visemes**.

---

### Start lip sync timer

Once audio begins streaming, a timer is started that repeatedly calls:

```
ProcessLipSyncFrames()
```

every **10ms**.

This timer ensures lip sync processing continues **while buffered audio is still playing**.

### Timer Lifecycle

The lip sync timer is only started once per response:

```cpp
if (!GetWorldTimerManager().IsTimerActive(LipSyncTimerHandle))
```

This ensures:

- only one timer runs at a time
- no duplicate frame processing occurs
- lip sync remains stable and consistent

---

# ProcessLipSyncFrames()

Unlike `HandleAudioDeltaReceived`, this function is responsible for **actual lip sync analysis**.

It is called repeatedly by a timer every **10 milliseconds**.

---

### Frame size

OVRLipSync expects fixed-size audio frames.

At the project's **24kHz sample rate**, one frame equals:

```
240 samples = 10ms of audio
```

---

### Extract frame from buffer

The function checks whether the playback buffer contains at least **240 samples**.

If so, one frame is extracted from the buffer.

---

### Send frame to OVRLipSync

```cpp
LipSyncContext->ProcessFrame(...)
```

OVRLipSync analyzes the audio frame and returns **viseme weights**.

These values represent the probability of different mouth shapes being spoken.

---

### Update CurrentVisemes

The viseme values returned from `ProcessFrame()` are stored in:

```
CurrentVisemes
```

This array is later accessed by the **MetaHuman animation blueprint**.

---

### Remove processed samples

After analysis, the processed samples are removed from `PlaybackPCMBuffer`.

This keeps the buffer aligned with the current playback position.

---

# Why Two Functions Are Required

Without separating these responsibilities, lip sync would fail during streaming playback.

```
HandleAudioDeltaReceived()
```

handles **incoming audio packets**.

```
ProcessLipSyncFrames()
```

handles **continuous lip sync analysis**.

Because audio playback continues after packets stop arriving, the timer-driven frame analysis ensures the character's mouth continues moving until the sound finishes playing.

---

# HandleAudioFinished()

This function runs when the procedural sound wave finishes playing.

At this point the system:

1. Stops the lip sync processing timer
2. Clears any remaining PCM samples from the playback buffer
3. Broadcasts that the AI response has finished speaking

Stopping the timer prevents lip sync processing from continuing after playback ends.

## Enhanced Audio Completion Handling

In addition to stopping lip sync processing, this function performs full system cleanup to ensure a clean transition back to idle.

### Additional Responsibilities

- Clears buffered PCM audio:
```cpp
PlaybackPCMBuffer.Empty();
```

- Resets viseme values to neutral:
```cpp
for (float& Value : CurrentVisemes) {
    Value = 0.0f;
}
```

- Resets loudness:
```cpp
CurrentVisemeLoudness = 0.0f;
```

- Clears subtitles:
```cpp
SubtitleText = "";
OnSubtitleUpdated.Broadcast(SubtitleText);
```

- Restarts microphone capture:
```cpp
AudioInputSubsystem->StartCapturing();
```

- Updates response state:
```cpp
RequestInProgress = false;
ResponseFullyCompleted = true;
```

- Broadcasts talking stopped:
```cpp
OnTalkingStopped.Broadcast();
```

### Result

This ensures:

- the face returns to a neutral pose
- no residual animation persists
- the system is ready for the next interaction

## Talking State Detection (C++)

The system determines whether the AI is actively speaking based on the presence of streamed audio data.

```cpp
bool bHasAudioData = AIResponseSoundWave->GetAvailableAudioByteCount() > 0;
```

A delay is applied to ensure stable completion detection:

```cpp
if (TimeSinceLastAudio > 1.0f)
```

### Purpose

This prevents:

- early cutoff due to streaming gaps
- jitter between talking and idle states
- incorrect animation transitions

---

# Animation Blueprint

Animation Blueprint used:

```
MetaHumans/Common/Face/ABP_Face_PostProcess
```
## Microphone Capture Control

To prevent feedback loops and unintended responses, microphone capture is explicitly controlled during AI playback.

### When AI Starts Speaking

```cpp
AudioInputSubsystem->StopCapturing();
```

### When AI Finishes Speaking

```cpp
AudioInputSubsystem->StartCapturing();
```

### Importance

This prevents:

- the AI from hearing its own output
- recursive responses
- duplicate or unintended dialogue triggers

---

# AnimGraph Setup

Add a **ModifyCurve node** immediately before:

```
AnimNode_RigLogic
```

Settings:

| Setting | Value |
|---|---|
Apply Mode | Add |
Alpha | 1.0 |
Curve Map | LipSyncCurves |

This node applies the curve values generated in the EventGraph.

---

# Event Graph

Two events control the runtime behavior.

---

# EventBlueprintInitializeAnimation

Purpose: cache a reference to the IntervieweeActor.

Steps:

1. Event fires on animation initialization.
2. Get Owning Actor
3. Get Parent Actor
4. Cast To IntervieweeActor
5. Store reference in:

```
IntervieweeActorRef
```

---

# EventBlueprintUpdateAnimation

Runs every animation frame and drives the facial animation curves used by the ModifyCurve node.

---

## Step 1 — Validate Actor Reference

The blueprint first verifies that the cached IntervieweeActor reference is valid.

```
IsValid(IntervieweeActorRef)
```

If the reference is invalid, the blueprint attempts to cast the owning actor again.

---

## Step 2 — Retrieve Viseme Array

The animation blueprint retrieves the current viseme weights from C++.

```
GetCurrentVisemes()
```

This returns the **15 element viseme array** generated by OVRLipSync.

Each element corresponds to a viseme index.

Index **0** represents silence and is ignored.

---

## Step 3 — Retrieve Loudness

Loudness is retrieved separately from the IntervieweeActor.

```
GetCurrentLoudness()
```

The returned value is stored in:

```
CurrentLoudness
```

This value represents the **normalized RMS loudness of the audio frame (0-1)**.

Loudness is used to amplify visemes that primarily drive **jaw opening**.

---

## Step 4 — Store Viseme Values

Each viseme index is stored in local animation blueprint variables.

```
VisemePP
VisemeFF
VisemeTH
VisemeDD
VisemeKK
VisemeCH
VisemeSS
VisemeNN
VisemeRR
VisemeAA
VisemeE
VisemeIH
VisemeOH
VisemeOU
```

---

## Step 5 — Apply Multipliers

The raw viseme values returned by OVRLipSync are very small, so multipliers are applied.

```
AmplifiedValue = VisemeValue * Multiplier
```

---

## Step 6 — Loudness Driven Visemes

The following visemes also multiply by loudness because they primarily control **jaw opening**:

```
AA
KK
NN
IH
DD
```

Formula used:

```
AmplifiedValue = Multiplier * CurrentLoudness * VisemeValue
```

---

## Step 7 — Clamp

All values are clamped to prevent curve values exceeding valid ranges.

```
Clamp(0,1)
```

---

## Step 8 — Apply FInterpTo Smoothing

The clamped values are smoothed using **FInterpTo**.

This prevents jitter between animation frames and produces smoother lip motion.

### Dynamic Interpolation Based on Talking State

Interpolation speed is not constant and is now driven by the character's talking state (`IsTalking`).

When `IsTalking = true`:

- Higher interpolation speeds are used
- Visemes respond quickly to incoming audio
- Produces responsive lip sync

When `IsTalking = false`:

- Lower interpolation speeds are used
- Visemes gradually return to neutral
- Prevents the mouth from freezing in a partially open shape after speech ends

This is implemented using Select Float nodes that switch interpolation speed values based on `IsTalking`.

### Post-Speech Viseme Decay (Return to Neutral)

A common issue in real-time lip sync systems is that the mouth can remain partially open after audio playback ends.

To solve this, an additional decay system is applied when the character is no longer speaking.

### Implementation

- The `IsTalking` boolean is used to determine whether speech is active
- When `IsTalking` becomes false:
  - Target viseme values effectively decay toward 0
  - Interpolation speeds are reduced
  - This creates a smooth return to the neutral facial pose

### Blueprint Logic

This behavior is implemented using:

- Select Float nodes for dynamic interpolation speed
- Conditional targets that reduce viseme intensity when not talking
- FInterpTo smoothing applied every frame

### Result

- No frozen mouth shapes after speech
- Natural relaxation of facial animation
- Improved realism between dialogue segments

---

## Step 9 — Clear Curve Map

Before writing new values the map used by the ModifyCurve node is cleared.

```
LipSyncCurves.Clear()
```

---

## Step 10 — Add Curve Values To Map

Smoothed viseme values are added to the map:

```
LipSyncCurves.Add()
```

Each viseme may drive one or more MetaHuman facial curves.
---

# Curve Mappings

Based on the blueprint implementation.

| Viseme | Curves |
|---|---|
PP | CTRL_expressions_mouthLipsTogetherUL / UR / DL / DR |
FF | CTRL_expressions_mouthLowerLipBiteL / R |
TH | CTRL_expressions_tongueTipUp |
DD | CTRL_expressions_jawOpen |
KK | CTRL_expressions_jawOpen |
CH | CTRL_expressions_mouthFunnelUL / UR / DL / DR |
SS | CTRL_expressions_mouthLowerLipTowardsTeethL / R + CTRL_expressions_mouthUpperLipTowardsTeethL / R |
NN | CTRL_expressions_jawOpen |
RR | CTRL_expressions_mouthFunnelUL / UR / DL / DR |
AA | CTRL_expressions_jawOpen |
E | CTRL_expressions_mouthStretchL / R |
IH | CTRL_expressions_jawOpen |
OH | CTRL_expressions_mouthLipFunnelUL / UR / DL / DR |
OU | CTRL_expressions_mouthLipPurseUL / UR / DL / DR |

---

# Viseme Multipliers

| Viseme | Multiplier |
|---|---|
PP | 2.5 |
FF | 6.0 |
TH | 4.0 |
DD | 4.0 |
KK | 2.6 |
CH | 2.4 |
SS | 1.8 |
NN | 2.5 |
RR | 2.0 |
AA | 15.0 |
E | 2.3 |
IH | 4.0 |
OH | 2.0 |
OU | 2.5 |

---

# FInterpTo Smoothing Speeds (Talking State)

| Viseme | Speed |
|---|---|
PP | 21 |
FF | 19 |
TH | 19 |
DD | 21 |
KK | 21 |
CH | 19 |
SS | 23 |
NN | 19 |
RR | 17 |
AA | 17 |
E | 17 |
IH | 17 |
OH | 19 |
OU | 19 |

### Idle (Not Talking) Speeds

When `IsTalking` is false, lower interpolation speeds are used to allow visemes to decay smoothly:

Example:

- Talking speeds: 17–23
- Idle speeds: 0–5 (or near zero depending on desired decay rate)

These values are selected dynamically in the Animation Blueprint using Select Float nodes.

---

# Important Notes About Curve Names

Only curves beginning with:

```
CTRL_expressions_
```

should be used.

Examples:

```
CTRL_expressions_jawOpen
CTRL_expressions_mouthStretchL
CTRL_expressions_mouthStretchR
CTRL_expressions_mouthFunnelUL
CTRL_expressions_mouthFunnelUR
```

Using curves such as:

```
MouthClose
MouthPucker
```

will **not correctly drive MetaHuman facial deformation**.

---

# Finding Curve Names

To locate valid curves:

1. Open the **AnimGraph**
2. Right-click the **ModifyCurve node**
3. Select **Add Curve Pin**
4. Search for curves beginning with:

```
CTRL_expressions
```

When adding curves to the **LipSyncCurves map**, the names must **match the ModifyCurve pin names exactly**.

---

# Related Files

```
IntervieweeActor.cpp
IntervieweeActor.h
MetaHumans/Common/Face/ABP_Face_PostProcess
```