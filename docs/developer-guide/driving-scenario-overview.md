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
