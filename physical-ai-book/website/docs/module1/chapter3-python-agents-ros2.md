---
sidebar_label: '3. Python Agents with ROS2'
---

# Chapter 3: Python Agents with ROS2

## Integrating AI Agents with ROS2

This chapter covers how to create intelligent Python agents that can interact with ROS2 systems.

## Agent Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   AI Agent      │────▶│   ROS2 Bridge    │────▶│   Robot System  │
│  (Decision)     │     │  (Communication) │     │   (Execution)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Creating a ROS2 Agent Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64
import asyncio

class AIAgentNode(Node):
    def __init__(self):
        super().__init__('ai_agent_node')
        
        # Subscribers - Receive sensor data
        self.sensor_sub = self.create_subscription(
            Float64,
            'sensor_data',
            self.sensor_callback,
            10)
        
        # Publishers - Send commands
        self.command_pub = self.create_publisher(
            String,
            'robot_commands',
            10)
        
        self.latest_sensor_data = None
    
    def sensor_callback(self, msg):
        self.latest_sensor_data = msg.data
        self.process_and_decide()
    
    def process_and_decide(self):
        # AI decision logic here
        if self.latest_sensor_data > 50.0:
            command = "STOP"
        else:
            command = "CONTINUE"
        
        self.send_command(command)
    
    def send_command(self, command):
        msg = String()
        msg.data = command
        self.command_pub.publish(msg)
```

## Async Agent Pattern

```python
class AsyncAIAgent(Node):
    def __init__(self):
        super().__init__('async_ai_agent')
        self.executor = None
    
    async def run_agent_loop(self):
        while rclpy.ok():
            # Perception
            data = await self.perceive()
            
            # Cognition
            decision = await self.think(data)
            
            # Action
            await self.act(decision)
            
            await asyncio.sleep(0.1)
```

## Next Steps

We'll now explore URDF modeling for humanoid robots.
