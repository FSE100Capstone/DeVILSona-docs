
# 🚀 Unreal Engine – AWS Server-Based Save & Login System Guide

This document explains how to integrate Unreal Engine with AWS (Lambda + API Gateway + DynamoDB) to:

1. Save student session data on a remote AWS server
2. Load existing session data when a student logs in
3. Support multiple scenarios per character (returned as arrays)
4. Verify the full pipeline from Unreal → AWS → DynamoDB → Unreal

---

# 📌 Overview

We expanded the original local TXT/JSON save system to support:

* Server-side session storage
* Login-based data retrieval
* Multiple rows per student (scenario-based saves)
* Blueprint-accessible output data
* Fully asynchronous HTTP communication inside Unreal

---

# 🛠 Architecture

```
Unreal C++ → API Gateway → Lambda (Node.js) → DynamoDB
                  ↑                ↓
             Login / Save     Query / Update
```

---

# ️⃣ DynamoDB Setup

### 📌 Create DynamoDB Table

* **Table Name:** `StudentSessions`
* **Primary Key Schema:**

  * Partition Key: `StudentID` (Number)
  * Sort Key: `SessionKey` (String)

### 📌 SessionKey Format (Important)

```
SessionID#CharacterName#ScenarioNumber

Examples:
0001#Mike#1
0001#Mike#2
```

This structure allows storing **multiple scenarios** and **multiple characters** under the same student and session.

### 📌 Example Item

```json
{
  "StudentID": 3,
  "SessionKey": "0001#Mike#1",
  "StudentName": "Namett",
  "SessionID": "0001",
  "ScenarioCharacterName": "Mike",
  "ScenarioNumber": 1,
  "Progress": 0,
  "CompletionTime": "2025-11-16 10:39:32"
}
```

---

# ️⃣ Lambda Functions (Node.js 20)

## 📌 2-1. Save API (`POST /session`)

Stores session data in DynamoDB.

### Code

```js
const AWS = require("aws-sdk");
const ddb = new AWS.DynamoDB();

exports.handler = async (event) => {
  const body = JSON.parse(event.body);

  const {
    StudentID,
    StudentName,
    SessionID,
    ScenarioCharacterName,
    ScenarioNumber,
    Progress,
    CompletionTime
  } = body;

  const SessionKey = `${SessionID}#${ScenarioCharacterName}#${ScenarioNumber}`;

  const params = {
    TableName: "StudentSessions",
    Item: {
      StudentID: { N: String(StudentID) },
      SessionKey: { S: SessionKey },
      StudentName: { S: StudentName },
      SessionID: { S: SessionID },
      ScenarioCharacterName: { S: ScenarioCharacterName },
      ScenarioNumber: { N: String(ScenarioNumber) },
      Progress: { N: String(Progress) },
      CompletionTime: { S: CompletionTime }
    }
  };

  try {
    await ddb.putItem(params).promise();
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ok: true,
        message: "Session stored in DynamoDB",
        sessionKey: SessionKey
      })
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal error", error: err })
    };
  }
};
```

---

## 📌 2-2. Login API (`POST /login`)

Queries all scenario saves for a given StudentID + SessionID prefix.

### Code

```js
const AWS = require("aws-sdk");
const ddb = new AWS.DynamoDB();

