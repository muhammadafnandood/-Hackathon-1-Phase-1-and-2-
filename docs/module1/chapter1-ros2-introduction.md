---
title: Introduction to ROS 2
description: Learn the fundamentals of ROS 2, the middleware that powers modern robotics communication
sidebar_label: 1.1 ROS 2 Introduction
---

# Chapter 1: Introduction to ROS 2

## Learning Objectives

By the end of this chapter, you will be able to:

- **Explain** what ROS is and why it was created
- **Differentiate** between ROS 1 and ROS 2 architectures
- **Understand** the middleware concept in robotics
- **Describe** the DDS communication layer
- **Install** ROS 2 Humble on Ubuntu 22.04
- **Create** your first ROS 2 node

---

## Concept Explanation

### What is ROS?

**ROS (Robot Operating System)** is not an operating system in the traditional sense. It is a **middleware framework** that provides:

- **Hardware abstraction** — Interface with sensors, actuators, and robots
- **Low-level device control** — Direct communication with hardware components
- **Inter-process communication** — Messages between different software modules
- **Package management** — Organized code distribution and reuse

> **Definition: Middleware** — Software that sits between the operating system and applications, enabling different systems to communicate. In robotics, middleware handles message passing between components.

### Why ROS 2 Was Created

ROS 1 served the robotics community for over a decade. However, it had critical limitations:

| ROS 1 Limitation | Impact |
|------------------|--------|
| Single point of failure (ROS Master) | Entire system fails if master dies |
| No real-time support | Unsuitable for production robots |
| Linux-only | Limited deployment options |
| Custom networking stack | Complex firewall configurations |
| No security features | Vulnerable to attacks |

**ROS 2** was designed to address these issues with:

- **DDS-based communication** — Industry-standard data distribution
- **Decentralized architecture** — No single point of failure
- **Real-time support** — Deterministic behavior for safety-critical systems
- **Cross-platform** — Windows, macOS, Linux, RTOS
- **Built-in security** — Authentication and encryption

### ROS vs ROS 2: Key Differences

```
┌─────────────────────────────────────────────────────────────┐
│                     ROS 1 Architecture                       │
│                                                              │
│   Node 1 ──┐                                                 │
│   Node 2 ──┼──► ROS Master (Single Point of Failure)         │
│   Node 3 ──┘                                                 │
│                                                              │
│   All communication routes through central master            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     ROS 2 Architecture                       │
│                                                              │
│   Node 1 ◄─────── DDS Discovery ───────► Node 2              │
│      │                                     │                 │
│      │            Peer-to-Peer             │                 │
│      ▼                                     ▼                 │
│   Node 3 ◄────────────────────────────► Node 4               │
│                                                              │
│   Direct communication, no central master                    │
└─────────────────────────────────────────────────────────────┘
```

### Middleware Concept in Robotics

Robots consist of multiple components that must communicate:

```
┌─────────────────────────────────────────────────────────────┐
│                    Robot Software Stack                      │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Perception │  │  Planning   │  │  Control    │          │
│  │   (Camera)  │  │   (Path)    │  │  (Motors)   │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                  │
│         └────────────────┼────────────────┘                  │
│                          │                                   │
│              ┌───────────▼───────────┐                       │
│              │    ROS 2 Middleware   │                       │
│              │   (Message Passing)   │                       │
│              └───────────┬───────────┘                       │
│                          │                                   │
│         ┌────────────────┼────────────────┐                  │
│         │                │                │                  │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐          │
│  │   Camera    │  │    LiDAR    │  │   Motors    │          │
│  │   Driver    │  │    Driver   │  │   Driver    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**ROS 2 middleware provides:**

1. **Discovery** — Nodes find each other automatically
2. **Serialization** — Convert data to transmittable format
3. **Transport** — Move data between processes/machines
4. **QoS (Quality of Service)** — Reliability, durability, history settings

### DDS Communication Layer

**DDS (Data Distribution Service)** is an industrial middleware standard used in:

- Aerospace systems (NASA, SpaceX)
- Medical devices
- Autonomous vehicles
- Defense systems

**How DDS Works in ROS 2:**

```
┌─────────────────────────────────────────────────────────────┐
│                    DDS Communication Flow                    │
│                                                              │
│  Publisher Node                    Subscriber Node           │
│  ┌─────────────┐                  ┌─────────────┐           │
│  │   Data      │                  │   Data      │           │
│  │   Writer    │─────Topic───────►│   Reader    │           │
│  └─────────────┘                  └─────────────┘           │
│       │                                    │                 │
│       ▼                                    ▼                 │
│  ┌─────────────┐                  ┌─────────────┐           │
│  │   DDS       │                  │   DDS       │           │
│  │   Domain    │◄────Domain──────►│   Domain    │           │
│  │   Participant│     ID: 0       │   Participant│          │
│  └─────────────┘                  └─────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key DDS Concepts:**

