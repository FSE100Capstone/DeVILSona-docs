# 🎮 VR Project Save System Documentation

This document describes the **Save System architecture** used in the VR Capstone project.  
The system is built using **Unreal Engine 5**, and its core components include:

- `VRGameMode`
- `BP_GameInstance`
- `SG_LocalGameSetting` (local save)
- `SG_SaveData` (per-user save)
- Login / Save UI widgets


---

# Overall Flow

When the game starts:

1. **VRGameMode** is the first blueprint to run.
2. Inside `BeginPlay`, VRGameMode:
   - Casts to **BP_GameInstance**
   - Calls initialization logic in GameInstance
   - Loads the last used user ID (`LastUserID`) from `SG_LocalGameSetting`
   - Automatically loads the correct `SG_SaveData`
3. During gameplay:
   - Scenario progress is managed through functions in **BP_GameInstance**
   - Progress is written into `SG_SaveData`

---

# Save File Types

The system uses **two SaveGame files**:

- `SG_LocalGameSetting`
- `SG_SaveData`

---

## SG_LocalGameSetting

`SG_LocalGameSetting` stores local settings related to the last used save.

### Stored Field

| Field | Type | Description |
|-------|-------|-------------|
| `LastUserID` | STRING | Stored in the format `"UserID_SessionID"` |

### LastUserID Format


### Examples

- `123456_0001`
- `842193_0002`
- `554400_0010`

### Purpose

- During game startup, `LastUserID` is loaded.
- The Login UI automatically parses this string and fills:
  - **ASUID** → extracted before the underscore
  - **SessionID** → extracted after the underscore
- This allows the player to **continue immediately** without retyping their ID.

---

## SG_SaveData

Each **UserID + SessionID** combination generates a unique save file.

### Fields

| Field | Type | Description |
|--------|--------|------------|
| `ASUID` | INT | Student/user ID |
| `StudentName` | STRING | Player name |
| `SessionID` | INT | The session (save slot) number |
| `ScenarioProgress` | Array of Struct | Stores progress for all scenarios |

### ScenarioProgress Struct

| Field | Type | Description |
|--------|----------|-------------|
| `CharacterName` | STRING | Scenario character |
| `ScenarioNumber` | INT | Scenario ID number |
| `Progress` | FLOAT | Scenario progress value |
| `LastSaveTime` | STRING / DateTime | Timestamp of the last save |

---

# BP_GameInstance Functions

`BP_GameInstance` serves as the central controller for save management.

---

## Initial()

Executed during `VRGameMode → BeginPlay`.

### Responsibilities

- Load or create `SG_LocalGameSetting`
- Read `LastUserID`
- Automatically load the corresponding `SG_SaveData`
- Prepare the login screen with auto-filled values

---

## Login(ASUID, StudentName, SessionID)

Triggered by the **Login UI**.

### Login Flow

1. The user enters:
   - **ASUID**
   - **SessionID**
2. User presses **Login**.
3. The system checks if a save file exists:
   - **If save exists** → Load `SG_SaveData`
   - **If no save exists** → Show a warning popup:
     - “No save data found for this ID and Session. Please create a new save.”

---

### New Save Flow

- User presses **New Save**.
- `WB_Save_New` widget appears.
- User enters:
  - **ASUID**
  - **StudentName**
  - **SessionID**
- Upon pressing **Create**:
  - A new `SG_SaveData` is generated.
  - `SG_LocalGameSetting.LastUserID` is updated to:

ASUID + "_" + SessionID

  - The new save file is loaded and the game continues.

---

# Save / Load UI Widgets

Two widgets support the login and save creation process.

---

## WB_Save_Main

- Displays existing save sessions
- Automatically fills fields using `LastUserID`
- Allows user to:
  - Continue an existing save
  - Open the **New Save** creation window

---

## WB_Save_New

Used to create a **brand-new save file**.

### User Inputs

- ASUID  
- StudentName  
- SessionID  

### Features

- VR **Virtual Keyboard** support  
- Default `SessionID` = `0001`  
- Generates a new save file and updates `SG_LocalGameSetting`

---

# SessionID Policy

A single user can create multiple independent save files using different SessionIDs.

### Example

| ASUID | SessionID | Meaning |
|--------|------------|---------|
| 123456 | 0001 | Practice session |
| 123456 | 0002 | Assessment session |
| 987654 | 0001 | Another user |

### Important

If the user forgets their SessionID, the save file **cannot be recovered** through normal gameplay.  
They must write it down or remember it.

---

# Map Transition Behavior

When changing maps:

1. `BP_GameInstance` retains current ASUID + SessionID
2. New map's GameMode casts to `BP_GameInstance`
3. Scenario progress is retrieved with `GetScenarioProgress()`
4. Spawn, UI, and skipped sequences depend on progress

---

# Future Improvements (Optional)

- Auto-save checkpoints  
- Administrator session recovery tools  
- Save sorting and tagging  
- Cloud or server-side save backups  

---

# End of Document

