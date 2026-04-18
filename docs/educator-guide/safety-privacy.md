# Student Safety & Privacy

!!! info "Audience"
    Educators, administrators, and project sponsors who want to understand how student safety and privacy are protected in DeVILSona.

This page explains the safeguards in place to protect students—both physically and digitally—during a DeVILSona session.

---

## OpenAI Content Guardrails

### How the AI Is Constrained

DeVILSona's AI characters are powered by OpenAI's Realtime API, which itself is governed by OpenAI's comprehensive [Usage Policies](https://openai.com/policies/usage-policies). On top of OpenAI's baseline safety measures, DeVILSona applies an additional layer of constraints through its **system prompt**—a set of detailed, pre-configured instructions that define what the AI character is, what it can discuss, and what it absolutely will not do.

Specifically, each AI persona is instructed to:

- **Stay in character at all times** as the defined persona (e.g., a community member with accessibility needs)
- **Refuse to discuss off-topic subjects** unrelated to their persona and the design challenge
- **Not engage with inappropriate, offensive, or distressing content** regardless of how the student phrases the request
- **Not break character** to discuss being an AI, the technology behind it, or any unrelated technical topics
- **Maintain a tone that is appropriate** for an educational context with first-year university students

### What Happens If a Student Tries to Misuse the AI

If a student attempts to get the AI to say something inappropriate (a common curiosity), the system is designed to:

1. **Redirect the conversation** back to topics relevant to the character's persona
2. **Default to neutral, in-character responses** rather than engaging with off-topic prompts
3. **Gently decline** without escalating the situation (the character might say something like "That's not really something I want to talk about—can we get back to discussing my experience with...")

The AI will not produce harmful content even with persistent or creative prompting. OpenAI's safety systems are applied before our system prompt, creating a dual-layer protection.

### Educator Override

If you observe a student attempting to misuse the experience or if the AI session becomes unproductive, you can immediately end the session by having the student remove the headset or by pressing the Meta button to exit to the home screen.

---

## Data Anonymization & Privacy

### What Data Is Collected

DeVILSona collects a minimal amount of data necessary for the session to function:

| Data Type | What Is Stored | Where It Is Stored | How Long |
|-----------|---------------|-------------------|----------|
| **Student ID (ASUID)** | A numeric identifier | AWS DynamoDB (encrypted in transit) | Duration of the course |
| **Session ID** | A 4-digit code students choose | AWS DynamoDB | Duration of the course |
| **Student Name** | Name entered at login | AWS DynamoDB | Duration of the course |
| **Scenario Progress** | Which scenarios completed, progress percentages | AWS DynamoDB | Duration of the course |

### What Data Is NOT Collected

This is equally important:

- ❌ **No audio recordings** are stored. The student's voice is processed in real-time by OpenAI and then discarded. No recording of the conversation is retained.
- ❌ **No video or camera footage** is captured. The Meta Quest uses internal cameras for tracking only; this data is not accessible to DeVILSona.
- ❌ **No conversation transcripts** are stored permanently in the database. (Note: OpenAI's own API infrastructure processes the audio, but DeVILSona does not request or store the conversation history in the project's database.)
- ❌ **No biometric data** (heart rate, eye tracking, movement patterns) is collected.

### Data Access

Session data in AWS DynamoDB is only accessible to:

- The **project's AWS infrastructure** (to allow a student to resume their session)
- **Designated project administrators** with AWS console access

Regular students, instructors, and third parties cannot access this data directly.

### Data Retention

Session data is maintained in the AWS DynamoDB table for the duration of the course. When the infrastructure is torn down at the end of the semester using DeVILStarter, the data in the database is preserved but the API access endpoints are removed. A future administrator with AWS console access could delete the table if complete data purge is required.

### FERPA Compliance Considerations

Because ASUID numbers are stored, this data falls under the FERPA (Family Educational Rights and Privacy Act) umbrella. The data is:

- Encrypted in transit (HTTPS/TLS)
- Stored in a secured AWS environment
- Not shared with any third party
- Not linked to assessment grades in the current implementation

For institutional compliance review, contact your university's privacy office with the data inventory above.

---

## Recognizing VR Motion Sickness

VR Motion Sickness (also called **cybersickness** or **VR-induced nausea**) is a genuine physiological response that affects some people who use VR headsets. It occurs because the visual system perceives motion while the body's vestibular system (inner ear) does not.

