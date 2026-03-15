---
sidebar_label: '3. Physics and Sensors'
---

# Chapter 3: Physics and Sensors

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand rigid body dynamics and contact physics
- Configure and calibrate simulated sensors
- Read and process data from depth cameras and RGB cameras
- Interpret IMU data for robot state estimation
- Implement LiDAR scanning and point cloud processing
- Simulate a biped humanoid robot walking in Gazebo

## Concept Explanation

### Rigid Body Dynamics

**Rigid body dynamics** is the foundation of robot physics simulation. A rigid body is an object that doesn't deform under force—its shape remains constant.

**Newton-Euler Equations:**

```
Linear Motion:    F = m × a
                  (Force = mass × acceleration)

Angular Motion:   τ = I × α
                  (Torque = inertia × angular acceleration)
```

**Key Concepts:**

```
┌─────────────────────────────────────────────────────────────┐
│                  RIGID BODY PROPERTIES                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Mass (m)          Center of Mass      Inertia Tensor       │
│  ────────          ───────────────     ──────────────       │
│  • Amount of       • Balance point     • Resistance to      │
│    matter          • Affects stability   rotation           │
│  • kg units        • CoM position      • 3×3 matrix         │
│                    • Critical for                          │
│                      balance                                 │
│                                                              │
│  Contact Model:                                             │
│  ──────────────                                             │
│  • Normal force (perpendicular to surface)                  │
│  • Friction force (parallel to surface)                     │
│  • Restitution (bounciness)                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Inertia Matrix:**

```
    ⎡ Ixx  Ixy  Ixz ⎤
I = ⎢ Iyx  Iyy  Iyz ⎥
    ⎣ Izx  Izy  Izz ⎦

Where:
• Ixx, Iyy, Izz = Moments of inertia (rotation about axes)
• Ixy, Ixz, Iyz = Products of inertia (coupling between axes)
```

### Contact Physics

When two bodies collide, Gazebo computes contact forces:

**Contact Model:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTACT FORCES                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│         Normal Force (N)                                     │
│              ↑                                               │
│              │                                               │
│    ┌─────────▼─────────┐                                    │
│    │     Object        │                                    │
│    └─────────┬─────────┘                                    │
│              │                                               │
│              │ Friction (f) ←─┐                             │
│              ▼                │                             │
│  ════════════════════════════│══════ Surface                │
│                              │                             │
│                              ▼                             │
│                                                              │
│  Normal Force: N = k × penetration_depth                    │
│  Friction: f = μ × N                                        │
│                                                              │
│  Where:                                                     │
│  • k = Contact stiffness                                    │
│  • μ = Friction coefficient                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**ODE Contact Parameters:**

```xml
<surface>
  <contact>
    <ode>
      <kp>1000000.0</kp>    <!-- Stiffness (higher = harder) -->
      <kd>1.0</kd>          <!-- Damping (dissipates energy) -->
    </ode>
  </contact>
  <friction>
    <ode>
      <mu>0.8</mu>          <!-- Friction coefficient -->
      <mu2>0.8</mu2>        <!-- Second friction direction -->
    </ode>
  </friction>
  <bounce>
    <restitution_coefficient>0.1</restitution_coefficient>
  </bounce>
</surface>
```

### Sensor Calibration

**Sensor calibration** ensures simulated sensors match real-world behavior:

**Calibration Parameters:**

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| **Noise Mean** | Systematic bias | 0.0 (ideal) |
| **Noise StdDev** | Random variation | 0.01-0.1 |
| **Update Rate** | Samples per second | 10-100 Hz |
| **Min/Max Range** | Detection limits | Sensor-specific |

**Noise Models:**

```python
# Gaussian noise model
noisy_value = true_value + random.gauss(mean, stddev)

# Example: IMU with bias
gyro_bias = [0.01, -0.02, 0.01]  # rad/s
accel_bias = [0.1, 0.05, -0.1]   # m/s²

noisy_gyro = true_gyro + gyro_bias + gaussian_noise(0, 0.001)
noisy_accel = true_accel + accel_bias + gaussian_noise(0, 0.01)
```

### Depth Camera Simulation

**Depth cameras** measure distance to objects using various technologies:

**Types of Depth Sensors:**

```
┌─────────────────────────────────────────────────────────────┐
│                   DEPTH CAMERA TYPES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Stereo Vision       Structured Light      Time-of-Flight   │
│  ─────────────       ──────────────────    ───────────────  │
│  • Two cameras       • Project pattern     • Measure light  │
│  • Triangulation     • Decode pattern      • TOF sensors    │
│  • Outdoor OK        • Indoor only         • Long range     │
│  • Compute heavy     • Kinect v1           • Kinect v2      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Depth Image Format:**

