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

## WB_DrivingScenarioComplete

**Path:** `Content/Main/UI/Scenario/Driving/ScenarioEnd`

`WB_DrivingScenarioComplete` is the end-of-scenario completion widget shown after the player successfully finishes the driving experience. It serves as the scenario completion screen for **Scenario 2: Driving to a Job Interview** and provides the player with navigation options after the level ends.

### Main Role

This widget is responsible for:

- presenting the end-of-scenario completion message
- playing the completion text animations
- allowing the player to return to the main menu
- allowing the player to jump directly to other scenarios from the completion screen
- triggering the project save/completion system before loading the next level

### Widget Layout

The widget contains a centered completion panel that includes:

- a congratulatory/completion text header
- a short success message
- a **Return to Main Menu** button
- a **Load Morning Routine Scenario** button
- a **Load Grocery Run and Preparing Dinner Scenario** button

This makes the widget both a scenario-end screen and a navigation hub for moving to other available experiences.

### Construct Logic

On construct, the widget plays two animations on the completion text:

- a pop animation
- a pulsing animation

These are used to give the completion message more visual emphasis when the widget first appears.

### Button Behavior

Each button in the widget follows the same general flow:

1. call `Commit Scenario Completion`
2. wait briefly using a short delay
3. open the selected level

The current button destinations shown in the Blueprint are:

- **Return to Main Menu** → `MainMenu`
- **Load Morning Routine Scenario** → `House`
- **Load Grocery Run and Preparing Dinner Scenario** → `GroceryStore`

### Save System / Completion Tracking

Before loading a new level, the widget calls `Commit Scenario Completion`, which is part of the project’s save/completion system.

In the intended design, this call is meant to record that the player fully completed the driving scenario before transitioning away from the level. However, the save system itself was developed separately and is designed to support broader progress-saving behavior, including partial scenario progress. Verification of whether full driving scenario completion from this widget is currently being saved successfully end-to-end, including AWS-backed persistence, was not completed during development of this level.

For more detail on the project save system, refer to the dedicated save system documentation.

### Notes

This widget is specific to the end-state of the driving scenario and is not part of the general runtime HUD flow used during moment-to-moment gameplay. It is only shown once the scenario has been successfully completed.

### Active Use vs. Legacy Logic

`WB_Subtitles` is part of the active VR subtitle path used by the current driving scenario. While some legacy non-VR subtitle references still exist elsewhere in the scenario Blueprints, this widget is the active subtitle display used in the current implementation.

## DT_Objectives

**Path:** `Content/Main/UI/Scenario/Driving/ScenarioEnd`

`DT_Objectives` is the primary objective data table used by the driving scenario. It defines the ordered sequence of player tasks that make up the full drive from Mike’s house to the interview location.

### Main Role

This table is the main source of truth for objective progression in the level. It is used to determine:

- what the current objective is
- what text should be shown to the player
- the order in which objectives occur
- whether a dialogue line is linked to a given objective
- whether the car should pause for that objective
- what interaction hint text should be shown on the HUD

The table currently contains **23 objectives** representing the full sequence of interactions in the driving scenario.

### Key Fields

Each objective entry includes:

- `ObjectiveID`
- `ObjectiveText`
- `SequenceOrder`
- `IsCompleted`
- `LineID`
- `bPauseCar`
- `InteractionHintText`

At a high level:

- `ObjectiveID` is the unique identifier used to reference the objective in Blueprint logic
- `ObjectiveText` is the main instruction shown to the player
- `SequenceOrder` determines where the objective appears in the scenario progression
- `IsCompleted` stores objective completion state in the data format
- `LineID` links the objective to a dialogue line when applicable
- `bPauseCar` indicates whether the driving flow should stop for that objective
- `InteractionHintText` stores the more specific gameplay hint shown to help the player complete the task

### How It Is Used

`DT_Objectives` is used heavily by `BP_DialogueManager`, `BP_CarSplineController`, and the HUD widgets. It drives both objective display and scenario progression.

In practice, it supports:

- initial objective display
- ordered scenario progression
- mapping dialogue to objective state
- progress bar updates
- interaction hint updates
- pause/resume logic tied to scenario beats

Because the scenario is objective-driven, this table is one of the most important assets in the level.

