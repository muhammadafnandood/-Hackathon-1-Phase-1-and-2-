---
sidebar_label: '5. Building the Digital Twin'
---

# Chapter 5: Building the Digital Twin

## Learning Objectives

By the end of this chapter, you will be able to:

- Integrate Gazebo physics with Unity visualization into a complete digital twin
- Combine multiple sensor simulations for sensor fusion
- Implement robot model integration across simulation platforms
- Test AI perception algorithms in the digital twin environment
- Apply digital twin best practices for sim-to-real transfer
- Build a complete digital twin of a humanoid robot with full sensor suite

## Concept Explanation

### What is a Digital Twin?

A **Digital Twin** is a comprehensive virtual representation of a physical robot that mirrors its:

```
┌─────────────────────────────────────────────────────────────┐
│                  DIGITAL TWIN COMPONENTS                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Physical Robot              Digital Twin                    │
│  ──────────────              ────────────                    │
│                                                              │
│  ┌──────────────┐            ┌──────────────┐               │
│  │   Motors     │◄──────────►│  Actuators   │               │
│  │  (Torque)    │  Real-time │  (Simulation)│               │
│  └──────────────┘  Data Sync └──────────────┘               │
│                                                              │
│  ┌──────────────┐            ┌──────────────┐               │
│  │   Sensors    │◄──────────►│  Sensor      │               │
│  │ (LiDAR, IMU) │  Streaming │  Models      │               │
│  └──────────────┘            └──────────────┘               │
│                                                              │
│  ┌──────────────┐            ┌──────────────┐               │
│  │  Controller  │◄──────────►│  Control     │               │
│  │  (Real HW)   │  Commands  │  Algorithm   │               │
│  └──────────────┘            └──────────────┘               │
│                                                              │
│  ┌──────────────┐            ┌──────────────┐               │
│  │ Environment  │◄──────────►│  Physics     │               │
│  │  (Real)      │  Matching  │  Simulation  │               │
│  └──────────────┘            └──────────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Digital Twin vs Simple Simulation:**

| Feature | Simulation | Digital Twin |
|---------|------------|--------------|
| **Connection** | Standalone | Real-time bidirectional |
| **Purpose** | Testing/Training | Monitoring + Control |
| **Data** | Synthetic | Real + Synthetic |
| **Update** | Manual | Continuous |
| **Fidelity** | Approximate | Mirror-accurate |

### Robot Model Integration

**Integrating robot models** across platforms requires careful synchronization:

```
┌─────────────────────────────────────────────────────────────┐
│              ROBOT MODEL INTEGRATION FLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  URDF (ROS Standard)                                         │
│         ↓                                                    │
│  Convert to SDF (for Gazebo)                                │
│         ↓                                                    │
│  Convert to FBX (for Unity)                                 │
│         ↓                                                    │
│  Synchronize Parameters:                                     │
│  • Joint limits                                              │
│  • Link masses                                               │
│  • Inertia tensors                                           │
│  • Visual meshes                                             │
│  • Collision geometry                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Conversion Tools:**

```bash
# URDF to SDF (automatic in Gazebo)
gz sdf -p robot.urdf > robot.sdf

# URDF to FBX (using Blender)
# 1. Install urdf-importer addon
# 2. File → Import → URDF
# 3. File → Export → FBX
```

### Sensor Fusion

**Sensor fusion** combines data from multiple sensors for robust perception:

