---
title: Python AI Agents with ROS 2
description: Learn to build AI agents using rclpy that process sensor data and control robot behavior
sidebar_label: 1.3 Python AI Agents
---

# Chapter 3: Python AI Agents with ROS 2

## Learning Objectives

By the end of this chapter, you will be able to:

- **Build** AI agent nodes using the rclpy client library
- **Process** sensor data for intelligent decision-making
- **Connect** LLMs and AI models with robot controllers
- **Implement** behavior trees for complex robot behaviors
- **Design** event-driven architectures for reactive robots
- **Deploy** AI agents in production robotics systems

---

## Concept Explanation

### What is an AI Agent in Robotics?

**Definition: AI Agent** — A software entity that perceives its environment through sensors, processes information using AI models, and takes actions through actuators to achieve goals.

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent Architecture                     │
│                                                              │
│  ┌─────────────┐     Sensor Data      ┌─────────────┐       │
│  │ Environment │─────────────────────►│  Perception │       │
│  │  (World)    │                      │   Module    │       │
│  └─────────────┘                      └──────┬──────┘       │
│                                              │               │
│                                              ▼               │
│                                       ┌─────────────┐       │
│                                       │    AI/LLM   │       │
│                                       │   Brain     │       │
│                                       └──────┬──────┘       │
│                                              │               │
│                                              ▼               │
│                                       ┌─────────────┐       │
│                                       │  Planning   │       │
│                                       │   Module    │       │
│                                       └──────┬──────┘       │
│                                              │               │
│                                              ▼               │
│  ┌─────────────┐     Action Commands  ┌─────────────┐       │
│  │   Robot     │◄─────────────────────│   Control   │       │
│  │  Actuators  │                      │   Module    │       │
│  └─────────────┘                      └─────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**AI Agent Components:**

| Component | Function | ROS 2 Implementation |
|-----------|----------|---------------------|
| **Perception** | Process sensor data | Subscriber nodes |
| **Reasoning** | Make decisions | AI/LLM integration |
| **Planning** | Generate action sequences | Service/Action clients |
| **Control** | Execute actions | Publisher nodes |

### The rclpy Client Library

**rclpy** is the official ROS 2 client library for Python.

**Key Features:**

- Full access to ROS 2 communication primitives
- Async/await support for concurrent operations
- Integration with Python AI/ML libraries
- Easy prototyping and testing

**Basic rclpy Node Structure:**

```python
import rclpy
from rclpy.node import Node

class AIAgentNode(Node):
    def __init__(self):
        super().__init__('ai_agent_node')
        
        # Subscribers (Perception)
        self.sensor_sub = self.create_subscription(
            SensorMsg,
            '/sensor_topic',
            self.sensor_callback,
            10
        )
        
        # Publishers (Control)
        self.command_pub = self.create_publisher(
            CommandMsg,
            '/command_topic',
            10
        )
        
        # Services (Reasoning)
        self.ai_service = self.create_service(
            AIMsg,
            '/ai_query',
            self.ai_callback
        )
    
    def sensor_callback(self, msg):
        # Process sensor data
        pass
    
    def ai_callback(self, request, response):
        # AI reasoning
        return response

def main():
    rclpy.init()
    node = AIAgentNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Connecting AI Agents with Robot Controllers

**Architecture Pattern:**

```
┌─────────────────────────────────────────────────────────────┐
│              AI Agent + Robot Controller Integration         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              AI Agent Node (Python)                  │    │
│  │                                                      │    │
│  │  ┌──────────────┐    ┌──────────────┐               │    │
│  │  │  LLM/Model   │    │  Decision    │               │    │
│  │  │  Integration │───►│   Logic      │               │    │
│  │  └──────────────┘    └──────────────┘               │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│                    ROS 2 Topics/Services                     │
│                              │                               │
│  ┌───────────────────────────▼─────────────────────────┐    │
│  │           Robot Controller Node (Python/C++)         │    │
│  │                                                      │    │
│  │  ┌──────────────┐    ┌──────────────┐               │    │
│  │  │   Command    │    │   Hardware   │               │    │
│  │  │  Interpreter │───►│   Interface  │               │    │
│  │  └──────────────┘    └──────────────┘               │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│                    Hardware Interface                        │
│                              │                               │
│  ┌───────────────────────────▼─────────────────────────┐    │
│  │              Robot Hardware                          │    │
│  │    Motors │ Sensors │ Cameras │ LiDAR               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Sensor Data Processing Pipeline

