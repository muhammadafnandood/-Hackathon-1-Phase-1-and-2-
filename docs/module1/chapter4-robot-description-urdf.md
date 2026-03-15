---
title: Robot Description using URDF
description: Learn to model humanoid robots using URDF format with links, joints, sensors, and actuators
sidebar_label: 1.4 Robot Description (URDF)
---

# Chapter 4: Robot Description using URDF

## Learning Objectives

By the end of this chapter, you will be able to:

- **Explain** what URDF is and its role in ROS 2
- **Create** robot models with links and joints
- **Design** kinematic chains for humanoid robots
- **Add** sensors and actuators to URDF models
- **Visualize** robot models in RViz
- **Validate** URDF files using command-line tools

---

## Concept Explanation

### What is URDF?

**Definition: URDF (Unified Robot Description Format)** — An XML format used in ROS to describe the physical and visual properties of a robot.

**URDF Defines:**

| Property | Description |
|----------|-------------|
| **Links** | Rigid bodies with visual, collision, and inertial properties |
| **Joints** | Connections between links with motion constraints |
| **Sensors** | Cameras, LiDAR, IMU, force/torque sensors |
| **Actuators** | Motors, servos, hydraulic actuators |
| **Transmission** | Mapping between actuators and joints |

**Why URDF Matters:**

- **Simulation** — Gazebo, Isaac Sim require accurate robot models
- **Visualization** — RViz displays robot state in 3D
- **Motion Planning** — MoveIt needs kinematic chains
- **Control** — Controllers need joint limits and dynamics

### Robot Links

**Definition: Link** — A rigid body in the robot with physical properties.

```xml
<link name="base_link">
    <!-- Visual properties (what you see in RViz) -->
    <visual>
        <geometry>
            <box size="0.5 0.3 0.2"/>
        </geometry>
        <material name="blue">
            <color rgba="0 0 0.8 1"/>
        </material>
    </visual>
    
    <!-- Collision properties (for physics simulation) -->
    <collision>
        <geometry>
            <box size="0.5 0.3 0.2"/>
        </geometry>
    </collision>
    
    <!-- Inertial properties (for dynamics) -->
    <inertial>
        <mass value="10.0"/>
        <inertia ixx="0.5" ixy="0.0" ixz="0.0"
                 iyy="0.5" iyz="0.0"
                 izz="0.5"/>
    </inertial>
</link>
```

**Link Components:**

| Element | Purpose | Required |
|---------|---------|----------|
| `<visual>` | 3D appearance | No |
| `<collision>` | Physics collision mesh | No |
| `<inertial>` | Mass and inertia | No (but recommended) |

**Geometry Types:**

```xml
<!-- Box -->
<geometry>
    <box size="length width height"/>
</geometry>

<!-- Cylinder -->
<geometry>
    <cylinder radius="0.1" length="0.5"/>
</geometry>

<!-- Sphere -->
<geometry>
    <sphere radius="0.2"/>
</geometry>

<!-- Mesh (CAD model) -->
<geometry>
    <mesh filename="package://my_robot/meshes/link.stl" scale="1 1 1"/>
</geometry>
```

### Robot Joints

**Definition: Joint** — A connection between two links that allows motion.

```xml
<joint name="hip_joint" type="revolute">
    <!-- Parent and child links -->
    <parent link="base_link"/>
    <child link="hip_link"/>
    
    <!-- Joint origin (position and orientation) -->
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    
    <!-- Joint axis -->
    <axis xyz="0 1 0"/>
    
    <!-- Joint limits -->
    <limit lower="-1.57" upper="1.57" effort="100" velocity="3.14"/>
    
    <!-- Dynamics -->
    <damping damping="0.1"/>
    <friction friction="0.1"/>
</joint>
```

**Joint Types:**

| Type | Description | Example |
|------|-------------|---------|
| **revolute** | Rotational joint with limits | Knee, elbow |
| **continuous** | Rotational joint without limits | Wheel |
| **prismatic** | Linear sliding joint | Piston |
| **fixed** | No motion | Rigid connection |
| **floating** | 6 DOF motion | Free body |
| **planar** | 2 DOF planar motion | Ground robot |

### Kinematic Chains

**Definition: Kinematic Chain** — A series of links connected by joints forming a path from base to end-effector.

```
┌─────────────────────────────────────────────────────────────┐
│              Humanoid Robot Kinematic Chains                 │
│                                                              │
│                      Head                                    │
│                       │                                      │
│                  neck_joint                                  │
│                       │                                      │
│  Left Arm         torso_link          Right Arm              │
│     │                 │                    │                 │
│  shoulder_joint   waist_joint       shoulder_joint           │
│     │                 │                    │                 │
│  elbow_joint     hip_joint           elbow_joint             │
│     │                 │                    │                 │
│  wrist_joint     left_leg_joint    right_leg_joint           │
│     │                 │                    │                 │
│    hand            knee_joint          knee_joint            │
│                      │                    │                  │
│                   ankle_joint         ankle_joint            │
│                      │                    │                  │
│                   foot_link           foot_link              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Sensors in URDF

**Gazebo Plugin for Sensors:**

```xml
<gazebo reference="camera_link">
    <sensor type="camera" name="robot_camera">
        <update_rate>30.0</update_rate>
        
        <camera name="head">
            <horizontal_fov>1.3962634</horizontal_fov>
            <image>
                <width>800</width>
                <height>600</height>
                <format>R8G8B8</format>
            </image>
            <clip>
                <near>0.02</near>
                <far>300</far>
            </clip>
        </camera>
        
        <plugin name="camera_controller" 
                filename="libgazebo_ros_camera.so">
            <frame_name>camera_link</frame_name>
        </plugin>
    </sensor>
