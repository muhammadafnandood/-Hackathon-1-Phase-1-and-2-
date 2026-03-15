---
title: Building the Robot Nervous System
description: Integrate ROS 2 nodes, launch files, and parameters to build a complete robot control system
sidebar_label: 1.5 Building Robot System
---

# Chapter 5: Building the Robot Nervous System

## Learning Objectives

By the end of this chapter, you will be able to:

- **Integrate** multiple ROS 2 nodes into a cohesive system
- **Create** launch files for complex robot configurations
- **Configure** parameters for robot behavior customization
- **Debug** multi-node systems using ROS 2 CLI tools
- **Build** a complete robot nervous system architecture
- **Deploy** robot systems in simulation and hardware

---

## Concept Explanation

### The Robot Nervous System Analogy

Just like a biological nervous system connects the brain to the body, a ROS 2 robot nervous system connects AI agents to hardware:

```
┌─────────────────────────────────────────────────────────────┐
│           Biological vs Robot Nervous System                 │
│                                                              │
│  Biological System              Robot System                 │
│  ─────────────────              ────────────                 │
│                                                              │
│  Brain                          AI Agent / LLM               │
│       │                               │                      │
│  Spinal Cord                    ROS 2 Middleware             │
│       │                               │                      │
│  Nerves                         Topics/Services/Actions      │
│       │                               │                      │
│  Sensory Receptors              Sensors (Camera, IMU)        │
│       │                               │                      │
│  Muscles                        Actuators (Motors)           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Robot Nervous System Components:**

| Biological | ROS 2 Equivalent | Purpose |
|------------|------------------|---------|
| Brain | AI Agent Node | Decision making |
| Spinal Cord | ROS 2 Middleware | Message routing |
| Nerves | Topics/Services | Communication channels |
| Sensory Receptors | Sensor Nodes | Data acquisition |
| Muscles | Actuator Nodes | Movement execution |
| Reflexes | Controller Nodes | Fast local responses |

### Node Integration Patterns

**Pattern 1: Pipeline Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│              Pipeline Architecture                           │
│                                                              │
│  Sensor → Perception → Planning → Control → Actuator         │
│     │         │           │          │          │            │
│     ▼         ▼           ▼          ▼          ▼            │
│  Camera    Vision     Navigation   Motor      Motor          │
│  Node      Node       Node         Cmd Node   Driver         │
│                                                              │
│  Data flows in one direction (feedforward)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Pattern 2: Blackboard Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│              Blackboard Architecture                         │
│                                                              │
│                    ┌─────────────┐                          │
│                    │  Blackboard │                          │
│                    │  (Shared    │                          │
│                    │   State)    │                          │
│                    └──────┬──────┘                          │
│                           │                                  │
│     ┌──────────┬──────────┼──────────┬──────────┐           │
│     │          │          │          │          │           │
│     ▼          ▼          ▼          ▼          ▼           │
│  Sensor    Perception  Planning  Control   Monitor          │
│  Node       Node       Node      Node      Node             │
│                                                              │
│  All nodes read/write to shared state                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Pattern 3: Hierarchical Control**

```
┌─────────────────────────────────────────────────────────────┐
│              Hierarchical Control Architecture               │
│                                                              │
│                    ┌─────────────┐                          │
│                    │   High-level│                          │
│                    │   Planner   │                          │
│                    │   (LLM)     │                          │
│                    └──────┬──────┘                          │
│                           │                                  │
│              ┌────────────┼────────────┐                    │
│              │            │            │                    │
│              ▼            ▼            ▼                    │
│     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│     │   Arm       │ │   Leg       │ │   Head      │        │
│     │ Controller  │ │ Controller  │ │ Controller  │        │
│     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘        │
│            │               │               │                 │
│            ▼               ▼               ▼                 │
│     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│     │   Motor     │ │   Motor     │ │   Motor     │        │
│     │   Drivers   │ │   Drivers   │ │   Drivers   │        │
│     └─────────────┘ └─────────────┘ └─────────────┘        │
│                                                              │
│  High-level commands decomposed to low-level actions         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Launch Files

**Definition: Launch File** — A configuration file that starts multiple ROS 2 nodes with specific parameters and settings.

**Why Use Launch Files?**

- **Automation** — Start entire systems with one command
- **Consistency** — Same configuration every time
- **Parameterization** — Easy to swap configurations
- **Modularity** — Include other launch files