**Data Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│              Sensor Data Processing Pipeline                 │
│                                                              │
│  Raw Sensor Data                                             │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐                                            │
│  │  Filtering  │ (Noise removal, smoothing)                 │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │  Fusion     │ (Combine multiple sensors)                 │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │  Feature    │ (Extract relevant information)             │
│  │  Extraction │                                             │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │  AI/ML      │ (Classification, prediction)               │
│  │  Inference  │                                             │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  Decision Output                                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Overview

### Complete AI Agent System for Humanoid Robot

```
┌─────────────────────────────────────────────────────────────┐
│           Humanoid Robot AI Agent System Architecture        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Voice Interface Layer                   │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐    │    │
│  │  │  Whisper  │───►│   LLM     │───►│   Task    │    │    │
│  │  │  (STT)    │    │  Planner  │    │  Decoder  │    │    │
│  │  └───────────┘    └───────────┘    └───────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Perception Layer                        │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐    │    │
│  │  │  Vision   │    │   Audio   │    │  Proprio- │    │    │
│  │  │  (YOLO)   │    │  (VAD)    │    │  ception  │    │    │
│  │  └───────────┘    └───────────┘    └───────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Decision Layer                          │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐    │    │
│  │  │  Behavior │    │   Motion  │    │  Safety   │    │    │
│  │  │   Tree    │───►│  Planner  │───►│  Monitor  │    │    │
│  │  └───────────┘    └───────────┘    └───────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Control Layer                           │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐    │    │
│  │  │   Whole   │    │   Joint   │    │  Motor    │    │    │
│  │  │   Body    │───►│  Space    │───►│  Drivers  │    │    │
│  │  │  Control  │    │  Control  │    │           │    │    │
│  │  └───────────┘    └───────────┘    └───────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Communication: ROS 2 Topics, Services, Actions              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### AI Agent Communication Graph

```
┌─────────────────────────────────────────────────────────────┐
│              ROS 2 Topics for AI Agent Communication         │
│                                                              │
│  /voice/command (std_msgs/String)                            │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────┐                                         │
│  │  Voice Agent    │──► /llm/intent (CustomMsg)              │
│  │  (Whisper+LLM)  │                                         │
│  └─────────────────┘                                         │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────┐                                         │
│  │  Task Agent     │──► /motion/goal (GeometryMsg)           │
│  │  (Planner)      │                                         │
│  └─────────────────┘                                         │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────┐                                         │
│  │  Motion Agent   │──► /joint/commands (SensorMsg)          │
│  │  (Controller)   │                                         │
│  └─────────────────┘                                         │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────┐                                         │
│  │  Hardware Agent │──► /motor/ pwm (CustomMsg)              │
│  │  (Driver)       │                                         │
│  └─────────────────┘                                         │
│                                                              │
│  Feedback Loop:                                              │
│  /sensor/imu, /sensor/camera, /sensor/joint_states          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Example 1: Basic AI Agent Node