**Good news for DeVILSona:** The simulation is **stationary**—the student does not physically move through a 3D environment. This dramatically reduces the risk of motion sickness compared to VR experiences with locomotion (flying, running, etc.). Most students experience no discomfort at all.

### Who Is at Higher Risk

Some individuals are more susceptible than others:

- People who experience car sickness or seasickness regularly
- People trying VR for the first time (the body typically acclimates with repeated exposure)
- People who are tired, dehydrated, or have not eaten recently
- People with inner ear conditions or vestibular disorders

### Early Warning Signs to Watch For

Watch for these behavioral cues even while the student is wearing the headset:

| Sign | What to Do |
|------|-----------|
| Student becomes unusually quiet after being talkative | Ask if they're okay |
| Student starts looking downward frequently | May be a reflex to orient themselves |
| Student shifts weight repeatedly or grabs something | May be experiencing imbalance |
| Student removes the headset mid-session without being told to | Always check in immediately |
| Student reports dizziness, headache, or nausea verbally | End the session immediately |

### Immediate Steps If a Student Feels Unwell

1. **Calmly end the session:** Ask the student to hand you the controllers and help them remove the headset. Do not rush them—sudden removal can sometimes worsen dizziness.
2. **Seat the student:** Have them sit down immediately if they feel dizzy. Do not let them stand unsupported.
3. **Fresh air:** If the room is stuffy, open a window or move to a cooler area.
4. **Time:** Motion sickness symptoms typically resolve within **5–15 minutes** of stopping VR. In some cases it can take up to an hour.
5. **Do not have them attempt VR again that day.** Even if they feel better after 10 minutes, returning to VR the same day generally causes a recurrence.
6. **Hydration:** Encourage water. Avoid coffee or anything acidic while symptomatic.

!!! warning "If symptoms persist beyond 30 minutes"
    or the student experiences vomiting, severe headache, or chest discomfort that does not seem plausibly related to motion sickness, follow your university's standard health emergency protocol and contact campus health services.

### Prevention

Brief students before their session:

*"If at any point you feel dizzy, nauseous, or uncomfortable during the VR experience, just say something immediately. There's no penalty for stopping early—your comfort is the priority. This kind of VR simulation rarely causes motion sickness because you're standing still, but everyone's different."*

---

## Physical Safety in VR

Students wearing the headset are **visually disconnected from the real world**. They rely entirely on you to ensure their physical safety during the experience.

### Establishing the Safe Play Area

Always confirm the play area is clear **immediately before** each student session, not just at the start of class. Other students may have moved bags or furniture during earlier sessions.

Minimum clearances:

- **2m × 2m** of clear floor space (see [Classroom Setup & Hardware](classroom-setup.md))
- No obstacles within **1.5m** of the student's starting position in any direction
- No objects **at head height** that a student could accidentally contact when turning

### The Guardian System

The Meta Quest headset has a built-in feature called the **Guardian** (also called the safety boundary system). When properly set up:

- The student draws a boundary around their play area the first time they use a new space
- When they approach that boundary in VR, a **visual grid overlay** appears through the headset, warning them they are near the edge of their safe area
- If they exit the boundary, the headset shows the real world through passthrough cameras

If this is the first time the headset is being used in a new room, the Guardian setup will run automatically before the app launches. Follow the on-screen instructions to define a safe play area.

### Monitor Actively

**Do not leave a student unattended in VR**, especially a first-time user. Stand nearby and watch that:

- The student stays within the play area boundary
- The student does not reach toward real-world objects they can see in VR (this is called "presence bleed"—the student forgets the VR object isn't real)
- The student maintains a stable stance

For seated sessions (recommended for students who may have balance or mobility concerns), ensure the chair cannot tip and that the student is seated before putting the headset on.

### Students with Specific Needs

- **Students with epilepsy or seizure history:** Flickering lights in VR can potentially trigger photosensitive responses in sensitive individuals. The DeVILSona environment uses standard indoor lighting simulation with no strobe effects, but consult with the student or their disability accommodations advisor before having them participate.
- **Students with vestibular conditions:** Recommend seated sessions.
- **Students with visual impairments or low vision:** The VR headset's display may not be suitable for students with severe visual impairments. Discuss alternative assessment options with your accessibility services office.

---

➡️ **Next:** [Troubleshooting for Educators](troubleshooting.md)