**Launch File Formats:**

| Format | Extension | Use Case |
|--------|-----------|----------|
| Python | `.launch.py` | Complex logic, conditionals |
| XML | `.launch.xml` | Simple configurations |
| YAML | `.launch.yaml` | Data-driven configurations |

### ROS 2 Parameters

**Definition: Parameter** — A configuration value that can be set at runtime without recompiling code.

**Parameter Types:**

- `bool` — True/false
- `int` — Integer numbers
- `float` — Floating-point numbers
- `string` — Text values
- `array` — Lists of values

**Parameter Use Cases:**

```yaml
# Robot configuration
robot_name: "humanoid_01"
max_velocity: 1.5
max_payload: 5.0

# Sensor configuration
camera_fps: 30
lidar_range: 10.0
imu_update_rate: 100

# Control gains
kp_position: 100.0
kd_position: 10.0
ki_position: 1.0
```

### Debugging Tools

**ROS 2 CLI Tools:**

| Tool | Command | Purpose |
|------|---------|---------|
| Node list | `ros2 node list` | Show running nodes |
| Topic list | `ros2 topic list` | Show active topics |
| Topic echo | `ros2 topic echo <topic>` | View messages |
| Service list | `ros2 service list` | Show services |
| Parameter get | `ros2 param get <node> <param>` | Read parameters |
| Parameter set | `ros2 param set <node> <param> <value>` | Modify parameters |
| Bag record | `ros2 bag record <topics>` | Record data |
| Bag play | `ros2 bag play <file>` | Playback data |

---

## Architecture Overview

### Complete Humanoid Robot System

```
┌─────────────────────────────────────────────────────────────┐
│           Complete Humanoid Robot Nervous System             │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              AI Layer (High-level)                   │    │
│  │                                                      │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐    │    │
│  │  │  Voice    │───►│   LLM     │───►│   Task    │    │    │
│  │  │  Agent    │    │  Planner  │    │  Manager  │    │    │
│  │  └───────────┘    └───────────┘    └───────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            │ /task/goal                      │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Coordination Layer                      │    │
│  │                                                      │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐    │    │
│  │  │  Motion   │───►│  Balance  │───►│  Gait     │    │    │
│  │  │  Planner  │    │ Controller│    │ Generator │    │    │
│  │  └───────────┘    └───────────┘    └───────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│              ┌─────────────┼─────────────┐                   │
│              │             │             │                   │
│              ▼             ▼             ▼                   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   Arm Control   │ │   Leg Control   │ │  Head Control   │ │
│  │                 │ │                 │ │                 │ │
│  │ /l_arm/joint_cmd│ │/l_leg/joint_cmd │ │ /head/joint_cmd │ │
│  │ /r_arm/joint_cmd│ │/r_leg/joint_cmd │ │                 │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│              │             │             │                   │
│              └─────────────┼─────────────┘                   │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Hardware Layer                          │    │
│  │                                                      │    │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐        │    │
│  │  │  Motor    │  │  Motor    │  │  Sensor   │        │    │
│  │  │  Drivers  │  │  Drivers  │  │  Drivers  │        │    │
│  │  └───────────┘  └───────────┘  └───────────┘        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Feedback Loop:                                              │
│  /sensor/imu, /sensor/joint_states, /sensor/camera          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Topic Map for Robot System

```
┌─────────────────────────────────────────────────────────────┐
│              ROS 2 Topic Communication Map                   │
│                                                              │
│  Input Topics (Sensors → System):                           │
│  ──────────────────────────────────                          │
│  /sensor/imu/data              — IMU measurements           │
│  /sensor/joint_states          — Joint positions/velocities │
│  /sensor/camera/image_raw      — Camera images              │
│  /sensor/lidar/scan            — LiDAR point clouds         │
│  /sensor/force_torque          — Force/torque measurements  │
│                                                              │
│  Output Topics (System → Actuators):                        │
│  ───────────────────────────────────────                     │
│  /control/l_arm/joint_cmd      — Left arm commands          │
│  /control/r_arm/joint_cmd      — Right arm commands         │
│  /control/l_leg/joint_cmd      — Left leg commands          │
│  /control/r_leg/joint_cmd      — Right leg commands         │
│  /control/head/joint_cmd       — Head commands              │
│                                                              │
│  Internal Topics (Inter-node Communication):                │
│  ──────────────────────────────────────────                  │
│  /planner/goal               — Task goals                   │
│  /planner/path               — Planned paths                │
│  /balance/state              — Balance state                │
│  /gait/pattern               — Walking patterns             │
│                                                              │
│  Status Topics (Monitoring):                                │
│  ─────────────────────────────                               │
│  /system/status              — Overall system health        │
│  /system/battery             — Battery status               │
│  /system/errors              — Error messages               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Example 1: Complete Launch File (Python)