```
┌─────────────────────────────────────────┐
│  Depth Image (640 × 480)                │
│                                         │
│  Each pixel = distance in meters        │
│                                         │
│  [0.5] [0.6] [0.7] [0.8] ...           │
│  [0.5] [0.6] [0.7] [0.8] ...           │
│  [0.6] [0.7] [0.8] [0.9] ...           │
│  ...   ...   ...   ...   ...           │
│                                         │
│  Black = far (e.g., 10m)                │
│  White = near (e.g., 0.1m)              │
└─────────────────────────────────────────┘
```

**Point Cloud Generation:**

```python
# Convert depth image to point cloud
import numpy as np

def depth_to_pointcloud(depth_image, camera_intrinsics):
    """Convert depth image to 3D point cloud."""
    
    fx, fy, cx, cy = camera_intrinsics  # Focal length, principal point
    
    height, width = depth_image.shape
    
    # Create grid of pixel coordinates
    u, v = np.meshgrid(np.arange(width), np.arange(height))
    
    # Convert to 3D coordinates
    x = (u - cx) * depth_image / fx
    y = (v - cy) * depth_image / fy
    z = depth_image
    
    # Stack into point cloud (N × 3)
    points = np.stack([x, y, z], axis=-1)
    
    return points.reshape(-1, 3)
```

### IMU Data Reading

**Inertial Measurement Units (IMU)** measure linear acceleration and angular velocity:

**IMU Components:**

```
┌─────────────────────────────────────────────────────────────┐
│                      IMU SENSORS                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Accelerometer           Gyroscope        Magnetometer       │
│  ─────────────           ─────────        ────────────       │
│  • Linear acceleration   • Angular rate   • Magnetic field  │
│  • 3 axes (x, y, z)      • 3 axes (roll,  • 3 axes          │
│  • Includes gravity      • pitch, yaw)    • Compass heading│
│  • m/s² units            • rad/s units    • μT units       │
│                                                              │
│  Fusion → Orientation (quaternion)                           │
│  ──────                                                        │
│  • Combines all sensors                                        │
│  • Estimates robot tilt and heading                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**IMU Message Format (ROS2):**

```python
# sensor_msgs/msg/Imu
header:
  stamp: time
  frame_id: "imu_link"

orientation:
  x: 0.0  # Quaternion components
  y: 0.0
  z: 0.0
  w: 1.0
orientation_covariance: [0.01, 0, 0, 0, 0.01, 0, 0, 0, 0.01]

angular_velocity:
  x: 0.01  # rad/s
  y: -0.02
  z: 0.005
angular_velocity_covariance: [0.001, 0, 0, 0, 0.001, 0, 0, 0, 0.001]

linear_acceleration:
  x: 0.1  # m/s²
  y: -0.05
  z: 9.81
linear_acceleration_covariance: [0.01, 0, 0, 0, 0.01, 0, 0, 0, 0.01]
```

### LiDAR Scanning

**LiDAR** (Light Detection and Ranging) uses laser beams to measure distances:

**LiDAR Operating Principle:**

```
┌─────────────────────────────────────────────────────────────┐
│                     LiDAR SCANNING                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│       Laser Pulse                                            │
│           ↓                                                  │
│    ┌────────────┐                                           │
│    │   LiDAR    │──→ Rotating mirror                        │
│    └────────────┘                                           │
│           │                                                  │
│           │ Laser beam                                       │
│           ↓                                                  │
│    ════════════════════════  Object surface                 │
│                                                              │
│  Time of Flight: distance = (speed_of_light × time) / 2     │
│                                                              │
│  Scan Pattern:                                               │
│  ─────────────                                               │
│  • 2D: Single scanning plane (360°)                         │
│  • 3D: Multiple planes (vertical stack)                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**LaserScan Message (ROS2):**

