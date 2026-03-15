---
sidebar_label: '4. URDF Humanoid'
---

# Chapter 4: URDF Humanoid Modeling

## What is URDF?

URDF (Unified Robot Description Format) is an XML format for describing a robot's physical properties in ROS2.

## Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot">
    
    <!-- Base Link -->
    <link name="base_link">
        <visual>
            <geometry>
                <sphere radius="0.1"/>
            </geometry>
            <material name="blue">
                <color rgba="0 0 0.8 1"/>
            </material>
        </visual>
        <collision>
            <geometry>
                <sphere radius="0.1"/>
            </geometry>
        </collision>
        <inertial>
            <mass value="1.0"/>
            <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
        </inertial>
    </link>
    
    <!-- Torso Link -->
    <link name="torso">
        <visual>
            <geometry>
                <cylinder radius="0.15" length="0.5"/>
            </geometry>
        </visual>
    </link>
    
    <!-- Joint connecting base to torso -->
    <joint name="base_to_torso" type="fixed">
        <parent link="base_link"/>
        <child link="torso"/>
        <origin xyz="0 0 0.25" rpy="0 0 0"/>
    </joint>
    
    <!-- Head Link -->
    <link name="head">
        <visual>
            <geometry>
                <sphere radius="0.12"/>
            </geometry>
        </visual>
    </link>
    
    <joint name="neck_joint" type="revolute">
        <parent link="torso"/>
        <child link="head"/>
        <origin xyz="0 0 0.3" rpy="0 0 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" velocity="1.0" effort="10"/>
    </joint>
    
    <!-- Arm Links -->
    <link name="left_arm">
        <visual>
            <geometry>
                <cylinder radius="0.05" length="0.4"/>
            </geometry>
        </visual>
    </link>
    
    <joint name="left_shoulder" type="revolute">
        <parent link="torso"/>
        <child link="left_arm"/>
        <origin xyz="0 0.2 0.2" rpy="0 1.57 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" velocity="1.0" effort="10"/>
    </joint>
    
    <link name="right_arm">
        <visual>
            <geometry>
                <cylinder radius="0.05" length="0.4"/>
            </geometry>
        </visual>
    </link>
    
    <joint name="right_shoulder" type="revolute">
        <parent link="torso"/>
        <child link="right_arm"/>
        <origin xyz="0 -0.2 0.2" rpy="0 1.57 0"/>
        <axis xyz="0 0 1"/>
        <limit lower="-1.57" upper="1.57" velocity="1.0" effort="10"/>
    </joint>
    
    <!-- Leg Links -->
    <link name="left_leg">
        <visual>
            <geometry>
                <cylinder radius="0.08" length="0.5"/>
            </geometry>
        </visual>
    </link>
    
    <joint name="left_hip" type="revolute">
        <parent link="base_link"/>
        <child link="left_leg"/>
        <origin xyz="0 0.1 -0.1" rpy="0 0 0"/>
        <axis xyz="0 1 0"/>
        <limit lower="-1.57" upper="1.57" velocity="1.0" effort="20"/>
    </joint>
    
    <link name="right_leg">
        <visual>
            <geometry>
                <cylinder radius="0.08" length="0.5"/>
            </geometry>
        </visual>
    </link>
    
    <joint name="right_hip" type="revolute">
        <parent link="base_link"/>
        <child link="right_leg"/>
        <origin xyz="0 -0.1 -0.1" rpy="0 0 0"/>
        <axis xyz="0 1 0"/>
        <limit lower="-1.57" upper="1.57" velocity="1.0" effort="20"/>
    </joint>
    
</robot>
```

## Loading URDF in ROS2

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    urdf_path = PathJoinSubstitution([
        FindPackageShare('my_robot'),
        'urdf',
        'humanoid_robot.urdf'
    ])
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': Command(['cat ', urdf_path])}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('my_robot'),
                'rviz',
                'robot_view.rviz'
            ])]
        )
    ])
```

## Visualizing in RViz2

```bash
# Launch robot visualization
ros2 launch my_robot display.launch.py
```

## Next Steps

Next, we'll build the complete robot nervous system integrating all components.