```python
#!/usr/bin/env python3
"""
robot_system.launch.py
Complete launch file for humanoid robot system
"""

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    TextSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():
    """Generate launch description for robot system."""
    
    # === Launch Arguments ===
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )
    
    use_gazebo_arg = DeclareLaunchArgument(
        'use_gazebo',
        default_value='false',
        description='Launch Gazebo simulation if true'
    )
    
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='Launch RViz visualization if true'
    )
    
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='humanoid',
        description='Name of the robot'
    )
    
    # === Launch Configurations ===
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_gazebo = LaunchConfiguration('use_gazebo')
    use_rviz = LaunchConfiguration('use_rviz')
    robot_name = LaunchConfiguration('robot_name')
    
    # === Package Paths ===
    pkg_share = FindPackageShare('robot_description')
    pkg_bringup = FindPackageShare('robot_bringup')
    
    urdf_path = PathJoinSubstitution([pkg_share, 'urdf', 'humanoid.urdf'])
    rviz_config = PathJoinSubstitution([pkg_share, 'rviz', 'robot.rviz'])
    
    # === Nodes ===
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_description': TextSubstitution(
                text='$(< ' + str(urdf_path) + ')'
            )},
        ],
    )
    
    # Joint State Publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )
    
    # AI Agent Node
    ai_agent_node = Node(
        package='ai_agents',
        executable='ai_agent_node',
        name='ai_agent',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_name': robot_name},
            {'llm_model': 'gpt-4'},
        ],
    )
    
    # Motion Controller Node
    motion_controller = Node(
        package='robot_control',
        executable='motion_controller',
        name='motion_controller',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'kp_gain': 100.0},
            {'kd_gain': 10.0},
        ],
    )
    
    # Balance Controller Node
    balance_controller = Node(
        package='robot_control',
        executable='balance_controller',
        name='balance_controller',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )
    
    # Sensor Fusion Node
    sensor_fusion = Node(
        package='robot_perception',
        executable='sensor_fusion_node',
        name='sensor_fusion',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )
    
    # RViz (conditional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(use_rviz),
    )
    
    # System Monitor Node
    system_monitor = Node(
        package='robot_bringup',
        executable='system_monitor',
        name='system_monitor',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )
    
    # === Launch Description ===
    return LaunchDescription([
        # Arguments
        use_sim_time_arg,
        use_gazebo_arg,
        use_rviz_arg,
        robot_name_arg,
        
        # Info message
        LogInfo(msg=['Launching robot system: ', robot_name]),
        
        # Core nodes
        robot_state_publisher,
        joint_state_publisher,
        
        # Intelligence and control
        ai_agent_node,
        motion_controller,
        balance_controller,
        
        # Perception
        sensor_fusion,
        
        # Monitoring
        system_monitor,
        
        # Visualization (optional)
        rviz_node,
    ])
```

---

### Example 2: Parameter Configuration File