```python
# sensor_msgs/msg/LaserScan
header:
  stamp: time
  frame_id: "laser_link"

angle_min: -3.14      # Start angle (radians)
angle_max: 3.14       # End angle (radians)
angle_increment: 0.0087  # Angle between measurements (radians)

time_increment: 0.0001  # Time between measurements
scan_time: 0.1          # Time for full scan

range_min: 0.1    # Minimum range (meters)
range_max: 10.0   # Maximum range (meters)

ranges: [1.5, 1.6, 1.7, 2.1, 3.5, ...]  # Distance measurements

intensities: [0.8, 0.7, 0.9, 0.6, 0.5, ...]  # Return intensity
```

## Real Robotics Example

### Boston Atlas Bipedal Walking

Boston Dynamics' **Atlas** humanoid uses advanced physics simulation for walking:

```
┌────────────────────────────────────────────────────────┐
│           ATLAS WALKING SIMULATION                      │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Physics Model:                                         │
│  ──────────────                                         │
│  • 28 DOF (Degrees of Freedom)                         │
│  • Full rigid body dynamics                            │
│  • Contact forces at feet                              │
│  • Center of Mass (CoM) trajectory                     │
│                                                         │
│  Control Strategy:                                      │
│  ────────────────                                       │
│  • Model Predictive Control (MPC)                      │
│  • Whole-body controller                               │
│  • Footstep planning                                   │
│                                                         │
│  Simulation → Real Transfer:                            │
│  ───────────────────────                                │
│  • 10,000+ walking steps in simulation                 │
│  • Domain randomization on friction                    │
│  • System identification for mass properties           │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Walking Gait Cycle:**

```
Step 1:        Step 2:        Step 3:        Step 4:
Left Support   Double Support Right Support  Double Support
    │              │              │              │
    ▼              ▼              ▼              ▼
  ┌─┴─┐          ┌─┴─┐          ┌─┴─┐          ┌─┴─┐
  │   │          │   │          │   │          │   │
  │   │          │   │          │   │          │   │
 ─┴───┴─        ─┴─ ─┴─        ─┴───┴─        ─┴─ ─┴─
 Left           Both           Right          Both
```

## Architecture Overview

### Complete Sensor Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    SENSOR PIPELINE                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Physical Sensors    Simulation      ROS2 Topics             │
│  ────────────────    ──────────      ───────────             │
│                                                              │
│  LiDAR          →    Gazebo Ray   →   /scan                │
│                     Sensor              (LaserScan)          │
│                                                              │
│  Depth Camera   →    Gazebo Depth →   /depth/image         │
│                     Camera              (Image)              │
│                                                              │
│  RGB Camera     →    Gazebo Wide  →   /camera/image        │
│                     Angle Camera        (Image)              │
│                                                              │
│  IMU            →    Gazebo IMU   →   /imu/data           │
│                     Sensor              (Imu)                │
│                                                              │
│  GPS            →    Gazebo GPS   →   /gps/fix            │
│                     Sensor              (NavSatFix)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Humanoid Robot Sensor Suite

```
┌─────────────────────────────────────────────────────────────┐
│              HUMANOID SENSOR CONFIGURATION                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                      ┌───────────┐                          │
│                      │   Head    │                          │
│                      │ ┌───────┐ │                          │
│                      │ │Camera │ │  ← Stereo vision         │
│                      │ │  IMU  │ │  ← Head orientation     │
│                      │ └───────┘ │                          │
│                      └─────┬─────┘                          │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         │                  │                  │             │
│    ┌────┴────┐        ┌────┴────┐       ┌────┴────┐        │
│    │  Left   │        │  Torso  │       │  Right  │        │
│    │   Arm   │        │   IMU   │       │   Arm   │        │
│    │ Force   │        │  (Core) │       │ Force   │        │
│    │ Sensor  │        │         │       │ Sensor  │        │
│    └─────────┘        └─────────┘       └─────────┘        │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         │                  │                  │             │
│    ┌────┴────┐                             ┌────┴────┐     │
│    │  Left   │                             │  Right  │     │
│    │   Leg   │                             │   Leg   │     │
│    │ ┌─────┐ │                             │ ┌─────┐ │     │
│    │ │Foot │ │                             │ │Foot │ │     │
│    │ │F/T  │ │                             │ │F/T  │ │     │
│    │ └─────┘ │                             │ └─────┘ │     │
│    └─────────┘                             └─────────┘     │
│                                                              │
│  F/T = Force/Torque Sensor                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Biped Humanoid URDF