```python
#!/usr/bin/env python3
"""
ai_agent_node.py
Basic AI agent that processes sensor data and makes decisions
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Bool
import numpy as np


class AIAgentNode(Node):
    """AI Agent that processes IMU data and commands robot movement."""
    
    def __init__(self):
        super().__init__('ai_agent_node')
        
        # === Perception: Subscribers ===
        self.imu_subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )
        
        self.voice_command_subscription = self.create_subscription(
            String,
            '/voice/command',
            self.voice_command_callback,
            10
        )
        
        # === Control: Publishers ===
        self.velocity_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        self.status_publisher = self.create_publisher(
            String,
            '/agent/status',
            10
        )
        
        # === State Variables ===
        self.current_imu = None
        self.current_command = None
        self.is_active = False
        self.agent_state = "IDLE"
        
        # === AI Model Parameters ===
        self.balance_threshold = 0.5  # rad/s
        self.movement_gain = 0.5
        
        self.get_logger().info('AI Agent Node initialized!')
        
        # Publish initial status
        self.publish_status("AI Agent started - waiting for commands")
    
    def imu_callback(self, msg: Imu):
        """Process IMU sensor data for balance control."""
        self.current_imu = msg
        
        # Calculate angular velocity magnitude
        angular_mag = np.sqrt(
            msg.angular_velocity.x ** 2 +
            msg.angular_velocity.y ** 2 +
            msg.angular_velocity.z ** 2
        )
        
        # Check if robot is losing balance
        if angular_mag > self.balance_threshold and self.is_active:
            self.get_logger().warn(f'Balance disturbance detected: {angular_mag:.3f}')
            self.execute_balance_recovery(msg)
    
    def voice_command_callback(self, msg: String):
        """Process voice commands."""
        command = msg.data.lower()
        self.current_command = command
        
        self.get_logger().info(f'Received voice command: {command}')
        
        # Parse command
        if 'start' in command or 'begin' in command:
            self.is_active = True
            self.agent_state = "ACTIVE"
            self.publish_status("Agent activated")
        
        elif 'stop' in command or 'halt' in command:
            self.is_active = False
            self.agent_state = "IDLE"
            self.stop_robot()
            self.publish_status("Agent deactivated")
        
        elif 'forward' in command or 'move' in command:
            if self.is_active:
                self.move_forward()
        
        elif 'backward' in command or 'back' in command:
            if self.is_active:
                self.move_backward()
        
        elif 'turn' in command or 'rotate' in command:
            if self.is_active:
                self.turn_in_place()
    
    def execute_balance_recovery(self, imu_msg: Imu):
        """Execute balance recovery maneuver."""
        self.get_logger().info('Executing balance recovery')
        
        # Create counter-movement command
        twist_msg = Twist()
        
        # Counter the angular velocity
        twist_msg.angular.x = -imu_msg.angular_velocity.x * self.movement_gain
        twist_msg.angular.y = -imu_msg.angular_velocity.y * self.movement_gain
        
        self.velocity_publisher.publish(twist_msg)
        
        self.agent_state = "BALANCE_RECOVERY"
    
    def move_forward(self):
        """Command robot to move forward."""
        twist_msg = Twist()
        twist_msg.linear.x = 0.3  # m/s
        self.velocity_publisher.publish(twist_msg)
        self.agent_state = "MOVING_FORWARD"
        self.publish_status("Moving forward")
    
    def move_backward(self):
        """Command robot to move backward."""
        twist_msg = Twist()
        twist_msg.linear.x = -0.3  # m/s
        self.velocity_publisher.publish(twist_msg)
        self.agent_state = "MOVING_BACKWARD"
        self.publish_status("Moving backward")
    
    def turn_in_place(self):
        """Command robot to turn in place."""
        twist_msg = Twist()
        twist_msg.angular.z = 0.5  # rad/s
        self.velocity_publisher.publish(twist_msg)
        self.agent_state = "TURNING"
        self.publish_status("Turning in place")
    
    def stop_robot(self):
        """Stop all robot movement."""
        twist_msg = Twist()
        self.velocity_publisher.publish(twist_msg)
        self.publish_status("Robot stopped")
    
    def publish_status(self, status_text: str):
        """Publish agent status."""
        status_msg = String()
        status_msg.data = f"[{self.agent_state}] {status_text}"
        self.status_publisher.publish(status_msg)
        self.get_logger().info(f'Status: {status_msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = AIAgentNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('AI Agent stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

### Example 2: AI Agent with LLM Integration

```python
#!/usr/bin/env python3
"""
llm_agent_node.py
AI agent with LLM integration for natural language task planning
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import json

# Note: In production, install openai package
# pip install openai


class LLMAgentNode(Node):
    """AI Agent with LLM integration for task planning."""
    
    def __init__(self):
        super().__init__('llm_agent_node')
        
        # Use reentrant callback group for concurrent operations
        self.callback_group = ReentrantCallbackGroup()
        
        # === Subscribers ===
        self.voice_subscription = self.create_subscription(
            String,
            '/voice/transcript',
            self.voice_callback,
            10,
            callback_group=self.callback_group
        )
        
        # === Publishers ===
        self.task_publisher = self.create_publisher(
            String,
            '/task/plan',
            10
        )
        
        self.response_publisher = self.create_publisher(
            String,
            '/agent/response',
            10
        )
        
        # === LLM Configuration ===
        # In production, use actual API key from environment
        self.llm_api_key = self.declare_parameter(
            'llm_api_key',
            'your-api-key-here'
        ).get_parameter_value().string_value
        
        self.llm_model = self.declare_parameter(
            'llm_model',
            'gpt-4'
        ).get_parameter_value().string_value
        
        # === Task History ===
        self.task_history = []
        
        self.get_logger().info('LLM Agent Node initialized!')
    
    def voice_callback(self, msg: String):
        """Process voice transcript and generate task plan."""
        user_input = msg.data
        self.get_logger().info(f'User said: {user_input}')
        
        # Query LLM for task planning
        task_plan = self.query_llm_for_task(user_input)
        
        # Publish task plan
        if task_plan:
            self.task_publisher.publish(String(data=task_plan))
            
            # Generate and publish response
            response = self.generate_response(user_input, task_plan)
            self.response_publisher.publish(String(data=response))
    
    def query_llm_for_task(self, user_input: str) -> str:
        """
        Query LLM to convert natural language to task plan.
        
        In production, this would call OpenAI API or similar.
        Here we use rule-based parsing for demonstration.
        """
        user_input_lower = user_input.lower()
        
        # Simple rule-based task planning (replace with actual LLM call)
        task_plan = {
            "input": user_input,
            "actions": [],
            "parameters": {}
        }
        
        # Parse common robot commands
        if 'pick up' in user_input_lower or 'grab' in user_input_lower:
            task_plan["actions"].append("navigate_to_object")
            task_plan["actions"].append("detect_object")
            task_plan["actions"].append("grasp_object")
            task_plan["parameters"]["grasp_type"] = "precision"
        
        if 'place' in user_input_lower or 'put' in user_input_lower:
            task_plan["actions"].append("navigate_to_location")
            task_plan["actions"].append("release_object")
        
        if 'go to' in user_input_lower or 'move to' in user_input_lower:
            task_plan["actions"].append("navigate_to_location")
            # Extract location (simplified)
            if 'kitchen' in user_input_lower:
                task_plan["parameters"]["location"] = "kitchen"
            elif 'bedroom' in user_input_lower:
                task_plan["parameters"]["location"] = "bedroom"
        
        if 'open' in user_input_lower:
            task_plan["actions"].append("approach_door")
            task_plan["actions"].append("grasp_handle")
            task_plan["actions"].append("rotate_handle")
            task_plan["actions"].append("push_door")
        
        # Convert to JSON string for ROS 2 message
        task_plan_json = json.dumps(task_plan)
        
        self.get_logger().info(f'Task plan: {task_plan_json}')
        
        return task_plan_json
    
    def generate_response(self, user_input: str, task_plan: str) -> str:
        """Generate natural language response."""
        # Parse task plan
        plan_dict = json.loads(task_plan)
        actions = plan_dict.get("actions", [])
        
        if not actions:
            return "I'm not sure how to help with that."
        
        # Generate response based on actions
        action_descriptions = {
            "navigate_to_object": "I'll move towards the object",
            "detect_object": "I'll locate the object",
            "grasp_object": "I'll pick it up",
            "navigate_to_location": "I'll go to the location",
            "release_object": "I'll place it there",
            "approach_door": "I'll approach the door",
            "grasp_handle": "I'll grasp the handle",
            "rotate_handle": "I'll turn the handle",
            "push_door": "I'll push the door open"
        }
        
        response_parts = [action_descriptions.get(a, a) for a in actions]
        response = "Acknowledged. " + ", then ".join(response_parts) + "."
        
        self.get_logger().info(f'Response: {response}')
        
        return response


def main(args=None):
    rclpy.init(args=args)
    node = LLMAgentNode()
    
    # Use multi-threaded executor for concurrent callbacks
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('LLM Agent stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

### Example 3: Sensor Data Processing with AI

```python
#!/usr/bin/env python3
"""
sensor_fusion_agent.py
AI agent that fuses multiple sensor inputs for decision making
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, LaserScan, Image
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
import numpy as np
from collections import deque