```
┌─────────────────────────────────────────────────────────────┐
│                    SENSOR FUSION                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Individual Sensors         Fused Output                     │
│  ──────────────────         ────────────                     │
│                                                              │
│  ┌──────────┐                                                │
│  │  LiDAR   │───┐                                            │
│  │ (Range)  │   │                                            │
│  └──────────┘   │                                            │
│                 │    ┌──────────────┐    ┌──────────────┐   │
│  ┌──────────┐   │───►│   Sensor     │───►│  Environment │   │
│  │  Camera  │───┤    │   Fusion     │    │    Model     │   │
│  │  (RGB)   │   │    │  Algorithm   │    └──────────────┘   │
│  └──────────┘   │    └──────────────┘                       │
│                 │                                            │
│  ┌──────────┐   │                                            │
│  │   IMU    │───┘                                            │
│  │(Motion)  │                                                │
│  └──────────┘                                                │
│                                                              │
│  Fusion Techniques:                                          │
│  • Kalman Filter                                             │
│  • Extended Kalman Filter (EKF)                              │
│  • Particle Filter                                           │
│  • Deep Learning                                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Testing AI Perception

**AI perception testing** in digital twins enables safe, scalable validation:

```
┌─────────────────────────────────────────────────────────────┐
│              AI PERCEPTION TESTING PIPELINE                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Scenario Generation                                      │
│     ────────────────────                                     │
│     • Vary lighting conditions                               │
│     • Add obstacles                                          │
│     • Change weather                                         │
│     • Modify textures                                        │
│                                                              │
│  2. Data Collection                                          │
│     ────────────────                                         │
│     • Record sensor data                                     │
│     • Log ground truth                                       │
│     • Capture edge cases                                     │
│                                                              │
│  3. Model Evaluation                                         │
│     ─────────────────                                        │
│     • Accuracy metrics                                       │
│     • Robustness analysis                                    │
│     • Failure mode identification                            │
│                                                              │
│  4. Sim-to-Real Transfer                                     │
│     ────────────────────                                     │
│     • Domain adaptation                                      │
│     • Fine-tuning on real data                               │
│     • Validation on physical robot                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Best Practices

**Digital Twin Best Practices:**

```
┌─────────────────────────────────────────────────────────────┐
│                  BEST PRACTICES                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Model Accuracy                                           │
│     ────────────────                                         │
│     ✓ Match physical parameters (mass, inertia)             │
│     ✓ Calibrate sensor models                                │
│     ✓ Validate against real robot                            │
│                                                              │
│  2. Real-time Synchronization                                │
│     ────────────────────────                                 │
│     ✓ Low-latency communication                              │
│     ✓ Timestamp alignment                                    │
│     ✓ Clock synchronization                                  │
│                                                              │
│  3. Validation                                               │
│     ─────────                                                │
│     ✓ Regular comparison with physical robot                │
│     ✓ System identification                                  │
│     ✓ Continuous calibration                                 │
│                                                              │
│  4. Documentation                                            │
│     ───────────────                                          │
│     ✓ Version control for models                             │
│     ✓ Change tracking                                        │
│     ✓ Configuration management                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### NASA Mars Rover Digital Twin

NASA maintains **digital twins** of Mars rovers for mission operations:

```
┌────────────────────────────────────────────────────────┐
│           MARS ROVER DIGITAL TWIN SYSTEM                │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Mars (Physical)          Earth (Digital Twin)         │
│  ─────────────            ──────────────────           │
│                                                         │
│  • Perseverance Rover  →  • Virtual Rover              │
│  • Mars Terrain        →  • Mars Terrain Map           │
│  • Real Commands       →  • Command Testing            │
│  • 20min delay         →  • Immediate Feedback         │
│                                                         │
│  Operations Workflow:                                   │
│  ───────────────────                                    │
│  1. Plan commands on Earth digital twin                │
│  2. Test in simulation (validate safety)               │
│  3. Uplink to Mars rover                               │
│  4. Rover executes commands                            │
│  5. Data downlinked to update digital twin             │
│                                                         │
│  Benefits:                                              │
│  • Risk mitigation (test before sending)               │
│  • Faster operations (no wait for execution)           │
│  • Training (new team members practice)                │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete Digital Twin Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              COMPLETE DIGITAL TWIN SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   PHYSICAL LAYER                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │  Robot   │  │ Sensors  │  │  Network │           │   │
│  │  │  Hardware│  │ (Real)   │  │  (5G/WiFi)│          │   │
│  │  └──────────┘  └──────────┘  └──────────┘           │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↕ Real-time Data                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   DIGITAL LAYER                       │   │
│  │                                                       │   │
│  │  ┌──────────────┐    ┌──────────────┐               │   │
│  │  │   Gazebo     │    │    Unity     │               │   │
│  │  │  (Physics)   │◄──►│ (Rendering)  │               │   │
│  │  └──────────────┘    └──────────────┘               │   │
│  │         ↕                    ↕                       │   │
│  │  ┌──────────────────────────────────────┐           │   │
│  │  │         ROS2 Middleware               │           │   │
│  │  │  (Topics, Services, Actions)         │           │   │
│  │  └──────────────────────────────────────┘           │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↕                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  APPLICATION LAYER                    │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │  AI/ML   │  │  Control │  │   HMI    │           │   │
│  │  │ Training │  │ Algorithms│  │ (Unity)  │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow in Digital Twin