```xml
<?xml version="1.0"?>
<robot name="biped_humanoid">

  <!-- Base (Torso) -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    
    <collision>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="20.0"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia ixx="1.5" ixy="0" ixz="0" iyy="1.0" iyz="0" izz="1.5"/>
    </inertial>
  </link>

  <!-- Left Leg -->
  <link name="left_leg">
    <visual>
      <geometry>
        <cylinder radius="0.08" length="0.5"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    
    <collision>
      <geometry>
        <cylinder radius="0.08" length="0.5"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Left Foot -->
  <link name="left_foot">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </visual>
    
    <collision>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Right Leg -->
  <link name="right_leg">
    <visual>
      <geometry>
        <cylinder radius="0.08" length="0.5"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    
    <collision>
      <geometry>
        <cylinder radius="0.08" length="0.5"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Right Foot -->
  <link name="right_foot">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </visual>
    
    <collision>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </collision>
    
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="left_hip" type="revolute">
    <parent link="torso"/>
    <child link="left_leg"/>
    <origin xyz="0 0.1 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" velocity="2.0" effort="100"/>
  </joint>

  <joint name="left_knee" type="revolute">
    <parent link="left_leg"/>
    <child link="left_foot"/>
    <origin xyz="0 0 -0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="0.5" velocity="2.0" effort="100"/>
  </joint>

  <joint name="right_hip" type="revolute">
    <parent link="torso"/>
    <child link="right_leg"/>
    <origin xyz="0 -0.1 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" velocity="2.0" effort="100"/>
  </joint>

  <joint name="right_knee" type="revolute">
    <parent link="right_leg"/>
    <child link="right_foot"/>
    <origin xyz="0 0 -0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="0.5" velocity="2.0" effort="100"/>
  </joint>

  <!-- IMU Sensor -->
  <gazebo reference="torso">
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <plugin name="imu_plugin" filename="libgazebo_ros_imu_sensor.so">
        <ros>
          <argument>~/out:=/imu/data</argument>
        </ros>
        <frame_name>torso</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <!-- LiDAR on Head -->
  <link name="head_lidar">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.1"/>
      </geometry>
    </visual>
  </link>

  <joint name="head_lidar_joint" type="fixed">
    <parent link="torso"/>
    <child link="head_lidar"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
  </joint>

  <gazebo reference="head_lidar">
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
      <plugin name="lidar_plugin" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <argument>~/out:=/scan</argument>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>head_lidar</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

### Example 2: Walking Controller

```python
#!/usr/bin/env python3
"""
Biped walking controller for humanoid robot.
Implements simple gait pattern generation.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import numpy as np


class BipedWalker(Node):
    """Simple biped walking controller."""
    
    def __init__(self):
        super().__init__('biped_walker')
        
        # Publisher for joint commands
        self.joint_pub = self.create_publisher(
            Float64MultiArray,
            '/joint_commands',
            10
        )
        
        # Timer for control loop (100 Hz)
        self.timer = self.create_timer(0.01, self.control_loop)
        
        # Gait parameters
        self.step_frequency = 0.5  # Hz
        self.step_amplitude = 0.3  # radians
        self.time = 0.0
        
        self.get_logger().info('Biped Walker started')
    
    def control_loop(self):
        """Generate walking gait pattern."""
        self.time += 0.01
        
        # Generate sinusoidal gait pattern
        # Left and right legs move in opposition
        left_hip = self.step_amplitude * np.sin(2 * np.pi * self.step_frequency * self.time)
        right_hip = self.step_amplitude * np.sin(2 * np.pi * self.step_frequency * self.time + np.pi)
        
        # Keep knees slightly bent
        left_knee = -0.1
        right_knee = -0.1
        
        # Publish joint commands
        msg = Float64MultiArray()
        msg.data = [
            left_hip,    # Left hip
            left_knee,   # Left knee
            right_hip,   # Right hip
            right_knee,  # Right knee
        ]
        
        self.joint_pub.publish(msg)
        
        # Log every second
        if int(self.time * 100) % 100 == 0:
            self.get_logger().info(
                f'Stepping: L={left_hip:.2f}, R={right_hip:.2f}'
            )


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    walker = BipedWalker()
    
    try:
        rclpy.spin(walker)
    except KeyboardInterrupt:
        pass
    finally:
        walker.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 3: Sensor Data Processor

```python
#!/usr/bin/env python3
"""
Process and fuse data from multiple sensors.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu, Image
from nav_msgs.msg import Odometry
import numpy as np


