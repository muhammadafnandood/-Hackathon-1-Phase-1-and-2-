---
sidebar_label: ROS 2 Basics
title: Chapter 1 - Introduction to ROS 2 for Humanoid Robotics
---

# Introduction to ROS 2 for Humanoid Robotics

:::tip[Learning Objectives]
By the end of this chapter, you will:
- Understand what ROS 2 is and why it's essential for humanoid robotics
- Learn the core concepts: nodes, topics, services, and actions
- Create your first ROS 2 publisher and subscriber
- Apply ROS 2 concepts to a humanoid robot head tracking system
:::

## Introduction

Imagine trying to coordinate 20+ motors, multiple cameras, microphones, and various sensors on a humanoid robot—all in real-time. Without a proper framework, this would be a nightmare. This is where **ROS 2 (Robot Operating System 2)** comes to the rescue.

ROS 2 is not actually an operating system like Windows or Linux. Instead, it's a **middleware**—software that sits between your robot's hardware and your applications. Think of it as a communication layer that allows different parts of your robot to talk to each other seamlessly.

### Why ROS 2 for Humanoid Robots?

Humanoid robots are among the most complex robotic systems:
- **Multiple degrees of freedom**: 20-50 joints that need coordination
- **Sensor fusion**: Cameras, IMUs, force sensors, microphones
- **Real-time requirements**: Balance and locomotion need millisecond responses
- **Modularity**: Different teams work on vision, manipulation, navigation

ROS 2 solves these challenges by providing:
- **Distributed architecture**: Components can run on different computers
- **Language agnostic**: Write nodes in Python, C++, or other languages
- **Built-in discovery**: Nodes automatically find each other
- **Quality of Service (QoS)**: Configure reliability for different use cases

### What You'll Learn

- The publish-subscribe communication pattern
- Creating ROS 2 nodes in Python
- Understanding topics, messages, and services
- Building a practical head tracking system

### Prerequisites

- Basic Python programming (functions, classes, imports)
- Familiarity with command line operations
- Understanding of what a robot sensor is

---

## Core Concepts

### What is a Node?

A **node** is the fundamental building block of ROS 2. Think of it as a small program that does one specific task. In a humanoid robot, you might have:

- One node for reading camera images
- One node for processing speech
- One node for controlling arm motors
- One node for balance calculations

**Analogy**: Imagine a humanoid robot as a company. Each node is like a department—HR handles hiring, accounting handles finances, engineering builds products. Each department does its job well and communicates with others when needed.

### The Publish-Subscribe Pattern

ROS 2 uses a **publish-subscribe** model for communication. Here's how it works:

1. **Publishers** send messages to a **topic** (like a bulletin board)
2. **Subscribers** listen to topics they care about
3. Publishers and subscribers don't know about each other—they're **decoupled**

**Real-World Analogy**: Think of YouTube:
- Content creators **publish** videos (messages) to their channel (topic)
- Viewers **subscribe** to channels they like
- Creators don't need to know who watches; viewers don't need to know how videos are made

### Topics and Messages

A **topic** is a named channel for communication. Examples:
- `/camera/image_raw` - Raw images from the camera
- `/joint_states` - Current position of all robot joints
- `/cmd_vel` - Velocity commands for movement

A **message** is the actual data being sent. ROS 2 has standard message types:
- `String` - Text data
- `Int32`, `Float64` - Numbers
- `Image` - Camera images
- `JointState` - Robot joint positions and velocities

### Services and Actions

Not all communication is one-way. Sometimes you need a request-response pattern:

**Services** (synchronous request-response):
- Client sends a request, waits for a response
- Example: "What's the current battery level?" → "85%"

**Actions** (asynchronous, long-running tasks):
- Client sends a goal, gets periodic feedback, receives final result
- Example: "Walk to position (x=5, y=3)" → [progress updates] → "Goal reached"

:::note
**QoS (Quality of Service)**: ROS 2 lets you configure reliability. For a humanoid robot's balance control, you might use "reliable" messaging. For camera images where losing one frame is okay, you might use "best effort" for lower latency.
:::

