---
title: ROS 2 Communication System
description: Master ROS 2 communication patterns: nodes, topics, publishers, subscribers, services, and actions
sidebar_label: 1.2 Communication System
---

# Chapter 2: ROS 2 Communication System

## Learning Objectives

By the end of this chapter, you will be able to:

- **Create** ROS 2 nodes that publish and subscribe to topics
- **Implement** service-based request/response communication
- **Design** action servers for long-running tasks
- **Define** custom message types for your robot
- **Configure** Quality of Service (QoS) policies
- **Debug** communication issues using ROS 2 CLI tools

---

## Concept Explanation

### The Node: Basic Unit of Computation

**Definition: Node** — A process that performs computation. Nodes are the building blocks of ROS 2 systems.

```
┌─────────────────────────────────────────────────────────────┐
│                    ROS 2 Node Structure                      │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Node: /camera_driver                │    │
│  │                                                      │    │
│  │  ┌──────────────┐         ┌──────────────┐          │    │
│  │  │  Publishers  │         │ Subscribers  │          │    │
│  │  │  (Sends)     │         │ (Receives)   │          │    │
│  │  │              │         │              │          │    │
│  │  │ /image_raw   │         │ /camera_info │          │    │
│  │  │ /camera_status│        │ /trigger     │          │    │
│  │  └──────────────┘         └──────────────┘          │    │
│  │                                                      │    │
│  │  ┌──────────────┐         ┌──────────────┐          │    │
│  │  │   Services   │         │    Actions   │          │    │
│  │  │  (Request/   │         │ (Long-running│          │    │
│  │  │   Response)  │         │  tasks)      │          │    │
│  │  │              │         │              │          │    │
│  │  │ /set_exposure│        │ /capture_seq │          │    │
│  │  └──────────────┘         └──────────────┘          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Node Characteristics:**

- Each node has a **unique name** (e.g., `/camera_driver`, `/navigation`)
- Nodes can be written in **Python** (rclpy) or **C++** (rclcpp)
- Multiple nodes can run in the **same process** or **different processes**
- Nodes can run on the **same machine** or **different machines**

### Topics: Publish/Subscribe Communication

**Definition: Topic** — A named bus over which nodes exchange messages. Topics use anonymous publish/subscribe semantics.

```
┌─────────────────────────────────────────────────────────────┐
│                 Topic-Based Communication                    │
│                                                              │
│   Publisher Node              Topic              Subscriber  │
│   ┌───────────┐           ┌─────────┐          ┌──────────┐ │
│   │           │──────────►│ /sensor │─────────►│          │ │
│   │  Camera   │  ImageMsg │  _data  │ ImageMsg │  Display │ │
│   │  Driver   │           │         │          │   Node   │ │
│   │           │──────────►│         │─────────►│          │ │
│   └───────────┘           └─────────┘          └──────────┘ │
│                              │                   │           │
│                              │                   ▼           │
│                              │              ┌──────────┐     │
│                              │─────────────►│          │     │
│                              │   ImageMsg   │  Logger  │     │
│                              │              │   Node   │     │
│                              │              └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

**Key Properties:**

| Property | Description |
|----------|-------------|
| **Anonymous** | Publishers don't know subscribers, and vice versa |
| **Many-to-Many** | Multiple publishers and subscribers allowed |
| **Asynchronous** | Publishers don't wait for subscribers |
| **Typed** | Each topic has a specific message type |

### Publishers and Subscribers

**Publisher:** A node that sends data on a topic

```python
# Create a publisher
self.publisher = self.create_publisher(
    MessageType,    # Type of message (e.g., String, Int32, custom)
    'topic_name',   # Topic to publish on
    qos_profile     # Queue size or QoS profile
)

# Publish a message
self.publisher.publish(message)
```

**Subscriber:** A node that receives data from a topic

```python
# Create a subscriber
self.subscription = self.create_subscription(
    MessageType,        # Type of message to receive
    'topic_name',       # Topic to subscribe to
    callback_function,  # Function called when message arrives
    qos_profile         # Queue size or QoS profile
)
```

### Services: Request/Response Communication

**Definition: Service** — A synchronous request/response communication pattern between two nodes.