```yaml
# config/robot_config.yaml
# Complete parameter configuration for humanoid robot

/**:
  ros__parameters:
    # === Robot Identity ===
    robot_name: "humanoid_01"
    robot_type: "bipedal"
    serial_number: "HN-2024-001"
    
    # === Control Parameters ===
    control:
      # Joint control gains
      position:
        kp: 100.0
        ki: 1.0
        kd: 10.0
      velocity:
        kp: 50.0
        ki: 0.5
        kd: 5.0
      effort:
        kp: 10.0
        ki: 0.1
        kd: 1.0
      
      # Limits
      max_velocity: 2.0        # rad/s
      max_acceleration: 10.0   # rad/s^2
      max_effort: 100.0        # Nm
    
    # === Balance Controller ===
    balance:
      enabled: true
      imu_topic: "/sensor/imu/data"
      
      # PID gains for balance
      kp_pitch: 500.0
      kd_pitch: 50.0
      kp_roll: 500.0
      kd_roll: 50.0
      
      # Thresholds
      tilt_threshold: 0.1      # radians
      recovery_threshold: 0.2  # radians
    
    # === Gait Parameters ===
    gait:
      step_length: 0.3         # meters
      step_height: 0.05        # meters
      step_frequency: 1.0      # Hz
      double_support_ratio: 0.2
      
      # Foot placement
      foot_separation: 0.15    # meters
      toe_off_angle: 0.3       # radians
    
    # === AI Agent ===
    ai_agent:
      llm_model: "gpt-4"
      llm_api_key_env: "OPENAI_API_KEY"
      
      # Voice settings
      voice_enabled: true
      whisper_model: "base"
      language: "en"
      
      # Task planning
      max_plan_length: 10
      replanning_interval: 5.0  # seconds
    
    # === Sensor Configuration ===
    sensors:
      imu:
        topic: "/sensor/imu/data"
        frame_id: "imu_link"
        update_rate: 100        # Hz
        
      camera:
        topic: "/sensor/camera/image_raw"
        frame_id: "camera_link"
        width: 640
        height: 480
        fps: 30
        
      lidar:
        topic: "/sensor/lidar/scan"
        frame_id: "lidar_link"
        update_rate: 10         # Hz
        min_range: 0.1          # meters
        max_range: 10.0         # meters
        
      joint_state:
        topic: "/sensor/joint_states"
        update_rate: 100        # Hz
    
    # === Safety ===
    safety:
      enabled: true
      
      # Emergency stop
      e_stop_topic: "/safety/estop"
      e_stop_timeout: 0.5       # seconds
      
      # Watchdog
      watchdog_timeout: 1.0     # seconds
      
      # Limits
      max_temperature: 80.0     # Celsius
      min_battery: 15.0         # Percent
    
    # === Communication ===
    communication:
      # QoS settings
      qos_depth: 10
      qos_reliability: "reliable"
      qos_durability: "volatile"
      
      # Network
      domain_id: 0
      multicast_enabled: true
    
    # === Logging ===
    logging:
      level: "info"             # debug, info, warn, error
      log_to_file: true
      log_directory: "/tmp/robot_logs"
```

---

### Example 3: System Monitor Node

