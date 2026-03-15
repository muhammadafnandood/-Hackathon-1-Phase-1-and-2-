---
sidebar_label: '3. Visual SLAM'
---

# Chapter 3: Visual SLAM (VSLAM)

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand Visual SLAM concepts and algorithms
- Configure Isaac ROS Visual SLAM for real-time localization
- Implement sensor fusion for robust state estimation
- Build 3D maps using visual data
- Deploy VSLAM on simulated and physical robots

## Concept Explanation

### What is Visual SLAM?

**Visual SLAM** (Simultaneous Localization and Mapping) estimates robot position and builds environment map using cameras:

```
┌─────────────────────────────────────────────────────────────┐
│                    VISUAL SLAM SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Input: Camera Images + IMU Data                            │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              VSLAM Pipeline                           │   │
│  │                                                       │   │
│  │  1. Feature Detection  →  Corners, edges, blobs      │   │
│  │  2. Feature Matching   →  Track features across frames│   │
│  │  3. Pose Estimation  →  Calculate camera motion      │   │
│  │  4. Map Building     →  Create 3D point cloud        │   │
│  │  5. Loop Closure     →  Detect revisited places      │   │
│  │  6. Optimization     →  Bundle adjustment            │   │
│  └──────────────────────────────────────────────────────┘   │
│         ↓                                                    │
│  Output: Robot Trajectory + 3D Map                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Applications:**

- Autonomous navigation (indoor/outdoor)
- Augmented reality
- 3D reconstruction
- Robot manipulation

### VSLAM Algorithms

**Common VSLAM approaches:**

```
┌─────────────────────────────────────────────────────────────┐
│                  VSLAM ALGORITHMS                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Feature-Based Methods                                       │
│  ────────────────────                                        │
│  • ORB-SLAM3 (State-of-the-art)                            │
│  • PTAM (Parallel Tracking and Mapping)                    │
│  • SVO (Semi-direct Visual Odometry)                       │
│                                                              │
│  Direct Methods                                              │
│  ──────────────                                              │
│  • DSO (Direct Sparse Odometry)                            │
│  • LSD-SLAM (Large-scale Direct SLAM)                      │
│  • DVO (Dense Visual Odometry)                             │
│                                                              │
│  Visual-Inertial Methods                                     │
│  ──────────────────────                                      │
│  • VINS-Mono (Monocular Visual-Inertial)                   │
│  • OKVIS (Open Keyframe-based Visual-Inertial)             │
│  • ROVIO (Robust Visual-Inertial Odometry)                 │
│                                                              │
│  Deep Learning Methods                                       │
│  ─────────────────────                                       │
│  • DeepVO (End-to-end Visual Odometry)                     │
│  • DROID-SLAM (Dense SLAM)                                 │
│  • Neural RGB-D SLAM                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Isaac ROS Visual SLAM

**Isaac ROS Visual SLAM** provides GPU-accelerated VSLAM:

```
┌─────────────────────────────────────────────────────────────┐
│              ISAAC ROS VISUAL SLAM FEATURES                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Supported Inputs:                                           │
│  ───────────────────                                         │
│  • Stereo cameras (rectified)                               │
│  • RGB-D cameras (depth + color)                            │
│  • Monocular + IMU                                          │
│  • Multi-camera setups                                      │
│                                                              │
│  Outputs:                                                    │
│  ───────                                                     │
│  • Camera pose (position + orientation)                     │
│  • Sparse 3D point cloud (map)                              │
│  • Loop closure detections                                  │
│  • Trajectory history                                       │
│                                                              │
│  Performance:                                                │
│  ───────────                                                 │
│  • 60+ FPS on NVIDIA GPU                                    │
│  • Sub-meter accuracy                                       │
│  • Real-time loop closure                                   │
│  • Robust to lighting changes                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Sensor Fusion

**Sensor fusion** combines multiple sensors for robust estimation:

```
┌─────────────────────────────────────────────────────────────┐
│                    SENSOR FUSION                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Sensors:                                                    │
│  ─────────                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Camera  │  │   IMU    │  │  LiDAR   │  │  Wheel   │    │
│  │  (Vision)│  │ (Motion) │  │ (Range)  │  │  Encoder │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│       └─────────────┴─────────────┴─────────────┘           │
│                         ↓                                    │
│              ┌────────────────────┐                         │
│              │  Sensor Fusion     │                         │
│              │  (Kalman Filter)   │                         │
│              └─────────┬──────────┘                         │
│                        ↓                                     │
│              ┌────────────────────┐                         │
│              │  Robot State       │                         │
│              │  (Pose + Velocity) │                         │
│              └────────────────────┘                         │
│                                                              │
│  Benefits:                                                   │
│  ─────────                                                   │
│  • Robust to individual sensor failures                     │
│  • Higher accuracy than single sensor                       │
│  • Handles different motion types                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Kalman Filter for Sensor Fusion:**

