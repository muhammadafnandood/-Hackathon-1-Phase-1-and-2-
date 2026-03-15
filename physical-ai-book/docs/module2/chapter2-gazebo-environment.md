---
sidebar_label: '2. Gazebo Simulation Environment'
---

# Chapter 2: Gazebo Simulation Environment

## Learning Objectives

By the end of this chapter, you will be able to:

- Set up Gazebo simulation environment with ROS2 integration
- Create URDF and SDF robot models
- Configure physics simulation parameters (gravity, collisions, friction)
- Add and configure sensors (LiDAR, IMU, cameras)
- Launch and control a simulated robot using ROS2 nodes

## Concept Explanation

### Gazebo Architecture

**Gazebo** is a powerful 3D robotics simulator with deep ROS2 integration. It consists of several components:

```
┌─────────────────────────────────────────────────────────────┐
│                      GAZEBO ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Gazebo    │  │   Gazebo    │  │   Gazebo    │          │
│  │    Sim      │  │   Classic   │  │    Server   │          │
│  │  (New 2021) │  │  (Legacy)   │  │  (Headless) │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Common Components                        │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  • Physics Engine (ODE/Bullet/DART)                  │   │
│  │  • Render Engine (OGRE3D)                            │   │
│  │  • Sensor Simulation                                  │   │
│  │  • ROS2 Bridge (ros_gz)                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Gazebo Versions:**

| Version | Status | Best For |
|---------|--------|----------|
| **Gazebo Sim** (Harmonic) | Current (2021+) | New projects, better performance |
| **Gazebo Classic** (11) | Legacy (2004-2021) | Existing projects, tutorials |
| **Gazebo Server** | Headless mode | CI/CD, cloud simulation |

### URDF vs SDF

**URDF** (Unified Robot Description Format) and **SDF** (Simulation Description Format) are XML formats for describing robots:

```
┌──────────────────────────────────────────────────────────┐
│                  URDF vs SDF                              │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  URDF                          SDF                        │
│  ────                          ────                       │
│  • ROS standard                • Gazebo native            │
│  • Robot only                  • Robot + Environment      │
│  • Limited physics             • Full physics support     │
│  • Tree structure              • Graph structure          │
│  • No world info               • Complete world desc.     │
│                                                           │
│  Conversion: urdf → SDF (automatic in Gazebo)             │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

**URDF Structure:**

```xml
<robot name="my_robot">
  <link name="base_link">
    <visual>...</visual>
    <collision>...</collision>
    <inertial>...</inertial>
  </link>
  
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="arm_link"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14"/>
  </joint>
</robot>
```

**SDF Structure:**

```xml
<sdf version="1.8">
  <world name="my_world">
    <model name="my_robot">
      <link name="base_link">
        <visual>...</visual>
        <collision>...</collision>
        <inertial>...</inertial>
      </link>
      <joint name="joint1" type="revolute">
        <parent>base_link</parent>
        <child>arm_link</child>
      </joint>
    </model>
    
    <!-- Environment -->
    <light>...</light>
    <model name="ground">...</model>
  </world>
</sdf>
```

### Physics Simulation Parameters

Gazebo simulates physics using these key parameters:

**1. Gravity:**

```xml
<gravity>0 0 -9.81</gravity>
```

**2. Time Step:**

```xml
<physics type="ode">
  <real_time_update_rate>1000</real_time_update_rate>
  <max_step_size>0.001</max_step_size>
</physics>
```

**3. Collision Properties:**

```xml
<collision name="collision">
  <geometry>
    <box>
      <size>1 1 1</size>
    </box>
  </geometry>
  <surface>
    <contact>
      <ode>
        <kp>1e9</kp>    <!-- Stiffness -->
        <kd>100</kd>    <!-- Damping -->
      </ode>
    </contact>
    <friction>
      <ode>
        <mu>0.5</mu>    <!-- Friction coefficient -->
      </ode>
    </friction>
  </surface>
</collision>
```

**4. Solver Parameters:**

```xml
<physics type="ode">
  <solver>
    <type>quick</type>
    <iters>100</iters>
    <precon>1</precon>
  </solver>
</physics>
```

### Sensor Simulation

Gazebo provides realistic sensor models:

**Sensor Types:**

