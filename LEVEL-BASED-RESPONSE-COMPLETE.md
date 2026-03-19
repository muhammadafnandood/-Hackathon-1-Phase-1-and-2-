# Level-Based Response Tone - Complete

## ✅ Changes Made

### 1. Frontend - Get User Level from Profile

**File Modified:** `physical-ai-book/src/components/Chatbot/index.tsx`

**Changes:**
- Added `userLevel` prop to Chatbot component
- Reads user's `experience_level` from localStorage
- Maps to appropriate level: Beginner, Student, Engineer, Researcher
- Sends `user_level` to backend in API request

**Level Mapping:**
```typescript
const levelMap = {
  'beginner': 'Beginner',
  'intermediate': 'Student', 
  'advanced': 'Engineer',
  'expert': 'Researcher'
};
```

---

### 2. Backend - Adapt Response to User Level

**File Modified:** `backend/routes/chat.py`

**Changes:**
- Added `user_level` field to `ChatRequest` model
- Created level-specific instructions for 4 expertise levels
- Prompt adapts tone, depth, and examples based on level

---

## 🎯 Level-Specific Response Styles

### 🟢 Beginner Level

**Tone:**
- Simple, friendly language
- No jargon without explanation
- Everyday analogies
- Encouraging tone
- Short paragraphs

**Example Response:**
```
Imagine a robot arm like your own arm. Just like you have 
shoulders, elbows, and wrists, a robot arm has joints that 
let it move.

### 🔧 Key Features
• Moves like a human arm - has "shoulder", "elbow", "wrist"
• Can be programmed to repeat the same motion over and over
• Safe to work alongside humans (doesn't need safety cages)

### 💰 Price Information
• Small hobby arms: Rs. 15,000 - 50,000
  (Like toy versions but actually useful!)
• Educational arms: Rs. 5 - 10 lakh
  (What universities use for teaching)
• Industrial arms: Rs. 50 lakh+
  (What factories use for real work)

Don't worry if terms like "degrees of freedom" sound confusing - 
we'll explain them as we go!
```

---

### 🟡 Student Level

**Tone:**
- Clear academic language
- Assumes basic programming knowledge
- Includes math concepts (explained)
- Coursework examples
- Key takeaways

**Example Response:**
```
A robot manipulator is a programmable mechanical arm designed 
to perform tasks with precision and repeatability.

### 🔧 Key Features
• 6 Degrees of Freedom (6-DOF) - mimics human arm kinematics
• ±0.1mm repeatability - can return to same position accurately
• Payload: 3-6 kg for educational models

### 🧩 Main Parts/Components
• Base: Fixed mounting point with power connection
• Joints 1-3: Position the end effector in space (X, Y, Z)
• Joints 4-6: Control orientation (roll, pitch, yaw)
• End Effector: Tool mounting interface (gripper, welder, etc.)

### ⚡ Performance Specifications
• Reach: 500-850 mm
• Max Speed: 1 m/s (TCP)
• Repeatability: ±0.1 mm

### 💰 Price Information
• Educational (Dobot MG400): Rs. 3 - 5 lakh
• Research (UR3e): Rs. 65 - 75 lakh
• Complete lab setup: Rs. 1 - 1.5 crore

### 📚 Key Takeaways
✓ 6-DOF provides full positional and orientational control
✓ Repeatability ≠ Accuracy (important distinction!)
✓ Collaborative robots don't need safety fencing
```

---

### 🟠 Engineer Level

**Tone:**
- Professional technical language
- Assumes engineering fundamentals
- Implementation details
- Industry best practices
- Trade-off discussions

**Example Response:**
```
The UR3e is a collaborative robot manipulator from Universal 
Robots, designed for light assembly and precision tasks.

### 🔧 Key Features
• Collaborative design - ISO 10218-1 certified for safe human 
  interaction without safety fencing (after risk assessment)
• Force control - built-in torque sensors in all joints
• Easy integration - Modbus TCP, RTU, digital/analog I/O
• Quick change tool mounting - automatic tool changer compatible

### 🧩 Main Parts/Components
• Base Module: Power distribution, safety circuits, Ethernet
• Shoulder/Elbow/Wrist: Harmonic drive gears, brushless DC 
  motors with torque sensing
• Controller: CB3 or e-Series, runs modified Ubuntu Linux
• Teach Pendant: Polyscope GUI (proprietary, intuitive)

### ⚡ Performance Specifications
• Reach: 500 mm (UR3e)
• Payload: 3 kg (wrist down), 2 kg (wrist up)
• Repeatability: ±0.03 mm (wrist down)
• Joint Range: J1/J2/J4/J5/J6: ±360°, J3: ±180°
• Power: 24V DC, 200W typical, 500W peak

### 💰 Price Information
• UR3e Arm Only: Rs. 65 - 75 lakh
• Complete System (arm + controller + software): Rs. 85 lakh - 1 crore
• Integration (grippers, vision, safety): Rs. 15 - 30 lakh additional
• Annual Support Contract: Rs. 5 - 8 lakh

### ⚠️ Common Pitfalls
• Payload calculations must include end effector weight
• Cable management critical for continuous rotation
• EMI shielding needed near welding equipment

### 📚 Related Concepts
• Denavit-Hartenberg parameters for kinematic modeling
• Trajectory planning (trapezoidal vs S-curve velocity profiles)
• Force-torque sensing for compliant control
```

