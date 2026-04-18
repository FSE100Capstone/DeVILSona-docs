# Scenario 2: Driving to a Job Interview Overview and Blueprint Guide

## Overview

This document provides a developer-focused overview of **Scenario 2: Driving to a Job Interview**. It is intended to help future capstone teams understand the overall level structure, primary Blueprint files, supporting assets, and the flow of scenario-specific logic used in the driving experience.

Most scenario-specific content for this level is located under:

`Content/Main/UI/Scenario/Driving`

This is the main folder where the majority of the driving scenario’s files and supporting content are organized. Some additional assets used by the scenario come from external or imported asset packs, including Fab content and other imported folders such as `HousingPack02`.

This level is almost entirely **Blueprint-based** and is both **spline-driven** and **objective-driven**. The scenario contains **23 total objectives** that guide the player through Mike’s drive from his house to the interview location. Because of how the level flow and objective progression are currently implemented, the player cannot partially complete the level and later return to their last completion point.

This level also went through multiple earlier implementation stages before reaching its final VR form. It was originally developed as a **grey-box prototype**, and was later implemented entirely in **non-VR** using keyboard input. As a result, some remaining Blueprints and assets in the project are still tied to those earlier prototype or non-VR versions and are no longer part of the primary active gameplay flow.

## Opening the Level in Unreal Engine

To open the driving scenario level in Unreal Engine:

1. Navigate to `Content/Main/Maps`
2. Double-click the level named `DrivingToInterview`

This is the main level used for **Scenario 2: Driving to a Job Interview** and serves as the entry point for reviewing, testing, and modifying the scenario.

## Scope of This Guide

This guide documents the Blueprint architecture and core implementation for the driving scenario, including the major actors, level setup, scenario flow, interaction logic, and other supporting systems specific to this experience.

## Scenario Structure and Active Files

The primary active files used by this level are summarized below.

### Main Blueprints in Active Use

The main Blueprints currently in active use for this level are:

- `BP_CarFinal` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `BP_CarPath` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `BP_CarSplineController` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `BP_Driving_VRPawn` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `BP_HUDDisplay_Driving` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `BP_SceneWaypoint` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `BP_AI_InteractionDriver_Driving` — `Content/Main/UI/Scenario/Driving/ScriptedDialogue`
- `BP_DialogueManager` — `Content/Main/UI/Scenario/Driving/ScriptedDialogue`

### Enums

There are four enums used by the driving scenario:

- `E_DrivingHUDMode` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `E_HeadlightMode` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `E_ObjectivePhase` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `E_TurnSignalMode` — `Content/Main/UI/Scenario/Driving/Blueprints`

### Blueprint Interface

The primary Blueprint Interface used by this scenario is:

- `BPI_DrivingInteraction` — `Content/Main/UI/Scenario/Driving/Blueprints`

### Niagara Systems

Two Niagara systems are used for the rain effects in this level:

- `NS_Rain_CarAttached` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `NS_Rain_CarClose` — `Content/Main/UI/Scenario/Driving/Blueprints`

### Widgets

#### Master Widget

- `WB_DrivingHUD_Master` — `Content/Main/UI/Scenario/Driving/Blueprints`

#### Child or Supporting Widgets

- `WB_FadeScreen` — `Content/Main/UI/Scenario/Driving/Blueprints`
- `WB_DrivingScenarioComplete` — `Content/Main/UI/Scenario/Driving/ScenarioEnd`
- `WB_ControlsTutorial` — `Content/Main/UI/Scenario/Driving/ScenarioEnd`
- `WB_ObjectiveHUD` — `Content/Main/UI/Scenario/Driving/ScenarioEnd`
- `WB_Subtitles` — `Content/Main/UI/Scenario/Driving/ScriptedDialogue`

### Data Tables and Structures

The driving scenario uses the following Data Tables and Structures:

- `DT_DrivingDialogue` — `Content/Main/UI/Scenario/Driving/ScriptedDialogue`
- `ST_DrivingDialogue` — `Content/Main/UI/Scenario/Driving/ScriptedDialogue`
- `DT_Objectives` — `Content/Main/UI/Scenario/Driving/ScenarioEnd`
- `ST_ObjectiveData` — `Content/Main/UI/Scenario/Driving/ScenarioEnd`

### Level Blueprint Logic

The level also contains important logic inside the **Level Blueprint**, which is used as part of the scenario setup and runtime flow.

### Input Mapping Context

The driving scenario uses the input mapping context:

- `IMC_Driving_DebugVR` — `Content/Main/UI/Scenario/Driving/InputActions`

Although the name still includes `DebugVR`, this is the **active live input mapping context currently used in the level** for `BP_Driving_VRPawn`. The name was never updated after earlier development iterations, but it should be treated as the main input mapping context for the driving scenario in its current form.

This mapping context includes five active input actions implemented specifically for `BP_Driving_VRPawn`.

## BP_AI_InteractionDriver_Driving

**Path:** `Content/Main/UI/Scenario/Driving/ScriptedDialogue`

`BP_AI_InteractionDriver_Driving` is the scenario-specific Interviewee Actor used to convert scripted text input into spoken AI output during the driving level. It is derived from the shared `IntervieweeActor` class, but in this scenario it is configured for **scripted output rather than live back-and-forth conversation**.

At a high level, this actor is used when the driving scenario needs a spoken line to be played through the AI voice system. In the current implementation, it is configured with:

- a text-to-speech style prompt
- a selected voice option
- scripted input enabled
- forced audio responses enabled
- normal conversational input disabled

This allows the level to pass in text from the dialogue table and have it spoken back as audio without treating the driving scenario like an open-ended conversation system.

### Main Role in the Level

`BP_AI_InteractionDriver_Driving` is primarily used by `BP_DialogueManager` when a dialogue line needs to be played. Rather than storing prerecorded voice lines, the driving scenario sends text to this actor and uses the AI voice pipeline to generate the spoken output at runtime.

This actor is therefore responsible for the spoken delivery layer of the scenario’s scripted dialogue flow.

### Current Usage Notes

This Blueprint is configured specifically for the driving scenario’s scripted dialogue use case and should not be treated as a general-purpose conversational NPC. The actor is intended to speak lines provided by the scenario systems, not to handle unrestricted player conversation.

Because this Blueprint inherits from the shared `IntervieweeActor` implementation, some of the lower-level behavior comes from the parent C++ class rather than from extensive Blueprint graph logic inside this asset itself.

## BP_DialogueManager

**Path:** `Content/Main/UI/Scenario/Driving/ScriptedDialogue`

`BP_DialogueManager` acts as the main dialogue and HUD coordination layer for the driving scenario. It is responsible for connecting the scenario’s dialogue data, objective data, subtitle display, objective HUD updates, and scripted AI voice playback into one centralized Blueprint.

This Blueprint is one of the main control points for the scenario and should be treated as the manager for **what line should play**, **what subtitle should display**, and **what objective text should appear on the HUD**.

### BeginPlay Initialization

On `BeginPlay`, `BP_DialogueManager` performs a setup sequence to initialize the scenario’s HUD and dialogue references.

From the current implementation shown in the Blueprint:

- it waits briefly for the driving HUD to exist
- gets the active `BP_HUDDisplay_Driving` actor
- stores the `WB_DrivingHUD_Master` reference
- switches the master HUD to the controls tutorial mode
- stores references to key child widgets such as the objective HUD
- finds the active Interviewee Actor used for scripted AI voice playback
- stores that actor reference
- calls `InitializePersonaNative` once on the Interviewee Actor so the scripted voice system is ready before dialogue begins

This initialization step is important because `BP_DialogueManager` depends on both the HUD widget hierarchy and the AI Interaction Driver being valid before scenario dialogue starts.

### Main Responsibilities

The primary responsibilities of `BP_DialogueManager` are:

- retrieving dialogue lines from `DT_DrivingDialogue`
- retrieving objective data from `DT_Objectives`
- sending text to the Interviewee Actor for AI-spoken dialogue
- displaying subtitles in VR
- updating the current objective and progress HUD
- triggering sequences of dialogue associated with interaction tags

