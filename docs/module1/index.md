---
title: Module 1 - The Robotic Nervous System (ROS 2)
description: Learn how robots communicate internally using ROS 2 middleware, nodes, topics, services, and actions
sidebar_label: Module 1 Overview
sidebar_position: 1
---

# Module 1: The Robotic Nervous System (ROS 2)

## Module Overview

This module teaches you how to build the **nervous system of a robot** using ROS 2 (Robot Operating System 2). Just as your nervous system connects your brain to your muscles and senses, ROS 2 connects AI agents to robot hardware.

```
┌─────────────────────────────────────────────────────────────┐
│              The Robot Nervous System                        │
│                                                              │
│     AI Brain (LLM/Agent)                                    │
│           │                                                  │
│           ▼                                                  │
│     ROS 2 Middleware  ◄──── "Spinal Cord"                   │
│           │                                                  │
│    ┌──────┼──────┐                                           │
│    │      │      │                                           │
│    ▼      ▼      ▼                                           │
│  Topics  Services Actions  ◄──── "Nerves"                    │
│    │      │      │                                           │
│    ▼      ▼      ▼                                           │
│ ┌────┐ ┌────┐ ┌────┐                                        │
│ │Sens│ │Ctrl│ │Act │  ◄──── "Muscles & Senses"              │
│ └────┘ └────┘ └────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## What You Will Learn

By the end of this module, you will be able to:

| Skill | Application |
|-------|-------------|
| Install and configure ROS 2 | Set up development environment |
| Create ROS 2 nodes | Build modular robot software |
| Implement publish/subscribe | Enable sensor data flow |
| Design service-based communication | Handle request/response patterns |
| Model robots using URDF | Create digital twins |
| Integrate AI agents with robots | Connect LLMs to hardware |
| Launch multi-node systems | Deploy complete robot architectures |
| Debug robot systems | Diagnose and fix issues |

## Prerequisites

Before starting this module, ensure you have:

- **Operating System**: Ubuntu 22.04 (recommended) or Windows 10/11 with WSL2
- **Python**: Version 3.10 or higher
- **Terminal**: Basic command-line familiarity
- **Programming**: Basic Python knowledge

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Storage | 20 GB free | 50 GB SSD |
| GPU | Integrated | NVIDIA RTX (for simulation) |

## Module Structure

This module contains **5 chapters**:

### Chapter 1: Introduction to ROS 2

Learn the fundamentals of ROS 2:

- What is ROS and why it was created
- ROS 1 vs ROS 2 architecture differences
- DDS middleware and communication layers
- Installing ROS 2 Humble on Ubuntu
- Creating your first Hello World node

**[Start Chapter 1 →](./chapter1-ros2-introduction)**

---

### Chapter 2: ROS 2 Communication System

Master ROS 2 communication patterns:

- Nodes: The basic unit of computation
- Topics: Publish/subscribe messaging
- Services: Request/response communication
- Actions: Long-running tasks with feedback
- Message types and custom definitions

**[Start Chapter 2 →](./chapter2-ros2-communication)**

---

### Chapter 3: Python AI Agents with ROS 2

Build intelligent robot controllers:

- The rclpy client library
- Processing sensor data for decisions
- Integrating LLMs with robot control
- Sensor fusion for robust perception
- Event-driven architectures

**[Start Chapter 3 →](./chapter3-ros2-python-agents)**

---

### Chapter 4: Robot Description using URDF

Model your robot in XML:

- URDF format and structure
- Links: Rigid body definitions
- Joints: Kinematic connections
- Sensors and actuators in URDF
- Visualizing robots in RViz

**[Start Chapter 4 →](./chapter4-robot-description-urdf)**

---

### Chapter 5: Building the Robot Nervous System

Integrate everything into a complete system:

- Node integration patterns
- Launch files for automation
- Parameter configuration
- System monitoring and diagnostics
- Debugging with ROS 2 CLI tools

**[Start Chapter 5 →](./chapter5-building-robot-system)**

---

## Hands-On Projects

Throughout this module, you will build:

### Project 1: Sensor Publisher/Subscriber System
Create nodes that publish simulated IMU data and subscribers that process it.

### Project 2: AI Agent with Voice Control
Build an AI agent that responds to voice commands and controls robot movement.

### Project 3: Humanoid Robot Model
Design a complete humanoid robot URDF model with arms, legs, and head.

### Project 4: Complete Robot System
Integrate all components into a launchable robot nervous system.

---

## Code Examples

All code examples use these languages:

```python
# Python (rclpy) - Primary language for AI agents
import rclpy
from rclpy.node import Node
```

```bash
# Bash - Command line operations
ros2 node list
ros2 topic echo /sensor_data
```

```yaml
# YAML - Configuration files
robot:
  name: humanoid_01
  max_velocity: 1.5