```
┌─────────────────────────────────────────────────────────────┐
│                 Service-Based Communication                  │
│                                                              │
│   Client Node                          Server Node           │
│   ┌─────────────┐                    ┌─────────────┐        │
│   │   Request   │───────────────────►│   Handler   │        │
│   │  (AddTwoInts│    Service Request │  (Process   │        │
│   │   a=2, b=3) │                    │   Request)  │        │
│   └─────────────┘                    └──────┬──────┘        │
│         ▲                                   │                │
│         │                                   │                │
│         │            Service Response       │                │
│         │───────────────────────────────────│                │
│         │             (sum = 5)             │                │
│         ▼                                   ▼                │
│   ┌─────────────┐                    ┌─────────────┐        │
│   │   Result    │                    │   Service   │        │
│   │  Received   │                    │  /add_two   │        │
│   └─────────────┘                    └─────────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Service Characteristics:**

- **Synchronous** — Client waits for response
- **One-to-One** — One client, one server (per request)
- **Blocking** — Client blocks until response received (or timeout)
- **Use Cases:** Configuration changes, calculations, database queries

### Actions: Long-Running Tasks

**Definition: Action** — An asynchronous request/response communication pattern for long-running tasks with feedback.

```
┌─────────────────────────────────────────────────────────────┐
│                  Action Communication Flow                   │
│                                                              │
│   Action Client                      Action Server           │
│   ┌─────────────┐                  ┌─────────────┐          │
│   │   Send      │────────Goal─────►│   Execute   │          │
│   │   Goal      │                  │   Task      │          │
│   └─────────────┘                  └──────┬──────┘          │
│         ▲                                 │                  │
│         │            Feedback             │                  │
│         │◄───────(Progress: 50%)──────────│                  │
│         │                                 │                  │
│         │            Feedback             │                  │
│         │◄───────(Progress: 75%)──────────│                  │
│         │                                 │                  │
│         │            Result               │                  │
│         │◄───────(Success: True)──────────│                  │
│         ▼                                 ▼                  │
│   ┌─────────────┐                  ┌─────────────┐          │
│   │   Task      │                  │   Action:   │          │
│   │  Complete   │                  │ /navigate   │          │
│   └─────────────┘                  └─────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Action Components:**

| Component | Purpose |
|-----------|---------|
| **Goal** | Request sent to action server (e.g., "navigate to x=5, y=3") |
| **Feedback** | Periodic updates during execution (e.g., "50% complete") |
| **Result** | Final response when task completes (e.g., "success: true") |

**Use Cases:**

- Robot navigation (takes time, needs progress updates)
- Object manipulation (grasping, placing)
- Complex computations with progress tracking

### Message Types

ROS 2 uses **Interface Definition Language (IDL)** for message types.

**Built-in Message Types:**

```
std_msgs/msg/String      — Text data
std_msgs/msg/Int32       — 32-bit integer
std_msgs/msg/Float64     — 64-bit float
std_msgs/msg/Bool        — Boolean (true/false)
std_msgs/msg/Header      — Timestamp and frame ID
geometry_msgs/msg/Point  — 3D point (x, y, z)
geometry_msgs/msg/Twist  — Velocity (linear, angular)
sensor_msgs/msg/Image    — Camera image
sensor_msgs/msg/LaserScan — LiDAR scan data
nav_msgs/msg/Odometry    — Robot position and velocity
```

**Custom Message Types:**

Create `.msg` files to define your own message structures:

```text
# File: msg/RobotStatus.msg
int32 robot_id
string robot_name
bool is_active
float64 battery_level
string[] active_sensors
```

---

## Architecture Overview

### Complete Robot Communication Network

```
┌─────────────────────────────────────────────────────────────┐
│              Humanoid Robot Communication Network            │
│                                                              │
│  ┌─────────────┐     /joint_states      ┌─────────────┐     │
│  │   Motor     │◄───────────────────────│   Motion    │     │
│  │  Controller │                        │   Planner   │     │
│  │   Node      │───────────────────────►│   Node      │     │
│  └─────────────┘    /cmd_joint          └─────────────┘     │
│         ▲                                      │             │
│         │                                      │             │
│         │ /imu_data                            │ /goal_pose  │
│         ▼                                      ▼             │
│  ┌─────────────┐     /sensor_fusion    ┌─────────────┐      │
│  │     IMU     │◄──────────────────────│  Navigation │      │
│  │   Driver    │                        │   Server    │      │
│  │   Node      │───────────────────────►│   Node      │      │
│  └─────────────┘    /odom              └─────────────┘      │
│         ▲                                      │             │
│         │                                      │             │
│         │ /camera_info                         │ /cmd_vel    │
│         ▼                                      ▼             │
│  ┌─────────────┐     /image_raw       ┌─────────────┐       │
│  │   Camera    │◄─────────────────────│  Perception │       │
│  │   Driver    │                       │   Node      │       │
│  │   Node      │──────────────────────►│ (AI Agent)  │       │
│  └─────────────┘    /detected_objects └─────────────┘       │
│                                                              │
│  Services:                                                   │
│  /set_motor_params  /reset_odometry  /clear_costmap         │
│                                                              │
│  Actions:                                                    │
│  /navigate_to_pose  /pick_object     /place_object          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Topic Communication Flow

```
┌─────────────────────────────────────────────────────────────┐
│              ROS 2 Topic Discovery and Communication         │
│                                                              │
│  Step 1: Node Startup                                        │
│  ┌──────────┐                           ┌──────────┐        │
│  │ Node A   │                           │ Node B   │        │
│  │(Publisher)│                          │(Subscriber)│       │
│  └────┬─────┘                           └────┬─────┘        │
│       │                                      │               │
│       └──────────────┬───────────────────────┘               │
│                      │                                        │
│              DDS Discovery Protocol                           │
│              (Nodes find each other)                          │
│                                                              │
│  Step 2: Communication Established                           │
│  ┌──────────┐     Topic: /sensor_data     ┌──────────┐      │
│  │ Node A   │────────────────────────────►│ Node B   │      │
│  │         │      Message: SensorMsg       │         │      │
│  └──────────┘                             └──────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Example 1: Publisher Node (Sensor Data)