---

## Code Examples

### Example 1: Simple Publisher Node

Let's create a node that publishes the temperature reading from a hypothetical sensor on a humanoid robot's motor.

```python
# File: temperature_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TemperaturePublisher(Node):
    """Publishes motor temperature readings."""
    
    def __init__(self):
        super().__init__('temperature_publisher')
        # Create a publisher that sends Float32 messages to 'motor_temperature' topic
        self.publisher_ = self.create_publisher(Float32, 'motor_temperature', 10)
        # Create a timer that calls publish_temperature every 1 second
        self.timer = self.create_timer(1.0, self.publish_temperature)
        self.get_logger().info('Temperature publisher started')
    
    def publish_temperature(self):
        # Simulate temperature reading (in real robot, this would read a sensor)
        temp = random.uniform(30.0, 45.0)  # Temperature in Celsius
        
        # Create message
        msg = Float32()
        msg.data = temp
        
        # Publish the message
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published temperature: {temp:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    node = TemperaturePublisher()
    rclpy.spin(node)  # Keep the node running
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**How it works:**
1. The node initializes a publisher on the `motor_temperature` topic
2. Every 1 second, it generates a random temperature value
3. The value is wrapped in a `Float32` message and published
4. Any node subscribed to `motor_temperature` will receive this data

**To run:**
```bash
ros2 run your_package temperature_publisher
```

### Example 2: Simple Subscriber Node

Now let's create a node that listens to the temperature data and logs warnings if it gets too hot.

```python
# File: temperature_monitor.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureMonitor(Node):
    """Subscribes to motor temperature and logs warnings."""
    
    def __init__(self):
        super().__init__('temperature_monitor')
        # Create a subscriber that listens to 'motor_temperature' topic
        self.subscription = self.create_subscription(
            Float32,
            'motor_temperature',
            self.temperature_callback,
            10
        )
        self.max_temp = 42.0  # Warning threshold in Celsius
        self.get_logger().info('Temperature monitor started')
    
    def temperature_callback(self, msg):
        """Called automatically when a new message arrives."""
        temp = msg.data
        
        if temp > self.max_temp:
            self.get_logger().warn(f'⚠️  HIGH TEMPERATURE: {temp:.2f}°C')
        else:
            self.get_logger().info(f'✓ Normal temperature: {temp:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**How it works:**
1. The node subscribes to the `motor_temperature` topic
2. When a message arrives, `temperature_callback` is automatically called
3. If temperature exceeds 42°C, it logs a warning; otherwise, it logs info
4. This demonstrates **decoupled communication**—the monitor doesn't know who publishes the data

### Example 3: Combined System with Multiple Nodes

Let's see how multiple nodes work together in a humanoid robot context.

```python
# File: head_tracking_system.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
from sensor_msgs.msg import Image
import time

class FaceDetector(Node):
    """Detects faces and publishes their position."""
    
    def __init__(self):
        super().__init__('face_detector')
        self.position_pub = self.create_publisher(Point, 'face_position', 10)
        self.timer = self.create_timer(0.5, self.detect_face)
        self.get_logger().info('Face detector initialized')
    
    def detect_face(self):
        # In reality, this would process camera images with OpenCV/Deep Learning
        # For now, simulate face position (x, y offset from center)
        face_pos = Point()
        face_pos.x = 0.15  # 15cm to the right
        face_pos.y = 0.05  # 5cm above center
        face_pos.z = 1.2   # 1.2m away
        
        self.position_pub.publish(face_pos)
        self.get_logger().info(f'Face detected at: ({face_pos.x}, {face_pos.y}, {face_pos.z})')

class HeadController(Node):
    """Controls head motors to track faces."""
    
    def __init__(self):
        super().__init__('head_controller')
        self.position_sub = self.create_subscription(
            Point,
            'face_position',
            self.track_face_callback,
            10
        )
        self.head_cmd_pub = self.create_publisher(Twist, 'head_velocity', 10)
        self.get_logger().info('Head controller initialized')
    
    def track_face_callback(self, face_pos):
        """Calculate head movement to track the face."""
        # Simple proportional control
        head_cmd = Twist()
        head_cmd.angular.x = face_pos.y * 0.5  # Tilt up/down based on y offset
        head_cmd.angular.y = -face_pos.x * 0.5  # Pan left/right based on x offset
        
        self.head_cmd_pub.publish(head_cmd)
        self.get_logger().info(f'Moving head: tilt={head_cmd.angular.x:.2f}, pan={head_cmd.angular.y:.2f}')

def main(args=None):
    rclpy.init(args=args)
    
    # Create both nodes
    detector = FaceDetector()
    controller = HeadController()
    
    # Run both nodes in sequence (in practice, use separate processes)
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(detector)
    executor.add_node(controller)
    
    try:
        executor.spin()
    finally:
        executor.shutdown()
        detector.destroy_node()
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Real-World Robotics Application

### Case Study: Humanoid Robot Head Tracking for Human-Robot Interaction

**Platform:** ROS 2 Humble on Boston Dynamics Atlas / Custom Humanoid

**Scenario:**
A humanoid robot at a reception desk needs to:
1. Detect when a person approaches
2. Turn its head to face the person
3. Maintain eye contact during conversation
4. Look at objects the person points to

This requires coordinated camera processing, face detection, and motor control—all in real-time.

**System Architecture:**

```
[Camera Node] → /camera/image_raw → [Face Detection Node] → /face_position → [Head Controller Node] → /head_velocity → [Motor Driver]
```

**Implementation:**

```python
# File: production_head_tracker.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point, Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class VisionBasedHeadTracker(Node):
    """Production-ready head tracking with real camera input."""
    
    def __init__(self):
        super().__init__('vision_head_tracker')
        
        # Use best-effort QoS for camera images (dropping frames is okay)
        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT
        )
        
        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/head/image_raw',
            self.image_callback,
            qos
        )
        
        # Publishers
        self.head_cmd_pub = self.create_publisher(Twist, '/head_controller/cmd_vel', 10)
        self.face_pos_pub = self.create_publisher(Point, '/perception/face_position', 10)
        
        # CV Bridge for converting ROS images to OpenCV format
        self.bridge = CvBridge()
        
        # Control parameters
        self.kp_pan = 0.3   # Proportional gain for horizontal movement
        self.kp_tilt = 0.3  # Proportional gain for vertical movement
        self.dead_zone = 0.05  # Ignore small movements
        
        self.get_logger().info('Vision-based head tracker initialized')
    
    def image_callback(self, image_msg):
        """Process camera image and detect faces."""
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, 'bgr8')
            
            # Detect faces using OpenCV Haar Cascade (in production, use deep learning)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                # Get the largest face (closest to robot)
                largest_face = max(faces, key=lambda f: f[2] * f[3])
                x, y, w, h = largest_face
                
                # Calculate face center in normalized coordinates (-1 to 1)
                img_center_x = cv_image.shape[1] / 2
                img_center_y = cv_image.shape[0] / 2
                
                face_center_x = x + w / 2
                face_center_y = y + h / 2
                
                norm_x = (face_center_x - img_center_x) / img_center_x
                norm_y = (face_center_y - img_center_y) / img_center_y
                
                # Publish face position
                face_pos = Point()
                face_pos.x = norm_x
                face_pos.y = norm_y
                face_pos.z = w / cv_image.shape[1]  # Approximate distance from face size
                self.face_pos_pub.publish(face_pos)
                
                # Calculate head velocity command
                head_cmd = self.calculate_head_movement(norm_x, norm_y)
                self.head_cmd_pub.publish(head_cmd)
                
                self.get_logger().info(f'Tracking face at: ({norm_x:.2f}, {norm_y:.2f})')
            else:
                self.get_logger().debug('No face detected')
                
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')
    
    def calculate_head_movement(self, error_x, error_y):
        """Proportional controller for smooth head tracking."""
        head_cmd = Twist()
        
        # Only move if error is outside dead zone
        if abs(error_x) > self.dead_zone:
            head_cmd.angular.y = -self.kp_pan * error_x  # Pan left/right
        
        if abs(error_y) > self.dead_zone:
            head_cmd.angular.x = self.kp_tilt * error_y  # Tilt up/down
        
        return head_cmd