In practice, this Blueprint is the main bridge between the data tables and the player-facing UI/audio systems.

### PlayDialogueLine

`PlayDialogueLine` is the core event used to play an individual dialogue line based on its `LineID`.

At a high level, this event:

1. retrieves the dialogue entry by `LineID` from `DT_DrivingDialogue`
2. stores the current dialogue line
3. sends the line’s voice type and text to the Interviewee Actor
4. retrieves any objective linked to that same line
5. updates the current objective state if applicable
6. displays the corresponding subtitle in VR

This event therefore handles both the spoken line itself and the associated scenario/UI updates tied to that dialogue line.

### ShowInstructionOnly

`ShowInstructionOnly` is used when the scenario needs to update the player’s current objective/instruction without immediately playing a spoken dialogue line.

This event retrieves the objective from `DT_Objectives` using `ObjectiveID`, stores the current objective information, updates the current sequence order, and pushes the objective text/progress values into `WB_ObjectiveHUD`.

This is important for scenario beats where the player should first see the next task on the HUD before any dialogue is triggered.

### OnInteractionTriggered

`OnInteractionTriggered` is the custom event used to trigger dialogue based on a `TriggerTag` defined in `DT_DrivingDialogue`.

Rather than directly calling a single hardcoded line, this event searches the dialogue table for all rows associated with the provided trigger tag and then plays the matching lines. The current implementation supports sequential dialogue behavior for entries that share the same trigger tag, including the delayed playback flow shown in the Blueprint.

This is one of the key mechanisms used to connect player interactions and scenario state changes to dialogue playback.

### Data Lookup Functions

`BP_DialogueManager` also contains several helper functions for retrieving structured data from the scenario Data Tables.

#### GetDialogueLineByID

This function searches `DT_DrivingDialogue` using the `LineID` field rather than relying on the row name directly. It is used when the scenario logic already knows which `LineID` should be played.

#### GetObjectiveByObjectiveID

This function retrieves an objective from `DT_Objectives` based on the `ObjectiveID`. It is used for objective text and HUD updates tied directly to a known objective identifier.

#### GetObjectiveByLineID

This function retrieves an objective from `DT_Objectives` using the `LineID` field. This is useful when a dialogue line is linked to a specific objective and the scenario needs to derive the related objective entry from the dialogue being played.

### VR vs. Legacy Non-VR Logic

`BP_DialogueManager` still contains some logic left over from earlier non-VR implementations of the driving scenario. This includes nodes and references related to a non-VR subtitle/widget path that is no longer part of the active VR version.

That logic remains in the Blueprint as legacy implementation residue, but it is **not part of the current active scenario flow**. The active version of the level uses the VR HUD and subtitle widget path through `WB_DrivingHUD_Master`.

### Summary

In the current driving scenario, `BP_DialogueManager` should be understood as the central manager for:

- dialogue lookup
- subtitle display
- objective lookup
- objective HUD updates
- interaction-triggered dialogue sequencing
- communication with the AI Interaction Driver for spoken output

If future teams need to modify how dialogue is selected, how subtitles are shown, or how the objective HUD is updated in response to scenario progression, `BP_DialogueManager` is one of the first Blueprints they should inspect.

## DT_DrivingDialogue

**Path:** `Content/Main/UI/Scenario/Driving/ScriptedDialogue`

`DT_DrivingDialogue` is the primary dialogue data table used by the driving scenario. It stores the scripted spoken lines that can be triggered during the level and serves as the main dialogue source for `BP_DialogueManager`.

Each row represents a single dialogue entry and includes the fields defined by `ST_DrivingDialogue`.

### Main Purpose

This data table is used to define:

- the unique line identifier for a dialogue entry
- who is speaking
- what trigger tag should activate that line
- what subtitle text should be displayed
- which voice type should be used for spoken playback

This allows the driving scenario to remain largely data-driven rather than hardcoding dialogue text directly into Blueprint logic.

