# Classroom Setup & Hardware Requirements

!!! info "Audience"
    Educators and lab staff who are preparing the physical classroom environment for a DeVILSona session.

This page provides a complete, practical guide to preparing your classroom for a DeVILSona lab. Proper setup takes approximately **15–20 minutes** before students arrive and is essential for a safe, smooth experience.

---

## Physical Space Configuration

VR requires more physical space than a typical classroom activity. Before the session begins, you must designate and prepare a dedicated **play area** for each headset in use.

### Defining the Play Area

Each active VR station requires a minimum **2m × 2m (approximately 6.5ft × 6.5ft)** of clear floor space. This area must be:

- **Completely clear of furniture**, bags, cables, and any tripping hazards
- **Away from walls**, windows, and sharp-edged furniture (students may step or reach toward objects they see in VR)
- **Marked or delineated** so students know where to stand and where not to walk—blue painter's tape on the floor works well for this purpose

!!! warning "Critical Safety Note"
    Students wearing the headset cannot see the real world. A tripping hazard that seems minor in a normal classroom becomes a genuine fall risk during a VR session. Clear the area thoroughly.

#### Setting up the Virtual Boundary

Once the physical space is cleared, you need to configure the virtual boundary within the headset to match your designated play area. The Meta Quest boundary system warns users if they step too close to the edge of the safe zone.

1. Put on the headset and power it on.
2. If prompted automatically, follow the on-screen instructions to create a Roomscale boundary.
3. Trace the boundary to encompass the safe, cleared space you prepared earlier.
4. If you need to redraw or reset the boundary later, navigate to **Quick Settings > Boundary** in the headset's main menu.