</gazebo>
```

**Common Sensor Types:**

| Sensor | Gazebo Type | ROS Plugin |
|--------|-------------|------------|
| Camera | camera | gazebo_ros_camera |
| LiDAR | ray | gazebo_ros_laser |
| IMU | imu | gazebo_ros_imu |
| Contact | contact | gazebo_ros_bumper |
| GPS | gps | gazebo_ros_gps |

---

## Architecture Overview

### Complete Humanoid Robot URDF Structure

```
┌─────────────────────────────────────────────────────────────┐
│              Humanoid Robot URDF Structure                   │
│                                                              │
│  <robot name="humanoid">                                     │
│                                                              │
│    <!-- Base Link -->                                        │
│    <link name="base_link">...</link>                         │
│                                                              │
│    <!-- Torso Chain -->                                      │
│    <link name="torso_link">...</link>                        │
│    <joint name="waist_joint" ...>                            │
│      <parent link="base_link"/>                              │
│      <child link="torso_link"/>                              │
│    </joint>                                                  │
│                                                              │
│    <!-- Head Chain -->                                       │
│    <link name="head_link">...</link>                         │
│    <joint name="neck_joint" ...>                             │
│      <parent link="torso_link"/>                             │
│      <child link="head_link"/>                               │
│    </joint>                                                  │
│                                                              │
│    <!-- Left Arm Chain -->                                   │
│    <link name="l_shoulder_link">...</link>                   │
│    <joint name="l_shoulder_joint" ...>                       │
│    <link name="l_elbow_link">...</link>                      │
│    <joint name="l_elbow_joint" ...>                          │
│    <link name="l_hand_link">...</link>                       │
│    <joint name="l_wrist_joint" ...>                          │
│                                                              │
│    <!-- Right Arm Chain -->                                  │
│    <link name="r_shoulder_link">...</link>                   │
│    <joint name="r_shoulder_joint" ...>                       │
│    <link name="r_elbow_link">...</link>                      │
│    <joint name="r_elbow_joint" ...>                          │
│    <link name="r_hand_link">...</link>                       │
│    <joint name="r_wrist_joint" ...>                          │
│                                                              │
│    <!-- Left Leg Chain -->                                   │
│    <link name="l_hip_link">...</link>                        │
│    <joint name="l_hip_joint" ...>                            │
│    <link name="l_knee_link">...</link>                       │
│    <joint name="l_knee_joint" ...>                           │
│    <link name="l_ankle_link">...</link>                      │
│    <joint name="l_ankle_joint" ...>                          │
│    <link name="l_foot_link">...</link>                       │
│                                                              │
│    <!-- Right Leg Chain -->                                  │
│    <link name="r_hip_link">...</link>                        │
│    <joint name="r_hip_joint" ...>                            │
│    <link name="r_knee_link">...</link>                       │
│    <joint name="r_knee_joint" ...>                           │
│    <link name="r_ankle_link">...</link>                      │
│    <joint name="r_ankle_joint" ...>                          │
│    <link name="r_foot_link">...</link>                       │
│                                                              │
│    <!-- Sensors -->                                          │
│    <gazebo reference="head_link">...</gazebo>                │
│    <gazebo reference="l_foot_link">...</gazebo>              │
│    <gazebo reference="r_foot_link">...</gazebo>              │
│                                                              │
│  </robot>                                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### URDF Processing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│              URDF Processing Pipeline                        │
│                                                              │
│  URDF File                                                   │
│  (robot.urdf.xacro)                                          │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐                                            │
│  │  xacro      │ (XML macro processor)                      │
│  │  Processing │                                             │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │  URDF       │ (Parsed robot model)                       │
│  │  Parser     │                                             │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │  Robot      │ (Link poses, joint states)                 │
│  │  State      │                                             │
│  │  Publisher  │                                             │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐     ┌─────────────┐                        │
│  │  RViz       │     │  Gazebo     │                        │
│  │  (Visualize)│     │  (Simulate) │                        │
│  └─────────────┘     └─────────────┘                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Example 1: Simple Humanoid Robot URDF

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
    
    <!-- ==================== MATERIALS ==================== -->
    <material name="black">
        <color rgba="0 0 0 1"/>
    </material>
    <material name="white">
        <color rgba="1 1 1 1"/>
    </material>
    <material name="blue">
        <color rgba="0 0 0.8 1"/>
    </material>
    <material name="red">
        <color rgba="0.8 0 0 1"/>
    </material>
    
    <!-- ==================== BASE LINK ==================== -->
    <link name="base_link">
        <visual>
            <geometry>
                <box size="0.2 0.15 0.1"/>
            </geometry>
            <material name="blue"/>
            <origin xyz="0 0 0" rpy="0 0 0"/>
        </visual>
        <collision>
            <geometry>
                <box size="0.2 0.15 0.1"/>
            </geometry>
        </collision>
        <inertial>
            <mass value="5.0"/>
            <inertia ixx="0.05" ixy="0.0" ixz="0.0" 
                     iyy="0.05" iyz="0.0" 
                     izz="0.05"/>
        </inertial>
    </link>
    
    <!-- ==================== TORSO ==================== -->
    <link name="torso_link">
        <visual>
            <geometry>
                <cylinder radius="0.1" length="0.4"/>
            </geometry>
            <material name="white"/>
        </visual>
        <collision>
            <geometry>
                <cylinder radius="0.1" length="0.4"/>
            </geometry>
        </collision>
        <inertial>
            <mass value="8.0"/>
            <inertia ixx="0.1" ixy="0.0" ixz="0.0" 
                     iyy="0.1" iyz="0.0" 
                     izz="0.05"/>
        </inertial>
    </link>
    
    <joint name="waist_joint" type="revolute">
        <parent link="base_link"/>
        <child link="torso_link"/>
        <origin xyz="0 0 0.1" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="50" velocity="1.0"/>
    </joint>
    
    <!-- ==================== HEAD ==================== -->
    <link name="head_link">
        <visual>
            <geometry>
                <sphere radius="0.08"/>
            </geometry>
            <material name="white"/>
        </visual>
        <collision>
            <geometry>
                <sphere radius="0.08"/>
            </geometry>
        </collision>
        <inertial>
            <mass value="2.0"/>
            <inertia ixx="0.01" ixy="0.0" ixz="0.0" 
                     iyy="0.01" iyz="0.0" 
                     izz="0.01"/>
        </inertial>
    </link>
    
    <joint name="neck_joint" type="revolute">
        <parent link="torso_link"/>
        <child link="head_link"/>
        <origin xyz="0 0 0.25" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="20" velocity="2.0"/>
    </joint>
    
    <!-- ==================== LEFT ARM ==================== -->
    <link name="l_shoulder_link">
        <visual>
            <geometry>
                <cylinder radius="0.04" length="0.15"/>
            </geometry>
            <material name="blue"/>
        </visual>
        <inertial>
            <mass value="1.5"/>
            <inertia ixx="0.01" ixy="0.0" ixz="0.0" 
                     iyy="0.01" iyz="0.0" 
                     izz="0.005"/>
        </inertial>
    </link>
    
    <joint name="l_shoulder_joint" type="revolute">
        <parent link="torso_link"/>
        <child link="l_shoulder_link"/>
        <origin xyz="0 0.12 0.2" rpy="0 1.57 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="30" velocity="2.0"/>
    </joint>
    
    <link name="l_elbow_link">
        <visual>
            <geometry>
                <cylinder radius="0.035" length="0.15"/>
            </geometry>
            <material name="blue"/>
        </visual>
        <inertial>
            <mass value="1.0"/>
            <inertia ixx="0.005" ixy="0.0" ixz="0.0" 
                     iyy="0.005" iyz="0.0" 
                     izz="0.003"/>
        </inertial>
    </link>
    
    <joint name="l_elbow_joint" type="revolute">
        <parent link="l_shoulder_link"/>
        <child link="l_elbow_link"/>
        <origin xyz="0 0.075 0" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="25" velocity="2.5"/>
    </joint>
    
    <link name="l_hand_link">
        <visual>
            <geometry>
                <box size="0.08 0.04 0.02"/>
            </geometry>
            <material name="black"/>
        </visual>
        <inertial>
            <mass value="0.5"/>
            <inertia ixx="0.001" ixy="0.0" ixz="0.0" 
                     iyy="0.001" iyz="0.0" 
                     izz="0.001"/>
        </inertial>
    </link>
    
    <joint name="l_wrist_joint" type="revolute">
        <parent link="l_elbow_link"/>
        <child link="l_hand_link"/>
        <origin xyz="0 0.075 0" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.0" upper="1.0" effort="15" velocity="3.0"/>
    </joint>
    
    <!-- ==================== RIGHT ARM ==================== -->
    <link name="r_shoulder_link">
        <visual>
            <geometry>
                <cylinder radius="0.04" length="0.15"/>
            </geometry>
            <material name="blue"/>
        </visual>
        <inertial>
            <mass value="1.5"/>
            <inertia ixx="0.01" ixy="0.0" ixz="0.0" 
                     iyy="0.01" iyz="0.0" 
                     izz="0.005"/>
        </inertial>
    </link>
    
    <joint name="r_shoulder_joint" type="revolute">
        <parent link="torso_link"/>
        <child link="r_shoulder_link"/>
        <origin xyz="0 -0.12 0.2" rpy="0 1.57 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="30" velocity="2.0"/>
    </joint>
    
    <link name="r_elbow_link">
        <visual>
            <geometry>
                <cylinder radius="0.035" length="0.15"/>
            </geometry>
            <material name="blue"/>
        </visual>
        <inertial>
            <mass value="1.0"/>
            <inertia ixx="0.005" ixy="0.0" ixz="0.0" 
                     iyy="0.005" iyz="0.0" 
                     izz="0.003"/>
        </inertial>
    </link>
    
    <joint name="r_elbow_joint" type="revolute">
        <parent link="r_shoulder_link"/>
        <child link="r_elbow_link"/>
        <origin xyz="0 0.075 0" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="25" velocity="2.5"/>
    </joint>
    
    <link name="r_hand_link">
        <visual>
            <geometry>
                <box size="0.08 0.04 0.02"/>
            </geometry>
            <material name="black"/>
        </visual>
        <inertial>
            <mass value="0.5"/>
            <inertia ixx="0.001" ixy="0.0" ixz="0.0" 
                     iyy="0.001" iyz="0.0" 
                     izz="0.001"/>
        </inertial>
    </link>
    
    <joint name="r_wrist_joint" type="revolute">
        <parent link="r_elbow_link"/>
        <child link="r_hand_link"/>
        <origin xyz="0 0.075 0" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.0" upper="1.0" effort="15" velocity="3.0"/>
    </joint>
    
    <!-- ==================== LEFT LEG ==================== -->
    <link name="l_hip_link">
        <visual>
            <geometry>
                <cylinder radius="0.06" length="0.1"/>
            </geometry>
            <material name="red"/>
        </visual>
        <inertial>
            <mass value="3.0"/>
            <inertia ixx="0.02" ixy="0.0" ixz="0.0" 
                     iyy="0.02" iyz="0.0" 
                     izz="0.015"/>
        </inertial>
    </link>
    
    <joint name="l_hip_joint" type="revolute">
        <parent link="base_link"/>
        <child link="l_hip_link"/>
        <origin xyz="0 0.08 -0.05" rpy="1.57 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="80" velocity="2.0"/>
    </joint>
    
    <link name="l_knee_link">
        <visual>
            <geometry>
                <cylinder radius="0.05" length="0.3"/>
            </geometry>
            <material name="red"/>
        </visual>
        <inertial>
            <mass value="2.5"/>
            <inertia ixx="0.03" ixy="0.0" ixz="0.0" 
                     iyy="0.03" iyz="0.0" 
                     izz="0.02"/>
        </inertial>
    </link>
    
    <joint name="l_knee_joint" type="revolute">
        <parent link="l_hip_link"/>
        <child link="l_knee_link"/>
        <origin xyz="0 0.05 0" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="0" upper="2.5" effort="100" velocity="2.0"/>
    </joint>
    
    <link name="l_ankle_link">
        <visual>
            <geometry>
                <box size="0.15 0.08 0.05"/>
            </geometry>
            <material name="black"/>
        </visual>
        <inertial>
            <mass value="1.0"/>
            <inertia ixx="0.01" ixy="0.0" ixz="0.0" 
                     iyy="0.01" iyz="0.0" 
                     izz="0.015"/>
        </inertial>
    </link>
    
    <joint name="l_ankle_joint" type="revolute">
        <parent link="l_knee_link"/>
        <child link="l_ankle_link"/>
        <origin xyz="0 0 -0.3" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-0.5" upper="0.5" effort="50" velocity="3.0"/>
    </joint>
    
    <link name="l_foot_link">
        <visual>
            <geometry>
                <box size="0.2 0.1 0.05"/>
            </geometry>
            <material name="black"/>
        </visual>
        <collision>
            <geometry>
                <box size="0.2 0.1 0.05"/>
            </geometry>
        </collision>
        <inertial>
            <mass value="0.5"/>
            <inertia ixx="0.005" ixy="0.0" ixz="0.0" 
                     iyy="0.005" iyz="0.0" 
                     izz="0.008"/>
        </inertial>
    </link>
    
    <joint name="l_foot_joint" type="fixed">
        <parent link="l_ankle_link"/>
        <child link="l_foot_link"/>
        <origin xyz="0 0 -0.05" rpy="0 0 0"/>
    </joint>
    
    <!-- ==================== RIGHT LEG ==================== -->
    <link name="r_hip_link">
        <visual>
            <geometry>
                <cylinder radius="0.06" length="0.1"/>
            </geometry>
            <material name="red"/>
        </visual>
        <inertial>
            <mass value="3.0"/>
            <inertia ixx="0.02" ixy="0.0" ixz="0.0" 
                     iyy="0.02" iyz="0.0" 
                     izz="0.015"/>
        </inertial>
    </link>
    
    <joint name="r_hip_joint" type="revolute">
        <parent link="base_link"/>
        <child link="r_hip_link"/>
        <origin xyz="0 -0.08 -0.05" rpy="1.57 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="80" velocity="2.0"/>
    </joint>
    
    <link name="r_knee_link">
        <visual>
            <geometry>
                <cylinder radius="0.05" length="0.3"/>
            </geometry>
            <material name="red"/>
        </visual>
        <inertial>
            <mass value="2.5"/>
            <inertia ixx="0.03" ixy="0.0" ixz="0.0" 
                     iyy="0.03" iyz="0.0" 
                     izz="0.02"/>
        </inertial>
    </link>
    
    <joint name="r_knee_joint" type="revolute">
        <parent link="r_hip_link"/>
        <child link="r_knee_link"/>
        <origin xyz="0 0.05 0" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="0" upper="2.5" effort="100" velocity="2.0"/>
    </joint>
    
    <link name="r_ankle_link">
        <visual>
            <geometry>
                <box size="0.15 0.08 0.05"/>
            </geometry>
            <material name="black"/>
        </visual>
        <inertial>
            <mass value="1.0"/>
            <inertia ixx="0.01" ixy="0.0" ixz="0.0" 
                     iyy="0.01" iyz="0.0" 
                     izz="0.015"/>
        </inertial>
    </link>
    
    <joint name="r_ankle_joint" type="revolute">
        <parent link="r_knee_link"/>
        <child link="r_ankle_link"/>
        <origin xyz="0 0 -0.3" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-0.5" upper="0.5" effort="50" velocity="3.0"/>
    </joint>
    
    <link name="r_foot_link">
        <visual>
            <geometry>
                <box size="0.2 0.1 0.05"/>
            </geometry>
            <material name="black"/>
        </visual>
        <collision>
            <geometry>
                <box size="0.2 0.1 0.05"/>
            </geometry>
        </collision>
        <inertial>
            <mass value="0.5"/>
            <inertia ixx="0.005" ixy="0.0" ixz="0.0" 
                     iyy="0.005" iyz="0.0" 
                     izz="0.008"/>
        </inertial>
    </link>
    
    <joint name="r_foot_joint" type="fixed">
        <parent link="r_ankle_link"/>
        <child link="r_foot_link"/>
        <origin xyz="0 0 -0.05" rpy="0 0 0"/>
    </joint>
    