```python
#!/usr/bin/env python3
"""
system_monitor.py
Monitors system health and publishes status
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64, Bool
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
import psutil
import json
from datetime import datetime


class SystemMonitor(Node):
    """Monitors system health and resource usage."""
    
    def __init__(self):
        super().__init__('system_monitor')
        
        # === Publishers ===
        self.status_pub = self.create_publisher(
            String,
            '/system/status',
            10
        )
        
        self.battery_pub = self.create_publisher(
            Float64,
            '/system/battery',
            10
        )
        
        self.error_pub = self.create_publisher(
            String,
            '/system/errors',
            10
        )
        
        self.diagnostics_pub = self.create_publisher(
            DiagnosticArray,
            '/diagnostics',
            10
        )
        
        # === Subscribers ===
        self.node_status_sub = self.create_subscription(
            String,
            '/agent/status',
            self.node_status_callback,
            10
        )
        
        # === State ===
        self.node_statuses = {}
        self.error_count = 0
        self.start_time = self.get_clock().now()
        
        # === Monitoring Timer ===
        self.monitor_timer = self.create_timer(1.0, self.monitor_callback)
        
        self.get_logger().info('System Monitor initialized')
    
    def node_status_callback(self, msg: String):
        """Receive status from other nodes."""
        # Parse status message
        try:
            status_data = json.loads(msg.data)
            node_name = status_data.get('node', 'unknown')
            self.node_statuses[node_name] = {
                'status': status_data.get('status', 'unknown'),
                'timestamp': self.get_clock().now().to_msg()
            }
        except json.JSONDecodeError:
            # Plain text status
            self.node_statuses['unknown'] = {
                'status': msg.data,
                'timestamp': self.get_clock().now().to_msg()
            }
    
    def monitor_callback(self):
        """Periodic system monitoring."""
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # Create system status message
        uptime = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        status_msg = String()
        status_msg.data = json.dumps({
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': uptime,
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'active_nodes': len(self.node_statuses),
            'error_count': self.error_count
        })
        self.status_pub.publish(status_msg)
        
        # Publish diagnostics
        self.publish_diagnostics(cpu_percent, memory_percent, disk_percent)
        
        # Log warnings
        if cpu_percent > 80:
            self.get_logger().warn(f'High CPU usage: {cpu_percent}%')
        if memory_percent > 80:
            self.get_logger().warn(f'High memory usage: {memory_percent}%')
        
        # Log status summary
        self.get_logger().info(
            f'System: CPU={cpu_percent:.1f}%, '
            f'Mem={memory_percent:.1f}%, '
            f'Nodes={len(self.node_statuses)}'
        )
    
    def publish_diagnostics(self, cpu: float, memory: float, disk: float):
        """Publish diagnostic array."""
        diag_array = DiagnosticArray()
        diag_array.header.stamp = self.get_clock().now().to_msg()
        
        # CPU diagnostic
        cpu_status = DiagnosticStatus()
        cpu_status.name = 'System: CPU'
        cpu_status.level = self.get_level(cpu, [70, 90])
        cpu_status.message = f'CPU Usage: {cpu:.1f}%'
        cpu_status.values.append(KeyValue(key='cpu_percent', value=f'{cpu:.1f}'))
        diag_array.status.append(cpu_status)
        
        # Memory diagnostic
        mem_status = DiagnosticStatus()
        mem_status.name = 'System: Memory'
        mem_status.level = self.get_level(memory, [70, 90])
        mem_status.message = f'Memory Usage: {memory:.1f}%'
        mem_status.values.append(KeyValue(key='memory_percent', value=f'{memory:.1f}'))
        diag_array.status.append(mem_status)
        
        # Robot status diagnostic
        robot_status = DiagnosticStatus()
        robot_status.name = 'Robot: Status'
        robot_status.level = DiagnosticStatus.OK if self.error_count == 0 else DiagnosticStatus.WARN
        robot_status.message = f'Active nodes: {len(self.node_statuses)}'
        robot_status.values.append(KeyValue(key='active_nodes', value=str(len(self.node_statuses))))
        robot_status.values.append(KeyValue(key='error_count', value=str(self.error_count)))
        diag_array.status.append(robot_status)
        
        self.diagnostics_pub.publish(diag_array)
    
    def get_level(self, value: float, thresholds: list) -> int:
        """Get diagnostic level based on thresholds."""
        if value < thresholds[0]:
            return DiagnosticStatus.OK
        elif value < thresholds[1]:
            return DiagnosticStatus.WARN
        else:
            return DiagnosticStatus.ERROR


def main(args=None):
    rclpy.init(args=args)
    node = SystemMonitor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('System Monitor stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

### Example 4: Multi-Node Robot System

```python
#!/usr/bin/env python3
"""
complete_robot_system.py
Main entry point that coordinates all robot subsystems
"""

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
import json