```
Prediction Step:
  x_pred = F * x + B * u  (Predict state)
  P_pred = F * P * F' + Q  (Predict uncertainty)

Update Step:
  y = z - H * x_pred  (Innovation)
  S = H * P_pred * H' + R  (Innovation covariance)
  K = P_pred * H' * S^-1  (Kalman gain)
  
  x = x_pred + K * y  (Update state)
  P = (I - K * H) * P_pred  (Update uncertainty)

Where:
  x = State (position, velocity, orientation)
  P = State covariance
  F = State transition matrix
  Q = Process noise
  R = Measurement noise
  K = Kalman gain
```

## Real Robotics Example

### NASA Mars Rover VSLAM

NASA uses VSLAM for **Mars rover navigation**:

```
┌────────────────────────────────────────────────────────┐
│           MARS ROVER VISUAL SLAM SYSTEM                 │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Challenge:                                             │
│  ─────────                                              │
│  • No GPS on Mars                                      │
│  • Communication delay (20 min)                        │
│  • Rough terrain                                       │
│  • Extreme lighting                                    │
│                                                         │
│  Solution:                                              │
│  ────────                                               │
│  • Stereo cameras for visual odometry                  │
│  • IMU for motion constraints                          │
│  • Wheel encoders for dead reckoning                   │
│  • Orbital imagery for global localization             │
│                                                         │
│  Performance:                                           │
│  ───────────                                            │
│  • Position error: < 5% of distance traveled           │
│  • Autonomous navigation: 100+ meters/day              │
│  • Obstacle avoidance: Real-time                       │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete VSLAM System with Isaac ROS

```
┌─────────────────────────────────────────────────────────────┐
│              ISAAC ROS VSLAM ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Stereo      │    │  Isaac ROS   │    │  Pose        │  │
│  │  Cameras     │───►│  Visual SLAM │───►│  Estimation  │  │
│  │  (Left/Right)│    │  Node        │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                            │                                 │
│                            │                                 │
│  ┌──────────────┐    ┌─────▼──────┐    ┌──────────────┐    │
│  │  IMU         │    │  Sensor    │    │  3D Map      │    │
│  │  (Optional)  │───►│  Fusion    │───►│  (Point      │    │
│  └──────────────┘    │  (EKF)     │    │   Cloud)     │    │
│                      └────────────┘    └──────────────┘    │
│                                                              │
│  ROS2 Topics:                                                │
│  ────────────                                                │
│  Input:                                                      │
│  • /stereo/left/image_raw                                  │
│  • /stereo/right/image_raw                                 │
│  • /imu/data (optional)                                    │
│                                                              │
│  Output:                                                     │
│  • /visual_slam/pose                                       │
│  • /visual_slam/map                                        │
│  • /visual_slam/trajectory                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Isaac ROS Visual SLAM Launch File

