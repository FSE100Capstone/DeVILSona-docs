# Network Requirements

!!! info "Audience"
    Educators who need to ensure their classroom network supports DeVILSona, and campus IT staff who need to configure firewall or network rules.

DeVILSona requires a reliable internet connection on the classroom Wi-Fi network. This page documents the exact network requirements so you can verify your setup or share this page directly with your campus IT team.

---

## Quick Summary

DeVILSona needs outbound internet access to **two services**, both on **standard port 443 (HTTPS)**:

| Service | Address | Protocol | Port | Purpose |
|---------|---------|----------|------|---------|
| **OpenAI** | `api.openai.com` | WebSocket over HTTPS | 443 | Real-time AI voice conversation |
| **AWS Backend** | `*.execute-api.us-east-2.amazonaws.com` | HTTPS | 443 | Student login and session saving |
| **AWS Management** (DeVILStarter laptop only) | `*.amazonaws.com` | HTTPS | 443 | Starting/stopping the cloud backend |

No unusual or non-standard ports are required. All traffic is encrypted.

---

## OpenAI Connection (AI Voice)

### What It Does

When a student begins a conversation with the AI character, the headset opens a persistent **WebSocket connection** to OpenAI. This connection:

- Sends the student's voice audio to OpenAI in real time
- Receives the AI character's voice response back in real time
- Stays open for the entire duration of the conversation (typically 5–10 minutes)
- Closes automatically when the student exits the session

### Why This Matters for Firewalls

WebSocket connections are different from regular web browsing. A regular website loads a page and then the connection ends. A WebSocket connection stays open continuously — like a phone call rather than sending letters back and forth.

**Many university and corporate firewalls block WebSocket connections**, even on port 443. This is the **single most common cause of the AI character not responding** during a session.

### What to Tell Your IT Team

Ask your campus network/firewall team to allow the following:

```
ALLOW TCP OUTBOUND → api.openai.com:443
  - WebSocket Upgrade headers must be permitted (not just standard HTTPS)
  - Connection must be allowed to remain open (idle timeout at least 5 minutes)
  - Do NOT apply SSL inspection/interception to this address
    (OpenAI validates certificates and will reject modified connections)
```

!!! warning "SSL Inspection"
    If your campus network uses a **TLS-intercepting proxy** (sometimes called "SSL inspection") that examines encrypted traffic, it may break the OpenAI connection. Ask IT to **exclude `api.openai.com` from SSL inspection**.

---

## AWS Backend Connection (Student Data)

### What It Does

When a student logs in or their session is saved, the headset makes a brief HTTPS request to the AWS backend. These are standard web requests (like loading a web page) and are much less likely to be blocked.

### The Challenge: Dynamic URLs

The AWS backend URL changes each time the cloud infrastructure is restarted (which can happen between semesters). The URL looks like:

```
https://<random-id>.execute-api.us-east-2.amazonaws.com
```

### What to Tell Your IT Team

Rather than whitelisting a specific URL (which would change), ask IT to allow the entire AWS API Gateway subdomain:

```
ALLOW HTTPS OUTBOUND → *.execute-api.us-east-2.amazonaws.com:443
```

This is a standard AWS address pattern and ensures the rule remains valid even if the backend is recreated.

---

## DeVILStarter Laptop Requirements

The Windows laptop running **DeVILStarter** needs outbound HTTPS access to AWS services for infrastructure management. This laptop does **not** need to be on the same Wi-Fi network as the headsets — it can be on a completely separate network, as long as it has internet access.

```
ALLOW HTTPS OUTBOUND → *.amazonaws.com:443
```

---

## Wi-Fi Network Considerations

### Captive Portals (Login Pages)

Many university guest Wi-Fi networks require you to accept terms on a web page before you get internet access. Meta Quest headsets can handle this, but it's awkward in a classroom setting.

**Recommended:** Place the headsets on a network that does **not** require a captive portal login, such as:

- The institutional `eduroam` network (if the headsets can be enrolled)
- A dedicated lab or device network with WPA2 password authentication (no portal page)

**If you must use a captive portal network:**

1. Put on the headset
2. Open the **Meta Quest Browser** app (from the App Library)
3. Navigate to any website (e.g., `http://example.com`) — the captive portal page should appear
4. Accept the terms
5. Internet access should then work for all apps, including DeVILSona

### Client Isolation

Some access points have a security feature called **"client isolation"** that prevents devices on the same Wi-Fi from seeing each other. This does **not** affect DeVILSona's core functionality (all connections go to external internet services). However, if you want to **cast** a student's VR view to your laptop on the same network, client isolation must be **disabled** for those devices.

---

## Bandwidth & Latency Requirements

The AI voice conversation requires a continuous, low-latency connection. Here are the network requirements **per active headset**:

| Metric | Minimum | Recommended |
|--------|---------|-------------|
| **Upload bandwidth** | 200 Kbps | 500 Kbps |
| **Download bandwidth** | 500 Kbps | 1 Mbps |
| **Latency** | < 200ms | < 100ms |
| **Packet loss** | < 2% | < 0.5% |

### For a Full Classroom (8 Headsets Simultaneously)

| Metric | Total Required |
|--------|---------------|
| Upload | ~4 Mbps |
| Download | ~8 Mbps |
| **Total** | **~12 Mbps** |

This is well within the capacity of any modern campus access point. The more common bottleneck is **latency and packet loss** on a congested network, which causes noticeable delays in the AI's responses.

### Pre-Session Network Test

Before your first session, you can run a quick network test from a laptop connected to the **same Wi-Fi network** the headsets will use:

1. Open a web browser and go to [https://www.speedtest.net](https://www.speedtest.net) — verify the network meets the bandwidth requirements above
2. Open PowerShell (or Command Prompt) and run `ping api.openai.com` — verify latency is under 200ms and there is no packet loss

---

## Pre-Session Network Checklist

Use this checklist before each semester's first session:

- [ ] Headsets can connect to the classroom Wi-Fi (correct SSID and password)
- [ ] `api.openai.com:443` is reachable from the classroom Wi-Fi (WebSocket connections allowed)
- [ ] `*.execute-api.us-east-2.amazonaws.com:443` is reachable
- [ ] No captive portal on the headset's network (or staff can assist with portal acceptance)
- [ ] No SSL inspection on `api.openai.com`
- [ ] WebSocket idle timeout is at least 5 minutes
- [ ] Available bandwidth is at least 12 Mbps for a group of 8 headsets
- [ ] DeVILStarter laptop has outbound access to `*.amazonaws.com:443`

---

➡️ **Next:** [Running a Session](running-a-session.md)
