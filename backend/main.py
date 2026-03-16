from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import hashlib
import re

app = FastAPI(title="AI Tutor Backend", version="1.0.0")

# CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory user database (for demo/development)
users_db: Dict[str, Dict[str, Any]] = {}

# Pydantic models for request validation
class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    """Hash password using SHA-256 (for demo only - use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/")
def home():
    """Home endpoint"""
    return {
        "message": "AI Tutor for Robotics - Backend API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-tutor-backend"
    }

@app.post("/auth/register")
def register(data: RegisterRequest):
    """
    Register a new user
    """
    try:
        # Validate email format
        if "@" not in data.email or "." not in data.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Validate password length
        if len(data.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
        
        # Check if user already exists
        if data.email in users_db:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Create user with hashed password
        user_id = str(uuid.uuid4())
        users_db[data.email] = {
            "id": user_id,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
            "password_hash": hash_password(data.password),
            "created_at": str(uuid.uuid4())
        }
        
        return {
            "status": "success",
            "message": "User registered successfully",
            "user": {
                "id": user_id,
                "email": data.email,
                "first_name": data.first_name,
                "last_name": data.last_name
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/auth/login")
def login(data: LoginRequest):
    """
    Login user and return access token
    """
    try:
        # Validate email format
        if "@" not in data.email or "." not in data.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Check if user exists
        if data.email not in users_db:
            # Auto-register new users for demo purposes
            user_id = str(uuid.uuid4())
            users_db[data.email] = {
                "id": user_id,
                "first_name": data.email.split('@')[0],
                "last_name": "User",
                "email": data.email,
                "password_hash": hash_password(data.password),
                "created_at": str(uuid.uuid4())
            }
        else:
            # Verify password
            user = users_db[data.email]
            if user["password_hash"] != hash_password(data.password):
                raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user = users_db[data.email]
        
        # Generate access token
        access_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.{user['id']}.{uuid.uuid4()}"
        
        return {
            "status": "success",
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/auth/me")
def get_current_user():
    """Get current user profile (placeholder - add JWT validation in production)"""
    return {
        "message": "User profile endpoint",
        "note": "Add JWT token validation for production use"
    }

@app.post("/auth/logout")
def logout():
    """Logout user (client should remove token)"""
    return {
        "status": "success",
        "message": "Logged out successfully"
    }

@app.post("/api/translate/urdu")
def translate_to_urdu(data: dict):
    """
    Translate text to Urdu (simple translation for demo)
    In production, use Google Translate API or similar
    """
    text = data.get("text", "")

    # Simple Urdu translations for common phrases
    translations = {
        "welcome back": "خوش آمدید",
        "how can i help you today": "میں آج آپ کی کیسے مدد کر سکتا ہوں؟",
        "ai explanation": "AI وضاحت",
        "great question": "بہترین سوال",
        "ros 2": "ROS 2",
        "node": "نوڈ",
        "nodes": "نوڈز",
        "topic": "ٹاپک",
        "topics": "ٹاپکس",
        "service": "سروس",
        "services": "سروسز",
        "action": "ایکشن",
        "actions": "ایکشنز",
        "middleware": "مڈل ویئر",
        "communication": "مواصلات",
        "robot": "روبوٹ",
        "robotics": "روبوٹکس",
        "system": "سسٹم",
        "data": "ڈیٹا",
        "message": "پیغام",
        "publish": "پبلش",
        "subscribe": "سبسکرائب",
    }

    # Simple word-by-word translation
    translated = text.lower()
    for english, urdu in translations.items():
        translated = translated.replace(english, urdu)

    # For demo, return a mix of Urdu and English
    # In production, use actual translation API
    return {
        "status": "success",
        "translated_text": text,  # Return original for now
        "note": "For full Urdu translation, integrate Google Translate API or similar"
    }

# Book content database
BOOK_CONTENT = {
    "ros2": {
        "chapter": 1,
        "title": "Introduction to ROS 2",
        "content": """ROS 2 (Robot Operating System 2) is a set of software libraries and tools for building robot applications. 
        It uses a publish-subscribe model for communication between nodes. This decentralized architecture makes ROS 2 highly 
        scalable and suitable for complex robotic systems.
        
        Key Concepts:
        - Nodes: Independent processes that perform specific tasks
        - Topics: Named channels for message exchange
        - Services: Request-response communication
        - Actions: Long-running tasks with feedback
        - DDS: Middleware protocol for distributed systems""",
        "keywords": ["ros 2", "robot operating system", "nodes", "topics", "services", "actions", "dds", "publish", "subscribe"]
    },
    "physical_ai": {
        "chapter": 2,
        "title": "Physical AI Fundamentals",
        "content": """Physical AI refers to artificial intelligence systems that interact with the physical world through 
        sensors and actuators. Unlike traditional AI that operates purely in digital domains, Physical AI must understand 
        and manipulate real-world objects and environments.
        
        Key Components:
        - Perception: Gathering information through sensors
        - Cognition: Processing data and making decisions
        - Action: Executing physical movements""",
        "keywords": ["physical ai", "sensors", "actuators", "perception", "cognition", "robotics"]
    },
    "humanoid": {
        "chapter": 3,
        "title": "Humanoid Robotics",
        "content": """Humanoid robots are robots that resemble the human body in shape and structure. They typically have 
        a head, torso, two arms, and two legs, mimicking human anatomy to enable human-like movement and interaction.
        
        Robot Parts & Components:
        - Head: Cameras (Intel RealSense D435 - $150), Microphones
        - Torso: Main computer (NVIDIA Jetson AGX - $7000), Battery (48V Li-ion - $500)
        - Arms: 6-DOF manipulators (Dynamixel servos - $200 each), Grippers (Robotiq 2F-85 - $3500)
        - Legs: Linear actuators (Actuator L12 - $150 each), Force sensors (ATI Mini45 - $2000)
        - Joints: High-torque motors (Maxon EC-i 52 - $800 each), Harmonic drives ($1500 each)
        
        Performance Specifications:
        - Walking Speed: 0-3 km/h
        - Payload Capacity: 5-20 kg
        - Battery Life: 2-4 hours
        - Operating Time: 8-12 hours with battery swap
        
        Benefits:
        - Can operate in human environments
        - Use existing tools and infrastructure
        - Natural human-robot interaction
        
        Challenges/Defects:
        - High cost ($50,000 - $200,000)
        - Complex balance control
        - Limited battery life
        - Maintenance intensive
        
        Where to Buy Parts:
        - RobotShop (www.robotshop.com)
        - DigiKey (www.digikey.com)
        - Mouser Electronics (www.mouser.com)
        - Amazon Industrial (www.amazon.com/industrial)
        - Local distributors: Pakistan - RoboPakistan, India - Robu.in""",
        "keywords": ["humanoid", "robot", "parts", "components", "motors", "sensors", "actuators", "price", "cost", "buy"]
    },
    "sensors": {
        "chapter": 4,
        "title": "Sensors and Perception",
        "content": """Sensors are the eyes, ears, and skin of robots. They provide the raw data that perception systems 
        process to understand the environment.
        
        Types of Sensors with Prices:
        
        1. Cameras:
           - RGB Camera: Intel RealSense D435 ($150) - Depth sensing
           - Stereo Camera: ZED 2 ($449) - 3D vision
           - Event Camera: Prophesee EVK4 ($2000) - High-speed detection
           - Thermal Camera: FLIR Lepton 3.5 ($200) - Heat detection
           
        2. LiDAR:
           - 2D LiDAR: RPLidar A3 ($400) - 25m range
           - 3D LiDAR: Velodyne VLP-16 ($4000) - 100m range
           - Solid State: Ouster OS1 ($6000) - High resolution
           
        3. IMU (Inertial Measurement Unit):
           - MPU6050 ($10) - Basic orientation
           - XSens MTi-300 ($3000) - High precision
           
        4. Force/Torque Sensors:
           - ATI Mini45 ($2000) - Wrist mounting
           - Robotiq FT 300 ($3500) - High accuracy
           
        5. Proximity Sensors:
           - Ultrasonic: HC-SR04 ($5) - Short range
           - IR: Sharp GP2Y0A21 ($8) - Medium range
           
        Performance Comparison:
        - Accuracy: LiDAR > Stereo Camera > RGB Camera
        - Range: LiDAR (100m) > Camera (30m)
        - Cost: Camera ($) < LiDAR ($$$)
        
        Where to Buy:
        - SparkFun (www.sparkfun.com)
        - Adafruit (www.adafruit.com)
        - DigiKey (www.digikey.com)
        - Mouser (www.mouser.com)
        - Local: RoboPakistan (Lahore), ElectroOptics (Karachi)""",
        "keywords": ["sensors", "camera", "lidar", "imu", "perception", "vision", "price", "cost", "buy", "range"]
    },
    "motion_planning": {
        "chapter": 5,
        "title": "Motion Planning and Control",
        "content": """Motion planning is the process of finding a sequence of movements that takes a robot from its 
        current state to a desired goal while avoiding obstacles.
        
        Approaches:
        - Sampling-based planning (RRT, PRM)
        - Optimization-based planning
        - Control methods (PID, MPC)
        
        Actuators & Motors (with prices):
        
        1. Servo Motors:
           - Dynamixel AX-12A ($120) - 12kg.cm torque
           - Dynamixel XM430-W350 ($290) - 41kg.cm torque
           - Futaba S9151 ($250) - High speed
           
        2. Stepper Motors:
           - NEMA 17 ($20) - 3D printers
           - NEMA 23 ($50) - Medium robots
           - NEMA 34 ($150) - Large robots
           
        3. DC Motors:
           - Maxon EC-i 52 ($800) - High precision
           - Faulhaber 2232 ($150) - Compact
           - Pololu 37D ($35) - Budget option
           
        4. Linear Actuators:
           - Actuator L12 ($150) - 100mm stroke
           - Firgelli L16 ($100) - 200mm stroke
           
        5. Motor Drivers:
           - ODrive v3.6 ($140) - Dual motor control
           - SimpleFOC Shield ($25) - Budget FOC
           
        Performance Metrics:
        - Torque: 0.1-100 Nm (small to large robots)
        - Speed: 10-10000 RPM
        - Precision: 0.01-1 degree
        - Efficiency: 70-95%
        
        Benefits:
        - Precise control
        - Smooth movements
        - Energy efficient
        
        Common Issues:
        - Motor overheating
        - Backlash in gears
        - Encoder noise""",
        "keywords": ["motion", "planning", "control", "motors", "actuators", "servo", "stepper", "price", "torque", "speed"]
    },
    "machine_learning": {
        "chapter": 6,
        "title": "Machine Learning for Robotics",
        "content": """Machine learning enables robots to learn from experience rather than being explicitly programmed.
        
        Learning Approaches:
        - Supervised Learning: Training on labeled data
        - Reinforcement Learning: Learning through rewards
        - Imitation Learning: Learning from demonstrations
        
        Hardware for ML (with prices):
        
        1. Edge AI Computers:
           - NVIDIA Jetson AGX Orin ($2000) - 275 TOPS
           - NVIDIA Jetson Nano ($150) - Entry level
           - Google Coral Dev Board ($150) - TPU加速
           - Intel NUC ($500-1500) - General purpose
           
        2. GPUs for Training:
           - NVIDIA RTX 4090 ($1600) - Consumer flagship
           - NVIDIA A100 ($10000) - Data center
           - AMD RX 7900 XTX ($1000) - Alternative
           
        3. AI Accelerators:
           - Google Coral USB ($75) - Portable TPU
           - Intel Neural Compute Stick 2 ($80) - USB accelerator
           
        Performance:
           - Jetson AGX: Real-time object detection (60 FPS)
           - Jetson Nano: Basic ML (15-30 FPS)
           - RTX 4090: Training (10x faster than CPU)
        
        Benefits:
        - Adaptive behavior
        - Improved accuracy over time
        - Handle uncertainty
        
        Challenges:
        - Requires large datasets
        - Computationally expensive
        - Safety verification difficult
        
        Where to Buy:
        - NVIDIA Store (www.nvidia.com)
        - Amazon (www.amazon.com)
        - Seeed Studio (www.seeedstudio.com)""",
        "keywords": ["machine learning", "ml", "ai", "jetson", "gpu", "training", "inference", "price", "performance"]
    },
    "vla": {
        "chapter": 7,
        "title": "Vision-Language-Action Models",
        "content": """VLA models represent the cutting edge of robotics AI. These models combine visual perception, 
        language understanding, and action generation in a single unified system.
        
        Architecture:
        - Vision Encoder: Processes images (ViT, ResNet)
        - Language Encoder: Understands instructions (LLM, Transformer)
        - Action Head: Generates robot commands
        
        State-of-the-Art Models:
        - Google RT-2: Vision-language-action model
        - DeepMind GATO: Generalist agent
        - Tesla Optimus: Neural network control
        
        Hardware Requirements:
        - Training: 8x A100 GPUs ($80,000)
        - Inference: Jetson AGX ($2000)
        - Memory: 32GB+ RAM ($300)
        
        Performance:
        - Success Rate: 85-95% on trained tasks
        - Generalization: 60-80% on new tasks
        - Latency: 50-200ms per action
        
        Benefits:
        - Natural language control
        - Transfer learning capabilities
        - Multi-task learning
        
        Limitations:
        - Requires massive datasets
        - Safety concerns
        - Interpretability issues
        
        Applications:
        - Warehouse automation
        - Home assistance
        - Industrial manipulation""",
        "keywords": ["vla", "vision", "language", "action", "rt-2", "gato", "transformer", "llm", "multimodal"]
    },
    "system_integration": {
        "chapter": 8,
        "title": "System Integration",
        "content": """System integration is the process of combining all robot components into a cohesive system that 
        works reliably in real-world conditions.
        
        Integration Areas:
        - Hardware Integration
        - Software Integration
        - Testing and Validation
        - Deployment
        
        Complete Robot Build Cost Estimate:
        
        Budget Humanoid ($5,000):
        - Frame: Aluminum extrusions ($500)
        - Motors: 20x Dynamixel AX-12A ($2400)
        - Sensors: Basic IMU + Cameras ($300)
        - Computer: Raspberry Pi 4 ($100)
        - Battery: 24V LiPo ($200)
        - Misc: Cables, connectors ($500)
        
        Mid-Range Humanoid ($25,000):
        - Frame: Carbon fiber ($2000)
        - Motors: 30x Dynamixel XM430 ($8700)
        - Sensors: LiDAR + Depth cameras ($2000)
        - Computer: Jetson AGX ($2000)
        - Battery: 48V Li-ion ($1000)
        - Grippers: Robotiq 2F-85 ($3500)
        - Misc: ($5800)
        
        Research-Grade Humanoid ($150,000+):
        - Custom actuators ($50,000)
        - Force sensors ($10,000)
        - High-end computer ($15,000)
        - Safety systems ($20,000)
        - Integration labor ($55,000)
        
        Benefits of Integration:
        - Unified system
        - Better performance
        - Easier maintenance
        
        Common Issues:
        - Compatibility problems
        - Timing synchronization
        - Power distribution
        - Heat management
        
        Testing Checklist:
        - ✓ Unit tests for each component
        - ✓ Integration tests
        - ✓ Stress testing
        - ✓ Safety validation
        - ✓ Field testing""",
        "keywords": ["integration", "system", "deployment", "testing", "cost", "budget", "build", "assembly"]
    },
    "robot_parts": {
        "chapter": 0,
        "title": "Complete Robot Parts Guide",
        "content": """COMPREHENSIVE ROBOT PARTS GUIDE WITH PRICES
        
        1. STRUCTURAL COMPONENTS:
        
        Frames & Chassis:
        - Aluminum Extrusion (80/20): $50-200 per meter
        - Carbon Fiber Sheets: $100-500 per sheet
        - 3D Printed Parts (PLA): $20-100 per kg
        - Steel Frame: $100-300
        
        Fasteners:
        - Screw Kit (M3-M6): $30
        - Bearings (608ZZ): $5 each
        - Couplings: $15-50
        
        2. POWER SYSTEM:
        
        Batteries:
        - LiPo 3S 5000mAh: $50 (Turnigy)
        - Li-ion 18650 (3500mAh): $8 each (Panasonic)
        - LiFePO4 12V 100Ah: $300 (Battle Born)
        
        Power Management:
        - BEC (Battery Eliminator Circuit): $20
        - Power Distribution Board: $50
        - Voltage Regulator (LM2596): $5
        
        Charging:
        - LiPo Charger (iMAX B6): $50
        - Fast Charger: $100-300
        
        3. COMPUTING:
        
        Microcontrollers:
        - Arduino Uno: $25
        - Arduino Mega: $35
        - Teensy 4.0: $25
        - STM32 Nucleo: $20
        
        Single Board Computers:
        - Raspberry Pi 4 (4GB): $55
        - Raspberry Pi 5: $80
        - Orange Pi 5: $100
        
        AI Computers:
        - NVIDIA Jetson Nano: $150
        - NVIDIA Jetson Orin Nano: $500
        - NVIDIA Jetson AGX Orin: $2000
        
        4. SENSORS (Detailed):
        
        Vision:
        - Raspberry Pi Camera V2: $30
        - Arducam Stereo Camera: $100
        - Intel RealSense D435i: $180
        - ZED 2 Stereo Camera: $449
        - FLIR Thermal Camera: $200-2000
        
        Distance:
        - Ultrasonic HC-SR04: $5
        - LiDAR Lite v3: $100
        - RPLidar A1: $250
        - RPLidar A3: $400
        - Velodyne VLP-16: $4000
        
        Motion:
        - MPU6050 (IMU): $10
        - BNO055 (9-DOF): $35
        - XSens MTi-100: $1500
        
        Force:
        - Load Cell (10kg): $15
        - Force Sensitive Resistor: $20
        - ATI Mini45: $2000
        
        5. ACTUATORS:
        
        Servo Motors:
        - SG90 Micro Servo: $5 (9g, 1.6kg.cm)
        - MG996R Metal Gear: $15 (55g, 10kg.cm)
        - Dynamixel AX-12A: $120 (520g, 12kg.cm)
        - Dynamixel XM430-W350: $290 (165g, 41kg.cm)
        
        Stepper Motors:
        - NEMA 17: $20 (1.8°, 0.5Nm)
        - NEMA 23: $50 (1.8°, 2Nm)
        - NEMA 34: $150 (1.8°, 8Nm)
        
        Brushless DC Motors:
        - T-Motor MN4012: $100 (KV350)
        - Maxon EC-i 52: $800 (High precision)
        
        Linear Actuators:
        - Firgelli L12: $100 (100mm stroke)
        - Actuonix L16: $150 (200mm stroke)
        
        6. END EFFECTORS:
        
        Grippers:
        - 3D Printed Gripper: $20
        - Robotiq 2F-85: $3500
        - Schunk EGP 40: $5000
        - Soft Gripper (SoftRobotics): $2000
        
        Tools:
        - Welding Torch: $500
        - Screwdriver Attachment: $50
        - Suction Cup: $30
        
        7. WHEELS & LOCOMOTION:
        
        Wheels:
        - 65mm Omni Wheel: $25
        - 200mm Pneumatic Wheel: $50
        - Mecanum Wheel Set: $150
        
        Tracks:
        - Tank Track Set: $100
        
        Legs:
        - Quadruped Leg Kit: $500
        - Hexapod Leg Kit: $800
        
        WHERE TO BUY (Online):
        - RobotShop (www.robotshop.com) - Worldwide
        - DigiKey (www.digikey.com) - Electronics
        - Mouser (www.mouser.com) - Components
        - SparkFun (www.sparkfun.com) - Sensors
        - Adafruit (www.adafruit.com) - Electronics
        - Amazon Industrial (www.amazon.com/industrial)
        - AliExpress (www.aliexpress.com) - Budget options
        - eBay (www.ebay.com) - Used parts
        
        WHERE TO BUY (Pakistan):
        - RoboPakistan (Lahore) - www.robopakistan.com
        - ElectroOptics (Karachi)
        - TechSource (Islamabad)
        - RoboStore.pk
        
        WHERE TO BUY (India):
        - Robu.in (www.robu.in)
        - ElectronicsComp.com
        - Amazon.in
        
        BULK DISCOUNTS:
        - 10+ units: 10-15% discount
        - 50+ units: 20-25% discount
        - 100+ units: 30-35% discount
        
        SHIPPING:
        - DHL Express: 3-5 days ($50-200)
        - FedEx: 3-7 days ($40-150)
        - Standard Post: 2-4 weeks ($10-50)""",
        "keywords": ["parts", "components", "motors", "sensors", "price", "cost", "buy", "where", "budget", "build", "frame", "battery", "computer", "actuators", "grippers"]
    }
}

# Chat request model
class ChatRequest(BaseModel):
    message: str
    level: Optional[str] = "Beginner"
    top_k: Optional[int] = 5

def find_relevant_content(query: str) -> List[Dict]:
    """Find relevant book content based on query"""
    query_lower = query.lower()
    results = []
    
    # Remove "explain this:" prefix if present
    if query_lower.startswith("explain this:"):
        query_lower = query_lower.replace("explain this:", "").strip()
    
    for key, content in BOOK_CONTENT.items():
        # Check if query matches keywords
        score = 0
        for keyword in content["keywords"]:
            if keyword in query_lower:
                score += 2
            # Partial match
            if keyword[:4] in query_lower:
                score += 1
        
        # Check if query matches content
        if key in query_lower or content["title"].lower() in query_lower:
            score += 5
        
        # Check if any content from the book is in the query
        content_lower = content["content"].lower()
        words_in_query = 0
        for word in content_lower.split():
            if len(word) > 3 and word in query_lower:
                words_in_query += 1
        
        if words_in_query > 3:
            score += 3
        
        if score > 0:
            results.append({
                "score": score,
                "chapter": content["chapter"],
                "title": content["title"],
                "content": content["content"],
                "keywords": content["keywords"]
            })
    
    # Sort by score and return top results
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]

def generate_diagram(query: str) -> Optional[Dict]:
    """Generate diagram based on query"""
    query_lower = query.lower()
    
    # ROS 2 Architecture
    if "ros 2" in query_lower or "ros2" in query_lower:
        if "publisher" in query_lower or "subscriber" in query_lower or "pubsub" in query_lower or "publish" in query_lower:
            return {
                "title": "🏗️ ROS 2 Publisher-Subscriber Architecture",
                "mermaid": """graph LR
    subgraph ROS2_Network["ROS 2 Network"]
        direction LR
        subgraph Node1["Node 1"]
            P1[Publisher]
        end
        subgraph Node2["Node 2"]
            S1[Subscriber]
        end
        subgraph Node3["Node 3"]
            S2[Subscriber]
        end
        T[("Topic: /sensor_data")]
    end
    P1 -->|Publishes| T
    T -->|Subscribes| S1
    T -->|Subscribes| S2
    style Node1 fill:#4CAF50,color:#fff
    style Node2 fill:#2196F3,color:#fff
    style Node3 fill:#2196F3,color:#fff
    style T fill:#FF9800,color:#fff"""
            }
        else:
            return {
                "title": "🏗️ ROS 2 Node Architecture",
                "mermaid": """graph TB
    subgraph Node["ROS 2 Node"]
        Publishers[Publishers]
        Subscribers[Subscribers]
        Services[Services]
        Clients[Clients]
        Executor[Executor]
    end
    Publishers --> Executor
    Subscribers --> Executor
    Services --> Executor
    Clients --> Executor
    Executor --> ROS2Core[("ROS 2 Core<br/>DDS")]
    style Node fill:#E3F2FD
    style ROS2Core fill:#FF9800,color:#fff"""
            }
    
    # DDS Architecture
    if "dds" in query_lower or "data distribution" in query_lower:
        return {
            "title": "🏗️ DDS (Data Distribution Service) Architecture",
            "mermaid": """graph TB
    subgraph DDS_Domain["DDS Domain"]
        direction TB
        Publisher1[Publisher 1]
        Publisher2[Publisher 2]
        Subscriber1[Subscriber 1]
        Subscriber2[Subscriber 2]
        Topic[("Global Data Space<br/>Topic")]
    end
    Publisher1 --> Topic
    Publisher2 --> Topic
    Topic --> Subscriber1
    Topic --> Subscriber2
    style DDS_Domain fill:#E8F5E9
    style Topic fill:#FF9800,color:#fff"""
        }
    
    # RAG Architecture
    if "rag" in query_lower or "retrieval" in query_lower or "generation" in query_lower:
        return {
            "title": "🏗️ RAG (Retrieval-Augmented Generation) Pipeline",
            "mermaid": """graph TD
    User[("User Query")] --> Embed[Embedding Model]
    subgraph Retrieval["Retrieval Phase"]
        Embed --> Search[("Vector Search<br/>Qdrant")]
        Search --> Rank[Rank Results]
        Rank --> Retrieve[Retrieve Chunks]
    end
    subgraph Generation["Generation Phase"]
        Retrieve --> Context[Build Context]
        Context --> Prompt[Construct Prompt]
        Prompt --> LLM[("LLM<br/>GPT")]
        LLM --> Answer[Generate Answer]
    end
    Answer --> Output[("Response + Sources")]
    style User fill:#E3F2FD
    style Embed fill:#FFF3E0
    style LLM fill:#FFEBEE
    style Output fill:#E0F2F1"""
        }
    
    # Physical AI Architecture
    if "physical ai" in query_lower or "perception" in query_lower or "cognition" in query_lower:
        return {
            "title": "🏗️ Physical AI Architecture",
            "mermaid": """graph TB
    subgraph Perception["Perception Layer"]
        Sensors[Sensors]
        Vision[Computer Vision]
        Audio[Audio Processing]
    end
    subgraph Cognition["Cognition Layer"]
        AI[AI Models]
        Decision[Decision Making]
        Learning[Machine Learning]
    end
    subgraph Action["Action Layer"]
        Motors[Motor Control]
        Actuators[Actuators]
        Movement[Movement]
    end
    Sensors --> Vision
    Vision --> AI
    AI --> Decision
    Decision --> Motors
    Motors --> Movement
    style Perception fill:#E3F2FD
    style Cognition fill:#FFF3E0
    style Action fill:#E8F5E9"""
        }
    
    # Robot Perception/Sensors
    if "sensor" in query_lower or "camera" in query_lower or "lidar" in query_lower:
        return {
            "title": "🏗️ Robot Perception Pipeline",
            "mermaid": """graph TD
    subgraph Sensors["Sensors"]
        Camera[("Camera<br/>RGB-D")]
        LiDAR[("LiDAR<br/>3D Points")]
        IMU[("IMU<br/>Orientation")]
    end
    subgraph Processing["Processing"]
        Camera --> Fuse[Sensor Fusion]
        LiDAR --> Fuse
        IMU --> Fuse
        Fuse --> Detect[Object Detection]
        Detect --> Track[Tracking]
    end
    subgraph Output["Output"]
        Track --> Map[3D Map]
        Track --> Objects[Detected Objects]
    end
    style Sensors fill:#E3F2FD
    style Processing fill:#FFF3E0
    style Output fill:#E8F5E9"""
        }
    
    # Humanoid Robot Architecture
    if "humanoid" in query_lower or "robot" in query_lower or "walking" in query_lower:
        return {
            "title": "🏗️ Humanoid Robot Architecture",
            "mermaid": """graph TB
    subgraph Head["Head"]
        Cameras[Cameras]
        Microphone[Microphone]
    end
    subgraph Torso["Torso"]
        Computer[Main Computer]
        Battery[Battery]
    end
    subgraph Arms["Arms"]
        LeftArm[Left Arm]
        RightArm[Right Arm]
        Gripper[Gripper]
    end
    subgraph Legs["Legs"]
        LeftLeg[Left Leg]
        RightLeg[Right Leg]
        Balance[Balance Control]
    end
    Head --> Torso
    Torso --> Arms
    Torso --> Legs
    Arms --> Gripper
    Legs --> Balance
    style Head fill:#FFE0B2
    style Torso fill:#E3F2FD
    style Arms fill:#C8E6C9
    style Legs fill:#F8BBD0"""
        }
    
    # Machine Learning Pipeline
    if "machine learning" in query_lower or "ml" in query_lower or "training" in query_lower:
        return {
            "title": "🏗️ Machine Learning Pipeline for Robotics",
            "mermaid": """graph TD
    Data[Training Data] --> Preprocess[Preprocessing]
    Preprocess --> Train[Model Training]
    Train --> Validate[Validation]
    Validate --> Deploy[Deployment]
    Deploy --> Robot[Robot Execution]
    Robot --> Feedback[Feedback Loop]
    Feedback --> Data
    style Data fill:#E3F2FD
    style Train fill:#FFF3E0
    style Robot fill:#E8F5E9"""
        }
    
    # VLA Models
    if "vla" in query_lower or "vision-language" in query_lower or "vision language" in query_lower:
        return {
            "title": "🏗️ Vision-Language-Action (VLA) Model Architecture",
            "mermaid": """graph TB
    subgraph Input["Input Layer"]
        Image[Camera Image]
        Text[Text Instruction]
    end
    subgraph Encoding["Encoding Layer"]
        Image --> VisionEnc[Vision Encoder<br/>ViT]
        Text --> LangEnc[Language Encoder<br/>LLM]
    end
    subgraph Fusion["Fusion Layer"]
        VisionEnc --> Transformer[Multimodal<br/>Transformer]
        LangEnc --> Transformer
    end
    subgraph Output["Output Layer"]
        Transformer --> ActionHead[Action Head]
        ActionHead --> JointCmd[Joint Commands]
    end
    style Input fill:#E3F2FD
    style Encoding fill:#FFF3E0
    style Fusion fill:#F3E5F5
    style Output fill:#E8F5E9"""
        }
    
    # Motion Planning
    if "motion" in query_lower or "planning" in query_lower or "path" in query_lower:
        return {
            "title": "🏗️ Motion Planning Architecture",
            "mermaid": """graph TD
    Start[Start Position] --> Sense[Sense Environment]
    Sense --> Plan[Plan Path]
    Plan --> Check[Collision Check]
    Check --> Optimize[Optimize Trajectory]
    Optimize --> Execute[Execute Movement]
    Execute --> Goal[Goal Position]
    Check -->|Collision| Plan
    style Start fill:#C8E6C9
    style Plan fill:#FFF3E0
    style Goal fill:#FFCDD2"""
        }
    
    # System Integration
    if "integration" in query_lower or "system" in query_lower or "deployment" in query_lower:
        return {
            "title": "🏗️ Robot System Integration Architecture",
            "mermaid": """graph TB
    subgraph Hardware["Hardware Layer"]
        Sensors[Sensors]
        Actuators[Actuators]
        Computer[Compute Unit]
    end
    subgraph Middleware["Middleware Layer"]
        ROS2[ROS 2]
        Drivers[Device Drivers]
    end
    subgraph Software["Software Layer"]
        Perception[Perception]
        Planning[Planning]
        Control[Control]
    end
    subgraph Interface["Interface Layer"]
        UI[User Interface]
        API[API]
    end
    Hardware --> Middleware
    Middleware --> Software
    Software --> Interface
    style Hardware fill:#E3F2FD
    style Middleware fill:#FFF3E0
    style Software fill:#E8F5E9
    style Interface fill:#F3E5F5"""
        }
    
    # Control Systems
    if "control" in query_lower or "pid" in query_lower or "feedback" in query_lower:
        return {
            "title": "🏗️ Robot Control System Architecture",
            "mermaid": """graph LR
    Ref[Reference Input] --> Sum[Summing Point]
    Sum --> Controller[PID Controller]
    Controller --> Plant[Robot System]
    Plant --> Output[Output]
    Output --> Sensor[Sensor Feedback]
    Sensor --> Sum
    style Ref fill:#C8E6C9
    style Controller fill:#FFF3E0
    style Plant fill:#E3F2FD
    style Output fill:#FFCDD2"""
        }
    
    # Robot Parts with Images
    if "parts" in query_lower or "components" in query_lower or "motor" in query_lower or "sensor" in query_lower:
        return {
            "title": "🏗️ Robot Components Overview",
            "mermaid": """graph TB
    subgraph Structural["Structural"]
        Frame[Frame/Chassis]
        Joints[Joints]
    end
    subgraph Power["Power System"]
        Battery[Battery]
        PDU[Power Distribution]
    end
    subgraph Compute["Computing"]
        CPU[Main Computer]
        MCU[Microcontroller]
    end
    subgraph Sense["Sensing"]
        Camera[Cameras]
        LiDAR[LiDAR]
        IMU[IMU]
    end
    subgraph Actuate["Actuation"]
        Motors[Motors]
        Gripper[Gripper]
    end
    Structural --> Power
    Power --> Compute
    Compute --> Sense
    Compute --> Actuate
    style Structural fill:#FFE0B2
    style Power fill:#C8E6C9
    style Compute fill:#E3F2FD
    style Sense fill:#F8BBD0
    style Actuate fill:#F3E5F5"""
        }
    
    # Default: Show general AI/Robotics architecture
    if "architecture" in query_lower or "system" in query_lower or "how" in query_lower:
        return {
            "title": "🏗️ General Robotics System Architecture",
            "mermaid": """graph TB
    subgraph Perception["Perception"]
        Sensors[Sensors]
        Processing[Sensor Processing]
    end
    subgraph Decision["Decision Making"]
        Planning[Planning]
        AI[AI Models]
    end
    subgraph Action["Action"]
        Control[Control Systems]
        Actuators[Actuators]
    end
    Perception --> Decision
    Decision --> Action
    Action --> Environment[Environment]
    Environment --> Perception
    style Perception fill:#E3F2FD
    style Decision fill:#FFF3E0
    style Action fill:#E8F5E9"""
        }
    
    return None