</robot>
```

---

### Example 2: URDF with Sensors (Camera + IMU)

```xml
<?xml version="1.0"?>
<robot name="humanoid_with_sensors">
    
    <!-- Include the base humanoid URDF -->
    <!-- In practice, use xacro to include files -->
    
    <!-- ==================== CAMERA SENSOR ==================== -->
    <link name="camera_link">
        <visual>
            <geometry>
                <box size="0.05 0.05 0.05"/>
            </geometry>
            <material name="black"/>
        </visual>
    </link>
    
    <joint name="camera_joint" type="fixed">
        <parent link="head_link"/>
        <child link="camera_link"/>
        <origin xyz="0.08 0 0" rpy="0 0.5 0"/>
    </joint>
    
    <!-- Gazebo Camera Plugin -->
    <gazebo reference="camera_link">
        <sensor type="camera" name="head_camera">
            <update_rate>30.0</update_rate>
            
            <camera name="head">
                <horizontal_fov>1.3962634</horizontal_fov>
                <image>
                    <width>800</width>
                    <height>600</height>
                    <format>R8G8B8</format>
                </image>
                <clip>
                    <near>0.1</near>
                    <far>100</far>
                </clip>
                <noise>
                    <type>gaussian</type>
                    <mean>0.0</mean>
                    <stddev>0.007</stddev>
                </noise>
            </camera>
            
            <plugin name="camera_controller" 
                    filename="libgazebo_ros_camera.so">
                <frame_name>camera_link</frame_name>
                <camera_info_topic>/camera/camera_info</camera_info_topic>
                <image_topic>/camera/image_raw</image_topic>
            </plugin>
        </sensor>
    </gazebo>
    
    <!-- ==================== IMU SENSOR ==================== -->
    <link name="imu_link">
        <visual>
            <geometry>
                <box size="0.02 0.02 0.02"/>
            </geometry>
            <material name="red"/>
        </visual>
    </link>
    
    <joint name="imu_joint" type="fixed">
        <parent link="base_link"/>
        <child link="imu_link"/>
        <origin xyz="0 0 0" rpy="0 0 0"/>
    </joint>
    
    <!-- Gazebo IMU Plugin -->
    <gazebo reference="imu_link">
        <sensor type="imu" name="imu_sensor">
            <always_on>true</always_on>
            <update_rate>100</update_rate>
            
            <imu>
                <angular_velocity>
                    <x>
                        <noise type="gaussian">
                            <mean>0.0</mean>
                            <stddev>0.001</stddev>
                        </noise>
                    </x>
                    <y>
                        <noise type="gaussian">
                            <mean>0.0</mean>
                            <stddev>0.001</stddev>
                        </noise>
                    </y>
                    <z>
                        <noise type="gaussian">
                            <mean>0.0</mean>
                            <stddev>0.001</stddev>
                        </noise>
                    </z>
                </angular_velocity>
                <linear_acceleration>
                    <x>
                        <noise type="gaussian">
                            <mean>0.0</mean>
                            <stddev>0.01</stddev>
                        </noise>
                    </x>
                    <y>
                        <noise type="gaussian">
                            <mean>0.0</mean>
                            <stddev>0.01</stddev>
                        </noise>
                    </y>
                    <z>
                        <noise type="gaussian">
                            <mean>0.0</mean>
                            <stddev>0.01</stddev>
                        </noise>
                    </z>
                </linear_acceleration>
            </imu>
            
            <plugin name="imu_controller" 
                    filename="libgazebo_ros_imu_sensor.so">
                <frame_name>imu_link</frame_name>
                <topic_name>/imu/data</topic_name>
            </plugin>
        </sensor>
    </gazebo>
    
    <!-- ==================== LiDAR SENSOR ==================== -->
    <link name="lidar_link">
        <visual>
            <geometry>
                <cylinder radius="0.05" length="0.05"/>
            </geometry>
            <material name="white"/>
        </visual>
    </link>
    
    <joint name="lidar_joint" type="fixed">
        <parent link="torso_link"/>
        <child link="lidar_link"/>
        <origin xyz="0.05 0 0.15" rpy="0 0 0"/>
    </joint>
    
    <!-- Gazebo LiDAR Plugin -->
    <gazebo reference="lidar_link">
        <sensor type="ray" name="head_lidar">
            <pose>0 0 0 0 0 0</pose>
            <visualize>true</visualize>
            <update_rate>10</update_rate>
            
            <ray>
                <scan>
                    <horizontal>
                        <samples>360</samples>
                        <resolution>1</resolution>
                        <min_angle>-3.14159</min_angle>
                        <max_angle>3.14159</max_angle>
                    </horizontal>
                </scan>
                <range>
                    <min>0.1</min>
                    <max>10.0</max>
                    <resolution>0.01</resolution>
                </range>
                <noise>
                    <type>gaussian</type>
                    <mean>0.0</mean>
                    <stddev>0.01</stddev>
                </noise>
            </ray>
            
            <plugin name="lidar_controller" 
                    filename="libgazebo_ros_ray_sensor.so">
                <ros>
                    <argument>~/out:=/scan</argument>
                </ros>
                <output_type>sensor_msgs/LaserScan</output_type>
                <frame_name>lidar_link</frame_name>
            </plugin>
        </sensor>
    </gazebo>
    