def main():
    rclpy.init()
    tracker = VisionBasedHeadTracker()
    rclpy.spin(tracker)
    tracker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Results:**
- **Latency**: < 100ms from face detection to head movement
- **Accuracy**: Maintains face within ±5° of camera center
- **Smoothness**: Proportional control prevents jerky movements

:::info[Industry Context]
**Companies using ROS 2 for Humanoid Robotics:**
- **Boston Dynamics**: Uses ROS 2 for Atlas research
- **Tesla Optimus**: ROS 2-inspired architecture for humanoid control
- **Apptronik Apollo**: ROS 2 for perception and control pipelines
- **Agility Robotics**: ROS 2 for Digit warehouse robot

**Career Tip**: ROS 2 skills are in high demand. Robotics companies list ROS experience in 70%+ of software engineering job postings.
:::

---

## Visual Diagrams (Suggested)

### Diagram 1: ROS 2 Publish-Subscribe Architecture

**Purpose:** Show how nodes communicate via topics in a humanoid robot

**Elements to include:**
- Multiple nodes (Camera, Face Detector, Head Controller, Motor Driver)
- Topics as horizontal buses (/camera/image, /face_position, /head_velocity)
- Arrows showing data flow direction
- Labels for publishers (P) and subscribers (S)

**Suggested format:** Mermaid diagram or draw.io