```python
#!/usr/bin/env python3
"""
sensor_publisher.py
Publishes simulated sensor data for a humanoid robot
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
import math
import time


class SensorPublisherNode(Node):
    """Publishes IMU sensor data."""
    
    def __init__(self):
        super().__init__('sensor_publisher_node')
        
        # Publisher for IMU data
        self.imu_publisher = self.create_publisher(
            Imu,
            '/imu/data',
            10
        )
        
        # Publisher for battery level
        self.battery_publisher = self.create_publisher(
            Float64,
            '/battery_level',
            10
        )
        
        # Timer for publishing at 100 Hz
        self.timer = self.create_timer(0.01, self.publish_sensor_data)
        
        self.sequence_number = 0
        
        self.get_logger().info('Sensor Publisher Node started!')
    
    def publish_sensor_data(self):
        """Publish IMU and battery data."""
        self.sequence_number += 1
        
        # Create and publish IMU message
        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'imu_link'
        
        # Simulate IMU readings (walking motion)
        t = time.time()
        imu_msg.angular_velocity.x = 0.1 * math.sin(t)
        imu_msg.angular_velocity.y = 0.1 * math.cos(t)
        imu_msg.angular_velocity.z = 0.05 * math.sin(2 * t)
        
        imu_msg.linear_acceleration.x = 0.5 * math.cos(t)
        imu_msg.linear_acceleration.y = 0.5 * math.sin(t)
        imu_msg.linear_acceleration.z = 9.81  # Gravity
        
        self.imu_publisher.publish(imu_msg)
        
        # Create and publish battery message
        battery_msg = Float64()
        # Simulate battery drain
        battery_msg.data = max(0.0, 100.0 - (self.sequence_number * 0.001))
        self.battery_publisher.publish(battery_msg)
        
        # Log every 100 messages
        if self.sequence_number % 100 == 0:
            self.get_logger().info(
                f'Published sensor data #{self.sequence_number} | '
                f'Battery: {battery_msg.data:.1f}%'
            )


def main(args=None):
    rclpy.init(args=args)
    node = SensorPublisherNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

### Example 2: Subscriber Node (Sensor Consumer)

```python
#!/usr/bin/env python3
"""
sensor_subscriber.py
Subscribes to sensor data and logs robot status
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64


class SensorSubscriberNode(Node):
    """Subscribes to sensor data and monitors robot status."""
    
    def __init__(self):
        super().__init__('sensor_subscriber_node')
        
        # Subscriber for IMU data
        self.imu_subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )
        
        # Subscriber for battery level
        self.battery_subscription = self.create_subscription(
            Float64,
            '/battery_level',
            self.battery_callback,
            10
        )
        
        # State variables
        self.latest_battery = 100.0
        self.message_count = 0
        
        self.get_logger().info('Sensor Subscriber Node started!')
    
    def imu_callback(self, msg: Imu):
        """Process incoming IMU data."""
        self.message_count += 1
        
        # Log significant movements
        angular_magnitude = math.sqrt(
            msg.angular_velocity.x ** 2 +
            msg.angular_velocity.y ** 2 +
            msg.angular_velocity.z ** 2
        )
        
        if angular_magnitude > 0.5:
            self.get_logger().warning(
                f'High angular velocity detected: {angular_magnitude:.3f} rad/s'
            )
        
        # Log every 50 messages
        if self.message_count % 50 == 0:
            self.get_logger().info(
                f'IMU Message #{self.message_count} | '
                f'Angular: ({msg.angular_velocity.x:.3f}, '
                f'{msg.angular_velocity.y:.3f}, '
                f'{msg.angular_velocity.z:.3f})'
            )
    
    def battery_callback(self, msg: Float64):
        """Process incoming battery data."""
        self.latest_battery = msg.data
        
        # Warn on low battery
        if msg.data < 20.0:
            self.get_logger().error(
                f'LOW BATTERY WARNING: {msg.data:.1f}%'
            )
        elif msg.data < 50.0:
            self.get_logger().warn(
                f'Battery below 50%: {msg.data:.1f}%'
            )


# Import math for callback
import math


def main(args=None):
    rclpy.init(args=args)
    node = SensorSubscriberNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

### Example 3: Service Server

```python
#!/usr/bin/env python3
"""
motion_control_service.py
Service server for robot motion control
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class MotionControlService(Node):
    """Service server for motion control calculations."""
    
    def __init__(self):
        super().__init__('motion_control_service')
        
        # Create service server
        self.service = self.create_service(
            AddTwoInts,
            '/calculate_step',
            self.calculate_step_callback
        )
        
        self.get_logger().info('Motion Control Service started!')
    
    def calculate_step_callback(self, request, response):
        """
        Calculate step parameters.
        
        Request: a = step_length, b = step_height
        Response: sum = total_step_energy
        """
        # Simulate step energy calculation
        step_length = request.a
        step_height = request.b
        
        # Energy = length * 10 + height * 50 (simplified model)
        energy = step_length * 10 + step_height * 50
        
        response.sum = int(energy)
        
        self.get_logger().info(
            f'Calculated step: length={step_length}, '
            f'height={step_height}, energy={energy}'
        )
        
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MotionControlService()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Service stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