### Current Fields

Based on the current structure, each row includes:

- `LineID`
- `Speaker`
- `TriggerTag`
- `SubtitleText`
- `VoiceType`

### How It Is Used

`BP_DialogueManager` uses `DT_DrivingDialogue` in several different ways depending on the scenario flow:

- `GetDialogueLineByID` searches the table using `LineID`
- `PlayDialogueLine` retrieves a specific dialogue entry and uses it to drive subtitles, voice type selection, and spoken output
- `OnInteractionTriggered` searches for entries associated with a matching `TriggerTag`

This means the same data table supports both:

- direct line lookup by a known ID
- grouped or sequential playback tied to interaction tags

### Practical Notes

The table currently includes lines for:

- Mike’s internal driving dialogue
- hands-free phone call dialogue
- arrival/interviewer dialogue

Because voice type is stored per row, this table also determines which AI voice/persona configuration should be used for a given spoken line.

## ST_DrivingDialogue

**Path:** `Content/Main/UI/Scenario/Driving/ScriptedDialogue`

`ST_DrivingDialogue` is the structure used by `DT_DrivingDialogue`. It defines the format of each dialogue entry used by the driving scenario.

### Fields

Each entry in `ST_DrivingDialogue` contains the following fields:

- `LineID`
- `Speaker`
- `TriggerTag`
- `SubtitleText`
- `VoiceType`

### Purpose

This structure is used to standardize how dialogue lines are stored and retrieved throughout the scenario. It provides the data format that `BP_DialogueManager` expects when pulling rows from `DT_DrivingDialogue`.

At a high level, the fields serve the following purposes:

- `LineID` uniquely identifies a dialogue line for direct lookup
- `Speaker` identifies who is delivering the line
- `TriggerTag` groups lines by interaction or event trigger
- `SubtitleText` stores the text shown to the player and also used for scripted spoken output
- `VoiceType` determines which AI voice/persona configuration should be used when that line is spoken

Because both subtitle display and scripted audio playback depend on this same structure, `ST_DrivingDialogue` acts as the shared data format tying those systems together.

## WB_Subtitles

**Path:** `Content/Main/UI/Scenario/Driving/ScriptedDialogue`

`WB_Subtitles` is the widget used to display subtitle text during the driving scenario. In the active VR implementation, it is the main subtitle presentation layer connected to `BP_DialogueManager` through `WB_DrivingHUD_Master`.

### Main Role

This widget is responsible for:

- receiving subtitle text when a dialogue line is played
- updating the displayed subtitle text
- handling the subtitle fade animation behavior
- preventing visual flicker during rapid sequential subtitle updates

### DisplaySubtitle

The main custom event in this widget is `DisplaySubtitle`.

At a high level, this event:

1. receives subtitle text as input
2. updates the text widget content
3. marks the subtitle as active
4. plays the fade animation
5. clears the active state again once the fade animation has finished

This event is used by `BP_DialogueManager` whenever a new spoken line needs to be shown to the player.

### Sequential Phone Call Handling

`WB_Subtitles` also contains special handling for the sequential hands-free phone call lines in the driving scenario.

Because the phone conversation lines occur in quick succession, this widget includes logic to prevent each new subtitle from waiting on a full fade-out/fade-in cycle before the next line appears. This avoids subtitle flicker and makes the phone call sequence display more smoothly when multiple lines are triggered close together.

This special handling is specific to those phone call dialogue entries and was added to support the pacing of that sequence.

### Widget Layout

The widget itself is very simple. It contains:

- a `Canvas Panel`
- a `Border`
- a `SubtitleText` text element

The `SubtitleText` element is the primary text field updated during runtime. The widget is positioned and styled to serve as an in-HUD subtitle display rather than a full-screen dialogue panel.

### Active Use vs. Legacy Logic

`WB_Subtitles` is part of the active VR subtitle path used by the current driving scenario. While some legacy non-VR subtitle references still exist elsewhere in the scenario Blueprints, this widget is the active subtitle display used in the current implementation.