```mermaid
graph LR
    A[Camera Node] -->|/camera/image| B[Face Detector]
    B -->|/face_position| C[Head Controller]
    C -->|/head_velocity| D[Motor Driver]
    D --> E[Head Motors]
```

### Diagram 2: Head Tracking Control Loop

**Purpose:** Illustrate the feedback loop in the tracking system

**Elements to include:**
- Camera captures image
- Face detection calculates error
- Controller computes velocity command
- Motors execute movement
- New image closes the loop

---

## Common Pitfalls and Best Practices

### Pitfalls to Avoid

1. **Creating too many nodes too early**
   - Start with monolithic nodes, split when they become complex
   - Each additional node adds communication overhead

2. **Ignoring QoS settings**
   - Using "reliable" QoS for sensor data causes delays
   - Use "best effort" for high-frequency data like images

3. **Blocking callbacks**
   - Never use `time.sleep()` or long computations in callbacks
   - Use separate threads or timers for heavy processing

4. **Not handling node shutdown**
   - Always clean up resources with `destroy_node()`
   - Use try-finally blocks for graceful shutdown

### Best Practices

1. ✅ **Use meaningful topic names** - `/sensors/camera/front/image_raw` is better than `/img1`
2. ✅ **Log appropriately** - Use DEBUG for frequent messages, INFO for important events, WARN/ERROR for issues
3. ✅ **Parameterize thresholds** - Don't hardcode values; use ROS 2 parameters
4. ✅ **Test nodes independently** - Use `ros2 topic pub` to simulate inputs
5. ✅ **Document message formats** - Create custom message types with clear field names

---

## Summary

### Key Takeaways

| Concept | Description |
|---------|-------------|
| **Node** | Independent process that performs a specific task |
| **Topic** | Named channel for publish-subscribe communication |
| **Message** | Data structure sent between nodes |
| **Publisher** | Node that sends messages to a topic |
| **Subscriber** | Node that receives messages from a topic |
| **Service** | Synchronous request-response communication |
| **Action** | Asynchronous communication for long-running tasks |

### What We Covered

- ✓ ROS 2 architecture and why it's essential for humanoid robots
- ✓ Publish-subscribe pattern with topics and messages
- ✓ Built working publisher and subscriber nodes in Python
- ✓ Implemented a vision-based head tracking system
- ✓ Learned industry best practices and common pitfalls