class CompleteRobotSystem(Node):
    """Coordinates all robot subsystems."""
    
    def __init__(self):
        super().__init__('complete_robot_system')
        
        # === Subsystems ===
        self.ai_agent = None      # AI/LLM integration
        self.perception = None    # Sensor processing
        self.planning = None      # Motion planning
        self.control = None       # Low-level control
        
        # === Publishers ===
        self.system_status_pub = self.create_publisher(
            String,
            '/system/overall_status',
            10
        )
        
        # === Subscribers ===
        self.command_sub = self.create_subscription(
            String,
            '/system/command',
            self.command_callback,
            10
        )
        
        # === State Machine ===
        self.system_state = 'INITIALIZING'
        self.subsystems_ready = {
            'ai_agent': False,
            'perception': False,
            'planning': False,
            'control': False
        }
        
        # === Timers ===
        self.status_timer = self.create_timer(0.5, self.publish_status)
        
        self.get_logger().info('Complete Robot System initializing...')
        
        # Initialize subsystems
        self.initialize_subsystems()
    
    def initialize_subsystems(self):
        """Initialize all robot subsystems."""
        try:
            # Import and initialize each subsystem
            # In practice, these would be separate nodes
            
            self.get_logger().info('Initializing AI Agent...')
            # self.ai_agent = AIAgentNode(self)
            self.subsystems_ready['ai_agent'] = True
            
            self.get_logger().info('Initializing Perception...')
            # self.perception = PerceptionNode(self)
            self.subsystems_ready['perception'] = True
            
            self.get_logger().info('Initializing Planning...')
            # self.planning = PlanningNode(self)
            self.subsystems_ready['planning'] = True
            
            self.get_logger().info('Initializing Control...')
            # self.control = ControlNode(self)
            self.subsystems_ready['control'] = True
            
            # Check if all subsystems are ready
            if all(self.subsystems_ready.values()):
                self.system_state = 'READY'
                self.get_logger().info('All subsystems initialized - System READY')
            else:
                self.system_state = 'PARTIAL'
                self.get_logger().warn('Some subsystems failed to initialize')
                
        except Exception as e:
            self.system_state = 'ERROR'
            self.get_logger().error(f'Initialization failed: {e}')
    
    def command_callback(self, msg: String):
        """Handle system-level commands."""
        try:
            command = json.loads(msg.data)
            cmd_type = command.get('type', '')
            cmd_data = command.get('data', {})
            
            self.get_logger().info(f'Received command: {cmd_type}')
            
            if cmd_type == 'START':
                self.system_state = 'RUNNING'
                self.get_logger().info('System started')
            
            elif cmd_type == 'STOP':
                self.system_state = 'STOPPED'
                self.get_logger().info('System stopped')
            
            elif cmd_type == 'EMERGENCY_STOP':
                self.system_state = 'ESTOP'
                self.get_logger().error('EMERGENCY STOP ACTIVATED')
                # Trigger emergency stop in all subsystems
            
            elif cmd_type == 'TASK':
                if self.system_state == 'READY' or self.system_state == 'RUNNING':
                    self.execute_task(cmd_data)
            
        except json.JSONDecodeError:
            self.get_logger().error('Invalid command format')
    
    def execute_task(self, task_data: dict):
        """Execute a high-level task."""
        task_type = task_data.get('task_type', '')
        
        self.get_logger().info(f'Executing task: {task_type}')
        
        # Coordinate subsystems to execute task
        # Example: "walk_forward"
        if task_type == 'WALK_FORWARD':
            distance = task_data.get('distance', 1.0)
            # 1. Planning: Generate walking trajectory
            # 2. Control: Execute joint commands
            # 3. Perception: Monitor for obstacles
            pass
        
        elif task_type == 'PICK_OBJECT':
            object_id = task_data.get('object_id', '')
            # 1. Perception: Locate object
            # 2. Planning: Plan arm trajectory
            # 3. Control: Execute grasp
            pass
    
    def publish_status(self):
        """Publish overall system status."""
        status_msg = String()
        status_data = {
            'system_state': self.system_state,
            'subsystems': self.subsystems_ready,
            'timestamp': self.get_clock().now().to_msg()
        }
        status_msg.data = json.dumps(status_data)
        self.system_status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    
    # Create the main robot system node
    robot_system = CompleteRobotSystem()
    
    # Use multi-threaded executor for concurrent operations
    executor = MultiThreadedExecutor()
    executor.add_node(robot_system)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        robot_system.get_logger().info('Robot System shutting down')
    finally:
        robot_system.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## Hands-on Lab

### Lab 5.1: Build a Multi-Node ROS 2 System

**Objective:** Create and launch a complete robot system with multiple nodes

**Prerequisites:**
- Chapters 1-4 completed
- ROS 2 Humble installed
- Basic Python knowledge

**Time:** 90 minutes

---

### Step 1: Create Robot Bringup Package

```bash
cd ~/ros2_ws/src

# Create bringup package
ros2 pkg create --build-type ament_python robot_bringup \
    --dependencies rclpy std_msgs sensor_msgs diagnostic_msgs

cd robot_bringup/robot_bringup
```

---

### Step 2: Create Launch File

Create the main launch file:

```bash
mkdir launch
nano launch/robot_system.launch.py
```

Copy the code from **Example 1: Complete Launch File** above.

Make executable:

```bash
chmod +x launch/robot_system.launch.py
```

---

### Step 3: Create Configuration File

```bash
mkdir config
nano config/robot_config.yaml
```

Copy the parameter configuration from **Example 2** above.

---

### Step 4: Create System Monitor Node

```bash
nano system_monitor.py
```

Copy the code from **Example 3: System Monitor Node** above.

Make executable:

```bash
chmod +x system_monitor.py
```

---

### Step 5: Update setup.py

Edit `setup.py`:

```python
from setuptools import setup

package_name = 'robot_bringup'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/robot_system.launch.py']),
        ('share/' + package_name + '/config', ['config/robot_config.yaml']),
    ],
    install_requires=['setuptools', 'psutil'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'system_monitor = robot_bringup.system_monitor:main',
        ],
    },
)
```

---

### Step 6: Install Dependencies

