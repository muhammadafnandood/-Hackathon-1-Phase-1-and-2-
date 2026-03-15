---
title: "Chapter 5: ROS 2 for Robotics Development"
sidebar_label: "ROS 2 Basics"
---

# Chapter 5: ROS 2 for Robotics Development

## What is ROS 2?

ROS 2 (Robot Operating System 2) is an open-source robotics middleware framework that provides services, tools, and libraries for building robot applications. It's a complete rewrite of ROS 1 with improvements for production use.

## Why ROS 2?

### Improvements Over ROS 1

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| Communication | Custom TCP/UDP | DDS (Data Distribution Service) |
| Real-time Support | Limited | Native support |
| Security | None | DDS Security |
| Network | Single network | Multiple networks, NAT-friendly |
| Lifecycle Management | Manual | Built-in lifecycle nodes |
| Discovery | Master node required | Decentralized discovery |

### Key Features

- **Distributed Architecture**: Nodes can run on different machines
- **Language Support**: C++, Python, and more
- **Hardware Abstraction**: Unified interface for different hardware
- **Package Management**: Easy sharing and distribution
- **Visualization Tools**: RViz, rqt for debugging
- **Simulation Integration**: Gazebo, Webots support

## Core Concepts

### Nodes

Nodes are the basic computational units in ROS 2:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Node started!')

def main():
    rclpy.init()
    node = MinimalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Topics

Topics enable publish-subscribe communication:

```python
# Publisher
class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, 'topic_name', 10)
        self.timer = self.create_timer(1.0, self.publish_message)
    
    def publish_message(self):
        msg = String()
        msg.data = 'Hello ROS 2!'
        self.publisher.publish(msg)

# Subscriber
class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String, 
            'topic_name', 
            self.callback, 
            10
        )
    
    def callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')
```

### Services

Services enable request-response communication:

```python
# Service Server
class ServiceServer(Node):
    def __init__(self):
        super().__init__('service_server')
        self.service = self.create_service(
            AddTwoInts, 
            'add_two_ints', 
            self.callback
        )
    
    def callback(self, request, response):
        response.sum = request.a + request.b
        return response

# Service Client
class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
    
    def call_service(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future = self.client.call_async(request)
        return future
```

### Actions

Actions are for long-running tasks with feedback:

```python
# Action Server
class ActionServer(Node):
    def __init__(self):
        super().__init__('action_server')
        self.action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )
    
    async def execute_callback(self, goal_handle):
        feedback = Fibonacci.Feedback()
        sequence = [0, 1]
        
        for i in range(1, goal_handle.request.order):
            sequence.append(sequence[-1] + sequence[-2])
            feedback.sequence = sequence
            goal_handle.publish_feedback(feedback)
        
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = sequence
        return result
```

### Parameters

Parameters configure nodes at runtime:

```python
class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')
        
        # Declare parameters
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('robot_name', 'my_robot')
        
        # Get parameters
        max_vel = self.get_parameter('max_velocity').value
        name = self.get_parameter('robot_name').value
```

## ROS 2 Architecture

### Client Libraries

- **rclpy**: Python client library
- **rclcpp**: C++ client library
- **rcl**: C client library (base for others)
- **Third-party**: Java, MATLAB, Rust, Go

### Middleware (RMW)

ROS 2 uses DDS implementations:

- **Fast DDS**: Default, good performance
- **Cyclone DDS**: Lightweight, Apache 2.0 licensed
- **Connext DDS**: Commercial, high performance
- **OpenSplice DDS**: Open source option

### Build System

#### Colcon

Common build tool for ROS 2:

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Build
colcon build

# Source environment
source install/setup.bash

# Run a node
ros2 run package_name node_name
```

## Common ROS 2 Tools

### Command Line Interface

```bash
# List running nodes
ros2 node list

# Get node information
ros2 node info /node_name

# List topics
ros2 topic list

# Echo topic messages
ros2 topic echo /topic_name

# List services
ros2 service list

# Call a service
ros2 service call /service_name ServiceType "{param: value}"

# List parameters
ros2 param list

# Get/set parameters
ros2 param get /node_name param_name
ros2 param set /node_name param_name value

# Launch files
ros2 launch package_name launch_file.py
```

### RViz2

3D visualization tool:

- Display robot models
- Visualize sensor data
- Show paths and plans
- Interactive markers

### rqt

GUI toolkit with plugins:

- **rqt_graph**: Visualize node/topic connections
- **rqt_plot**: Plot data over time
- **rqt_console**: Log message viewer
- **rqt_reconfigure**: Dynamic parameter adjustment

## Working with URDF

### Robot Description

URDF (Unified Robot Description Format) defines robot geometry:

```xml
<robot name="my_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0"
               iyy="0.1" iyz="0.0"
               izz="0.1"/>
    </inertial>
  </link>
  
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link2"/>
    <origin xyz="0.25 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="10" velocity="1.0"/>
  </joint>
</robot>
```

### Loading URDF in ROS 2

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    urdf_path = PathJoinSubstitution([
        FindPackageShare('my_robot'),
        'urdf',
        'my_robot.urdf.xacro'
    ])
    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['xacro ', urdf_path]),
                value_type=str
            )
        }]
    )
    
    return LaunchDescription([robot_state_publisher])
```

## Navigation Stack (Nav2)

### Components

- **Controller Server**: Local planning, trajectory following
- **Planner Server**: Global path planning
- **Recoveries**: Recovery behaviors when stuck
- **Behavior Server**: High-level behavior coordination
- **Waypoint Follower**: Navigate through waypoints

### Configuration

```yaml
controller_server:
  ros__parameters:
    controller_frequency: 20.0
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle"]
      acc_lim_x: 2.5
      acc_lim_theta: 3.2

planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
```

## Simulation with Gazebo

### Launch Simulation

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('gazebo_ros'),
            '/launch',
            '/gazebo.launch.py'
        ])
    )
    
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-topic', 'robot_description']
    )
    
    return LaunchDescription([gazebo, spawn_robot])
```

### Gazebo Plugins

Add sensors and actuators to URDF:

```xml
<gazebo reference="camera_link">
  <sensor type="camera" name="camera">
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## Best Practices

### Code Organization

- Keep nodes small and focused
- Use launch files for complex setups
- Separate configuration from code
- Document interfaces clearly

### Performance

- Use appropriate QoS settings
- Minimize message copying
- Use nodelets for zero-copy intra-process
- Profile before optimizing

### Debugging

- Use rqt_graph to understand topology
- Log at appropriate levels
- Use ros2 doctor for diagnostics
- Test with simulation first

## Summary

ROS 2 provides a robust foundation for robotics development with its distributed architecture, rich toolset, and strong community. Mastering ROS 2 is essential for modern robotics engineers working on complex systems like humanoid robots.