```python
#!/usr/bin/env python3
"""
ROS2 Launch file for Isaac ROS Visual SLAM.
Module 3 - Chapter 3
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Generate launch description for Isaac ROS Visual SLAM."""
    
    # Arguments
    camera_frame = DeclareLaunchArgument(
        'camera_frame',
        default_value='stereo_camera',
        description='Camera frame ID'
    )
    
    use_imu = DeclareLaunchArgument(
        'use_imu',
        default_value='false',
        description='Use IMU for visual-inertial SLAM'
    )
    
    # Isaac ROS Visual SLAM Node
    visual_slam_node = Node(
        package='isaac_ros_visual_slam',
        executable='isaac_ros_visual_slam_node',
        name='visual_slam',
        output='screen',
        parameters=[{
            'use_imu': LaunchConfiguration('use_imu'),
            'camera_frame': LaunchConfiguration('camera_frame'),
            'enable_loop_closure': True,
            'enable_relocalization': True,
            'enable_global_bundle_adjustment': True,
            'map_frame': 'map',
            'odom_frame': 'odom',
            'base_frame': 'base_link',
        }],
        remappings=[
            ('/stereo/left/image_raw', '/camera/left/image_raw'),
            ('/stereo/right/image_raw', '/camera/right/image_raw'),
            ('/imu/data', '/imu/data'),
        ]
    )
    
    # Visual SLAM to TF broadcaster
    tf_broadcaster = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='map_to_odom_broadcaster',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )
    
    return LaunchDescription([
        camera_frame,
        use_imu,
        visual_slam_node,
        tf_broadcaster,
    ])


if __name__ == '__main__':
    generate_launch_description()
```

### Example 2: VSLAM Python Node

```python
#!/usr/bin/env python3
"""
Visual SLAM integration node for robot navigation.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry, Path
from sensor_msgs.msg import Image, Imu
from tf2_ros import TransformBroadcaster
import numpy as np


class VSLAMIntegrator(Node):
    """Integrate VSLAM output for robot navigation."""
    
    def __init__(self):
        super().__init__('vslam_integrator')
        
        # Subscribers
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/visual_slam/pose',
            self.pose_callback,
            10
        )
        
        self.map_sub = self.create_subscription(
            Image,  # Point cloud as image
            '/visual_slam/map',
            self.map_callback,
            10
        )
        
        # Publishers
        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )
        
        self.path_pub = self.create_publisher(
            Path,
            '/trajectory',
            10
        )
        
        # TF Broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # State
        self.current_pose = None
        self.trajectory = []
        
        self.get_logger().info('VSLAM Integrator started')
    
    def pose_callback(self, msg: PoseStamped):
        """Process pose from VSLAM."""
        self.current_pose = msg
        
        # Publish odometry
        odom_msg = Odometry()
        odom_msg.header = msg.header
        odom_msg.child_frame_id = 'base_link'
        odom_msg.pose.pose = msg.pose
        
        # Set covariance (simplified)
        odom_msg.pose.covariance = [
            0.01, 0, 0, 0, 0, 0,
            0, 0.01, 0, 0, 0, 0,
            0, 0, 0.01, 0, 0, 0,
            0, 0, 0, 0.01, 0, 0,
            0, 0, 0, 0, 0.01, 0,
            0, 0, 0, 0, 0, 0.01
        ]
        
        self.odom_pub.publish(odom_msg)
        
        # Update trajectory
        self.trajectory.append(msg)
        self.publish_trajectory()
        
        # Broadcast TF
        self.broadcast_tf(msg)
        
        self.get_logger().debug(
            f"Pose: x={msg.pose.position.x:.2f}, "
            f"y={msg.pose.position.y:.2f}, "
            f"z={msg.pose.position.z:.2f}"
        )
    
    def map_callback(self, msg: Image):
        """Process map from VSLAM."""
        # Convert to point cloud (implementation depends on format)
        self.get_logger().debug('Received map update')
    
    def publish_trajectory(self):
        """Publish robot trajectory."""
        path_msg = Path()
        path_msg.header.stamp = self.get_clock().now().to_msg()
        path_msg.header.frame_id = 'map'
        path_msg.poses = self.trajectory
        self.path_pub.publish(path_msg)
    
    def broadcast_tf(self, pose_msg: PoseStamped):
        """Broadcast transform from map to base_link."""
        from geometry_msgs.msg import TransformStamped
        
        t = TransformStamped()
        t.header.stamp = pose_msg.header.stamp
        t.header.frame_id = 'map'
        t.child_frame_id = 'base_link'
        
        t.transform.translation.x = pose_msg.pose.position.x
        t.transform.translation.y = pose_msg.pose.position.y
        t.transform.translation.z = pose_msg.pose.position.z
        t.transform.rotation = pose_msg.pose.orientation
        
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    integrator = VSLAMIntegrator()
    
    try:
        rclpy.spin(integrator)
    except KeyboardInterrupt:
        pass
    finally:
        integrator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 3: Sensor Fusion with EKF

```python
#!/usr/bin/env python3
"""
Extended Kalman Filter for Visual-Inertial Sensor Fusion.
"""