class SensorFusion(Node):
    """Fuse data from LiDAR, IMU, and cameras."""
    
    def __init__(self):
        super().__init__('sensor_fusion')
        
        # Subscribers
        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )
        
        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )
        
        # Publisher for fused state
        self.state_pub = self.create_publisher(
            Odometry,
            '/robot_state',
            10
        )
        
        # State
        self.latest_scan = None
        self.latest_imu = None
        self.obstacle_distance = float('inf')
        self.robot_tilt = 0.0
        
        self.get_logger().info('Sensor Fusion node started')
    
    def lidar_callback(self, msg: LaserScan):
        """Process LiDAR data."""
        self.latest_scan = msg
        
        # Find closest obstacle
        valid_ranges = [r for r in msg.ranges if 0.1 < r < 10.0]
        
        if valid_ranges:
            self.obstacle_distance = min(valid_ranges)
        else:
            self.obstacle_distance = float('inf')
        
        self.get_logger().debug(f'Closest obstacle: {self.obstacle_distance:.2f}m')
    
    def imu_callback(self, msg: Imu):
        """Process IMU data."""
        self.latest_imu = msg
        
        # Extract orientation (simplified)
        # In practice, use quaternion to Euler conversion
        self.robot_tilt = msg.orientation.z  # Approximate yaw
        
        self.get_logger().debug(f'Robot tilt: {self.robot_tilt:.2f} rad')
        
        # Publish fused state
        self.publish_state()
    
    def publish_state(self):
        """Publish fused robot state."""
        if self.latest_scan is None or self.latest_imu is None:
            return
        
        state_msg = Odometry()
        state_msg.header.stamp = self.get_clock().now().to_msg()
        state_msg.header.frame_id = 'odom'
        
        # Include obstacle distance and tilt in state
        state_msg.child_frame_id = f'obstacle:{self.obstacle_distance:.2f}'
        
        self.state_pub.publish(state_msg)


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    fusion = SensorFusion()
    
    try:
        rclpy.spin(fusion)
    except KeyboardInterrupt:
        pass
    finally:
        fusion.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Hands-on Lab

### Lab 3.1: Simulate Biped Walking with Sensor Data Recording

**Objective**: Create a biped humanoid robot simulation in Gazebo and record sensor data during walking.

**Prerequisites**:
- ROS2 Humble and Gazebo installed
- Module 1 and 2 completed
- Python and NumPy knowledge

**Duration**: 90 minutes

---

#### Step 1: Create Biped Robot Package

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python biped_robot \
  --dependencies rclpy geometry_msgs sensor_msgs std_msgs

mkdir -p biped_robot/urdf
mkdir -p biped_robot/worlds
mkdir -p biped_robot/launch
```

#### Step 2: Create Biped URDF

Create `biped_robot/urdf/biped_humanoid.urdf`:

```xml
<!-- Copy URDF from Example 1 above -->
```

#### Step 3: Create Walking World

Create `biped_robot/worlds/walking_track.sdf`:

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="walking_track">
    
    <physics type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
      <max_step_size>0.001</max_step_size>
    </physics>
    
    <gravity>0 0 -9.81</gravity>
    
    <!-- Ground with friction -->
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
          <surface>
            <contact>
              <ode>
                <kp>1000000.0</kp>
                <kd>1.0</kd>
              </ode>
            </contact>
            <friction>
              <ode>
                <mu>0.8</mu>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <size>50 50</size>
            </plane>
          </geometry>
        </visual>
      </link>
    </model>
    
    <!-- Obstacles -->
    <model name="obstacle1">
      <pose>3 0 0.5 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.2 0.2 1</ambient>
          </material>
        </visual>
      </link>
    </model>
    
  </world>
</sdf>
```

#### Step 4: Create Launch File

Create `biped_robot/launch/walk_simulation.py`:

```python
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        # Launch Gazebo
        ExecuteProcess(
            cmd=['gz', 'sim', 'walking_track.sdf'],
            output='screen'
        ),
        
        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher'
        ),
        
        # Walking controller
        Node(
            package='biped_robot',
            executable='biped_walker',
            name='biped_walker',
            output='screen'
        ),
        
        # Sensor fusion
        Node(
            package='biped_robot',
            executable='sensor_fusion',
            name='sensor_fusion',
            output='screen'
        ),
    ])
```