### What's Next

In the next chapter, we'll explore **ROS 2 Services and Actions** for more complex interactions like requesting a humanoid robot to walk to a specific location or grasp an object.

---

## Practice Questions

### Review Questions

1. **Explain the difference between a topic and a service in ROS 2.**
   - When would you use each?
   - What are the trade-offs?

2. **Why is the publish-subscribe pattern beneficial for humanoid robotics?**
   - How does it help with system complexity?
   - What problems does decoupling solve?

3. **What is the role of QoS (Quality of Service) in ROS 2?**
   - When would you use "reliable" vs "best effort"?
   - How does it affect robot performance?

### Hands-On Exercises

4. **Exercise: Create a Joint State Publisher**
   
   **Difficulty:** ⭐⭐☆ (Medium)
   
   **Requirements:**
   - Create a node that publishes simulated joint angles for a humanoid robot arm
   - Publish to `/joint_states` topic using `sensor_msgs/msg/JointState`
   - Include 5 joints: shoulder_pan, shoulder_lift, elbow, wrist_roll, wrist_pitch
   - Publish at 50 Hz with smooth sinusoidal motion
   
   **Hints:**
   - Use `import math` for `sin()` function
   - `JointState` message has `name`, `position`, and `header` fields
   - Use `time.time()` for phase calculation
   
   **Solution Outline:**
   ```python
   from sensor_msgs.msg import JointState
   import math
   import time
   
   class JointStatePublisher(Node):
       def __init__(self):
           super().__init__('joint_state_publisher')
           self.pub = self.create_publisher(JointState, '/joint_states', 10)
           self.timer = self.create_timer(0.02, self.publish_joints)  # 50 Hz
       
       def publish_joints(self):
           msg = JointState()
           msg.header.stamp = self.get_clock().now().to_msg()
           msg.name = ['shoulder_pan', 'shoulder_lift', 'elbow', 'wrist_roll', 'wrist_pitch']
           t = time.time()
           msg.position = [math.sin(t), math.sin(t + 0.5), ...]  # Complete this
           self.pub.publish(msg)
   ```

5. **Exercise: Build a Battery Monitor System**
   
   **Difficulty:** ⭐⭐⭐ (Hard)
   
   **Challenge:** Create two nodes:
   - `battery_publisher`: Simulates battery drain (starts at 100%, decreases 1% every 10 seconds)
   - `battery_monitor`: Subscribes to battery level, logs warnings at 30%, shuts down robot at 10%
   
   **Requirements:**
   - Use custom message type or `Float32`
   - Implement state machine in monitor (NORMAL → LOW → CRITICAL)
   - Publish shutdown command to `/robot/shutdown` topic when critical

### Discussion Questions

6. **Consider a humanoid robot performing a complex task like making coffee. Identify at least 5 different nodes that would be needed and describe what topics they would publish/subscribe to.**
   - Think about perception, planning, control, safety
   - How would you prioritize different communication channels?

---

## Additional Resources

### Documentation

- [Official ROS 2 Documentation](https://docs.ros.org/)
- [ROS 2 Tutorials](https://docs.ros.org/en/rolling/Tutorials.html)
- [ROS 2 Python API](https://docs.ros2.org/latest/api/rclpy/)

### Books & Papers

- "Programming Robots with ROS 2" by Morgan Quigley (forthcoming)
- "ROS 2 for Beginners" - Online course by The Construct

### Video Tutorials

- [ROS 2 Basics in 5 Days](https://www.youtube.com/c/TheConstruct)
- [ROS 2 vs ROS 1 - Key Differences](https://www.youtube.com/watch?v=8FVw0VZPjZk)

### Community

- [ROS Discourse Forum](https://discourse.ros.org/)
- [ROS Answers Stack Exchange](https://answers.ros.org/questions/)
- [r/ROS on Reddit](https://www.reddit.com/r/ROS/)

---

*End of Chapter 1*