## ST_ObjectiveData

**Path:** `Content/Main/UI/Scenario/Driving/ScenarioEnd`

`ST_ObjectiveData` is the structure used by `DT_Objectives`. It defines the data format for each objective entry in the driving scenario.

### Fields

Each entry in `ST_ObjectiveData` contains:

- `ObjectiveID`
- `ObjectiveText`
- `SequenceOrder`
- `IsCompleted`
- `LineID`
- `bPauseCar`
- `InteractionHintText`

### Purpose

This structure standardizes the objective data used throughout the driving scenario. It is the shared data format expected by the Blueprints and widgets that retrieve objective information from `DT_Objectives`.

At a high level, it provides the fields needed for:

- identifying the current objective
- displaying the player-facing objective text
- ordering scenario steps
- linking objectives to dialogue
- controlling whether the car pauses
- showing interaction hint text on the HUD

Because objective progression, HUD updates, and dialogue-to-objective linking all depend on the same data format, `ST_ObjectiveData` acts as the shared structure tying those systems together.

## WB_ControlsTutorial

**Path:** `Content/Main/UI/Scenario/Driving/ScenarioEnd`

`WB_ControlsTutorial` is the introductory tutorial widget shown at the start of the driving scenario. It introduces the player to the scenario context, explains the main VR controls, and allows the player to enable or disable subtitles and AI voice before gameplay begins.

### Main Role

This widget is responsible for:

- presenting the scenario introduction text
- explaining the core VR driving controls
- providing subtitle and AI voice toggle options
- passing those settings into `BP_DialogueManager`
- switching the HUD from tutorial mode into normal driving mode
- triggering the first objective of the scenario
- enabling the initial outside driver door interaction

### Widget Layout

The widget contains:

- scenario introduction text
- control instructions for right trigger, right grip, and left grip interactions
- a subtitle checkbox
- an AI voice checkbox
- a continue button

This makes it the player’s first in-scenario setup screen before actual driving objectives begin.

### Construct Logic

On construct, `WB_ControlsTutorial` finds and stores a reference to `BP_DialogueManager`. This reference is later used when the player presses Continue so the widget can pass the selected subtitle and AI voice settings into the active dialogue system.

### Continue Button Flow

When the Continue button is pressed, the widget:

1. checks that the stored `BP_DialogueManager` reference is valid
2. writes the subtitle checkbox value into the Dialogue Manager
3. writes the AI voice checkbox value into the Dialogue Manager
4. gets the current `BP_Driving_VRPawn` and unlocks its controls
5. switches `WB_DrivingHUD_Master` into driving mode
6. calls `ShowInstructionOnly` using the first objective (`OpenDriverDoor_Outside`)
7. gets the active `BP_CarFinal`
8. enables the outside driver door interaction
9. removes the tutorial widget from the screen

This means the tutorial widget does more than just explain controls. It also acts as the transition point from pre-scenario setup into active gameplay.

### Notes

`WB_ControlsTutorial` is part of the active VR startup flow for this scenario. It is not just informational UI; it also initializes the first live objective state and enables the first required interaction.

## WB_ObjectiveHUD

**Path:** `Content/Main/UI/Scenario/Driving/ScenarioEnd`

`WB_ObjectiveHUD` is the widget used to display the player’s current objective, objective progress, and interaction hint text during the driving scenario.

### Main Role

This widget is responsible for:

- displaying the current objective text
- displaying objective progress through the full scenario sequence
- displaying the current interaction hint text
- updating the objective progress bar
- handling fade-in and fade-out behavior for objective updates

It is one of the main runtime HUD widgets used during the active driving experience.

### Widget Layout

The widget contains:

- `ObjectiveText`
- `ObjectiveHintText`
- `ObjectiveProgressBar`

These elements are presented as a compact objective display rather than a full-screen instructional menu.

### UpdateObjectiveHUD

The main custom event in this widget is `UpdateObjectiveHUD`.

At a high level, this event:

1. updates the main objective text
2. updates the progress bar percent
3. formats and updates the instructional/progress text
4. checks whether the objective changed from the previously displayed objective
5. stores the most recent objective ID
6. plays the fade-in animation when appropriate

This event is the primary entry point used by `BP_DialogueManager` when objective information changes.