| Term | Definition |
|------|------------|
| **Domain** | Isolated communication space (like a network VLAN) |
| **Publisher** | Node that sends data on a topic |
| **Subscriber** | Node that receives data from a topic |
| **Topic** | Named channel for data communication |
| **QoS Policy** | Rules for data delivery (reliability, history, etc.) |

### Real-World Robots Using ROS 2

**Boston Dynamics Spot:**
- Uses ROS 2 for perception and navigation
- Integrates with custom control systems

**Unitree Humanoids:**
- ROS 2 drivers for Go2 and H1 robots
- Open-source community support

**NASA Robonaut:**
- ROS 2 for space robotics applications
- Real-time control requirements

**Toyota Human Support Robot:**
- ROS 2 for home assistance tasks
- Safe human-robot interaction

---

## Architecture Overview

### ROS 2 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ROS 2 System Layers                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Application Layer                       │    │
│  │   (Your Python/C++ nodes, AI agents, controllers)   │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              ROS 2 Client Libraries                  │    │
│  │         (rclpy, rclcpp, rcljava)                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              ROS 2 Core (rcl)                        │    │
│  │         (Robot abstraction layer)                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              DDS Middleware                          │    │
│  │    (Fast DDS, Cyclone DDS, RTI Connext)             │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Operating System                        │    │
│  │         (Ubuntu 22.04, Windows, macOS)               │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Hardware                                │    │
│  │    (Sensors, Actuators, Cameras, LiDAR)             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Hello World ROS 2 Node

Create a simple publisher node that prints messages:

```python
#!/usr/bin/env python3
"""
hello_world_node.py
First ROS 2 node that publishes hello world messages
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HelloWorldNode(Node):
    """A simple node that publishes hello world messages."""
    
    def __init__(self):
        super().__init__('hello_world_node')
        
        # Create a publisher
        # Topic: /hello_topic
        # Message Type: String
        # Queue Size: 10 (buffer size)
        self.publisher_ = self.create_publisher(
            String,
            '/hello_topic',
            10
        )
        
        # Create a timer that calls publish_hello_world every 1 second
        self.timer = self.create_timer(1.0, self.publish_hello_world)
        
        # Counter for messages
        self.counter = 0
        
        self.get_logger().info('Hello World Node started!')
    
    def publish_hello_world(self):
        """Publish a hello world message."""
        self.counter += 1
        
        # Create message
        msg = String()
        msg.data = f'Hello World! Count: {self.counter}'
        
        # Publish message
        self.publisher_.publish(msg)
        
        # Log to console
        self.get_logger().info(f'Published: {msg.data}')


def main(args=None):
    """Initialize and run the node."""
    rclpy.init(args=args)
    
    # Create node instance
    node = HelloWorldNode()
    
    # Spin the node (keep it running)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user')
    finally:
        # Cleanup
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## Hands-on Lab

### Lab 1.1: Install ROS 2 Humble on Ubuntu 22.04

**Objective:** Set up ROS 2 Humble Hawksbill development environment

**Prerequisites:**
- Ubuntu 22.04 (Jammy Jellyfish)
- 4GB+ RAM
- 10GB+ free disk space
- Internet connection

**Time:** 30 minutes

---

### Step 1: Configure Locale

ROS 2 requires UTF-8 locale support:

```bash
# Check current locale
locale

# If not UTF-8, configure it
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Verify
locale
```

**Expected Output:**
```
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
```

---

### Step 2: Setup Sources

```bash
# Install required packages
sudo apt update && sudo apt install -y \
    curl \
    gnupg \
    lsb-release \
    software-properties-common

# Add ROS 2 GPG key
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | \
    sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository
echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu \
    $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

---

### Step 3: Install ROS 2 Humble

```bash
# Update package index
sudo apt update

# Install ROS 2 Humble Desktop (includes GUI tools)
sudo apt install -y ros-humble-desktop

# Install development tools
sudo apt install -y \
    ros-humble-rqt \
    ros-humble-rqt-common-plugins \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers
```

---

### Step 4: Setup Environment

```bash
# Source ROS 2 setup script (current terminal)
source /opt/ros/humble/setup.bash

# Make it permanent
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Optional: Source colcon setup (for building packages)
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc

# Reload bashrc
source ~/.bashrc
```