### Example 4: Service Client

```python
#!/usr/bin/env python3
"""
motion_control_client.py
Client that requests motion calculations
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class MotionControlClient(Node):
    """Client for motion control service."""
    
    def __init__(self):
        super().__init__('motion_control_client')
        
        # Create service client
        self.client = self.create_client(
            AddTwoInts,
            '/calculate_step'
        )
        
        # Wait for service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
        
        self.get_logger().info('Motion Control Client ready!')
    
    def send_step_request(self, step_length: int, step_height: int):
        """Send a step calculation request."""
        request = AddTwoInts.Request()
        request.a = step_length
        request.b = step_height
        
        self.get_logger().info(
            f'Sending request: length={step_length}, height={step_height}'
        )
        
        # Send request asynchronously
        future = self.client.call_async(request)
        
        return future


def main(args=None):
    rclpy.init(args=args)
    node = MotionControlClient()
    
    # Send a request
    future = node.send_step_request(step_length=30, step_height=5)
    
    # Wait for response
    while rclpy.ok():
        rclpy.spin_once(node)
        if future.done():
            try:
                response = future.result()
                node.get_logger().info(f'Result: Energy = {response.sum}')
            except Exception as e:
                node.get_logger().error(f'Service call failed: {e}')
            break
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## Hands-on Lab

### Lab 2.1: Create Publisher and Subscriber Nodes

**Objective:** Build a complete publish/subscribe system for robot sensor data

**Prerequisites:**
- ROS 2 Humble installed
- Basic Python knowledge
- Terminal access

**Time:** 45 minutes

---

### Step 1: Create Workspace and Package

```bash
# Navigate to workspace
cd ~/ros2_ws/src

# Create package for communication examples
ros2 pkg create --build-type ament_python comm_examples \
    --dependencies rclpy std_msgs sensor_msgs example_interfaces

# Navigate to package
cd comm_examples/comm_examples
```

---

### Step 2: Create Publisher Node

Create `sensor_publisher.py`:

```bash
nano sensor_publisher.py
```

Copy the publisher code from **Example 1** above.

Make executable:

```bash
chmod +x sensor_publisher.py
```

---

### Step 3: Create Subscriber Node

Create `sensor_subscriber.py`:

```bash
nano sensor_subscriber.py
```

Copy the subscriber code from **Example 2** above.

Make executable:

```bash
chmod +x sensor_subscriber.py
```

---

### Step 4: Update setup.py

Edit `setup.py` to register executables:

```python
from setuptools import setup

