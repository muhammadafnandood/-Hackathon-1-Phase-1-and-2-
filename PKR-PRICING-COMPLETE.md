# Pakistani Rupees (PKR) Pricing - Complete

## ✅ Changes Made

### 1. Updated Chatbot Prompt for PKR

**File Modified:** `backend/routes/chat.py`

**Price Format Changed:**
```python
# Before (USD):
- Budget option: $500 - basic models
- Mid-range: $5,000 - research models
- High-end: $74,000 - industrial grade

# After (PKR):
- Budget option: Rs. 1.4 lakh - basic models
- Mid-range: Rs. 14 lakh - research models
- High-end: Rs. 2 crore - industrial grade
```

**Conversion Rate:**
- 1 USD ≈ 280 PKR (approximate)
- Uses Pakistani numbering: lakh (100,000), crore (10,000,000)

---

### 2. Updated Price Formatting

**File Modified:** `physical-ai-book/src/components/Chatbot/AnswerCard.tsx`

**New Regex Patterns:**
```typescript
// Matches: Rs. 1000, Rs 50000, PKR 100000
.replace(/Rs\.?\s*([\d,]+(?:\s+(?:lakh|crore))?)?/gi, '<span class="price">Rs. $1</span>')
.replace(/PKR\s*([\d,]+)/gi, '<span class="price">PKR $1</span>')
.replace(/(\d+)\s*lakh/gi, '<span class="price">$1 lakh</span>')
.replace(/(\d+)\s*crore/gi, '<span class="price">$1 crore</span>')
```

**Visual Styling:**
- Prices shown in green gradient
- Pakistani numbering format (lakh, crore)
- Clear, highlighted display

---

## 💰 Price Conversion Examples

### Small Robots/Sensors

| Item | USD | PKR (Converted) |
|------|-----|-----------------|
| Arduino Uno | $25 | Rs. 7,000 |
| Raspberry Pi 4 | $55 | Rs. 15,400 |
| RPLIDAR A1 | $95 | Rs. 26,600 |
| ESP32 Camera | $10 | Rs. 2,800 |
| Servo Motor SG90 | $2 | Rs. 560 |

### Medium Robots

| Item | USD | PKR (Converted) |
|------|-----|-----------------|
| DJI Tello Drone | $99 | Rs. 27,700 |
| MakeX Robot Kit | $300 | Rs. 84,000 |
| Universal Robots UR5 (used) | $25,000 | Rs. 70 lakh |
| Intel RealSense D435i | $199 | Rs. 55,700 |
| NVIDIA Jetson Nano | $149 | Rs. 41,700 |

### High-End Robots

| Item | USD | PKR (Converted) |
|------|-----|-----------------|
| Boston Dynamics Spot | $74,000 | Rs. 2 crore |
| Universal Robots UR5e (new) | $39,900 | Rs. 1.1 crore |
| Velodyne VLP-16 LiDAR | $4,000 | Rs. 11.2 lakh |
| Ouster OS0-64 LiDAR | $6,500 | Rs. 18.2 lakh |
| KUKA KR6 Robot | $50,000 | Rs. 1.4 crore |

---

## 🎯 Example Chatbot Responses

### Example 1: Arduino Question

**User:** "What is Arduino Uno?"

**Chatbot:**
```
🧠 Additional Information:

Arduino Uno is a popular microcontroller board for electronics projects.

### 🔧 Key Features
• ATmega328P microcontroller
• 14 digital I/O pins
• 6 analog inputs
• USB interface for programming
• Breadboard-friendly design

### 🧩 Main Parts/Components
• Microcontroller: ATmega328P (brain)
• USB Interface: CH340G or ATmega16U2
• Voltage Regulator: 5V output
• I/O Pins: Digital and analog
• Power Jack: 7-12V input
• Crystal Oscillator: 16 MHz

### ⚡ Performance Specifications
• Operating Voltage: 5V
• Input Voltage: 7-12V (recommended)
• Clock Speed: 16 MHz
• Flash Memory: 32 KB
• SRAM: 2 KB
• EEPROM: 1 KB
• Weight: 25 grams

### 💰 Price Information
• Original Arduino (Italy): Rs. 3,500 - 4,500
• Chinese Clone: Rs. 800 - 1,500
• Pakistani Local: Rs. 1,200 - 2,000
• Available at: Hall Road (Lahore), Techno City (Karachi)

### 📚 Related Concepts
• Microcontroller programming
• Digital vs analog signals
• Pulse Width Modulation (PWM)
```

---

### Example 2: Drone Question

**User:** "Tell me about quadcopter drones"

**Chatbot:**
```
🧠 Additional Information:

A quadcopter is a drone with 4 rotors/motors.

### 🔧 Key Features
• VTOL (Vertical Take-Off and Landing)
• Stable hover capability
• Simple mechanical design
• Redundant lift (can lose 1 motor)
• Agile maneuvering

### 🧩 Main Parts/Components
• Frame: Carbon fiber or plastic (250-500mm)
• Motors: 4x Brushless DC motors (2200-2300KV)
• ESCs: 4x Electronic Speed Controllers (30A)
• Propellers: 2 CW + 2 CCW (10-inch)
• Flight Controller: F4 or F7 processor
• Battery: 3S or 4S LiPo (1500-2200mAh)
• Radio: 2.4GHz transmitter/receiver

### ⚡ Performance Specifications
• Flight Time: 15-25 minutes
• Max Speed: 60-80 km/h
• Control Range: 500m - 2km
• Payload: 200-500 grams
• Weight: 400-800 grams
• Charging Time: 60-90 minutes

### 💰 Price Information
• Toy Grade (no camera): Rs. 3,000 - 8,000
• Hobby Grade (with camera): Rs. 15,000 - 40,000
• Professional (4K camera): Rs. 80,000 - 2.5 lakh
• DJI Mini 2: Rs. 65,000 - 75,000
• DJI Air 2S: Rs. 1.2 - 1.5 lakh
• Custom Build: Rs. 25,000 - 50,000

### 📚 Related Concepts
• Gyroscopes and accelerometers
• PID control algorithms
• FPV (First Person View)
• LiPo battery safety
```

