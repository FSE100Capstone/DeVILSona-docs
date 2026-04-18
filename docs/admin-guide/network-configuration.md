# Network Configuration & Whitelisting

!!! info "Audience"
    IT Administrators who need to configure institutional networks to support DeVILSona VR sessions.

DeVILSona's functionality depends on reliable internet access for two real-time services. This page documents the exact network requirements to share with your networking team or campus IT.

---

## Traffic Summary

DeVILSona makes outbound connections to exactly two external services:

| Service | Address Pattern | Protocol | Port | Required? |
|---------|----------------|----------|------|-----------|
| **OpenAI Realtime API** | `api.openai.com` | WSS (WebSocket over TLS) | 443 | **Critical** |
| **AWS API Gateway** | `*.execute-api.us-east-2.amazonaws.com` | HTTPS | 443 | **Critical** |
| AWS Management (DeVILStarter only) | `*.amazonaws.com` | HTTPS | 443 | Required for instructor laptop only |

All traffic uses **port 443 over TLS 1.2+**. Neither service requires any non-standard ports.

---

## OpenAI API Endpoint Whitelisting

### What DeVILSona Sends

The VR headset opens a persistent **WebSocket connection** to the OpenAI Realtime API immediately when a conversation begins. This connection:

- Sends base64-encoded PCM16 audio chunks (student's voice) approximately every 100–200ms
- Receives base64-encoded audio deltas (AI response audio) and text transcripts
- Remains open for the duration of the student's session
- Terminates cleanly when the student exits or the session ends

### WebSocket vs. Standard HTTPS — Why This Matters for Firewalls

Standard HTTPS uses a request-response pattern. WebSockets begin as an HTTP request but then "upgrade" to a persistent, full-duplex connection. Many corporate and university firewalls have rules that:

- Allow HTTPS (request/response) ✅
- Block WebSocket upgrades (persistent connection) ❌

This is the **most common cause of AI silence in DeVILSona**—the headset is connected to the network, but WebSocket connections to OpenAI are being dropped by the firewall or proxy.

### Required Whitelist Rules

Ask your network/firewall team to allow the following:

```
# Outbound WebSocket (WSS) connections:
ALLOW TCP OUTBOUND → api.openai.com:443
  Protocol: HTTPS with WebSocket Upgrade header permitted
  Method: Persistent/long-lived connection allowed (not subject to short connection timeout)

# Connection timeout:
  Idle timeout should be at minimum 5 minutes (300 seconds)
  DeVILSona uses keep-alive pings to maintain the connection,
  but aggressive firewall timeouts (< 30 seconds) will terminate sessions
```

### Deep Packet Inspection Considerations

If the network uses a **TLS-intercepting proxy** or **SSL inspection** that terminates and re-signs TLS connections:

- OpenAI's SDK performs certificate pinning validation
- SSL inspection may cause the connection to fail with a certificate error
- The network team may need to exclude `api.openai.com` from SSL inspection, or add the proxy's CA certificate to the headset's trust store

For Meta Quest devices, adding custom CA certificates requires ADB and developer tooling. Contact the technical administrator if this is required.

---

## AWS API Gateway Endpoint Whitelisting

### The Challenge: Dynamic URLs

AWS API Gateway generates a **dynamically allocated URL** when the infrastructure is deployed. This URL changes each time `terraform destroy` + `terraform apply` is run (i.e., each time DeVILStarter tears down and recreates the infrastructure).

The URL format is:
```
https://<random-id>.execute-api.us-east-2.amazonaws.com/session
https://<random-id>.execute-api.us-east-2.amazonaws.com/login
```

Where `<random-id>` is a string like `abcd1234ef` that is assigned by AWS at creation time.

### Whitelisting Strategy

**Option A: Wildcard Subdomain (Recommended)**

Rather than whitelisting a specific URL, whitelist the entire `execute-api.us-east-2.amazonaws.com` subdomain space:
```
ALLOW HTTPS OUTBOUND → *.execute-api.us-east-2.amazonaws.com:443
```

This ensures the rule remains valid across infrastructure recreations.

**Option B: IP Address Ranges (Advanced)**

AWS publishes its IP ranges in a machine-readable JSON file at  
[https://ip-ranges.amazonaws.com/ip-ranges.json](https://ip-ranges.amazonaws.com/ip-ranges.json)

For API Gateway in `us-east-2`, filter for:
```json
"service": "API_GATEWAY",
"region": "us-east-2"
```

This approach requires periodic updates when AWS updates its IP ranges (they update this list regularly).

---

## Local Network Constraints

### Captive Portals

University guest Wi-Fi networks frequently use **captive portals**—web pages that must be accepted before internet access is granted. Meta Quest headsets can handle simple captive portals through their browser, but this process can be confusing in a classroom setting.

**Recommended approach:** Place the DeVILSona headsets on a **non-captive portal network** such as:

- The institutional `eduroam` network (if headsets can be enrolled)
- A dedicated IoT/device VLAN
- A separate access point with WPA2-PSK authentication (no portal)

If you must use a captive portal network:

1. Put on the headset
2. Open the **Meta Quest Browser** application
3. Navigate to any HTTP site (e.g., `http://example.com`)—the captive portal should intercept and display its acceptance page
4. Accept the terms
5. Internet access should then be available to other apps including DeVILSona

### Network Isolation / Client Isolation

Some access points enable **"client isolation"** or **"AP isolation"** which prevents devices on the same Wi-Fi from communicating with each other. This is a common security feature but can interfere with:

- Meta Quest casting (the headset broadcasts to the same network)
- Some mDNS-based discovery features

For DeVILSona's core functionality (AI conversations, session saves), client isolation is **not an issue**—all required connections go to external internet services. However, if you want to use casting to observe students from a laptop on the same network, client isolation must be **disabled** for those devices.

### Bandwidth & Latency Requirements

AI audio conversations require a continuous, low-latency connection. Here are the network requirements per active headset:

| Metric | Minimum | Recommended |
|--------|---------|-------------|
| **Bandwidth per headset (upload)** | 200 Kbps | 500 Kbps |
| **Bandwidth per headset (download)** | 500 Kbps | 1 Mbps |
| **Latency to openai.com** | < 200ms | < 100ms |
| **Packet loss** | < 2% | < 0.5% |
| **Jitter** | < 50ms | < 20ms |

**For a class of 8 simultaneous sessions:**

- Upload: ~4 Mbps sustained
- Download: ~8 Mbps sustained
- Total: ~12 Mbps with headroom

This is well within the capabilities of any modern campus access point. The bottleneck is more often **latency and packet loss** than raw bandwidth. A congested campus network with high latency can cause noticeable AI response delays.

### Measuring Network Quality

Before a session, an administrator can measure network quality from a laptop on the same SSID:

```powershell
# Measure latency to OpenAI
ping api.openai.com -n 20

# Test bandwidth using speedtest-cli (install: pip install speedtest-cli)
speedtest-cli --server auto

# Test WebSocket connectivity (requires wscat: npm install -g wscat)
wscat --connect wss://api.openai.com/v1/realtime `
  -H "Authorization: Bearer sk-proj-..."  `
  -H "OpenAI-Beta: realtime=v1"
```

A successful WebSocket connection that doesn't immediately close confirms that the network allows WebSocket traffic to OpenAI.

---

## DeVILStarter Laptop Network Requirements

The laptop running **DeVILStarter** requires outbound HTTPS to a broader set of AWS endpoints (for Terraform's provisioning operations):

```
ALLOW HTTPS OUTBOUND → *.amazonaws.com:443     # All AWS services
ALLOW HTTPS OUTBOUND → registry.terraform.io:443  # Terraform provider downloads (first time only)
```

The DeVILStarter laptop does **not** need to be on the same network as the headsets. It can be on a separate VLAN or even a completely different internet connection, as long as it has outbound access to AWS.

---

## Network Checklist for IT

Before each semester's lab deployment:

- [ ] `api.openai.com:443` reachable from the classroom Wi-Fi SSID (test WebSocket upgrade)
- [ ] `*.execute-api.us-east-2.amazonaws.com:443` reachable (or specific URL whitelisted)
- [ ] No captive portal on the headset's SSID (or staff can assist with portal acceptance)
- [ ] No SSL inspection on `api.openai.com` (or workaround documented)
- [ ] WebSocket idle timeout ≥ 5 minutes
- [ ] Available bandwidth ≥ 12 Mbps per concurrent group of 8 headsets
- [ ] DeVILStarter laptop has outbound access to `*.amazonaws.com:443`

---

➡️ **Next:** [Backend & Cloud Operations](backend-cloud.md)