```

```xml
<!-- URDF - Robot descriptions -->
<robot name="humanoid">
  <link name="base_link"/>
  <joint name="hip_joint" type="revolute"/>
</robot>
```

---

## Assessment

### Knowledge Checks

Each chapter includes:
- Conceptual questions
- Code modification exercises
- Research tasks

### Practical Labs

Each chapter includes:
- Step-by-step lab instructions
- Expected outputs
- Success criteria

### Final Project

Build a complete robot system that:
- Receives voice commands
- Processes sensor data
- Controls robot movement
- Monitors system health

---

## Time Commitment

| Activity | Estimated Time |
|----------|----------------|
| Reading chapters | 5-7 hours |
| Hands-on labs | 8-10 hours |
| Exercises | 3-4 hours |
| Final project | 4-6 hours |
| **Total** | **20-27 hours** |

---

## Learning Tips

### For Success

1. **Install ROS 2 early** — Don't wait until the labs
2. **Run every code example** — Typing helps learning
3. **Use the CLI tools** — They're your debugging friends
4. **Join the community** — ROS Discourse is helpful
5. **Experiment** — Modify examples and see what happens

### Common Challenges

| Challenge | Solution |
|-----------|----------|
| Installation issues | Use Ubuntu 22.04 in VM if needed |
| Topic not publishing | Check node is running and topic name matches |
| Import errors | Source your workspace: `source install/setup.bash` |
| URDF not visualizing | Check `robot_state_publisher` is running |

---

## Resources

### Official Documentation

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Design](https://docs.ros.org/en/humble/The-ROS2-Project/Contributing/Design-Guidelines.html)

### Community

- [ROS Discourse](https://discourse.ros.org/) — Ask questions
- [ROS 2 GitHub](https://github.com/ros2/ros2) — Report issues
- [Stack Overflow](https://stackoverflow.com/questions/tagged/ros2) — Q&A

### Video Tutorials

- [The Construct — ROS 2 Basics](https://www.theconstructsim.com/)
- [Open Robotics YouTube](https://www.youtube.com/c/OpenRoboticsOrg)

---

## What's Next?

After completing Module 1, continue to:

| Module | Topic |
|--------|-------|
| [Module 2](../module2) | Digital Twin Simulation (Gazebo, Unity) |
| [Module 3](../module3) | AI Robot Brain (NVIDIA Isaac, SLAM) |
| [Module 4](../module4) | Vision Language Action (LLM + Robotics) |
| [Capstone](../capstone) | Autonomous Humanoid Project |

---

## Quick Start

Ready to begin? Here's your first task:

```bash
# 1. Install ROS 2 Humble (see Chapter 1)
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | \
    sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

# 2. Add repository
echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu \
    $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 3. Install
sudo apt update && sudo apt install ros-humble-desktop

# 4. Source
source /opt/ros/humble/setup.bash

# 5. Test
ros2 --version
```

**[→ Start Chapter 1: Introduction to ROS 2](./chapter1-ros2-introduction)**