package_name = 'comm_examples'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Your Name',
    author_email='your.email@example.com',
    description='ROS 2 Communication Examples',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_publisher = comm_examples.sensor_publisher:main',
            'sensor_subscriber = comm_examples.sensor_subscriber:main',
        ],
    },
)
```

---

### Step 5: Build the Package

```bash
# Return to workspace root
cd ~/ros2_ws

# Build
colcon build --packages-select comm_examples

# Source workspace
source install/setup.bash
```

---

### Step 6: Run Publisher and Subscriber

**Terminal 1 — Run Publisher:**

```bash
source install/setup.bash
ros2 run comm_examples sensor_publisher
```

**Terminal 2 — Run Subscriber:**

```bash
source install/setup.bash
ros2 run comm_examples sensor_subscriber
```

**Expected Output:**

Terminal 1 (Publisher):
```
[INFO] [sensor_publisher_node]: Sensor Publisher Node started!
[INFO] [sensor_publisher_node]: Published sensor data #100 | Battery: 99.9%
[INFO] [sensor_publisher_node]: Published sensor data #200 | Battery: 99.8%
```

Terminal 2 (Subscriber):
```
[INFO] [sensor_subscriber_node]: Sensor Subscriber Node started!
[INFO] [sensor_subscriber_node]: IMU Message #50 | Angular: (0.084, 0.053, 0.042)
```

---

### Step 7: Inspect Topics

Open a **new terminal** and explore:

```bash
# List all active topics
ros2 topic list

# Expected output:
# /battery_level
# /imu/data
# /parameter_events
# /rosout

# View topic type
ros2 topic type /imu/data
# Expected: sensor_msgs/msg/Imu

# View topic info
ros2 topic info /imu/data --verbose

# Echo topic messages
ros2 topic echo /battery_level

# View messages at 1 Hz
ros2 topic hz /imu/data
```

---

### Step 8: Visualize with rqt

```bash
# Install rqt if not installed
sudo apt install ros-humble-rqt ros-humble-rqt-common-plugins

# Launch rqt
ros2 run rqt_gui rqt_gui
```

In rqt:
1. Go to **Plugins → Topics → Topic Monitor**
2. Expand `/imu/data` and `/battery_level`
3. Observe real-time data visualization

---

## Summary

### Key Takeaways

1. **Nodes** are the basic computational units in ROS 2
2. **Topics** enable anonymous publish/subscribe communication
3. **Services** provide synchronous request/response patterns
4. **Actions** handle long-running tasks with feedback
5. **Message types** define the structure of data exchanged
6. **QoS policies** control message delivery behavior

### Communication Pattern Comparison

| Pattern | Direction | Blocking | Use Case |
|---------|-----------|----------|----------|
| **Topic** | One-to-Many | No | Sensor data, status updates |
| **Service** | One-to-One | Yes | Configuration, calculations |
| **Action** | One-to-One | No | Navigation, manipulation |

---

## Exercises

### Exercise 2.1: Custom Message Type

Create a custom message type for robot joint states:

1. Create a `msg` directory in your package
2. Define `JointState.msg`:
   ```text
   string joint_name
   float64 position
   float64 velocity
   float64 effort
   float64 temperature
   ```
3. Update `package.xml` with message dependencies
4. Update `setup.py` to include message files
5. Rebuild and test

### Exercise 2.2: Multi-Topic Publisher

Modify the sensor publisher to:

1. Add a third topic publishing robot temperature
2. Publish at different rates (IMU: 100Hz, Battery: 1Hz, Temperature: 0.5Hz)
3. Use multiple timers

### Exercise 2.3: Service-Based Configuration

Create a service that:

1. Accepts a robot name and maximum velocity
2. Returns a confirmation message
3. Stores the configuration in node parameters

### Exercise 2.4: Topic Analysis

Use ROS 2 CLI tools to:

1. List all topics in a running system
2. Find which nodes publish/subscribe to each topic
3. Record topic data to a bag file
4. Play back the bag file

Document your findings.

---

## Next Chapter

In **Chapter 3: Python AI Agents with ROS 2**, you will learn:

- How to build AI agents using rclpy
- Processing sensor data for decision-making
- Integrating LLMs with robot controllers
- Creating intelligent behavior trees

---

## Resources

### Official Documentation

- [ROS 2 Topics](https://docs.ros.org/en/humble/Concepts/About-Topics.html)
- [ROS 2 Services](https://docs.ros.org/en/humble/Concepts/About-Services.html)
- [ROS 2 Actions](https://docs.ros.org/en/humble/Concepts/About-Actions.html)

### Tutorials

- [Writing a Simple Publisher and Subscriber](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [Writing a Simple Service and Client](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html)