---

### Example 3: Industrial Robot Arm

**User:** "What is a 6-axis robot arm?"

**Chatbot:**
```
🧠 Additional Information:

A 6-axis robot arm has 6 degrees of freedom for industrial automation.

### 🔧 Key Features
• Full 6-DOF movement (like human arm)
• High precision and repeatability
• Programmable paths
• Payload: 3-20 kg typical
• Reach: 500-1400 mm
• Collaborative or caged operation

### 🧩 Main Parts/Components
• Base: Mounting and power connection
• Axis 1-3: Positioning (shoulder, elbow)
• Axis 4-6: Orientation (wrist roll, pitch, yaw)
• Servo Motors: 6x AC or DC servos
• Gearboxes: Harmonic drive or planetary
• Controller: Industrial PC with teach pendant
• End Effector: Gripper, welder, or tool

### ⚡ Performance Specifications
• Repeatability: ±0.02 to ±0.1 mm
• Max Speed: 1-2 m/s (TCP)
• Payload: 3 kg, 6 kg, 12 kg, 20 kg options
• Reach: 550 mm to 1400 mm
• Weight: 25-75 kg (arm only)
• Power: 0.5 - 2 kW

### 💰 Price Information
• Chinese Brands (Inovance, Estun): Rs. 8 - 15 lakh
• Universal Robots (UR3e): Rs. 65 - 75 lakh
• Universal Robots (UR5e): Rs. 1.1 - 1.3 crore
• ABB/Fanuc/KUKA: Rs. 1.5 - 3 crore
• Complete Cell (with safety): Rs. 2 - 5 crore
• Used/Refurbished: Rs. 5 - 10 lakh

### 📚 Related Concepts
• Forward and inverse kinematics
• Trajectory planning
• Collaborative robots (cobots)
• Machine vision integration
```

---

### Example 4: LiDAR Sensor

**User:** "What is LiDAR and how much does it cost?"

**Chatbot:**
```
🧠 Additional Information:

LiDAR (Light Detection and Ranging) uses laser pulses for 3D mapping.

### 🔧 Key Features
• 360-degree scanning
• Distance measurement up to 100-200m
• Creates 3D point clouds
• Works day and night
• High accuracy (±2-3 cm)

### 🧩 Main Parts/Components
• Laser Transmitter: 905nm or 1550nm laser
• Scanner: Rotating mirror or MEMS
• Receiver: Avalanche photodiode
• Timing Circuit: Time-of-flight measurement
• GPS/IMU: For mobile mapping
• Processor: Point cloud generation

### ⚡ Performance Specifications
• Range: 25-200 meters
• Accuracy: ±2-3 cm
• Scan Rate: 10-20 Hz
• Points/Second: 300,000 - 2 million
• Field of View: 360° horizontal
• Power: 5-15 watts
• Weight: 0.5-1.5 kg

### 💰 Price Information
• 2D LiDAR (RPLIDAR A1): Rs. 25,000 - 35,000
• 2D LiDAR (SICK, Hokuyo): Rs. 1.5 - 3 lakh
• 3D LiDAR (Velodyne VLP-16): Rs. 12 - 15 lakh
• 3D LiDAR (Ouster OS0): Rs. 8 - 12 lakh
• 3D LiDAR (Hesai Pandar): Rs. 10 - 18 lakh
• Automotive Grade: Rs. 25 - 50 lakh
• Survey Grade (Leica): Rs. 50 lakh - 1.5 crore

### 📚 Related Concepts
• SLAM (Simultaneous Localization and Mapping)
• Point cloud processing
• Sensor fusion
• Autonomous navigation
```

---

## 📁 Files Modified

| File | Changes |
|------|---------|
| `backend/routes/chat.py` | Prompt updated for PKR pricing |
| `physical-ai-book/src/components/Chatbot/AnswerCard.tsx` | PKR price formatting |

---

## 🇵🇰 Pakistani Pricing Format

**Numbering System:**
- 1 Lakh = 100,000 (1,00,000)
- 1 Crore = 10,000,000 (1,00,00,000)

**Examples:**
- Rs. 50,000 = 50 thousand
- Rs. 1,50,000 = 1.5 lakh
- Rs. 15,00,000 = 15 lakh
- Rs. 2,00,00,000 = 2 crore

**Display Format:**
```
Rs. 1,200         (small amounts)
Rs. 15,000        (medium amounts)
Rs. 1.5 lakh      (lakhs)
Rs. 2 crore       (crores)
```

---

## ✅ Benefits

1. **Local Context**
   - Pakistani students understand prices better
   - Lakh/crore format familiar to locals

2. **Accurate Budgeting**
   - Real PKR prices for planning
   - Includes local market options

3. **Shopping Guidance**
   - Mentions Pakistani markets (Hall Road, Techno City)
   - Includes Chinese vs original price comparison

4. **Practical Information**
   - Conversion rate: 1 USD ≈ 280 PKR
   - Includes used/refurbished options

---

<div align="center">

**Pakistani Rupees Pricing Complete! 🇵🇰**

All prices now shown in:
✅ PKR (Rs.)
✅ Lakh/Crore format
✅ Local market availability
✅ Chinese vs Original comparison

</div>