#### Step 5: Implement Controller Nodes

Create `biped_robot/biped_robot/biped_walker.py` and `sensor_fusion.py`:

```python
# Copy code from Examples 2 and 3 above
```

#### Step 6: Build and Run

```bash
cd ~/ros2_ws
colcon build --packages-select biped_robot
source install/setup.bash

# Launch simulation
ros2 launch biped_robot walk_simulation.py
```

#### Step 7: Record Sensor Data

In a new terminal:

```bash
# Record all sensor data
ros2 bag record /scan /imu/data /joint_states /robot_state -o walking_data
```

#### Step 8: Analyze Data

```python
#!/usr/bin/env python3
"""Analyze recorded walking data."""
import rosbag2_py
from rclpy.serialization import deserialize_message
from sensor_msgs.msg import LaserScan, Imu
import matplotlib.pyplot as plt
import numpy as np

def analyze_bag(bag_path):
    """Analyze recorded bag file."""
    
    # Read bag (simplified - use actual rosbag API)
    scans = []
    imu_data = []
    
    # ... (implement bag reading)
    
    # Plot LiDAR data
    plt.figure(figsize=(12, 6))
    plt.plot(scans)
    plt.title('LiDAR Scan Data During Walking')
    plt.xlabel('Time')
    plt.ylabel('Distance (m)')
    plt.savefig('lidar_plot.png')
    
    # Plot IMU data
    plt.figure(figsize=(12, 6))
    plt.plot(imu_data)
    plt.title('IMU Data During Walking')
    plt.xlabel('Time')
    plt.ylabel('Angular Velocity (rad/s)')
    plt.savefig('imu_plot.png')
    
    print('Analysis complete!')

if __name__ == '__main__':
    analyze_bag('walking_data')
```

**Expected Result**:

Biped robot walks forward with alternating leg motion. LiDAR detects obstacles, IMU measures body tilt. Data is recorded for analysis.

## Summary

### Key Takeaways

1. **Rigid Body Dynamics**: Mass, inertia, and contact forces determine robot motion

2. **Sensor Calibration**: Noise models and calibration parameters make simulation realistic

3. **Depth Cameras**: Convert depth images to 3D point clouds for perception

4. **IMU Sensors**: Fuse accelerometer, gyroscope, and magnetometer for orientation

5. **LiDAR**: Use laser scanning for accurate distance measurement and obstacle detection

6. **Biped Walking**: Implement gait patterns with sinusoidal joint trajectories

### Key Terms

| Term | Definition |
|------|------------|
| **Rigid Body** | Object that doesn't deform under force |
| **Inertia Tensor** | 3×3 matrix describing resistance to rotation |
| **Contact Stiffness** | How hard a surface pushes back |
| **Point Cloud** | 3D points from depth sensor |
| **Sensor Fusion** | Combining data from multiple sensors |

## Exercises

### Exercise 3.1: Physics Tuning

1. Modify contact parameters (kp, kd, mu) in the world SDF
2. Test values: kp = [100000, 1000000, 10000000]
3. **Observe**: How does stiffness affect walking stability?
4. **Document** your findings with video clips

### Exercise 3.2: Sensor Noise Analysis

1. Add Gaussian noise to IMU sensor in URDF
2. Record IMU data with different noise levels
3. **Plot**: Noise standard deviation vs. orientation error
4. **Determine**: Maximum acceptable noise for stable walking

### Exercise 3.3: Obstacle Avoidance

1. Modify the walking controller to detect obstacles with LiDAR
2. Implement stop-and-turn behavior when obstacle is detected
3. **Test** with multiple obstacles in the path
4. **Measure**: Success rate of navigation

### Exercise 3.4: Point Cloud Visualization

1. Subscribe to depth camera topic
2. Convert depth images to point clouds
3. Visualize in RViz2 with PointCloud2 display
4. **Color** points by distance

### Exercise 3.5: Research Assignment

Research **sensor fusion algorithms** for humanoid robots:

- What is a Kalman Filter?
- How is IMU fused with other sensors?
- What is visual-inertial odometry (VIO)?

**Write** a 500-word technical summary with diagrams.

---

**Next Chapter**: [Chapter 4 — Unity Robot Visualization →](./chapter4-unity-visualization.md)