class SensorFusionAgent(Node):
    """AI agent that fuses IMU, LiDAR, and Odometry data."""
    
    def __init__(self):
        super().__init__('sensor_fusion_agent')
        
        # === Subscribers ===
        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )
        
        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )
        
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        
        # === Publisher ===
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        # === Sensor Buffers (for temporal fusion) ===
        self.imu_buffer = deque(maxlen=100)
        self.lidar_buffer = deque(maxlen=50)
        self.odom_buffer = deque(maxlen=50)
        
        # === Fused State ===
        self.robot_pose = None
        self.robot_velocity = None
        self.obstacle_detected = False
        self.obstacle_distance = float('inf')
        
        # === Safety Parameters ===
        self.collision_threshold = 0.5  # meters
        self.emergency_stop_distance = 0.3  # meters
        
        self.get_logger().info('Sensor Fusion Agent initialized!')
        
        # Timer for decision loop (10 Hz)
        self.decision_timer = self.create_timer(0.1, self.decision_loop)
    
    def imu_callback(self, msg: Imu):
        """Process IMU data."""
        self.imu_buffer.append({
            'timestamp': msg.header.stamp,
            'angular_velocity': np.array([
                msg.angular_velocity.x,
                msg.angular_velocity.y,
                msg.angular_velocity.z
            ]),
            'linear_acceleration': np.array([
                msg.linear_acceleration.x,
                msg.linear_acceleration.y,
                msg.linear_acceleration.z
            ])
        })
    
    def lidar_callback(self, msg: LaserScan):
        """Process LiDAR scan for obstacle detection."""
        # Convert to numpy array
        ranges = np.array(msg.ranges)
        
        # Filter out invalid readings
        valid_ranges = ranges[
            (ranges > msg.range_min) & 
            (ranges < msg.range_max)
        ]
        
        if len(valid_ranges) > 0:
            min_distance = np.min(valid_ranges)
            self.obstacle_distance = min_distance
            self.obstacle_detected = min_distance < self.collision_threshold
        else:
            self.obstacle_detected = False
    
    def odom_callback(self, msg: Odometry):
        """Process odometry data."""
        self.odom_buffer.append({
            'timestamp': msg.header.stamp,
            'pose': msg.pose.pose,
            'twist': msg.twist.twist
        })
        
        # Update current state
        self.robot_pose = msg.pose.pose
        self.robot_velocity = msg.twist.twist
    
    def decision_loop(self):
        """Main decision loop running at 10 Hz."""
        # Check if we have sensor data
        if not self.imu_buffer or not self.lidar_buffer:
            return
        
        # Get latest sensor data
        latest_imu = self.imu_buffer[-1]
        latest_lidar = self.lidar_buffer[-1]
        
        # Create velocity command
        cmd = Twist()
        
        # === Decision Logic ===
        
        # Emergency stop if obstacle too close
        if self.obstacle_detected and \
           self.obstacle_distance < self.emergency_stop_distance:
            self.get_logger().warn(
                f'EMERGENCY STOP! Obstacle at {self.obstacle_distance:.2f}m'
            )
            # Publish zero velocity
            self.cmd_pub.publish(cmd)
            return
        
        # Slow down if obstacle detected
        if self.obstacle_detected:
            self.get_logger().info(
                f'Obstacle detected at {self.obstacle_distance:.2f}m - slowing down'
            )
            cmd.linear.x = 0.1  # Slow forward
        else:
            # Normal operation
            cmd.linear.x = 0.3  # Normal forward speed
        
        # Check balance from IMU
        angular_magnitude = np.linalg.norm(latest_imu['angular_velocity'])
        if angular_magnitude > 0.5:
            self.get_logger().warn('High angular velocity - adjusting')
            cmd.angular.z = -latest_imu['angular_velocity'][2] * 0.5
        
        # Publish command
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = SensorFusionAgent()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Sensor Fusion Agent stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## Hands-on Lab