### Fade Handling

The widget also contains separate fade handling for objective transitions.

`PlayObjectiveFadeOut` is used to trigger the fade-out animation, while the construct logic binds to the end of that animation so the widget can reset its internal fading state once the fade-out completes.

This helps prevent repeated overlapping fade calls and keeps objective updates visually stable.

### Objective Formatting

The widget formats the player-facing progress display using the current objective number, total objectives, and interaction instruction text. This allows the HUD to show both the current task and how far through the scenario the player is.

### VR vs. Legacy Non-VR Logic

`WB_ObjectiveHUD` still contains a small amount of legacy non-VR logic, but the active implementation used by the current driving scenario is the VR HUD path. The widget is actively used as part of `WB_DrivingHUD_Master` during normal scenario gameplay.

### Notes

Because the scenario is highly objective-driven, `WB_ObjectiveHUD` is a key runtime widget. If future teams need to adjust how objectives are presented to the player, this is one of the main widgets they should inspect.

## Level Blueprint

The driving scenario’s **Level Blueprint** contains important setup and transition logic for the active VR implementation. Although the Level Blueprint still includes older non-VR and legacy prototype logic, the sections documented here focus only on the currently active logic used by the final scenario flow.

### Main Role

In the current implementation, the Level Blueprint is responsible for:

- handling initial level startup behavior
- spawning and possessing the driving VR pawn
- positioning the player correctly at the outside starting location
- applying the initial fade-in from the main menu transition
- listening for the event that transitions the player from outside the car to the seated in-car driving state
- moving and attaching the player pawn to the car when the player enters
- handling the fade-out / fade-in transition during the outside-to-inside car handoff

This means the Level Blueprint is not the main scenario logic controller, but it does handle several key one-time transitions that the rest of the level depends on.

### BeginPlay Startup Flow

On `BeginPlay`, the Level Blueprint runs an active sequence that performs the following setup:

1. creates and adds `WB_FadeScreen` to the viewport in order to complete the fade-in from the main menu redirect
2. spawns `BP_Driving_VRPawn`
3. possesses the spawned pawn with the player controller
4. uses the outside start anchor to snap the player into the correct starting position outside the car
5. sets the input mode for the player controller

Although a `PlayerStart` is still part of the flow, the active VR implementation relies on the outside start anchor and the pawn snap logic to place the player correctly from the headset/camera point of view.

### Outside Start Positioning

The active VR startup logic places the player outside the driver door using:

- the spawned `BP_Driving_VRPawn`
- the outside start anchor
- a short delay after possession
- `Snap To Outside Anchor`

This approach is used so that the player starts in the intended camera position regardless of headset offset or standing position at runtime.

### Outside-to-Inside Car Transition

The Level Blueprint also contains the active transition flow that runs once the player completes the outside door objective and needs to move into the seated in-car state.

At a high level, this flow:

1. waits for the relevant enter-car event to trigger
2. fades the camera to black
3. gets the current player pawn and casts it to `BP_Driving_VRPawn`
4. gets `BP_CarFinal`
5. gets the car’s `DriverCamera`
6. sets the VR pawn transform to the `DriverCamera` transform
7. attaches the VR pawn to the car actor
8. marks the car as driver-seated
9. calls `EnterCarSeat` on the VR pawn
10. fades the camera back in

This is the active handoff that transitions the player from the outside interaction phase into the seated driving phase while ensuring the pawn follows the car along the spline afterward.

### DriverCamera-Based Placement

For the seated in-car transition, the active logic uses the `DriverCamera` inside `BP_CarFinal` as the target position for the player. The pawn is first moved to that transform and then attached to the car so that the player and car move together during the driving portion of the scenario.

This means the car’s driver camera acts as the reference point for the player’s seated in-car placement.

### Fade Transitions

The Level Blueprint uses fade transitions to make the outside-to-inside handoff less abrupt.

The active flow includes:

- fade-out before repositioning and attachment
- a short delay during the transition
- fade-in after the player has been repositioned and attached

This helps hide the seat-transfer setup from the player and makes the transition feel more intentional.

### Legacy Logic

The Level Blueprint still contains additional older logic from earlier prototype and non-VR versions of the scenario. That legacy content is not part of the current active VR implementation documented here.