| Sensor | Gazebo Plugin | ROS2 Topic |
|--------|---------------|------------|
| **LiDAR** | `libgazebo_ros_ray_sensor.so` | `/scan` (sensor_msgs/LaserScan) |
| **Depth Camera** | `libgazebo_ros_camera.so` | `/depth/image_raw` (sensor_msgs/Image) |
| **RGB Camera** | `libgazebo_ros_camera.so` | `/camera/image_raw` (sensor_msgs/Image) |
| **IMU** | `libgazebo_ros_imu_sensor.so` | `/imu/data` (sensor_msgs/Imu) |
| **GPS** | `libgazebo_ros_gps_sensor.so` | `/gps/fix` (sensor_msgs/NavSatFix) |
| **Contact** | `libgazebo_ros_bumper.so` | `/bumper_states` (std_msgs/Bool) |

**Sensor Noise Model:**

```xml
<sensor name="lidar" type="ray">
  <ray>
    <scan>
      <horizontal>
        <samples>720</samples>
        <resolution>1</resolution>
        <min_angle>-3.14</min_angle>
        <max_angle>3.14</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
    </range>
  </ray>
  
  <!-- Noise model -->
  <noise>
    <type>gaussian</type>
    <mean>0.0</mean>
    <stddev>0.01</stddev>
  </noise>
</sensor>
```

## Real Robotics Example

### NASA Robonaut 2 Simulation

NASA uses Gazebo to simulate the **Robonaut 2** humanoid robot on the International Space Station:

```
┌────────────────────────────────────────────────────────┐
│              ROBOAUT 2 SIMULATION PIPELINE              │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Earth-Based Simulation    →    ISS Deployment         │
│         ↓                           ↓                   │
│  • Gazebo physics              • Real microgravity     │
│  • 50 DOF humanoid             • 47 DOF operational    │
│  • Full sensor suite           • Limited bandwidth     │
│  • Real-time control           • Delayed teleoperation │
│                                                         │
│  Validation Steps:                                      │
│  1. Simulation tests (1000+ hours)                     │
│  2. Ground truth comparison                             │
│  3. Parabolic flight tests                              │
│  4. ISS deployment                                      │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Key Lessons:**

- Simulation allowed testing in **microgravity** before space deployment
- **Sensor noise modeling** was critical for realistic testing
- **Communication delay simulation** prepared operators for real conditions

## Architecture Overview

### Gazebo-ROS2 Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  GAZEBO-ROS2 INTEGRATION                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  ROS2 Node   │◄───────►│  Gazebo Node │                 │
│  │  (rclpy)     │  ROS2   │  (Plugin)    │                 │
│  └──────────────┘  Topics └──────────────┘                 │
│         │                      │                            │
│         │                      │                            │
│         ▼                      ▼                            │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  Controller  │         │  Physics     │                 │
│  │  Algorithm   │         │  Engine      │                 │
│  └──────────────┘         └──────────────┘                 │
│                                                              │
│  Topic Examples:                                             │
│  • /cmd_vel       → Robot velocity commands                  │
│  • /joint_states  ← Joint position feedback                  │
│  • /scan          ← LiDAR data                               │
│  • /camera/image  ← Camera images                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Complete Simulation Stack

```
User Application (Python/C++)
         ↓
    ROS2 Nodes
         ↓
   ros_gz Bridge
         ↓
   Gazebo Plugins
         ↓
  Physics + Rendering
         ↓
   Sensor Models
```

## Code Examples

### Example 1: Complete URDF Robot Model

```xml
<?xml version="1.0"?>
<robot name="simple_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Right Wheel -->
  <link name="right_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.05"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Left Wheel -->
  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.05"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Right Wheel Joint -->
  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.15 0" rpy="1.57 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <!-- Left Wheel Joint -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.15 0" rpy="1.57 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <!-- Gazebo Plugins -->
  <gazebo>
    <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
      <ros>
        <namespace>/</namespace>
      </ros>
      
      <update_rate>100</update_rate>
      
      <!-- Wheels -->
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      
      <!-- Kinematics -->
      <wheel_separation>0.3</wheel_separation>
      <wheel_diameter>0.1</wheel_diameter>
      
      <!-- Limits -->
      <max_wheel_acceleration>1.0</max_wheel_acceleration>
      <max_wheel_torque>10.0</max_wheel_torque>
      
      <!-- Output -->
      <publish_odom>true</publish_odom>
      <publish_odom_tf>true</publish_odom_tf>
      <publish_wheel_tf>true</publish_wheel_tf>
      
      <odometry_frame>odom</odometry_frame>
      <robot_base_frame>base_link</robot_base_frame>
    </plugin>
  </gazebo>

  <!-- LiDAR Sensor -->
  <link name="laser_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="laser_joint" type="fixed">
    <parent link="base_link"/>
    <child link="laser_link"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>
  </joint>

  <gazebo reference="laser_link">
    <sensor name="laser" type="ray">
      <ray>
        <scan>
          <horizontal>
            <samples>720</samples>
            <resolution>1</resolution>
            <min_angle>-3.14</min_angle>
            <max_angle>3.14</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>10.0</max>
        </range>
      </ray>
      <plugin name="laser_plugin" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <argument>~/out:=/scan</argument>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>laser_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