</robot>
```

---

### Example 3: Xacro Macro for Reusable Components

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" 
       name="modular_humanoid">
    
    <!-- ==================== XACRO PROPERTIES ==================== -->
    <xacro:property name="PI" value="3.14159265359"/>
    
    <!-- ==================== ARM MACRO ==================== -->
    <xacro:macro name="arm" params="prefix parent *origin">
        
        <!-- Shoulder Link -->
        <link name="${prefix}_shoulder_link">
            <visual>
                <geometry>
                    <cylinder radius="0.04" length="0.15"/>
                </geometry>
                <material name="blue"/>
            </visual>
            <inertial>
                <mass value="1.5"/>
                <inertia ixx="0.01" ixy="0.0" ixz="0.0" 
                         iyy="0.01" iyz="0.0" 
                         izz="0.005"/>
            </inertial>
        </link>
        
        <!-- Shoulder Joint -->
        <joint name="${prefix}_shoulder_joint" type="revolute">
            <parent link="${parent}"/>
            <child link="${prefix}_shoulder_link"/>
            <xacro:insert_block name="origin"/>
            <axis xyz="0 0 1"/>
            <limit lower="-1.57" upper="1.57" effort="30" velocity="2.0"/>
        </joint>
        
        <!-- Elbow Link -->
        <link name="${prefix}_elbow_link">
            <visual>
                <geometry>
                    <cylinder radius="0.035" length="0.15"/>
                </geometry>
                <material name="blue"/>
            </visual>
            <inertial>
                <mass value="1.0"/>
                <inertia ixx="0.005" ixy="0.0" ixz="0.0" 
                         iyy="0.005" iyz="0.0" 
                         izz="0.003"/>
            </inertial>
        </link>
        
        <!-- Elbow Joint -->
        <joint name="${prefix}_elbow_joint" type="revolute">
            <parent link="${prefix}_shoulder_link"/>
            <child link="${prefix}_elbow_link"/>
            <origin xyz="0 0.075 0" rpy="0 0 0"/>
            <axis xyz="0 0 1"/>
            <limit lower="-1.57" upper="1.57" effort="25" velocity="2.5"/>
        </joint>
        
        <!-- Hand Link -->
        <link name="${prefix}_hand_link">
            <visual>
                <geometry>
                    <box size="0.08 0.04 0.02"/>
                </geometry>
                <material name="black"/>
            </visual>
            <inertial>
                <mass value="0.5"/>
                <inertia ixx="0.001" ixy="0.0" ixz="0.0" 
                         iyy="0.001" iyz="0.0" 
                         izz="0.001"/>
            </inertial>
        </link>
        
        <!-- Wrist Joint -->
        <joint name="${prefix}_wrist_joint" type="revolute">
            <parent link="${prefix}_elbow_link"/>
            <child link="${prefix}_hand_link"/>
            <origin xyz="0 0.075 0" rpy="0 0 0"/>
            <axis xyz="0 0 1"/>
            <limit lower="-1.0" upper="1.0" effort="15" velocity="3.0"/>
        </joint>
        
    </xacro:macro>
    
    <!-- ==================== LEG MACRO ==================== -->
    <xacro:macro name="leg" params="prefix parent *origin">
        
        <!-- Hip Link -->
        <link name="${prefix}_hip_link">
            <visual>
                <geometry>
                    <cylinder radius="0.06" length="0.1"/>
                </geometry>
                <material name="red"/>
            </visual>
            <inertial>
                <mass value="3.0"/>
                <inertia ixx="0.02" ixy="0.0" ixz="0.0" 
                         iyy="0.02" iyz="0.0" 
                         izz="0.015"/>
            </inertial>
        </link>
        
        <!-- Hip Joint -->
        <joint name="${prefix}_hip_joint" type="revolute">
            <parent link="${parent}"/>
            <child link="${prefix}_hip_link"/>
            <xacro:insert_block name="origin"/>
            <axis xyz="0 0 1"/>
            <limit lower="-1.57" upper="1.57" effort="80" velocity="2.0"/>
        </joint>
        
        <!-- Knee Link -->
        <link name="${prefix}_knee_link">
            <visual>
                <geometry>
                    <cylinder radius="0.05" length="0.3"/>
                </geometry>
                <material name="red"/>
            </visual>
            <inertial>
                <mass value="2.5"/>
                <inertia ixx="0.03" ixy="0.0" ixz="0.0" 
                         iyy="0.03" iyz="0.0" 
                         izz="0.02"/>
            </inertial>
        </link>
        
        <!-- Knee Joint -->
        <joint name="${prefix}_knee_joint" type="revolute">
            <parent link="${prefix}_hip_link"/>
            <child link="${prefix}_knee_link"/>
            <origin xyz="0 0.05 0" rpy="0 0 0"/>
            <axis xyz="0 0 1"/>
            <limit lower="0" upper="2.5" effort="100" velocity="2.0"/>
        </joint>
        
        <!-- Foot Link -->
        <link name="${prefix}_foot_link">
            <visual>
                <geometry>
                    <box size="0.2 0.1 0.05"/>
                </geometry>
                <material name="black"/>
            </visual>
            <collision>
                <geometry>
                    <box size="0.2 0.1 0.05"/>
                </geometry>
            </collision>
            <inertial>
                <mass value="0.5"/>
                <inertia ixx="0.005" ixy="0.0" ixz="0.0" 
                         iyy="0.005" iyz="0.0" 
                         izz="0.008"/>
            </inertial>
        </link>
        
        <!-- Ankle Joint -->
        <joint name="${prefix}_ankle_joint" type="revolute">
            <parent link="${prefix}_knee_link"/>
            <child link="${prefix}_foot_link"/>
            <origin xyz="0 0 -0.3" rpy="0 0 0"/>
            <axis xyz="0 0 1"/>
            <limit lower="-0.5" upper="0.5" effort="50" velocity="3.0"/>
        </joint>
        
    </xacro:macro>
    
    <!-- ==================== USE MACROS ==================== -->
    
    <!-- Base Link -->
    <link name="base_link">
        <visual>
            <geometry>
                <box size="0.2 0.15 0.1"/>
            </geometry>
            <material name="blue"/>
        </visual>
    </link>
    
    <!-- Torso -->
    <link name="torso_link">
        <visual>
            <geometry>
                <cylinder radius="0.1" length="0.4"/>
            </geometry>
            <material name="white"/>
        </visual>
    </link>
    
    <joint name="waist_joint" type="revolute">
        <parent link="base_link"/>
        <child link="torso_link"/>
        <origin xyz="0 0 0.1" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" effort="50" velocity="1.0"/>
    </joint>
    
    <!-- Left Arm -->
    <xacro:arm prefix="l" parent="torso_link">
        <origin xyz="0 0.12 0.2" rpy="0 1.57 0"/>
    </xacro:arm>
    
    <!-- Right Arm -->
    <xacro:arm prefix="r" parent="torso_link">
        <origin xyz="0 -0.12 0.2" rpy="0 1.57 0"/>
    </xacro:arm>
    
    <!-- Left Leg -->
    <xacro:leg prefix="l" parent="base_link">
        <origin xyz="0 0.08 -0.05" rpy="1.57 0 0"/>
    </xacro:leg>
    
    <!-- Right Leg -->
    <xacro:leg prefix="r" parent="base_link">
        <origin xyz="0 -0.08 -0.05" rpy="1.57 0 0"/>
    </xacro:leg>
    
</robot>
```

