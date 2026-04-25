# Welcome to DeVILSona

!!! note "This guide is written for educators and project sponsors."
    No technical background is required. This guide covers everything from classroom setup to headset deployment, network requirements, and troubleshooting.

---

## What Is DeVILSona?

**DeVILSona** is an immersive Virtual Reality (VR) simulation developed as part of the FSE100 undergraduate engineering curriculum at Arizona State University.

At its core, DeVILSona replaces the traditional "persona worksheet" exercise with something far more powerful: a live conversation. A student puts on a Meta Quest VR headset and finds themselves face-to-face with an AI-powered character—a realistic digital person who has their own name, background, challenges, and opinions. The student speaks naturally, asks questions, and learns directly from the character's responses. The AI has no script; it responds dynamically to whatever the student says.

This is not a video game. It is an **experiential learning tool** designed to build empathy, active listening, and human-centered design thinking in engineering students.

---

## The Educational Problem: Why Paper Personas Fall Short

In most introductory engineering design courses, students are introduced to the concept of a "user persona"—a written profile of a hypothetical person whose problem they are trying to solve. These personas typically include a name, age, occupation, goals, and frustrations. Students read them, acknowledge them, and then—in practice—largely forget them.

The fundamental problem with paper personas is **emotional distance**. Reading about someone's challenges is a fundamentally passive exercise. Research in educational psychology consistently shows that humans learn empathy and perspective-taking far more effectively through **interactive, emotionally engaging experiences** than through reading text.

Consider the difference:

- **Paper persona:** *"Maria, 58, uses a wheelchair and struggles with ramp accessibility at her local supermarket."*
- **DeVILSona:** *A student talks directly to Maria, hears the frustration in her voice as she describes missing a bus because the ramp was icy, and watches her expression change when asked about how the design problem affects her independence.*

The second experience is remembered. The first is forgotten by the next week.

### Key Limitations of Traditional Personas
| Traditional Persona | DeVILSona |
|---------------------|-----------|
| Static text document | Dynamic, real-time conversation |
| One-size-fits-all | Responds differently to every student's questions |
| No emotional engagement | Emotionally resonant, immersive experience |
| Students read passively | Students engage actively |
| Easily forgotten | Memorable and impactful |

---

## FSE100 Integration

**FSE100** is Arizona State University's foundational engineering design course. It introduces first-year engineering students to the design process, including how to identify user needs, define problems, and prototype solutions.

A critical component of FSE100 is learning to design *for people*—not just for technical specifications. DeVILSona is used during the **user empathy and needs-finding** phase of the course.

### How It Fits Into the Curriculum

1. **Prior to the Lab:** Students receive a brief introduction to the scenario and the characters they will meet. They are told the general problem domain (e.g., accessibility, communication, transportation) but not the specific details—those they must discover through conversation.

2. **During the Lab:** Students take turns wearing the headset. Each session typically lasts **5–10 minutes per student**. During this time, they speak freely with the AI character, asking questions and probing for details about the character's daily experiences and challenges.

3. **After the Lab:** Students reflect on what they learned and use their discoveries to inform their design challenge. Because the experience is personal and immersive, the insights they gain tend to be richer and more nuanced than those from reading a worksheet.

### Scenarios and Characters

DeVILSona supports multiple characters, each representing a different persona relevant to the engineering design challenge. For example, a single class session might feature:

- A working professional who struggles with commute accessibility
- A student with a visual impairment who relies on assistive technology
- An elderly person navigating digital interfaces for the first time

Each character has a detailed **AI persona prompt** that defines their background, personality, challenges, and the kinds of topics they can meaningfully discuss. This ensures that conversations stay relevant to the learning objective.

---

## The Role of AI: How DeVILSona Creates Dynamic Learning

The "magic" behind DeVILSona is the **OpenAI Realtime API**—a cutting-edge AI system capable of understanding and responding to natural spoken language in real time, with minimal delay.

### What This Means in Practice

Unlike traditional chatbots or scripted NPCs (non-player characters) in video games, DeVILSona's characters are not pre-programmed with a fixed set of responses. They:

- **Listen** to what the student actually says, in full context
- **Understand** the intent and emotional tone of the question
- **Respond** in character, consistently, with personality and depth
- **React** to follow-up questions and changes in conversational direction
- **Remember** what was said earlier in the same conversation

This means every student's experience is unique. A student who asks "How does this affect your daily routine?" will get a different, contextualized answer than a student who asks "What do you find most frustrating?" even if they are talking to the same character.

### The AI Is "In Character"

The AI is configured with a detailed system prompt that defines who the character is, how they speak, what they know, and what they don't know. The character will not break character to say "I am an AI" or discuss topics outside their persona. This creates a convincing, immersive interaction.

### Safety and Content Boundaries

The AI is explicitly instructed to remain within appropriate educational boundaries. It will not generate harmful, offensive, or off-topic content. For more details on AI content safety, see [Student Safety & Privacy](safety-privacy.md).

---

## Core Learning Outcomes

By the end of a DeVILSona session, students should be able to:

1. **Articulate specific, human-centered insights** about the problem domain from the perspective of a real stakeholder, rather than stating generic assumptions.

2. **Demonstrate active listening skills** by asking follow-up questions based on what the character said, rather than following a predetermined question script.

3. **Identify the emotional and social dimensions** of a design problem, not just the functional requirements. Students should understand *how* a problem makes someone feel, not just *what* the problem is.

4. **Develop greater empathy** for people whose lived experiences differ from their own, particularly regarding accessibility, aging, disability, and socioeconomic challenges that are commonly addressed in engineering design.

5. **Connect their experience** to the formal design process—specifically the needsfinding and problem definition stages—by translating their conversation insights into actionable design criteria.

### Assessment Integration

Instructors can assess these outcomes through reflection prompts, empathy maps, or design briefs that ask students to explicitly reference specific moments or statements from their DeVILSona conversation. The immersive, personal nature of the experience makes it far easier for students to recall and articulate specific details compared to a reading assignment.

---

## Next Steps

Continue to the next section to learn how to set up the physical classroom environment for a session:

➡️ **[Classroom Setup & Hardware](classroom-setup.md)**

Or jump to any section using the sidebar navigation.