```bash
cd ~/ros2_ws

# Install psutil for system monitoring
pip3 install psutil

# Add to requirements.txt
echo "psutil>=5.9.0" >> src/robot_bringup/requirements.txt
```

---

### Step 7: Build the System

```bash
colcon build --packages-select robot_bringup
source install/setup.bash
```

---

### Step 8: Launch the Robot System

```bash
# Launch with default settings
ros2 launch robot_bringup robot_system.launch.py

# Launch with RViz disabled
ros2 launch robot_bringup robot_system.launch.py use_rviz:=false

# Launch with custom robot name
ros2 launch robot_bringup robot_system.launch.py robot_name:=my_humanoid
```

---

### Step 9: Monitor the System

Open additional terminals:

```bash
# View system status topic
ros2 topic echo /system/status

# View diagnostics
ros2 topic echo /diagnostics

# List all running nodes
ros2 node list

# View node graph
ros2 run rqt_graph rqt_graph
```

---

### Step 10: Debug with ROS 2 CLI

```bash
# Check parameter values
ros2 param get /system_monitor use_sim_time

# List all parameters
ros2 param list

# View topic information
ros2 topic info /system/status --verbose

# Check QoS compatibility
ros2 topic type /system/status
```

---

### Step 11: Record Data with Bags

```bash
# Record important topics
ros2 bag record /system/status /diagnostics /agent/status

# Stop recording with Ctrl+C

# Play back recorded data
ros2 bag play <bag_folder_name>

# List bag contents
ros2 bag info <bag_folder_name>
```

---

## Summary

### Key Takeaways

1. **Launch files** automate starting complex multi-node systems
2. **Parameters** enable runtime configuration without recompilation
3. **System monitoring** provides visibility into robot health
4. **Debugging tools** help diagnose issues in running systems
5. **Node integration patterns** organize communication architecture

### Launch File Best Practices

| Practice | Description |
|----------|-------------|
| Use arguments | Make launch files configurable |
| Include conditionals | Enable/disable components |
| Organize logically | Group related nodes |
| Document parameters | Explain what each does |
| Test incrementally | Add nodes one at a time |

### Debugging Checklist

- [ ] All nodes are running (`ros2 node list`)
- [ ] Topics are publishing (`ros2 topic list`)
- [ ] Messages have correct types (`ros2 topic info`)
- [ ] Parameters are set correctly (`ros2 param list`)
- [ ] No errors in logs (`ros2 run rqt_console rqt_console`)
- [ ] TF tree is complete (`ros2 run tf2_tools view_frames`)

---

## Exercises

### Exercise 5.1: Add New Node

Add a new node to the launch file:
- Create a simple publisher node
- Add it to the launch file
- Configure parameters
- Verify it appears in the node graph

### Exercise 5.2: Create Custom Launch Arguments

Extend the launch file with:
- A `debug_mode` argument
- Conditional node launching based on debug mode
- Different parameter sets for simulation vs hardware

### Exercise 5.3: Implement Health Check

Create a health check node that:
- Monitors all subsystem nodes
- Publishes overall system health
- Triggers alerts when nodes fail

### Exercise 5.4: Bag Analysis

Record a bag file and:
- Play it back
- Extract specific topics
- Analyze message timing
- Create a visualization

---

## Module 1 Summary

### What You've Learned

| Chapter | Key Skills |
|---------|------------|
| Ch 1: ROS 2 Intro | Installation, Hello World node, ROS 2 architecture |
| Ch 2: Communication | Publishers, subscribers, services, actions |
| Ch 3: AI Agents | rclpy, sensor processing, LLM integration |
| Ch 4: URDF | Robot modeling, links, joints, sensors |
| Ch 5: System Integration | Launch files, parameters, debugging |

### Next Steps

Continue to **Module 2: Digital Twin Simulation** where you will:
- Simulate your robot in Gazebo
- Create virtual environments
- Test control algorithms safely
- Generate synthetic training data

---

## Resources

### Official Documentation

- [ROS 2 Launch](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html)
- [ROS 2 Parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/ROS-2-Parameters.html)
- [ROS 2 Bag](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)

### Tools

- [rqt_graph](http://wiki.ros.org/rqt_graph) — Visualize node graph
- [rqt_console](http://wiki.ros.org/rqt_console) — Log viewer
- [ros2bag](http://wiki.ros.org/rosbag2) — Data recording