```
Physical Robot Sensors
         ↓
    [Real Data]
         ↓
    ROS2 Topics
         ↓
    ┌───┴───┐
    ↓       ↓
 Gazebo   Unity
(Update  (Visual
 State)  Update)
    ↓       ↓
    └───┬───┘
        ↓
  AI/ML Models
        ↓
   Decisions
        ↓
Physical Robot Actuators
```

## Code Examples

### Example 1: Complete Digital Twin Launch File

```python
#!/usr/bin/env python3
"""
Launch complete digital twin: Gazebo + Unity + ROS2 Bridge.
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_unity_bridge(context, *args, **kwargs):
    """Launch Unity data streaming bridge."""
    return [
        Node(
            package='digital_twin',
            executable='unity_streamer',
            name='unity_streamer',
            output='screen',
            parameters=[{
                'websocket_port': 8765,
                'stream_rate': 60.0,  # Hz
            }]
        )
    ]


def generate_launch_description():
    """Generate launch description for digital twin."""
    
    # Arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='humanoid_lab',
        description='Gazebo world name'
    )
    
    robot_arg = DeclareLaunchArgument(
        'robot',
        default_value='humanoid',
        description='Robot model name'
    )
    
    # Paths
    pkg_share = FindPackageShare('digital_twin')
    world_path = os.path.join(pkg_share, 'worlds', 'humanoid_lab.sdf')
    urdf_path = os.path.join(pkg_share, 'urdf', 'humanoid.urdf')
    
    # Gazebo
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', world_path, '-s'],  # -s for headless (optional)
        output='screen'
    )
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': urdf_path}]
    )
    
    # Spawn Robot
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_robot',
        arguments=[
            '-entity', 'humanoid',
            '-file', urdf_path,
            '-x', '0', '-y', '0', '-z', '1.0',
        ]
    )
    
    # Sensor Fusion Node
    sensor_fusion = Node(
        package='digital_twin',
        executable='sensor_fusion',
        name='sensor_fusion',
        output='screen'
    )
    
    # Digital Twin Controller
    dt_controller = Node(
        package='digital_twin',
        executable='digital_twin_controller',
        name='dt_controller',
        output='screen'
    )
    
    return LaunchDescription([
        world_arg,
        robot_arg,
        gazebo,
        robot_state_publisher,
        spawn_robot,
        sensor_fusion,
        dt_controller,
        OpaqueFunction(function=launch_unity_bridge),
    ])


if __name__ == '__main__':
    generate_launch_description()
```

### Example 2: Digital Twin Synchronizer