---

### Step 5: Verify Installation

```bash
# Check ROS 2 version
ros2 --version

# List available commands
ros2 --help

# Check installed packages
dpkg -l | grep ros-humble

# Run a simple test
ros2 run demo_nodes_cpp talker
```

**Expected Output:**
```
[INFO] [talker]: Publishing: 'Hello World: 1'
[INFO] [talker]: Publishing: 'Hello World: 2'
[INFO] [talker]: Publishing: 'Hello World: 3'
...
```

Press `Ctrl+C` to stop.

---

### Step 6: Test with Listener

Open a **new terminal** and run:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

**Expected Output:**
```
[INFO] [listener]: I heard: [Hello World: 1]
[INFO] [listener]: I heard: [Hello World: 2]
[INFO] [listener]: I heard: [Hello World: 3]
...
```

**Success Criteria:** ✅ Messages are being published and received between nodes.

---

### Step 7: Create Your First Node

```bash
# Create workspace directory
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Create a Python package
cd src
ros2 pkg create --build-type ament_python my_first_node

# Navigate to package
cd my_first_node/my_first_node

# Create hello_world_node.py (use the code from Code Examples above)
nano hello_world_node.py
```

Paste the Hello World code, save, and make executable:

```bash
chmod +x hello_world_node.py
```

---

### Step 8: Build and Run

```bash
# Return to workspace root
cd ~/ros2_ws

# Build the package
colcon build

# Source the workspace
source install/setup.bash

# Run your node
ros2 run my_first_node hello_world_node
```

**Expected Output:**
```
[INFO] [hello_world_node]: Hello World Node started!
[INFO] [hello_world_node]: Published: Hello World! Count: 1
[INFO] [hello_world_node]: Published: Hello World! Count: 2
...
```

---

## Summary

### Key Takeaways

1. **ROS is middleware**, not an operating system — it enables robot component communication
2. **ROS 2 fixes ROS 1 limitations** — no single point of failure, real-time support, cross-platform
3. **DDS is the communication backbone** — industry-standard for distributed systems
4. **Nodes communicate via topics** — publishers send, subscribers receive
5. **Installation is straightforward** — Ubuntu 22.04 + ROS 2 Humble is the recommended setup

### Important Definitions

| Term | Definition |
|------|------------|
| **Node** | A process that performs computation |
| **Topic** | Named bus for data exchange |
| **Publisher** | Node that sends data on a topic |
| **Subscriber** | Node that receives data from a topic |
| **Middleware** | Software layer enabling communication |
| **DDS** | Data Distribution Service — ROS 2's communication layer |

---

## Exercises

### Exercise 1.1: Conceptual Questions

1. What is the main architectural difference between ROS 1 and ROS 2?
2. Why is DDS important for robotics applications?
3. Explain the concept of a "topic" in ROS 2.
4. What happens if a publisher node crashes in ROS 2?
5. List three real-world robots that use ROS 2.

### Exercise 1.2: Installation Verification

1. Install ROS 2 Humble on your system (or use a VM)
2. Run the talker/listener demo
3. Take a screenshot showing messages being exchanged
4. Document any issues you encountered and how you resolved them

### Exercise 1.3: Hello World Modification

Modify the Hello World node to:

1. Publish every 500 milliseconds instead of 1 second
2. Include a timestamp in each message
3. Stop after publishing 10 messages

**Hint:** Use `self.counter` to track message count and `datetime.now()` for timestamps.

### Exercise 1.4: Research Task

Research and write a one-page summary on:

- **Fast DDS** vs **Cyclone DDS** — What are the differences?
- When would you choose one over the other?
- Which DDS implementation does ROS 2 Humble use by default?

---

## Next Chapter

In **Chapter 2: ROS 2 Communication System**, you will learn:

- How nodes discover each other
- Topic-based publish/subscribe patterns
- Service-based request/response communication
- Action servers for long-running tasks
- Message types and custom message creation

---

## Resources

### Official Documentation

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [DDS Specification](https://www.omg.org/spec/DDS/1.4/)

### Video Resources

- [ROS 2 Basics — The Construct](https://www.theconstructsim.com/)
- [Open Robotics ROS 2 Talks](https://www.youtube.com/c/OpenRoboticsOrg)

### Community

- [ROS Discourse Forum](https://discourse.ros.org/)
- [ROS 2 GitHub](https://github.com/ros2/ros2)
- [Stack Overflow — ROS 2 Tag](https://stackoverflow.com/questions/tagged/ros2)