---

## Hands-on Lab

### Lab 4.1: Create a Simple Humanoid Robot Model

**Objective:** Build and visualize a basic humanoid robot URDF model

**Prerequisites:**
- ROS 2 Humble installed
- RViz installed (`sudo apt install ros-humble-rviz2`)
- Chapters 1-3 completed

**Time:** 60 minutes

---

### Step 1: Create URDF Package

```bash
cd ~/ros2_ws/src

# Create package for robot descriptions
ros2 pkg create --build-type ament_python robot_description \
    --dependencies urdf launch_xml launch_yaml

cd robot_description
mkdir -p urdf meshes launch
```

---

### Step 2: Create URDF File

Create the URDF file:

```bash
cd urdf
nano simple_humanoid.urdf
```

Copy the code from **Example 1: Simple Humanoid Robot URDF** above.

---

### Step 3: Create Launch File

Create a launch file to display the robot in RViz:

```bash
cd ../launch
nano display_robot.launch.py
```

```python
#!/usr/bin/env python3
"""
display_robot.launch.py
Launch file to display humanoid robot in RViz
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Get package path
    pkg_path = get_package_share_directory('robot_description')
    urdf_path = os.path.join(pkg_path, 'urdf', 'simple_humanoid.urdf')
    
    # Read URDF
    with open(urdf_path, 'r') as f:
        robot_desc = f.read()
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}],
    )
    
    # Joint State Publisher (for testing without controllers)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_gui': True}],
    )
    
    # RViz
    rviz_config = os.path.join(pkg_path, 'launch', 'robot.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
    )
    
    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher,
        rviz_node,
    ])
```