### Example 2: Gazebo World File with Sensors

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="robotics_lab">
    
    <!-- Physics Configuration -->
    <physics type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
      <max_step_size>0.001</max_step_size>
      <ode>
        <solver>
          <type>quick</type>
          <iters>100</iters>
        </solver>
      </ode>
    </physics>
    
    <!-- Gravity -->
    <gravity>0 0 -9.81</gravity>
    
    <!-- Ground Plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.3 0.3 0.3 1</ambient>
            <diffuse>0.3 0.3 0.3 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
    
    <!-- Lighting -->
    <light name="sun" type="directional">
      <pose>0 0 10 0 -1.57 0</pose>
      <diffuse>1 1 1 1</diffuse>
      <ambient>0.1 0.1 0.1 1</ambient>
    </light>
    
    <!-- Obstacle Box -->
    <model name="obstacle_box">
      <pose>2 0 0.5 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.2 0.2 1</ambient>
            <diffuse>0.8 0.2 0.2 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
    
  </world>
</sdf>
```

### Example 3: ROS2 Launch File for Gazebo

```python
#!/usr/bin/env python3
"""
Launch file for Gazebo simulation with robot.
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Generate launch description for Gazebo robot simulation."""
    
    # Declare arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='robotics_lab',
        description='Name of the Gazebo world to load'
    )
    
    # Paths
    pkg_share = FindPackageShare('my_robot')
    world_path = PathJoinSubstitution([pkg_share, 'worlds', 'robotics_lab.sdf'])
    urdf_path = PathJoinSubstitution([pkg_share, 'urdf', 'simple_robot.urdf'])
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': PathJoinSubstitution([urdf_path])}]
    )
    
    # Spawn robot in Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-entity', 'simple_robot',
            '-file', urdf_path,
            '-x', '0', '-y', '0', '-z', '0.5',
            '-R', '0', '-P', '0', '-Y', '0'
        ]
    )
    
    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('gazebo_ros'), '/launch', '/gazebo.launch.py'
        ]),
        launch_arguments={
            'world': world_path,
        }.items()
    )
    
    # Joint state publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )
    
    return LaunchDescription([
        world_arg,
        robot_state_publisher,
        joint_state_publisher,
        gazebo,
        spawn_robot,
    ])


if __name__ == '__main__':
    generate_launch_description()