### Lab 3.1: Build a Simple Robot Controller Node

**Objective:** Create an AI agent that processes sensor data and controls robot movement

**Prerequisites:**
- Chapters 1 and 2 completed
- ROS 2 Humble installed
- Python 3.10+

**Time:** 60 minutes

---

### Step 1: Create Agent Package

```bash
cd ~/ros2_ws/src

# Create package for AI agents
ros2 pkg create --build-type ament_python ai_agents \
    --dependencies rclpy std_msgs sensor_msgs geometry_msgs

cd ai_agents/ai_agents
```

---

### Step 2: Create the Agent Node

Create `robot_controller_agent.py`:

```bash
nano robot_controller_agent.py
```

Copy the code from **Example 1: Basic AI Agent Node** above.

Make executable:

```bash
chmod +x robot_controller_agent.py
```

---

### Step 3: Update setup.py

Edit `setup.py` to register the executable:

```python
entry_points={
    'console_scripts': [
        'robot_controller = ai_agents.robot_controller_agent:main',
    ],
},
```

---

### Step 4: Build the Package

```bash
cd ~/ros2_ws
colcon build --packages-select ai_agents
source install/setup.bash
```

---

### Step 5: Test the Agent

**Terminal 1 — Run Agent:**

```bash
source install/setup.bash
ros2 run ai_agents robot_controller
```

