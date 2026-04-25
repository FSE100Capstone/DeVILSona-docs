# Troubleshooting for Educators

!!! info "Audience"
    Educators running a live DeVILSona class session who encounter a problem and need a quick solution.

This page provides a simple **"If X happens, do Y"** guide for the most common classroom issues. For deeper technical diagnostics, see the [Advanced Diagnostics](#advanced-diagnostics-capturing-logs) section at the bottom of this page.

---

## Problem 1: The Headset Won't Connect to Wi-Fi

**Symptoms:** Wi-Fi icon shows a disconnected symbol or an exclamation mark. The DeVILSona app fails to log in.

### Resolution Steps (try in order)

1. **Double check the network name:** Go to **Settings → Wi-Fi** inside the headset and confirm you're connecting to the correct classroom Wi-Fi network. On many university campuses there are multiple SSIDs (e.g., `ASU-Guest`, `ASU-Secure`, `eduroam`). The headset must be on a network that allows WebSocket connections and outbound HTTPS (not all campus guest networks do this).

2. **Forget and reconnect:** In **Settings → Wi-Fi**, select the current network and tap **"Forget"**, then reconnect and re-enter the password.

3. **Restart the headset's network stack:** Go to **Settings → Wi-Fi**, toggle Wi-Fi **off**, wait 5 seconds, then toggle it back **on**.

4. **Restart the headset:** Hold the power button and select **Restart** (not Power Off). After restarting, try Wi-Fi again.

5. **Check if other headsets can connect:** If only one headset has issues while others connect fine, the problem is likely that specific headset. Try restarting it again or contact IT.

6. **Network may block required traffic:** If no headsets can connect and the network name is correct, the classroom network may be blocking the ports DeVILSona needs (port 443 for HTTPS, and WebSocket upgrade). Contact your IT department with this information. See [Network Requirements](network-requirements.md) for the exact rules to share with IT.

---

## Problem 2: The AI Character Is Not Responding ("The AI Is Ignoring Me")

**Symptoms:** The student speaks but the AI character does not respond, appears frozen, or only responds intermittently.

### Resolution Steps (try in order)

1. **Check the microphone:** Ensure the student is speaking clearly into the headset. The microphone is built into the front of the Meta Quest headset. Move closer to the student and listen—can *you* hear them speaking? If the student is speaking very quietly, ask them to project their voice more.

2. **Check the internet connection:** The AI requires a live internet connection to process speech. Return to the home screen (press the Meta button), check the Wi-Fi indicator. If disconnected, reconnect per Problem 1 above.

3. **Ask if the AI has been responding at all:** If the AI worked for the first minute and then stopped, the issue may be a **streaming interruption**. In this case, the fastest fix is to exit the app and relaunch it (see Problem 4 below).

4. **Verify cloud infrastructure is running:** Go back to the **DeVILStarter** laptop. Is the status indicator showing **green/running**? If it shows an error or the infrastructure has stopped, restart it using the "Start Infrastructure" button and allow 2–5 minutes for it to come back up. The AI cannot function without the backend being online.

5. **OpenAI service disruption:** Very rarely, OpenAI itself may have a service outage. Check [https://status.openai.com](https://status.openai.com) to confirm if there are any active incidents. If OpenAI is down, the AI component of DeVILSona will not function until service is restored.

---

## Problem 3: DeVILStarter Fails to Launch or Shows an Error

**Symptoms:** The DeVILStarter application opens but shows an error message, or clicking "Start Infrastructure" does not result in the status turning green after 5+ minutes.

### Resolution Steps (try in order)

1. **Check internet connectivity on the laptop:** Open a browser and navigate to [https://aws.amazon.com](https://aws.amazon.com). If the page doesn't load, the laptop doesn't have internet access. Reconnect to the correct network.

2. **Check the log output panel:** DeVILStarter shows detailed logs. Look for any red error lines. Common errors include:
   - `"credentials not found"` → The AWS credentials stored in DeVILStarter are missing or expired. Contact a technical administrator—they will need to re-enter the AWS access keys.
   - `"timeout"` or `"connection refused"` → Network issue. Check internet connectivity.
   - `"already running"` → A previous session's infrastructure may not have been torn down. Try clicking "Stop Infrastructure" first, wait until it completes, then try "Start Infrastructure" again.

3. **Restart DeVILStarter:** Fully close the application (from the taskbar, right-click → Quit) and reopen it. Sometimes the application state becomes corrupted after an unexpected closure.

4. **Restart the laptop:** As a last resort, fully restart the Windows machine running DeVILStarter and try again.

5. **Escalate to technical administrator:** If none of the above resolves the issue, contact the technical administrator on file for this course. They have access to the AWS Console directly and can verify whether the infrastructure is running independently of DeVILStarter.

---

## Problem 4: Restarting a Stuck Session

**Symptoms:** The app is frozen (the 3D character is not animating, the UI doesn't respond), or the student is stuck in a loading screen that doesn't progress past 30 seconds.

### Resolution Steps

1. **Exit to the home screen first:** Press the **Meta button** (the circular Meta logo button on the right controller). This brings up the home overlay. From here, you can navigate back to the App Library.

2. **Force-quit the app:** In the home overlay, find the DeVILSona app in the taskbar. Long-press on it and select **"Quit"**. Alternatively, navigate to **App Library**, find the app, hold the controller trigger over it, and select **"Close"**.

3. **Wait 10 seconds:** Give the headset a moment after force-quitting.

4. **Relaunch from App Library:** Open the App Library and relaunch DeVILSona normally.

5. **Have the student log in again:** Their progress is saved to AWS. When they enter their ASUID and Session ID again, their previous progress should be loaded automatically.

6. **If the app crashes immediately upon launch:** The issue may be deeper—try a full headset restart (hold power button → Restart). If crashes persist after a headset restart, the app may need to be reinstalled by a technical administrator.

---

## Problem 5: The Student's Progress Is Lost (Saved Data Not Loading)

**Symptoms:** A student who has used DeVILSona previously logs in but sees no saved progress.

### Resolution Steps

1. **Verify the correct ASUID and Session ID:** Students must enter the **exact same** ASUID and Session ID they used previously. A single digit difference creates a different save slot. Ask the student to double-check—typos are the most common cause.

2. **Verify the cloud infrastructure is running:** Save data is stored on AWS. If DeVILStarter is not running (or the infrastructure was not started today), the app cannot retrieve the saved data. Start the infrastructure and have the student retry.

3. **Session ID confusion:** Remind the student that the Session ID is a 4-digit code (e.g., `0001`). If they're trying `1` instead of `0001`, it won't match.

4. **Contact technical administrator:** If the student is certain they have the right credentials and the infrastructure is running, a technical administrator can check the DynamoDB database directly to locate the student's record and confirm whether the data exists.

---

## General Tips for Common Classroom Situations

| Situation | Quick Resolution |
|-----------|-----------------|
| Student feels dizzy mid-session | Remove headset immediately. Have student sit, drink water, and rest. Do not retry VR that day. |
| Headset shows "Guardian Setup" screen | Walk the student through the 3-step boundary drawing process—it takes about 30 seconds. |
| App prompts for a software update | Decline the update during class (click "Later"). Apply updates after class when headsets are charging. |
| Multiple students want to use the same headset quickly | Use Clorox Clean-Up Disinfectant Wipes for facial interface cleaning between students. Skip drying time—simply use a fresh wipe on the face gasket for each student. Reset session by pressing Meta button and logging out. |
| Student can't hear the AI's voice | The AI audio plays through the integrated speakers on the sides of the headset. Increase volume with the volume buttons on the right side of the headset. |
| Login screen keyboard is hard to use | Encourage the student to take their time. Controller precision improves with practice. Alternatively, help guide the student's hand by pointing at the correct key. |

---

## Advanced Diagnostics: Capturing Logs

If the quick-fix steps above don't resolve the issue, the next step is to **capture diagnostic logs** from the headset. These logs record everything happening inside the app and can help identify what went wrong.

### What You Need

- **SideQuest** installed on your computer (see [Headset Setup & Sideloading](headset-setup-and-sideloading.md) for installation instructions)
- The headset connected to your computer via **USB-C**
- SideQuest showing a **green connection indicator**

### Capturing Logs with SideQuest

1. Open **SideQuest** on your computer
2. Connect the headset via USB-C and confirm it shows as connected (green dot)
3. Click the **"Run ADB Commands"** button (wrench icon in the top-right toolbar)
4. Select **"Logcat"** from the menu
5. Choose a **folder** on your computer where the log file will be saved
6. Click **"Start collecting logs"**
7. **Reproduce the issue** on the headset (launch the app, trigger the problem)
8. Return to SideQuest and click **"Stop collecting logs"**
9. Navigate to the folder you selected — you'll find a log file (`.txt` or `.log`) with the captured data

### Interpreting Logs with an AI Assistant

The captured log files contain highly technical output that can be difficult to read. A quick and effective way to make sense of them is to **paste the log contents into an AI assistant** such as [ChatGPT](https://chat.openai.com) or a similar tool.

Try a prompt like:

> "I captured this log from a VR application called DeVILSona running on a Meta Quest headset. The issue I'm experiencing is [describe the problem]. Can you help me identify what went wrong? Here is the log:"
> 
> *(paste the log file contents)*

The AI can often identify error messages, failed connections, and common issues much faster than reading through the logs manually.

### What to Look For in Logs

If you prefer to scan the logs yourself, here are the key patterns:

| Log Pattern | What It Means |
|------------|---------------|
| `[AWS] Save API URL is not set!` | The app wasn't given the backend URL — restart DeVILStarter |
| `[AWS] SaveSession failed` | Couldn't reach the backend — check Wi-Fi and DeVILStarter status |
| `OpenAI WebSocket: Connection closed with code 1006` | AI connection dropped — check network and firewall rules |
| `CAPSTONE_PROJECT_OPENAI_API_KEY environment variable is not set` | Missing API key — this is a build issue, contact the development team |

---

## Escalation Path

If you've exhausted the troubleshooting steps and log capture above, escalate through the following levels:

### Level 1: Self-Service (You)

- Follow the troubleshooting steps on this page
- Restart the app, check Wi-Fi, restart the headset
- Restart DeVILStarter and re-deploy the infrastructure

### Level 2: Log Capture & AI-Assisted Diagnosis

- Capture logs using SideQuest (see above)
- Paste logs into an AI assistant for interpretation
- Try the suggested fixes from the AI

### Level 3: Contact the Development Team

Escalate to the capstone development team when:

- The app crashes **every time** on launch
- The AI never responds despite confirmed network connectivity
- DeVILStarter consistently fails despite correct credentials
- A new build of the app is needed (bug fix or new feature)

**When contacting the development team, provide:**

1. The **log file** captured from SideQuest
2. The **exact steps** you took to reproduce the issue
3. Which **headset model** is affected (Quest 2, Quest 3, etc.)
4. What **network** the headset was on (campus Wi-Fi name, any known restrictions)
5. Screenshots of any **error messages** visible in DeVILStarter or the headset