```python
#!/usr/bin/env python3
"""
Synchronize physical robot state with digital twin.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped, Twist
from std_msgs.msg import Float64MultiArray
import asyncio
import websockets
import json


class DigitalTwinSynchronizer(Node):
    """Synchronize physical and digital robot states."""
    
    def __init__(self):
        super().__init__('digital_twin_synchronizer')
        
        # Subscribers (from physical robot)
        self.joint_sub = self.create_subscription(
            JointState,
            '/physical/joint_states',
            self.physical_joint_callback,
            10
        )
        
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/physical/pose',
            self.physical_pose_callback,
            10
        )
        
        # Publishers (to digital twin)
        self.dt_joint_pub = self.create_publisher(
            Float64MultiArray,
            '/digital/joint_commands',
            10
        )
        
        self.dt_pose_pub = self.create_publisher(
            PoseStamped,
            '/digital/pose_command',
            10
        )
        
        # WebSocket to Unity
        self.unity_ws = None
        
        # State
        self.latest_physical_joints = None
        self.latest_physical_pose = None
        
        self.get_logger().info('Digital Twin Synchronizer started')
    
    def physical_joint_callback(self, msg: JointState):
        """Receive joint states from physical robot."""
        self.latest_physical_joints = msg
        
        # Mirror to digital twin
        dt_msg = Float64MultiArray()
        dt_msg.data = list(msg.position)
        self.dt_joint_pub.publish(dt_msg)
        
        self.get_logger().debug(f'Synchronized joints: {len(msg.name)} joints')
    
    def physical_pose_callback(self, msg: PoseStamped):
        """Receive pose from physical robot."""
        self.latest_physical_pose = msg
        
        # Mirror to digital twin
        self.dt_pose_pub.publish(msg)
        
        # Send to Unity for visualization
        asyncio.create_task(self.send_to_unity({
            'type': 'pose_update',
            'pose': {
                'position': [
                    msg.pose.position.x,
                    msg.pose.position.y,
                    msg.pose.position.z
                ],
                'orientation': [
                    msg.pose.orientation.x,
                    msg.pose.orientation.y,
                    msg.pose.orientation.z,
                    msg.pose.orientation.w
                ]
            }
        }))
    
    async def send_to_unity(self, data):
        """Send data to Unity visualization."""
        try:
            if self.unity_ws is None:
                self.unity_ws = await websockets.connect('ws://localhost:8765')
            
            await self.unity_ws.send(json.dumps(data))
        except Exception as e:
            self.get_logger().error(f'Unity send failed: {e}')
            self.unity_ws = None
    
    async def receive_from_unity(self):
        """Receive commands from Unity."""
        try:
            if self.unity_ws is None:
                self.unity_ws = await websockets.connect('ws://localhost:8765')
            
            async for message in self.unity_ws:
                data = json.loads(message)
                
                if data.get('type') == 'velocity_command':
                    # Forward velocity command to physical robot
                    cmd = Twist()
                    cmd.linear.x = data['linear']['x']
                    cmd.linear.y = data['linear']['y']
                    cmd.linear.z = data['linear']['z']
                    cmd.angular.z = data['angular']['z']
                    
                    # Publish to physical robot
                    # (implement publisher as needed)
                    
        except Exception as e:
            self.get_logger().error(f'Unity receive failed: {e}')
            self.unity_ws = None


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    synchronizer = DigitalTwinSynchronizer()
    
    # Run ROS2 spinner and Unity communication concurrently
    import threading
    
    async def run_unity_comm():
        await synchronizer.receive_from_unity()
    
    unity_thread = threading.Thread(target=lambda: asyncio.run(run_unity_comm()))
    unity_thread.start()
    
    try:
        rclpy.spin(synchronizer)
    except KeyboardInterrupt:
        pass
    finally:
        synchronizer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 3: Sensor Fusion with Kalman Filter

```python
#!/usr/bin/env python3
"""
Multi-sensor fusion using Extended Kalman Filter.
"""
import numpy as np
from filterpy.kalman import ExtendedKalmanFilter as EKF