---

### 🔴 Researcher Level

**Tone:**
- Advanced technical/academic language
- Assumes deep domain knowledge
- State-of-the-art developments
- Research paper references
- Open problems discussion

**Example Response:**
```
Collaborative manipulators represent a significant advancement 
in human-robot interaction, with applications ranging from 
assembly to surgical assistance.

### 🔧 Key Features
• Intrinsic safety via torque sensing and collision detection
  - Power and force limiting per ISO/TS 15066
  - Dual-channel safety rated monitoring (PL d, Cat. 3)
• Compliance control for delicate assembly operations
  - Impedance control bandwidth: ~10 Hz
  - Force resolution: ±0.5 N

### 🧩 Main Parts/Components
• Actuation: Frameless torque motors with harmonic drives
  - Gear ratio: 1:100 to 1:160
  - Backlash: <1 arcmin
• Sensing: Joint torque sensors (strain gauge based)
  - Resolution: 0.1 Nm
  - Sampling: 1 kHz
• Computation: Real-time kernel (RT-PREEMPT Linux)
  - Control loop: 8 ms cycle time

### ⚡ Performance Specifications
• Kinematic Calibration: DH parameters with uncertainty bounds
• Dynamic Performance:
  - Max joint velocity: 180°/s
  - Max joint acceleration: 300°/s²
  - End-effector speed: 1 m/s (typical)
• Positioning Uncertainty: 
  - Repeatability (ISO 9283): ±0.03 mm
  - Absolute accuracy (after calibration): ±0.5 mm

### 💰 Price Information
• Research Platform (UR3e + Robotiq gripper): Rs. 80 lakh - 1 crore
• Force-Torque Sensor (Robotiq FT 300): Rs. 8 - 10 lakh
• Vision System (Realsense D435 + mounting): Rs. 60,000
• Complete Research Cell: Rs. 1.5 - 2.5 crore

### 📚 Related Research Areas
• Learning from Demonstration (LfD) via kinesthetic teaching
  - Recent work: "Deep Imitation Learning for Bimanual Manipulation" (Science Robotics 2023)
• Adaptive impedance control for uncertain environments
  - "Variable Impedance Control" (IEEE T-RO 2022)
• Human intent prediction for proactive collaboration
  - Open problem: Real-time motion prediction with <100ms latency

### 🔬 Experimental Considerations
• For reproducible research:
  - Report DH parameters with uncertainty bounds
  - Specify controller gains and sampling rates
  - Include force-torque sensor calibration procedure
• Benchmark tasks:
  - Peg-in-hole (ISO standard)
  - Pick-and-place cycle time
  - Collaborative assembly task
```

---

## 📁 Files Modified

| File | Changes |
|------|---------|
| `physical-ai-book/src/components/Chatbot/index.tsx` | Added userLevel prop, reads from localStorage |
| `backend/routes/chat.py` | Added user_level field, level-specific prompts |

---

## 🧪 Testing

### Test 1: Beginner User
```
1. Login as beginner level user
2. Ask: "What is a robot arm?"
3. Verify: Simple language, analogies, encouraging tone
```

### Test 2: Student User
```
1. Login as intermediate/student level
2. Ask: "Explain inverse kinematics"
3. Verify: Math included but explained, academic tone
```

### Test 3: Engineer User
```
1. Login as advanced/engineer level
2. Ask: "How to integrate UR5 with ROS 2?"
3. Verify: Technical details, best practices, debugging tips
```

### Test 4: Researcher User
```
1. Login as expert/researcher level
2. Ask: "State-of-the-art in compliant manipulation"
3. Verify: Research references, SOTA, open problems
```

---

## 🎯 Level Comparison

| Aspect | Beginner | Student | Engineer | Researcher |
|--------|----------|---------|----------|------------|
| **Jargon** | Avoid/Explain | Use + Explain | Assume known | Advanced terms |
| **Math** | None/Minimal | Include + Explain | Use freely | Formulations |
| **Examples** | Everyday life | Coursework | Industry | Research papers |
| **Depth** | Big picture | Theory + Practice | Implementation | SOTA + Open problems |
| **Tone** | Friendly, encouraging | Academic | Professional | Academic/Technical |
| **Length** | Short, digestible | Medium | Detailed | Comprehensive |

---

## ✅ Benefits

1. **Personalized Learning**
   - Each user gets content at their level
   - No overwhelming beginners
   - No boring experts

2. **Better Engagement**
   - Beginners feel supported
   - Experts get depth they need

3. **Efficient Communication**
   - No unnecessary explanations for experts
   - No confusing jargon for beginners

4. **Pakistani Context**
   - PKR pricing for all levels
   - Local market availability mentioned

---

<div align="center">

**Level-Based Responses Complete! 🎯**

Chatbot now adapts to:
✅ Beginner (simple, friendly)
✅ Student (academic, explained)
✅ Engineer (technical, practical)
✅ Researcher (advanced, SOTA)

</div>