```

### Example 4: Python Node to Control Robot

```python
#!/usr/bin/env python3
"""
Simple robot controller for Gazebo simulation.
Publishes velocity commands to move the robot.
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool


class SimpleController(Node):
    """Simple obstacle-avoiding robot controller."""
    
    def __init__(self):
        super().__init__('simple_controller')
        
        # Publisher for velocity commands
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        # Subscriber for LiDAR data
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # Timer for control loop (10 Hz)
        self.timer = self.create_timer(0.1, self.control_loop)
        
        # State
        self.obstacle_detected = False
        self.scan_data = None
        
        self.get_logger().info('Simple Controller started')
    
    def scan_callback(self, msg: LaserScan):
        """Process LiDAR scan data."""
        self.scan_data = msg
        
        # Check for obstacles in front (within 1 meter)
        front_ranges = msg.ranges[len(msg.ranges)//2 - 10:len(msg.ranges)//2 + 10]
        
        # Filter out invalid readings
        valid_ranges = [r for r in front_ranges if 0.1 < r < 10.0]
        
        if valid_ranges and min(valid_ranges) < 1.0:
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False
    
    def control_loop(self):
        """Main control loop."""
        cmd = Twist()
        
        if self.obstacle_detected:
            # Obstacle detected: turn right
            cmd.linear.x = 0.0
            cmd.angular.z = -0.5
            self.get_logger().info('Obstacle detected! Turning right.')
        else:
            # No obstacle: move forward
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
            self.get_logger().debug('Moving forward.')
        
        self.cmd_pub.publish(cmd)


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    controller = SimpleController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Hands-on Lab

### Lab 2.1: Simulate a Mobile Robot in Gazebo

**Objective**: Create a complete Gazebo simulation with a differential drive robot and LiDAR sensor.

**Prerequisites**:
- ROS2 Humble installed
- Gazebo installed
- Basic Python knowledge

**Duration**: 60 minutes

---

#### Step 1: Create ROS2 Package

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create package
ros2 pkg create --build-type ament_python my_robot \
  --dependencies rclpy geometry_msgs sensor_msgs std_msgs \
  --license Apache-2.0

# Create directories
mkdir -p my_robot/urdf
mkdir -p my_robot/worlds
mkdir -p my_robot/launch
```

#### Step 2: Create Robot URDF

Create `my_robot/urdf/simple_robot.urdf`:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Copy URDF from Example 1 above -->
</robot>
```

#### Step 3: Create Gazebo World

Create `my_robot/worlds/robotics_lab.sdf`:

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="robotics_lab">
    <!-- Copy world from Example 2 above -->
  </world>
</sdf>
```

#### Step 4: Create Launch File

Create `my_robot/launch/gazebo_launch.py`:

```python
# Copy launch file from Example 3 above
```

#### Step 5: Create Controller Node

Create `my_robot/my_robot/simple_controller.py`:

```python
# Copy controller from Example 4 above
```

#### Step 6: Update setup.py

Edit `my_robot/setup.py`:

```python
from setuptools import setup

package_name = 'my_robot'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', ['urdf/simple_robot.urdf']),
        ('share/' + package_name + '/worlds', ['worlds/robotics_lab.sdf']),
        ('share/' + package_name + '/launch', ['launch/gazebo_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'simple_controller = my_robot.simple_controller:main',
        ],
    },
)
```

#### Step 7: Build and Run

```bash
# Build workspace
cd ~/ros2_ws
colcon build --packages-select my_robot
source install/setup.bash

# Launch simulation
ros2 launch my_robot gazebo_launch.py

# In another terminal, run controller
ros2 run my_robot simple_controller
```

#### Step 8: Observe Robot Behavior

- Robot should move forward
- When it detects obstacle (red box), it turns right
- Watch LiDAR data in RViz2:

```bash
rviz2
```

Add LaserScan display with topic `/scan`.

**Expected Result**:

Robot navigates the environment, avoiding the red obstacle box using LiDAR data.

## Summary

### Key Takeaways

1. **Gazebo Architecture**: Understand the difference between Gazebo Sim (new) and Gazebo Classic (legacy)

2. **URDF vs SDF**: URDF for robot description, SDF for complete worlds with environment

3. **Physics Configuration**: Gravity, time step, collision properties, and solver parameters affect simulation accuracy

4. **Sensor Plugins**: Gazebo provides plugins for LiDAR, cameras, IMU, GPS, and contact sensors

5. **ROS2 Integration**: Use ros_gz bridge to connect Gazebo with ROS2 nodes

### Key Terms

| Term | Definition |
|------|------------|
| **URDF** | Unified Robot Description Format (ROS standard) |
| **SDF** | Simulation Description Format (Gazebo native) |
| **ODE** | Open Dynamics Engine (physics engine) |
| **Diff Drive** | Differential drive kinematics |
| **ros_gz** | ROS2-Gazebo bridge package |

## Exercises

### Exercise 2.1: URDF Modification

1. Modify the robot URDF to add a **third caster wheel** for stability
2. Change wheel diameter from 0.1m to 0.15m
3. Add a **camera sensor** mounted on top of the robot
4. **Test** your changes in Gazebo

### Exercise 2.2: World Building

1. Create a new Gazebo world with:
   - Multiple obstacles (boxes, cylinders)
   - A maze-like structure
   - Different lighting conditions
2. Save as `my_robot/worlds/maze_world.sdf`
3. **Document** your world design with a screenshot

### Exercise 2.3: Controller Enhancement

1. Modify the controller to implement **wall following**:
   - Maintain a distance of 0.5m from the right wall
   - Use LiDAR data to measure distance
2. Add a **state machine**:
   - State 1: Move forward
   - State 2: Turn when obstacle detected
   - State 3: Wall follow
3. **Test** in the maze world

### Exercise 2.4: Sensor Analysis

1. Record LiDAR data:

```bash
ros2 bag record /scan -o lidar_data
```

2. Move robot manually using teleop:

```bash
ros2 run teleop_tw_keyboard teleop
```

3. **Analyze** the recorded data:
   - Plot distance readings over time
   - Identify obstacle detection patterns
   - Calculate sensor noise characteristics

### Exercise 2.5: Research Question

Research the **Mars Rover** simulation at NASA:

- What simulator do they use?
- How do they simulate Mars terrain?
- What sensors are simulated?
- How do they handle communication delay?

**Write** a 400-word summary with references.

---

**Next Chapter**: [Chapter 3 — Physics and Sensors →](./chapter3-physics-and-sensors.md)