class SensorFusionEKF:
    """Fuse LiDAR, IMU, and odometry using EKF."""
    
    def __init__(self):
        # State: [x, y, z, vx, vy, vz, roll, pitch, yaw]
        self.ekf = EKF(dim_x=9, dim_z=6)
        
        # Initial state
        self.ekf.x = np.array([
            0, 0, 0,  # Position
            0, 0, 0,  # Velocity
            0, 0, 0   # Orientation
        ])
        
        # State transition matrix (constant velocity model)
        dt = 0.01  # 100 Hz
        self.ekf.F = np.array([
            [1, 0, 0, dt, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, dt, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, dt, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
        ])
        
        # Measurement matrix (measure position and orientation)
        self.ekf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0],  # x
            [0, 1, 0, 0, 0, 0, 0, 0, 0],  # y
            [0, 0, 1, 0, 0, 0, 0, 0, 0],  # z
            [0, 0, 0, 0, 0, 0, 1, 0, 0],  # roll
            [0, 0, 0, 0, 0, 0, 0, 1, 0],  # pitch
            [0, 0, 0, 0, 0, 0, 0, 0, 1],  # yaw
        ])
        
        # Process noise
        self.ekf.Q = np.diag([0.1, 0.1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        
        # Measurement noise
        self.ekf.R = np.diag([0.5, 0.5, 0.5, 0.01, 0.01, 0.01])
        
        # Initial covariance
        self.ekf.P = np.eye(9) * 1.0
    
    def predict(self, dt=0.01):
        """Predict next state."""
        self.ekf.F[0, 3] = dt  # Update dt in state transition
        self.ekf.F[1, 4] = dt
        self.ekf.F[2, 5] = dt
        self.ekf.predict()
    
    def update(self, measurement):
        """
        Update with sensor measurement.
        
        measurement: [x, y, z, roll, pitch, yaw]
        """
        self.ekf.update(np.array(measurement))
    
    def get_state(self):
        """Get current state estimate."""
        return self.ekf.x.copy()
    
    def get_covariance(self):
        """Get state covariance."""
        return self.ekf.P.copy()


# Example usage
def test_sensor_fusion():
    """Test sensor fusion with simulated data."""
    fusion = SensorFusionEKF()
    
    # Simulate measurements (noisy)
    for i in range(100):
        # True state
        true_x = i * 0.1
        true_y = np.sin(i * 0.1)
        
        # Noisy measurements
        meas_x = true_x + np.random.randn() * 0.1
        meas_y = true_y + np.random.randn() * 0.1
        
        # Update
        fusion.predict()
        fusion.update([meas_x, meas_y, 0, 0, 0, 0])
        
        # Get estimate
        state = fusion.get_state()
        
        print(f"Step {i}: Estimate=({state[0]:.3f}, {state[1]:.3f}), "
              f"True=({true_x:.3f}, {true_y:.3f})")


if __name__ == '__main__':
    test_sensor_fusion()
```

### Example 4: Complete Humanoid Digital Twin

```xml
<!-- humanoid_digital_twin.launch.py -->
<?xml version="1.0"?>
<launch>
    
    <!-- Arguments -->
    <arg name="robot_name" default="humanoid"/>
    <arg name="world_name" default="humanoid_lab"/>
    
    <!-- Gazebo Simulation -->
    <include file="$(find-pkg-share gazebo_ros)/launch/gazebo.launch.py">
        <arg name="world" value="$(find-pkg-share digital_twin)/worlds/$(var world_name).sdf"/>
    </include>
    
    <!-- Robot State Publisher -->
    <node pkg="robot_state_publisher" exec="robot_state_publisher" name="robot_state_publisher">
        <param name="robot_description" value="$(find-pkg-share digital_twin)/urdf/humanoid.urdf"/>
    </node>
    
    <!-- Spawn Humanoid -->
    <node pkg="gazebo_ros" exec="spawn_entity.py" name="spawn_humanoid"
          args="-entity $(var robot_name) -file $(find-pkg-share digital_twin)/urdf/humanoid.urdf"/>
    
    <!-- Sensor Fusion -->
    <node pkg="digital_twin" exec="sensor_fusion_ekf" name="sensor_fusion" output="screen"/>
    
    <!-- Digital Twin Controller -->
    <node pkg="digital_twin" exec="dt_controller" name="dt_controller" output="screen"/>
    
    <!-- Unity Bridge -->
    <node pkg="digital_twin" exec="unity_streamer" name="unity_streamer" output="screen">
        <param name="websocket_port" value="8765"/>
        <param name="stream_rate" value="60.0"/>
    </node>
    
    <!-- RViz Visualization -->
    <node pkg="rviz2" exec="rviz2" name="rviz" 
          args="-d $(find-pkg-share digital_twin)/rviz/digital_twin.rviz"/>
    
</launch>
```

## Hands-on Lab

### Lab 5.1: Build Complete Humanoid Digital Twin

**Objective**: Create a complete digital twin of a humanoid robot with integrated sensors, Gazebo physics, and Unity visualization.

**Prerequisites**:
- All previous chapters completed
- ROS2 Humble, Gazebo, Unity installed
- Python and C# programming skills

**Duration**: 120 minutes

---

#### Step 1: Create Digital Twin Package

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python digital_twin \
  --dependencies rclpy geometry_msgs sensor_msgs std_msgs filterpy

mkdir -p digital_twin/urdf
mkdir -p digital_twin/worlds
mkdir -p digital_twin/launch
mkdir -p digital_twin/digital_twin
```

#### Step 2: Create Humanoid URDF

Create `digital_twin/urdf/humanoid.urdf`:

```xml
<?xml version="1.0"?>
<robot name="humanoid">
  <!-- Combine elements from Chapter 3 biped example -->
  <!-- Add: torso, head, arms, legs, hands -->
  <!-- Add sensors: LiDAR, cameras, IMU, force sensors -->
</robot>
```

#### Step 3: Create Laboratory World

Create `digital_twin/worlds/humanoid_lab.sdf`:

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="humanoid_lab">
    <!-- Physics -->
    <physics type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
      <max_step_size>0.001</max_step_size>
    </physics>
    
    <gravity>0 0 -9.81</gravity>
    
    <!-- Ground -->
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane><normal>0 0 1</normal></plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane><size>100 100</size></plane>
          </geometry>
        </visual>
      </link>
    </model>
    
    <!-- Obstacles -->
    <!-- Add tables, chairs, walls -->
    
  </world>
</sdf>
```

#### Step 4: Implement Launch File

Create `digital_twin/launch/digital_twin_launch.py`:

```python
# Copy from Example 1 above
```

#### Step 5: Implement Synchronizer

Create `digital_twin/digital_twin/synchronizer.py`:

```python
# Copy from Example 2 above
```

#### Step 6: Implement Sensor Fusion

Create `digital_twin/digital_twin/sensor_fusion.py`:

```python
# Copy from Example 3 above
```

#### Step 7: Setup Unity Project

1. Create new Unity HDRP project
2. Import ROS# package
3. Import humanoid FBX model
4. Create scene with lighting and cameras
5. Add RobotController script

#### Step 8: Build and Run

```bash
cd ~/ros2_ws
colcon build --packages-select digital_twin
source install/setup.bash

# Launch complete digital twin
ros2 launch digital_twin digital_twin_launch.py
```

#### Step 9: Test Synchronization

1. In Gazebo: Command robot to walk
2. In Unity: Observe robot mirroring motion
3. In RViz2: Verify sensor data visualization

#### Step 10: Validate Digital Twin

```bash
# Record data from both physical and digital
ros2 bag record \
  /physical/joint_states \
  /digital/joint_states \
  /physical/pose \
  /digital/pose \
  -o digital_twin_validation
```

**Expected Result**:

Humanoid robot walks in Gazebo, Unity visualization mirrors motion in real-time, sensor fusion provides accurate state estimation.

## Summary

### Key Takeaways

1. **Digital Twin**: Complete virtual representation synchronized with physical robot

2. **Model Integration**: URDF → SDF → FBX conversion for cross-platform compatibility

3. **Sensor Fusion**: Combine LiDAR, IMU, cameras using Kalman filters for robust perception

4. **AI Testing**: Digital twins enable safe, scalable AI perception testing

5. **Best Practices**: Model accuracy, real-time sync, validation, documentation

### Key Terms

| Term | Definition |
|------|------------|
| **Digital Twin** | Virtual replica synchronized with physical robot |
| **Sensor Fusion** | Combining multiple sensor measurements |
| **Kalman Filter** | Optimal state estimation algorithm |
| **Sim-to-Real** | Transfer from simulation to physical robot |
| **Synchronization** | Real-time state mirroring |

## Exercises

### Exercise 5.1: Model Conversion

1. Export humanoid URDF to SDF
2. Convert URDF to FBX using Blender
3. **Compare** models in Gazebo and Unity
4. **Document** any discrepancies

### Exercise 5.2: Sensor Fusion Tuning

1. Implement EKF from Example 3
2. Tune process noise (Q) and measurement noise (R)
3. **Plot**: Estimation error vs. noise parameters
4. **Find** optimal parameters

### Exercise 5.3: AI Perception Test

1. Create 10 test scenarios in digital twin
2. Run object detection algorithm
3. **Measure**: Accuracy, precision, recall
4. **Identify** failure modes

### Exercise 5.4: Sim-to-Real Transfer

1. Train controller in digital twin
2. Deploy to physical robot (or high-fidelity sim)
3. **Measure**: Performance degradation
4. **Implement** domain adaptation

### Exercise 5.5: Final Project

**Build a complete digital twin** for your robot project:

- Gazebo physics simulation
- Unity visualization
- Sensor fusion
- Real-time synchronization
- AI perception testing

**Deliverables**:
- Working digital twin system
- 5-minute demo video
- Technical report (1000 words)
- Code repository with documentation

---

**Module 2 Complete!** 🎉

You have learned:
- Robot simulation fundamentals
- Gazebo physics and sensors
- Unity visualization
- Digital twin integration

**Next Module**: [Module 3 — AI Robot Brain (Isaac Sim) →](../module3/chapter1-isaac-sim-intro.md)