---

### Step 4: Create RViz Configuration

Create RViz config file:

```bash
nano robot.rviz
```

```yaml
Panels:
  - Class: rviz_common/Displays
Visualization Manager:
  Displays:
    - Class: rviz_default_plugins/RobotModel
      Name: RobotModel
      Description Topic:
        Value: /robot_description
      Enabled: true
      Alpha: 1.0
    - Class: rviz_default_plugins/TF
      Name: TF
      Enabled: true
  Global Options:
    Fixed Frame: base_link
  Tools:
    - Class: rviz_default_plugins/MoveCamera
```

---

### Step 5: Update package.xml

Add dependencies:

```xml
<exec_depend>urdf</exec_depend>
<exec_depend>robot_state_publisher</exec_depend>
<exec_depend>joint_state_publisher</exec_depend>
<exec_depend>rviz2</exec_depend>
<exec_depend>launch</exec_depend>
<exec_depend>launch_ros</exec_depend>
```

---

### Step 6: Build and Run

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash

# Launch robot visualization
ros2 launch robot_description display_robot.launch.py
```

**Expected Result:**
- RViz opens with the humanoid robot model
- Use Joint State Publisher GUI to move joints
- Robot should respond to slider controls

---

### Step 7: Validate URDF

Use command-line tools to check URDF:

```bash
# Check URDF syntax
check_urdf src/robot_description/urdf/simple_humanoid.urdf