For comprehensive instructions on drawing and managing the virtual boundary, refer to the [Meta Quest Help Center: Set up boundaries for Meta Quest](https://www.meta.com/help/quest/463504908043519/).

### Classroom Lighting

- Avoid **direct bright windows** behind or in front of the student—reflections can interfere with the headset's internal tracking cameras
- **Standard indoor lighting** is ideal
- If your classroom has harsh overhead flickering lights (older fluorescent fixtures), consider turning some off—this won't affect VR quality but improves comfort
- **Do not use the session in complete darkness**; ambient light helps the headset's inside-out tracking system

### Noise Considerations

The VR environment uses **voice input**—the student's microphone picks up their speech and the AI responds. Background noise can interfere with voice recognition accuracy.

- Try to conduct sessions in a **quieter part of the classroom** or a separate room if possible
- Alert other students or staff that a VR session is in progress and to minimize loud activity nearby
- If the room is inherently noisy, the student may need to **speak slightly more clearly and directly** toward the headset, but sessions generally still function in moderately noisy environments

---

## Required Hardware Inventory

### Core Hardware

| Item | Quantity per Station | Notes |
|------|---------------------|-------|
| **Meta Quest headset** (Quest 2, 3, or Pro) | 1 per active student | Quest 3 recommended for best clarity |
| **Meta Quest controllers** | 2 per headset (one pair) | Included with headset; keep stored with the headset |
| **Charging cable** (USB-C) | 1 per headset | Use the official cable that ships with the headset |
| **Power adapter** | 1 per charging cable | Use official adapter or equivalent 18W+ |
| **Wi-Fi connection** | Classroom access point | Must support the headset connecting to the internet |

### Recommended Optional Hardware

| Item | Purpose | Notes |
|------|---------|-------|
| **Laptop or tablet (for casting)** | Allows instructor to see what the student sees in VR | Cast with the Meta Horizon app or via the headset's Casting menu |
| **External display or TV monitor** | Projects the student's VR view to the whole class | Very effective for group discussion/observation |
| **Replacement foam face gaskets** | Hygiene between students | Standard Meta Quest replacement foam faceplates are inexpensive |
| **Lens cleaning wipes** | Clean headset lenses between students | Use lens-safe wipes only; never standard paper towels |
| **Hand sanitizer** | Hygiene for controllers | Before and after each student use |

### DeVILStarter Laptop

**DeVILStarter** is the companion desktop application used to start and stop the cloud backend. You will need one **Windows laptop** running DeVILStarter nearby (it does not need to be in the play area).

- Operating System: **Windows 10 or 11**
- Internet connection: Yes (it communicates with AWS)
- For setup instructions, see: [Running a Session](running-a-session.md)

---

## Charging & Battery Management

Meta Quest headsets have a battery life of approximately **2–3 hours** under active VR use with Wi-Fi and AI processing. Proper battery management is essential for back-to-back class sessions.

### Before Each Class Session

**At least 2 hours before class, check all headsets:**

1. Power on each headset briefly by pressing the power button on the right side
2. Check the battery indicator in the top-right corner of the home screen
3. All headsets should be **above 80% charge** before class begins
4. If any headset is below 80%, charge it immediately—a headset at 50% may die mid-session

### Charging Procedure

1. Connect the USB-C cable to the side of the headset
2. Connect the other end to the power adapter (or a powered USB port—use at least 18W for reasonable charging speed)
3. A solid orange LED on the right side of the headset indicates charging; **green** indicates fully charged

!!! note "Pro Tip"
    Turn headsets **completely off** when not in use (hold power button → Power Off). A headset left in sleep/standby mode drains the battery significantly faster.

### Quick-Charge Strategy for Back-to-Back Classes

If you have classes back-to-back (e.g., two sections of FSE100 in one morning):

- Plug headsets in **immediately** after the first session ends
- Meta Quest supports **fast charging** when using the official 18W+ adapter
- A 30-minute charge can recover approximately **20–30%** battery on a Quest 3
- If you have spare headsets, rotate them: charge one set while using another

### Controller Battery Management

Controllers rely on **AA batteries** or built-in USB-C ports for power, depending on your headset model.

- Quest 2 controllers: Keep a supply of **AA Energizer or Duracell** alkaline batteries and replace them as needed. The controller's exposed battery compartment can be cleaned with alcohol-free wipes before removing batteries.
- Quest 3 controllers: Each controller has a **built-in USB-C port** for direct battery charging. Remove the AA batteries before using USB-C to charge the internal batteries. Recharge in a well-ventilated area while not worn. Controllers do not support official USB-C charging docks from Meta; use the built-in controller charging port instead.

---

## Sanitation Protocols

Multiple students will use the same headsets during a lab session. Proper hygiene between uses is both a health consideration and an important care practice for expensive equipment.

### Between-Student Cleaning (during the session)

After each student finishes their session:

1. **Remove the face gasket** (the foam ring around the face opening). For routine cleaning, gently wipe it with a dry or slightly damp microfiber cloth to remove surface debris and sweat. For sanitization between students, use alcohol-free disinfecting wipes designed for sensitive electronics. **Do not use alcohol-based products on any facial interface component**, as alcohol can damage the foam material over time ([per Meta official cleaning guidelines](https://www.meta.com/help/quest/467048561217367/)).
2. **Wipe the controllers** with a hand sanitizer wipe or mild disinfectant wipe. Pay attention to the grip areas and buttons. Avoid getting moisture in the battery compartments or controller ports.
3. **Do not touch the lenses** unless they are visibly smudged. If cleaning is needed, use only a **clean microfiber cloth**—never paper towels, tissues, or alcohol-based products directly on the lens.

### Deep Cleaning (after each class day)

1. Remove the foam face gasket (it clips or velcros off on most Quest models) and hand wash it with cool water and mild liquid detergent in a bowl. Rinse thoroughly to remove soap residue. **Do not submerge** the gasket or expose it to running water. Allow it to **fully air dry** before reattaching—damp foam against the face is uncomfortable and can damage the gasket over time. Per [Meta official cleaning guidelines](https://www.meta.com/help/quest/467048561217367/), hand washing with mild detergent is the recommended cleaning method for facial interface components.
2. Wipe the headset's exterior housing with a **dry or slightly damp** cloth. Avoid getting liquid near charging ports or speaker grilles.
3. Check controller grips for any accumulated dirt in the button recesses; use a dry toothbrush or compressed air to clear them. Use alcohol-free disinfecting wipes if sanitizing controller surfaces.

### Replacement Foam Gaskets

For high-frequency use (multiple sessions per day), consider purchasing replacement foam face gaskets. They are available from Meta's official store and third-party manufacturers for approximately $10–$20 per set.

- Replace foam gaskets when they show signs of **tearing, significant compression, or persistent odor** that does not resolve with cleaning.

### Students with Glasses

Many Meta Quest headsets include a **glasses spacer** that creates extra room between the lenses and the user's face. Ensure this spacer is installed before any student who wears glasses uses the headset. Inserting the headset **without the spacer** when wearing glasses can cause lens-to-glass contact that scratches both the VR lenses and the student's eyeglasses.

!!! note
    💡 **Note for students with prescription glasses:** Students with mild prescriptions (up to approximately ±3.0 diopters) can often use the headset comfortably without their glasses by adjusting the IPD (interpupillary distance) slider on the bottom of the headset. However, this varies by individual. Always check with the student first.

---

## Next Steps

Now that your physical space is ready, proceed to the session launch guide:

➡️ **[Running a Session](running-a-session.md)**