Future teams reviewing the Level Blueprint should be aware that not every section in that graph is still in use. The active sections are primarily the VR startup logic, fade screen initialization, player spawn/possess flow, and the outside-to-inside car transition sequence.

### Summary

In the current driving scenario, the Level Blueprint should be understood primarily as a **startup and transition controller**. It is responsible for:

- preparing the player’s initial VR spawn state
- completing the transition from main menu into the level
- moving the player into the car once the outside phase is complete
- attaching the seated player pawn to `BP_CarFinal`

It is not the main objective or dialogue controller, but it is essential to the player’s level entry flow and the shift from outside interaction into active driving.

## BP_Driving_VRPawn

**Path:** `Content/Main/UI/Scenario/Driving/Blueprints`

`BP_Driving_VRPawn` is the driving-specific VR pawn used in **Scenario 2: Driving to a Job Interview**. It is a child of the shared `VR_Pawn`, which is also used by the main menu and other parts of the project, but this child Blueprint adds the driving-specific hierarchy, input handling, interaction logic, and seated driving behavior required by this level.

### Main Role

This Blueprint is responsible for:

- setting up the driving-specific HUD references used by the scenario
- applying the input mapping contexts required for this level
- configuring tracking origin behavior for the driving experience
- handling the player’s seated in-car placement logic
- processing the VR input actions used for the driving interactions
- driving direct player interaction with the car controls
- updating the interaction state continuously during active grabs
- managing hand pose animation changes during trigger and grip interactions
- providing the HUD stabilization logic used during gameplay

This is one of the most important Blueprints in the level and serves as the main player interaction layer for the scenario.

### Relationship to the Parent `VR_Pawn`

`BP_Driving_VRPawn` is not a completely separate pawn implementation. It inherits from the project’s shared `VR_Pawn`, but overrides and extends that base pawn with logic specific to the driving scenario.

This allows the project to keep one common VR pawn foundation while still introducing scenario-specific behavior where needed.

### BeginPlay Responsibilities

On `BeginPlay`, the active logic in `BP_Driving_VRPawn` performs several setup tasks needed for the driving level.

At a high level, the Blueprint:

- initializes and stores the `DrivingHUD_Master` reference through `BP_HUDDisplay_Driving`
- passes that HUD reference into `BP_DialogueManager`
- sets the tracking origin to **Local Floor**
- applies the driving-specific input mapping context along with the hand input mapping context
- sets up the initial references used for outside door interaction
- prepares the inside-car interaction setup used later for the final objective
- begins the logic used to stabilize the HUD relative to the moving player/camera

These setup steps are specific to the driving scenario and are not part of the shared base pawn’s generic behavior.

### Tracking and Seated Placement

This Blueprint contains the driving-specific logic used to place the player correctly both outside the car and inside the driver seat.

For the seated in-car state, the Blueprint uses the `DriverCamera` in `BP_CarFinal` as the target reference and aligns the pawn’s transform so that the VR camera ends up at the intended seated driver position. This includes both rotation correction and location correction based on the difference between the pawn camera and the target seat camera.

This seated placement logic is used when the player transitions from the outside interaction phase into the in-car driving phase.

### Input Mapping Contexts

`BP_Driving_VRPawn` applies the scenario-specific input mapping context used by the level along with the hand mapping context.

The driving scenario uses:

- `IMC_Driving_DebugVR`
- `IMC_Hands`

Although the driving mapping context still contains `DebugVR` in its name, it is the active live mapping context used by the level.

### Interaction Model

The driving pawn processes most gameplay interaction through the scenario’s Enhanced Input actions, primarily using trigger and grip input from the right and left controllers.

Rather than relying on one generic interaction path, the Blueprint branches into interaction-specific behavior depending on:

- the current objective
- which hand is being used
- whether the player is grabbing a supported car control
- whether the relevant component can currently be grabbed or committed

This means the pawn acts as the direct player-side interaction layer, while the car Blueprint and the interaction interface handle the corresponding car-side behavior.

### Right Trigger Input

The right trigger input is used for interactions that behave more like pressing or confirming rather than continuously pulling/rotating.

From the current implementation, this includes:

- engine start interaction
- accepting the incoming phone call
- widget interaction with the scenario completion widget
- right-hand trigger pose animation updates

The Blueprint checks whether the currently targeted object implements the interaction interface and then calls the appropriate request functions as needed.

### Grip Input and Direct Manipulation

The grip inputs are used for direct manipulation of car controls.

At a high level, the pawn supports interaction with:

- outside driver door handle
- inside driver door handle
- seatbelt latch
- shift knob
- windshield wiper lever
- headlight lever
- turn signal lever

The Blueprint distinguishes between right-hand and left-hand interactions depending on the target control and the scenario’s intended motion pattern.

These interactions are generally handled in two phases:

1. grip press / grab begin
2. grip release / commit attempt

During the active grab, the pawn stores state such as whether the player is currently grabbing a given control and passes controller movement information into the relevant update logic.

### Event Tick Interaction Updates

A large portion of the pawn’s driving interaction behavior is updated continuously on `Event Tick`.

The active tick-based logic updates the current interaction state for controls that depend on hand movement over time, including:

- outside driver door pull
- inside driver door pull
- seatbelt pull
- shift knob movement
- windshield wiper lever movement
- turn signal lever movement
- headlight lever movement
- HUD stabilizer transform updates

This means the pawn is not only detecting input presses, but also continuously measuring controller movement during active interactions and passing those values into the car-side systems.

### Outside Driver Door Logic

For the first objective, `BP_Driving_VRPawn` contains the player-side handling for grabbing and pulling the outside driver door handle.

This includes:

- binding to the outside door grab component
- tracking when the right hand begins and ends the grab
- storing the initial grab hand location
- calculating pull distance and normalized pull alpha
- updating the outside door interaction through the relevant car-side logic
- resetting the interaction values when the grab is released

This is one of the most important early interaction paths because it begins the scenario and introduces the player to the control scheme.

### Inside Driver Door Logic

The pawn contains a similar but separate interaction path for the inside driver door used at the end of the scenario.

This logic mirrors the outside door pattern, but is tied to the final objective and the in-car phase of the level.

### Shift / Seatbelt / Lever Controls

For the seatbelt, shift knob, wipers, turn signal, and headlights, the pawn mainly acts as the hand/controller input side of the interaction.

It determines:

- whether the correct control can currently be grabbed
- whether the player is actively grabbing that control
- what the current controller position or rotation implies
- when to call the relevant notify/update/commit functions on the car or interaction interface

This keeps the pawn responsible for interpreting player hand motion while allowing the car-side Blueprints to apply the corresponding control state changes.

### Hand Animation Updates

`BP_Driving_VRPawn` also updates the VR hand animation state in response to trigger and grip input.

The Blueprint changes pose alpha and finger curl values for the hand animation blueprint so that the player’s hands visually react to:

- right trigger press/release
- right grip press/release
- left grip press/release

These animation adjustments improve the visual clarity of interactions, especially when the player is grabbing or pressing controls in the car.

### HUD Stabilizer

This Blueprint contains the active HUD stabilizer logic used during the driving scenario.

Rather than simply attaching the HUD directly and rigidly to the player view, the pawn updates the stabilizer transform with smoothing so the HUD remains readable while still following the player and camera during movement and interaction.

This is especially important in VR, where abrupt HUD motion can make the objective display difficult to read.

### Objective-Specific Behavior

A key feature of `BP_Driving_VRPawn` is that many interaction paths are tied directly to the active objective flow of the scenario.

This means the pawn does not expose every interaction at all times. Instead, interactions are effectively gated so the player can only perform the relevant car actions when the scenario expects them.

This objective-aware gating is one of the reasons the driving experience feels structured rather than fully freeform.

### Summary

`BP_Driving_VRPawn` should be understood as the driving scenario’s main **player interaction pawn**. It sits between the VR controllers and the rest of the scenario systems and is responsible for:

- scenario-specific player setup
- HUD hookup and stabilization
- input mapping
- seated placement
- grab and press detection
- direct manipulation tracking
- hand animation updates
- sending player interaction state into the rest of the driving systems

If future teams need to modify how the player interacts with the car, how the driving-specific input works, or how the HUD behaves during the scenario, `BP_Driving_VRPawn` is one of the first Blueprints they should inspect.