# Expected output:
# robot name is: simple_humanoid
# ... SUCCESS: All links and joints defined correctly
```

---

### Step 8: Visualize in RViz

In RViz:

1. Set **Fixed Frame** to `base_link`
2. Add **RobotModel** display
3. Set **Robot Description** to `/robot_description`
4. Add **TF** display to see coordinate frames
5. Use **joint_state_publisher** GUI to move joints

---

## Summary

### Key Takeaways

1. **URDF** describes robot geometry, physics, and sensors in XML
2. **Links** are rigid bodies with visual, collision, and inertial properties
3. **Joints** connect links and define motion constraints
4. **Kinematic chains** form the robot's structure from base to end-effectors
5. **Sensors** are added using Gazebo plugins
6. **Xacro** provides macros for reusable URDF components

### URDF Element Reference

| Element | Purpose | Example |
|---------|---------|---------|
| `<link>` | Rigid body | torso, arm, leg |
| `<joint>` | Connection | revolute, prismatic, fixed |
| `<visual>` | Appearance | box, cylinder, mesh |
| `<collision>` | Physics mesh | Simplified geometry |
| `<inertial>` | Mass properties | mass, inertia matrix |
| `<gazebo>` | Simulation | Sensors, plugins |

---

## Exercises

### Exercise 4.1: Add Fingers

Extend the hand model to include:
- Thumb with 2 joints
- Index finger with 3 joints
- Simple gripper mechanism

Test in RViz.

### Exercise 4.2: Add Color Materials

Define custom materials for:
- Skin color for head and hands
- Clothing color for torso
- Shoe color for feet

Use RGBA values.

### Exercise 4.3: Create Xacro Macros

Refactor the URDF using Xacro:
- Create a `finger` macro
- Create a `sensor_mount` macro
- Use properties for common dimensions

### Exercise 4.4: Add Collision Meshes

Add simplified collision geometry:
- Use boxes and cylinders instead of detailed meshes
- Ensure collision shapes are smaller than visual shapes
- Test collision detection in Gazebo

---

## Next Chapter

In **Chapter 5: Building the Robot Nervous System**, you will learn:

- How to integrate multiple ROS 2 nodes
- Create launch files for complex systems
- Configure parameters for robot behavior
- Debug using ROS 2 CLI tools
- Build a complete multi-node robot system

---

## Resources

### Official Documentation

- [URDF Tutorial](http://wiki.ros.org/urdf/Tutorials)
- [URDF API](http://wiki.ros.org/urdf/XML)
- [Xacro Documentation](http://wiki.ros.org/xacro)

### Tools

- [check_urdf](http://wiki.ros.org/urdf) — URDF validation
- [urdf_to_graphviz](http://wiki.ros.org/urdf) — Visualize robot structure
- [RViz](http://wiki.ros.org/rviz) — 3D visualization

### Mesh Resources

- [GrabCAD](https://grabcad.com/library) — Free CAD models
- [ROS 3D Objects](https://github.com/ros-gazebo/gazebo_ros_demos) — Example meshes