exports.handler = async (event) => {
  const body = JSON.parse(event.body);

  const StudentID = Number(body.StudentID);
  const SessionID = String(body.SessionID);
  const prefix = `${SessionID}#`;

  const params = {
    TableName: "StudentSessions",
    KeyConditionExpression:
      "StudentID = :sid AND begins_with(SessionKey, :prefix)",
    ExpressionAttributeValues: {
      ":sid": { N: String(StudentID) },
      ":prefix": { S: prefix }
    }
  };

  try {
    const result = await ddb.query(params).promise();

    const sessions = result.Items.map((item) => ({
      StudentID: Number(item.StudentID.N),
      SessionKey: item.SessionKey.S,
      StudentName: item.StudentName.S,
      SessionID: item.SessionID.S,
      ScenarioCharacterName: item.ScenarioCharacterName.S,
      ScenarioNumber: Number(item.ScenarioNumber.N),
      Progress: Number(item.Progress.N),
      CompletionTime: item.CompletionTime.S
    }));

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ok: true,
        exists: sessions.length > 0,
        sessions: sessions
      })
    };
  } catch (e) {
    return {
      statusCode: 500,
      body: JSON.stringify({
        ok: false,
        message: "Failed to query sessions",
        error: e.toString()
      })
    };
  }
};
```

---

# ️⃣ API Gateway Setup

* Create **REST API**
* Add Resources:

  * `/session` (POST)
  * `/login` (POST)
* Integrate each with the correct Lambda function
* Enable CORS:

  * `Access-Control-Allow-Origin: *`
  * `Access-Control-Allow-Headers: *`
  * `Access-Control-Allow-Methods: OPTIONS,POST`

---

# ️⃣ IAM Role Configuration

Add permissions to the Lambda execution role:

* `AmazonDynamoDBFullAccess` (development stage)

  * later restrict to minimum required permissions

Navigation:

```
Lambda → Your Function → Configuration → Permissions → Execution Role → IAM Role
```

---

# ️⃣ Unreal Engine C++ Integration

## 📌 5-1. Session Data Struct (Blueprint Accessible)

```cpp
USTRUCT(BlueprintType)
struct FStudentSessionData
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly) int32 StudentID;
    UPROPERTY(BlueprintReadOnly) FString SessionKey;
    UPROPERTY(BlueprintReadOnly) FString StudentName;
    UPROPERTY(BlueprintReadOnly) FString SessionID;
    UPROPERTY(BlueprintReadOnly) FString ScenarioCharacterName;
    UPROPERTY(BlueprintReadOnly) int32 ScenarioNumber;
    UPROPERTY(BlueprintReadOnly) float Progress;
    UPROPERTY(BlueprintReadOnly) FString CompletionTime;
};
```

---

## 📌 5-2. Save Function (`SendStudentSessionToAWS`)

Sends session JSON to AWS `/session`
(This is already implemented in your project.)

---

## 📌 5-3. Login Function (`LoginStudentFromAWS`)

Calls AWS `/login` and stores results in static variables.
Because HTTP is asynchronous, it **cannot return values immediately**.

---

## 📌 5-4. Get Login Result (Blueprint Callable)

```cpp
UFUNCTION(BlueprintCallable, Category="AWS")
static void GetLastLoginResult(
    bool& bSuccess,
    bool& bExists,
    TArray<FStudentSessionData>& Sessions
);
```

### Blueprint Flow Example

```
LoginStudentFromAWS
↓
Delay 0.5 sec
↓
GetLastLoginResult
↓
If Success && Exists → Load session from Sessions[0]
```

---

# ️⃣ Example Logs

## Save Success

```
[AWS] Status: 200
{"ok":true,"message":"Session stored in DynamoDB","sessionKey":"0001#Mike#1"}
```

## Login Success (multiple scenarios loaded)

```
[AWS-Login] Status: 200
{
  "ok": true,
  "exists": true,
  "sessions": [
    { ... Scenario 1 ... },
    { ... Scenario 2 ... }
  ]
}
```



---

# ️⃣ Unreal Engine – API URL Configuration (C++)

The AWS API Gateway endpoint must be configured inside Unreal Engine so that the project knows where to send Save and Login requests.

We use two separate endpoints:

* **Save API (POST /session)**
* **Login API (POST /login)**

Both URLs should be customizable from a single location in C++.

---

## 📌 7-1. Add API URL Variables (in SaveToAWS.h)

Inside your `USaveToAWS` class, add static FString variables at the top:

```cpp
// API Endpoints (set these after deploying API Gateway)
static FString SaveAPIUrl;
static FString LoginAPIUrl;
```

Now add a BlueprintCallable function to allow setting them easily:

```cpp
UFUNCTION(BlueprintCallable, Category="AWS")
static void SetAWSApiUrls(const FString& SaveUrl, const FString& LoginUrl);
```

---

## 📌 7-2. Implement URL Setter (SaveToAWS.cpp)

At the top of the file, define default empty values:

```cpp
FString USaveToAWS::SaveAPIUrl = "";
FString USaveToAWS::LoginAPIUrl = "";
```

Then implement the setter:

```cpp
void USaveToAWS::SetAWSApiUrls(const FString& SaveUrl, const FString& LoginUrl)
{
    SaveAPIUrl = SaveUrl;
    LoginAPIUrl = LoginUrl;

    UE_LOG(LogTemp, Log, TEXT("[AWS] API URLs set: Save=%s, Login=%s"), *SaveAPIUrl, *LoginAPIUrl);
}
```

---

## 📌 7-3. Update Save Function to Use API URL

Modify your existing save function:

```cpp
if (SaveAPIUrl.IsEmpty())
{
    UE_LOG(LogTemp, Error, TEXT("[AWS] Save API URL is not set!"));
    return;
}

Request->SetURL(SaveAPIUrl);
```

---

## 📌 7-4. Update Login Function to Use API URL

Inside `LoginStudentFromAWS`:

```cpp
if (LoginAPIUrl.IsEmpty())
{
    UE_LOG(LogTemp, Error, TEXT("[AWS-Login] Login API URL is not set!"));
    return;
}

Request->SetURL(LoginAPIUrl);
```

---

## 📌 7-5. How to Set URLs in Blueprint (or C++)

When the game starts, call this node:

### **SetAWSApiUrls**

```
SaveUrl : https://api.devilsona.click/session
LoginUrl: https://api.devilsona.click/login
```

Example Blueprint setup:

```
Event BeginPlay
→ SetAWSApiUrls("https://api.devilsona.click/session",
                "https://api.devilsona.click/login")
```

You only need to set this once at game startup (GameInstance recommended).

---

## 📌 7-6. Recommended: Use GameInstance for Global Settings

In your custom GameInstance:

```cpp
void UMyGameInstance::Init()
{
    Super::Init();

    USaveToAWS::SetAWSApiUrls(
        TEXT("https://api.devilsona.click/session"),
        TEXT("https://api.devilsona.click/login")
    );
}
```

This ensures the AWS endpoints are available from the beginning of the game.

---

# ✅ Summary

By adding API URL configuration:

* You can update the API Gateway address without modifying C++ code
* Blueprints can dynamically switch between dev/staging/prod servers
* The same save/login functions work universally
* Your AWS integration becomes modular and cleaner

---



---

# ✔️ Completed Features

* [x] DynamoDB table creation
* [x] Save & Login Lambda functions
* [x] API Gateway routing
* [x] IAM role permission setup
* [x] Unreal C++ integration
* [x] Blueprint-accessible login results
* [x] Multi-scenario support via arrays
* [x] End-to-end testing successful