import numpy as np
from filterpy.kalman import ExtendedKalmanFilter as EKF


class VisualInertialFusion:
    """Fuse visual odometry with IMU using EKF."""
    
    def __init__(self):
        # State: [x, y, z, vx, vy, vz, roll, pitch, yaw]
        self.ekf = EKF(dim_x=9, dim_z=6)
        
        # Initial state
        self.ekf.x = np.zeros(9)
        
        # State transition matrix (constant velocity + IMU)
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
        
        # Measurement matrix (visual odometry: position + yaw)
        self.ekf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0],  # x
            [0, 1, 0, 0, 0, 0, 0, 0, 0],  # y
            [0, 0, 1, 0, 0, 0, 0, 0, 0],  # z
            [0, 0, 0, 0, 0, 0, 0, 0, 1],  # yaw
        ])
        
        # Process noise (from IMU)
        self.ekf.Q = np.diag([0.1, 0.1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        
        # Measurement noise (from visual odometry)
        self.ekf.R = np.diag([0.5, 0.5, 0.5, 0.01])
        
        # Initial covariance
        self.ekf.P = np.eye(9) * 1.0
    
    def predict(self, imu_data, dt=0.01):
        """
        Predict state using IMU data.
        
        imu_data: [ax, ay, az, wx, wy, wz]
        """
        # Update state transition with IMU acceleration
        ax, ay, az = imu_data[:3]
        
        self.ekf.F[0, 3] = dt  # Update dt
        self.ekf.F[1, 4] = dt
        self.ekf.F[2, 5] = dt
        
        # Apply acceleration to velocity
        self.ekf.x[3] += ax * dt  # vx
        self.ekf.x[4] += ay * dt  # vy
        self.ekf.x[5] += az * dt  # vz
        
        self.ekf.predict()
    
    def update(self, visual_odometry):
        """
        Update state with visual odometry.
        
        visual_odometry: [x, y, z, yaw]
        """
        self.ekf.update(np.array(visual_odometry))
    
    def get_state(self):
        """Get current state estimate."""
        return self.ekf.x.copy()
    
    def get_covariance(self):
        """Get state covariance."""
        return self.ekf.P.copy()


# Example usage
def test_sensor_fusion():
    """Test visual-inertial fusion with simulated data."""
    fusion = VisualInertialFusion()
    
    # Simulate data
    for i in range(100):
        # IMU data (noisy)
        imu = [0.1 + np.random.randn()*0.01,  # ax
               0.0 + np.random.randn()*0.01,  # ay
               -9.81 + np.random.randn()*0.1, # az
               0.01 + np.random.randn()*0.001, # wx
               0.0 + np.random.randn()*0.001,  # wy
               0.0 + np.random.randn()*0.001]  # wz
        
        # Visual odometry (noisy)
        true_x = i * 0.01
        true_y = np.sin(i * 0.05) * 0.5
        visual = [true_x + np.random.randn()*0.1,
                  true_y + np.random.randn()*0.1,
                  0.0 + np.random.randn()*0.05,
                  0.0 + np.random.randn()*0.01]
        
        # Fuse
        fusion.predict(imu)
        fusion.update(visual)
        
        # Get estimate
        state = fusion.get_state()
        
        print(f"Step {i}: Estimated=({state[0]:.3f}, {state[1]:.3f}), "
              f"True=({true_x:.3f}, {true_y:.3f})")


if __name__ == '__main__':
    test_sensor_fusion()
```

## Hands-on Lab

### Lab 3.1: Implement VSLAM on Simulated Robot

**Objective**: Configure and run Isaac ROS Visual SLAM on a simulated robot in Isaac Sim.

**Prerequisites**:
- Isaac Sim installed
- ROS2 Humble with Isaac ROS packages
- Python 3.8+

**Duration**: 90 minutes

---

#### Step 1: Install Isaac ROS Visual SLAM

```bash
# Install Isaac ROS packages
cd ~/ros2_ws/src
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git

# Install dependencies
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -y

# Build
colcon build --symlink-install
source install/setup.bash
```

#### Step 2: Configure Stereo Camera

Create `camera_config.yaml`:

```yaml
/stereo_camera:
  ros__parameters:
    left_camera:
      topic: /camera/left/image_raw
      frame_id: stereo_left
    right_camera:
      topic: /camera/right/image_raw
      frame_id: stereo_right
    baseline: 0.12  # meters
    focal_length: 0.024  # meters
```

#### Step 3: Launch VSLAM

```bash
# Launch Isaac ROS Visual SLAM
ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam.launch.py \
  use_imu:=false \
  camera_frame:=stereo_camera
```

#### Step 4: Run Simulation

```bash
# In another terminal, launch Isaac Sim with stereo camera
python3 isaac_sim_vslam.py
```

#### Step 5: Visualize Output

```bash
# View trajectory
rviz2 -d vslam_config.rviz

# Echo pose
ros2 topic echo /visual_slam/pose

# View map
ros2 topic echo /visual_slam/map
```

#### Step 6: Record Data

```bash
# Record trajectory
ros2 bag record /visual_slam/pose /visual_slam/trajectory -o vslam_data
```

**Expected Result**:

Robot localizes itself in real-time, builds 3D map, trajectory published to ROS2 topics.

## Summary

### Key Takeaways

1. **Visual SLAM** estimates robot position and builds map using cameras

2. **Isaac ROS Visual SLAM** provides GPU-accelerated, real-time VSLAM

3. **Sensor Fusion** combines visual odometry with IMU for robust estimation

4. **Kalman Filter** is standard algorithm for multi-sensor fusion

5. **Loop Closure** detects revisited places to correct drift

### Key Terms

| Term | Definition |
|------|------------|
| **VSLAM** | Visual Simultaneous Localization and Mapping |
| **Visual Odometry** | Position estimation from camera images |
| **Loop Closure** | Detection of previously visited locations |
| **Bundle Adjustment** | Optimization of 3D structure and camera poses |
| **EKF** | Extended Kalman Filter for nonlinear systems |

## Exercises

### Exercise 3.1: VSLAM Accuracy Test

1. Run VSLAM in Isaac Sim
2. Move robot along known path
3. **Compare** estimated vs. true trajectory
4. **Calculate** position error
5. **Report** accuracy metrics

### Exercise 3.2: IMU Fusion Study

1. Run VSLAM with IMU disabled
2. Run VSLAM with IMU enabled
3. **Compare** accuracy and robustness
4. **Analyze** fast motion scenarios
5. **Document** findings

### Exercise 3.3: Loop Closure Detection

1. Create environment with loop
2. Run VSLAM and traverse loop multiple times
3. **Visualize** loop closure detections
4. **Measure** drift correction
5. **Analyze** map quality improvement

### Exercise 3.4: Lighting Robustness

1. Test VSLAM under different lighting:
   - Bright light
   - Dim light
   - Changing light
2. **Measure** tracking performance
3. **Identify** failure modes
4. **Propose** improvements

### Exercise 3.5: Research Assignment

Research **VSLAM applications**:

- Autonomous vehicles
- Drones
- AR/VR
- Planetary rovers

**Write** a 500-word summary with examples from 2 different domains.

---

**Next Chapter**: [Chapter 4 — Navigation with Nav2 →](./chapter4-nav2-navigation.md)