**Terminal 2 — Publish Voice Commands:**

```bash
source install/setup.bash

# Send "start" command
ros2 topic pub /voice/command std_msgs/msg/String "{data: 'start'}"

# Send "move forward" command
ros2 topic pub /voice/command std_msgs/msg/String "{data: 'move forward'}"

# Send "stop" command
ros2 topic pub /voice/command std_msgs/msg/String "{data: 'stop'}"
```

**Terminal 3 — Monitor Output:**

```bash
source install/setup.bash
ros2 topic echo /agent/status
ros2 topic echo /cmd_vel
```

---

### Step 6: Simulate Sensor Input

Create a sensor simulator:

```bash
cd ~/ros2_ws/src/ai_agents/ai_agents
nano sensor_simulator.py
```

```python
#!/usr/bin/env python3
"""
sensor_simulator.py
Simulates IMU sensor data for testing
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import math


class SensorSimulator(Node):
    def __init__(self):
        super().__init__('sensor_simulator')
        
        self.publisher = self.create_publisher(Imu, '/imu/data', 10)
        self.timer = self.create_timer(0.01, self.publish_imu)
        self.t = 0
    
    def publish_imu(self):
        self.t += 0.01
        
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'
        
        # Simulate walking motion
        msg.angular_velocity.x = 0.1 * math.sin(self.t)
        msg.angular_velocity.y = 0.1 * math.cos(self.t)
        msg.angular_velocity.z = 0.05 * math.sin(2 * self.t)
        
        msg.linear_acceleration.z = 9.81
        
        self.publisher.publish(msg)


def main():
    rclpy.init()
    node = SensorSimulator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Add to `setup.py` and rebuild:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

Run simulator in a new terminal:

```bash
ros2 run ai_agents sensor_simulator
```

---

## Summary

### Key Takeaways

1. **AI Agents** perceive, reason, and act using ROS 2 communication
2. **rclpy** provides full Python access to ROS 2 features
3. **Sensor fusion** combines multiple data sources for robust decisions
4. **LLM integration** enables natural language task planning
5. **Async patterns** allow concurrent sensor processing and control

### AI Agent Architecture Patterns

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| **Reactive** | Simple stimulus-response | Low |
| **Deliberative** | Planning with LLM | High |
| **Hybrid** | Combined reactive + planning | Medium |
| **Behavior Tree** | Complex task sequencing | Medium-High |

---

## Exercises

### Exercise 3.1: Add State Machine

Implement a state machine in the AI agent with states:
- IDLE
- MOVING
- BALANCING
- EMERGENCY_STOP

Document state transitions and test each state.

### Exercise 3.2: LLM Integration

Replace the rule-based task planner with actual LLM API calls:
1. Install OpenAI package: `pip install openai`
2. Implement `query_llm_for_task()` with actual API calls
3. Handle API errors gracefully
4. Test with various natural language commands

### Exercise 3.3: Behavior Tree

Implement a simple behavior tree for the robot:
- Sequence: Navigate → Detect → Grasp
- Fallback: Try precision grasp → Try power grasp → Report failure

### Exercise 3.4: Multi-Agent System

Create two AI agents that communicate:
- Agent 1: Vision processing (detects objects)
- Agent 2: Motion planning (navigates to objects)

Use ROS 2 topics for inter-agent communication.

---

## Next Chapter

In **Chapter 4: Robot Description using URDF**, you will learn:

- How to model robots using URDF format
- Define links, joints, and kinematic chains
- Add sensors and actuators to robot models
- Create a complete humanoid robot description

---

## Resources

### Official Documentation

- [rclpy Documentation](https://docs.ros.org/en/humble/Concepts/About-Client-Libraries.html)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)

### AI/ML Integration

- [LangChain ROS 2 Integration](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### Behavior Trees

- [BehaviorTree.CPP](https://www.behaviortree.dev/)
- [py_trees](https://splinteredcode.github.io/py-trees/)