def get_product_images(query: str) -> list:
    """Get product images based on query"""
    images = []
    query_lower = query.lower()
    
    # Robot images
    if "humanoid" in query_lower or "robot" in query_lower:
        images.extend([
            {"url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400", "alt": "Humanoid Robot", "caption": "Modern Humanoid Robot"},
            {"url": "https://images.unsplash.com/photo-1535378437327-b71097846923?w=400", "alt": "Robot Head", "caption": "Robot Head with Sensors"},
        ])
    
    # Motor images
    if "motor" in query_lower or "servo" in query_lower or "actuator" in query_lower:
        images.extend([
            {"url": "https://images.unsplash.com/photo-1622340523287-2c90b7e6e7a9?w=400", "alt": "Servo Motor", "caption": "High-Torque Servo Motor"},
            {"url": "https://images.unsplash.com/photo-1597424214711-41d2ae15b98e?w=400", "alt": "Electric Motor", "caption": "Precision Electric Motor"},
        ])
    
    # Sensor images
    if "sensor" in query_lower or "camera" in query_lower or "lidar" in query_lower:
        images.extend([
            {"url": "https://images.unsplash.com/photo-1555664424-778a6902201b?w=400", "alt": "Camera Sensor", "caption": "Depth Camera Sensor"},
            {"url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400", "alt": "Electronic Components", "caption": "Electronic Sensors"},
        ])
    
    # Circuit board images
    if "computer" in query_lower or "jetson" in query_lower or "electronics" in query_lower:
        images.extend([
            {"url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400", "alt": "Circuit Board", "caption": "Robot Control Board"},
            {"url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400", "alt": "AI Computer", "caption": "AI Computing Module"},
        ])
    
    # Battery images
    if "battery" in query_lower or "power" in query_lower:
        images.extend([
            {"url": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=400", "alt": "Robot Battery", "caption": "Li-ion Battery Pack"},
        ])
    
    # Gripper images
    if "gripper" in query_lower or "end effector" in query_lower:
        images.extend([
            {"url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400", "alt": "Robot Gripper", "caption": "Robotic Gripper"},
        ])
    
    return images

def adapt_to_level(content: str, level: str) -> str:
    """Adapt content explanation to user's expertise level"""
    
    if level == "Beginner":
        return f"""🌱 **Beginner-Friendly Explanation:**

{content}

---
**📖 In Simple Words:**
Imagine a robot like a human body:
- **Sensors** = Eyes and ears (to see and hear)
- **Computer** = Brain (to think and decide)
- **Motors** = Muscles (to move and act)

**🎯 Key Takeaways:**
✓ Focus on basic concepts first
✓ Don't worry about complex math yet
✓ Understand the "what" and "why" before the "how"

**💡 Simple Example:**
Think of a robot vacuum cleaner - it uses sensors to detect walls, a computer to decide where to go, and motors to move around. Same basic idea applies to all robots!

**❓ Common Beginner Questions:**
- Q: Do I need to know programming? A: Basic Python helps, but you can start with block-based tools
- Q: Is robotics expensive? A: You can start with $50-100 budget kits
- Q: Where should I start? A: Begin with Arduino or Raspberry Pi projects"""

    elif level == "Student":
        return f"""📚 **Educational Explanation:**

{content}

---
**🎓 Learning Objectives:**
After studying this topic, you should understand:
1. The fundamental concepts and terminology
2. How different components work together
3. Basic mathematical relationships
4. Common applications and use cases

**📐 Technical Details:**
- Study the underlying principles
- Understand cause and effect relationships
- Learn standard formulas and equations
- Practice with simulations

**🔬 Lab Exercises:**
1. Try simple experiments with sensor readings
2. Write basic control programs
3. Observe how changing parameters affects behavior
4. Document your findings

**📝 Exam Tips:**
- Memorize key definitions
- Understand block diagrams
- Practice numerical problems
- Review past papers

**🎯 Project Ideas:**
- Line follower robot ($50-100)
- Obstacle avoidance bot ($80-150)
- Basic robotic arm ($100-200)"""

    elif level == "Engineer":
        return f"""⚙️ **Technical/Engineering Explanation:**

{content}

---
**🔧 Implementation Considerations:**

**Design Requirements:**
- Performance specifications and constraints
- Power consumption analysis
- Thermal management
- Reliability and MTBF calculations

**Component Selection:**
- Compare datasheets carefully
- Consider availability and lead times
- Evaluate cost vs performance tradeoffs
- Check compatibility with existing systems

**System Integration:**
- Interface definitions and protocols
- Timing analysis and synchronization
- Error handling and fault tolerance
- Testing and validation procedures

**⚠️ Common Engineering Challenges:**
1. **EMI/EMC Issues:** Use proper shielding and grounding
2. **Thermal Problems:** Add heatsinks, fans, or liquid cooling
3. **Vibration:** Use dampening mounts and secure fasteners
4. **Power Noise:** Add decoupling capacitors and filters

**📊 Performance Metrics:**
- Efficiency: Target >85%
- Response Time: <100ms for real-time systems
- Accuracy: ±1% or better
- MTBF: >10,000 hours

**🛠️ Tools & Software:**
- CAD: SolidWorks, Fusion 360
- Simulation: MATLAB/Simulink, Gazebo
- PCB Design: KiCad, Altium Designer
- Version Control: Git

**💼 Industry Standards:**
- ISO 10218 (Robot Safety)
- IEC 61508 (Functional Safety)
- ROS 2 for software architecture"""

    elif level == "Researcher":
        return f"""🔬 **Research-Level Analysis:**

{content}

---
**📚 State-of-the-Art Review:**

**Current Research Frontiers:**
1. **Advanced Control Algorithms:**
   - Model Predictive Control (MPC)
   - Reinforcement Learning for Control
   - Adaptive and Robust Control

2. **Perception Advances:**
   - Deep Learning for Object Recognition
   - SLAM with Neural Networks
   - Multi-sensor Fusion Techniques

3. **Human-Robot Interaction:**
   - Natural Language Processing
   - Gesture Recognition
   - Emotion Detection

**🧪 Open Research Problems:**
- Safe human-robot collaboration in unstructured environments
- Long-term autonomy with minimal human intervention
- Learning from limited demonstrations
- Explainable AI for robotics
- Energy-efficient locomotion

**📈 Performance Benchmarks (SOTA 2024):**
- Object Detection: 95%+ accuracy (Vision Transformers)
- SLAM: <1% drift over 1km
- Grasping: 98% success rate (known objects)
- Walking: 5 km/h on uneven terrain

**🔭 Future Directions:**
- Neuromorphic computing for robotics
- Soft robotics and compliant actuators
- Swarm robotics and collective intelligence
- Bio-inspired designs
- Quantum sensing for navigation

**📄 Key Research Papers:**
1. "Attention Is All You Need" - Transformers (NeurIPS 2017)
2. "Deep Residual Learning" - ResNet (CVPR 2016)
3. "Human-Level Control through DRL" - Nature 2015
4. "End-to-End Training of Deep Visuomotor Policies" - CoRL 2016

**🎓 Research Methodologies:**
- Hypothesis-driven experimentation
- Statistical significance testing (p<0.05)
- Ablation studies
- Cross-validation techniques
- Open-source code and reproducibility

**💰 Funding Opportunities:**
- NSF Robotics Grants
- DARPA Programs
- EU Horizon Europe
- Industry partnerships (Google, Boston Dynamics, Tesla)"""

    return content

@app.post("/api/chat")
def chat(request: ChatRequest):
    """
    AI Chat endpoint with RAG (Retrieval-Augmented Generation)
    Combines book content with AI knowledge
    """
    try:
        query = request.message
        level = request.level or "Beginner"
        
        # Find relevant book content
        book_results = find_relevant_content(query)
        
        # Generate diagram if applicable
        diagram = generate_diagram(query)
        
        # Get product images
        images = get_product_images(query)
        
        # Build response
        if book_results:
            # Combine book content from multiple sources
            book_content = "\n\n".join([r["content"] for r in book_results])
            
            # Adapt to user level
            adapted_content = adapt_to_level(book_content, level)
            
            # Build sources list
            sources = [
                {
                    "chapter": r["chapter"],
                    "title": r["title"],
                    "relevance": "high" if r["score"] > 3 else "medium"
                }
                for r in book_results
            ]
            
            response_text = f"""{adapted_content}

**Additional AI Knowledge:**

Based on the textbook content, here's comprehensive information about {query}:

**Product Information:**
- Prices mentioned are approximate (USD)
- Check official websites for current pricing
- Bulk discounts available (10+ units: 10-15% off)

**Where to Buy:**
- International: RobotShop, DigiKey, Mouser, Amazon Industrial
- Pakistan: RoboPakistan (Lahore), ElectroOptics (Karachi)
- India: Robu.in, ElectronicsComp.com

**Performance Considerations:**
- Match components to your requirements
- Consider power consumption
- Check compatibility before purchasing

**Common Issues & Solutions:**
- Motor overheating → Add heatsinks, reduce load
- Sensor noise → Use shielded cables, proper grounding
- Communication errors → Check baud rates, wiring"""
            
        else:
            # No book content found - use general AI knowledge
            response_text = f"""🤖 **AI Assistant Response:**

That's an interesting question about "{query}"! While this specific topic isn't covered in detail in the textbook, I can share some general knowledge:

**General Information:**

This topic relates to the broader field of robotics and AI. Based on the concepts covered in the textbook, you might want to explore:

1. **Related Chapters:**
   - Chapter 1: ROS 2 fundamentals
   - Chapter 2: Physical AI concepts
   - Chapter 6: Machine learning approaches

2. **Key Concepts to Review:**
   - Sensor integration
   - Control systems
   - Perception pipelines

3. **Further Learning:**
   - Check ROS 2 documentation
   - Explore research papers
   - Practice with simulations"""
            
            sources = []
        
        # Build response
        response = {
            "status": "success",
            "message": response_text,
            "sources": sources,
            "diagram": diagram,
            "images": images,
            "level": level,
            "book_chunks_found": len(book_results),
            "confidence": min(0.95, 0.5 + (len(book_results) * 0.15))
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
