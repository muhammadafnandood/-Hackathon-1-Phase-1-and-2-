---
sidebar_label: '4. Nav2 Navigation'
---

# Chapter 4: Navigation with Nav2

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the Nav2 navigation stack for ROS2
- Configure Nav2 for bipedal humanoid robots
- Implement path planning and obstacle avoidance
- Set up costmaps for environment representation
- Deploy autonomous navigation in simulation

## Concept Explanation

### What is Nav2?

**Nav2** is the navigation framework for ROS2, providing autonomous navigation capabilities:

```
┌─────────────────────────────────────────────────────────────┐
│                    NAV2 NAVIGATION STACK                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  Mission     │  ← High-level goals                      │
│  │  Planning    │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Planner     │───►│  Controller  │───►│  Recovery    │  │
│  │  (Global)    │    │  (Local)     │    │  Behaviors   │  │
│  └──────┬───────┘    └──────┬───────┘    └──────────────┘  │
│         │                   │                                │
│         ▼                   ▼                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Costmaps (2D/3D)                         │   │
│  │  • Static map (obstacles)                            │   │
│  │  • Local map (dynamic obstacles)                     │   │
│  │  • Inflation layer (safety margin)                   │   │
│  └──────────────────────────────────────────────────────┘   │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Map Server  │    │  Amcl        │    │  Odometry    │  │
│  │  (Static)    │    │ (Localization)│   │  (Motion)    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Components:**

1. **Planner**: Generates global path from start to goal
2. **Controller**: Follows path while avoiding obstacles
3. **Recovery**: Handles stuck situations
4. **Costmaps**: Represent environment with obstacle costs
5. **Localization**: Estimates robot position (AMCL, VSLAM)

### Path Planning for Humanoids

**Bipedal robots** have unique navigation challenges:

```
┌─────────────────────────────────────────────────────────────┐
│          HUMANOID NAVIGATION CHALLENGES                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Challenge                  Solution                         │
│  ─────────                  ────────                         │
│                                                              │
│  Balance during motion     • ZMP-based planning             │
│  • Walking is unstable     • Capture point control          │
│                            • Whole-body control             │
│                                                              │
│  Footstep planning         • Discrete foothold selection    │
│  • Can't move freely       • Terrain classification         │
│                            • Step size optimization         │
│                                                              │
│  3D obstacles              • Height-aware costmaps          │
│  • Upper body collision    • Full robot footprint           │
│                            • Multi-layer costmaps           │
│                                                              │
│  Recovery from falls       • Fall detection                 │
│  • Bipedal robots fall   • Get-up behaviors                 │
│                            • Re-localization                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Nav2 for Humanoids:**

- Custom footprint (full body shape)
- Footstep planner (discrete steps)
- 3D costmaps (height awareness)
- Balance-aware controller

### Obstacle Avoidance

**Obstacle avoidance** uses local costmaps and controllers:

```
┌─────────────────────────────────────────────────────────────┐
│              OBSTACLE AVOIDANCE SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Sensor Input:                                               │
│  ─────────────                                               │
│  • LiDAR (2D/3D point cloud)                                │
│  • Depth cameras                                            │
│  • Ultrasonic sensors                                       │
│                                                              │
│  Costmap Layers:                                             │
│  ──────────────                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Static Layer (from map)                             │   │
│  │  ████████░░░░░░░░░░██████                            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Obstacle Layer (from sensors)                       │   │
│  │  ████░░░░▓▓░░░░░░░░░░████                            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Inflation Layer (safety margin)                     │   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Avoidance Strategies:                                       │
│  ────────────────────                                        │
│  • Dynamic Window Approach (DWA)                            │
│  • Timed Elastic Band (TEB)                                 │
│  • Model Predictive Control (MPC)                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Nav2 Costmaps

**Costmaps** represent environment as grid with cost values:

```
┌─────────────────────────────────────────────────────────────┐
│                    COSTMAP LAYERS                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Cost Values:                                                │
│  ────────────                                                │
│  0       = Free space (safe)                                │
│  1-253   = Inflated cost (caution)                          │
│  254     = Obstacle (lethal)                                │
│  255     = Unknown                                          │
│                                                              │
│  Layer Types:                                                │
│  ────────────                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Static Layer                                         │   │
│  │  • From pre-built map                                │   │
│  │  • Doesn't change during navigation                  │   │
│  │  • Walls, permanent obstacles                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Obstacle Layer                                       │   │
│  │  • From sensor data (LiDAR, depth)                   │   │
│  │  • Updates in real-time                              │   │
│  │  • Dynamic obstacles (people, objects)               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Inflation Layer                                      │   │
│  │  • Safety margin around obstacles                    │   │
│  │  • Cost decreases with distance                      │   │
│  │  • Prevents close proximity to obstacles             │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Filter Layer                                         │   │
│  │  • Custom filtering (keepout, speed limits)          │   │
│  │  • Virtual walls                                     │   │
│  │  • Area-specific constraints                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Amazon Warehouse Robots

Amazon uses Nav2-based navigation for **warehouse automation**:

```
┌────────────────────────────────────────────────────────┐
│         AMAZON WAREHOUSE NAVIGATION                     │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Environment:                                           │
│  ───────────                                            │
│  • Dynamic (moving robots, people)                     │
│  • Narrow aisles                                       │
│  • High traffic                                        │
│                                                         │
│  Nav2 Configuration:                                    │
│  ──────────────────                                     │
│  • Global planner: Dijkstra/A*                         │
│  • Local planner: TEB (Timed Elastic Band)             │
│  • Costmaps: Multi-layer with inflation                │
│  • Recovery: Backup and rotate                         │
│                                                         │
│  Performance:                                           │
│  ───────────                                            │
│  • 1000+ robots operating simultaneously               │
│  • Collision-free navigation                           │
│  • Efficient path planning                             │
│  • Real-time obstacle avoidance                        │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete Nav2 System for Humanoids

```
┌─────────────────────────────────────────────────────────────┐
│              NAV2 FOR HUMANOID ROBOTS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  Goal Input  │  ← Nav2 Goal (x, y, theta)               │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Behavior Tree (BT Navigator)             │   │
│  │  • NavigateToPose                                    │   │
│  │  • FollowPath                                        │   │
│  │  • RecoveryBehaviors                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │  Planner     │    │  Controller  │                      │
│  │  (NavFn)     │    │  (DWA/TEB)   │                      │
│  │              │    │              │                      │
│  │  Global Path │    │  Local Plan  │                      │
│  └──────┬───────┘    └──────┬───────┘                      │
│         │                   │                                │
│         └─────────┬─────────┘                                │
│                   │                                          │
│                   ▼                                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Costmap 2D/3D                            │   │
│  │  • Static layer (map)                                │   │
│  │  • Obstacle layer (sensors)                          │   │
│  │  • Inflation layer (safety)                          │   │
│  │  • Footprint layer (robot shape)                     │   │
│  └──────────────────────────────────────────────────────┘   │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Map Server  │    │  Amcl/VSLAM  │    │  Odometry    │  │
│  │  (Occupancy) │    │ (Localization)│   │  (Motion)    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
│  Output: /cmd_vel (velocity commands to robot)              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Nav2 Configuration for Humanoid

```yaml
# nav2_config_humanoid.yaml
# Nav2 configuration optimized for bipedal humanoid robot

amcl:
  ros__parameters:
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_link"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05
    scan_topic: scan

bt_navigator:
  ros__parameters:
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: true
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    plugin_lib_names:
      - nav2_compute_path_to_pose_action_bt_node
      - nav2_compute_path_through_poses_action_bt_node
      - nav2_follow_path_action_bt_node
      - nav2_back_up_action_bt_node
      - nav2_spin_action_bt_node
      - nav2_wait_action_bt_node
      - nav2_clear_costmap_service_bt_node
      - nav2_is_stuck_condition_bt_node
      - nav2_goal_reached_condition_bt_node
      - nav2_goal_updated_condition_bt_node
      - nav2_initial_pose_received_condition_bt_node
      - nav2_reinitialize_global_localization_service_bt_node
      - nav2_rate_controller_bt_node
      - nav2_distance_controller_bt_node
      - nav2_speed_controller_bt_node
      - nav2_truncate_path_action_bt_node
      - nav2_goal_updater_node_bt_node
      - nav2_recovery_node_bt_node
      - nav2_pipeline_sequence_bt_node
      - nav2_round_robin_node_bt_node
      - nav2_transform_available_condition_bt_node
      - nav2_time_expired_condition_bt_node
      - nav2_distance_traveled_condition_bt_node

bt_navigator_navigate_through_poses_rclcpp_node:
  ros__parameters:
    bt_xml_path: "navigate_through_poses_w_recovery.xml"

bt_navigator_navigate_to_pose_rclcpp_node:
  ros__parameters:
    bt_xml_path: "navigate_to_pose_w_recovery.xml"

controller_server:
  ros__parameters:
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3
    progress_checker_plugin: "progress_checker"
    goal_checker_plugins: ["general_goal_checker"]
    controller_plugins: ["FollowPath"]
    
    # Progress checker parameters
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0
    
    # Goal checker parameters
    general_goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: true
    
    # DWA Local Planner parameters
    FollowPath:
      plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
      desired_linear_vel: 0.5
      lookahead_dist: 0.6
      min_lookahead_dist: 0.3
      max_lookahead_dist: 0.9
      lookahead_time: 1.5
      rotate_to_heading_angular_vel: 1.8
      transform_tolerance: 0.1
      use_velocity_scaled_lookahead_dist: false
      min_approach_linear_velocity: 0.05
      approach_velocity_scaling_dist: 0.6
      collision_margin_dist: 0.25
      use_collision_detection: true
      max_allowed_time_to_collision_up_to_carrot: 1.0
      use_regulated_linear_velocity_scaling: true
      use_fixed_curvature_lookahead: false
      curvature_lookahead_dist: 0.3
      use_cost_regulated_linear_velocity_scaling: false
      regulated_linear_scaling_min_radius: 0.9
      regulated_linear_scaling_min_speed: 0.25
      use_rotate_to_heading: true
      allow_reversing: false
      rotate_to_heading_min_angle: 0.785
      max_angular_accel: 3.2
      max_robot_pose_search_dist: 10.0

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      rolling_window: true
      width: 3
      height: 3
      resolution: 0.05
      robot_radius: 0.4  # Humanoid footprint radius
      plugins: ["obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: true
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: true
          marking: true
          data_type: "LaserScan"
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        enabled: true
        inflation_radius: 0.55
        cost_scaling_factor: 3.0
      always_send_full_costmap: true

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      robot_radius: 0.4  # Humanoid footprint radius
      resolution: 0.05
      track_unknown_space: true
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        enabled: true
        map_subscribe_transient_local: true
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: true
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: true
          marking: true
          data_type: "LaserScan"
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        enabled: true
        inflation_radius: 0.55
        cost_scaling_factor: 3.0
      always_send_full_costmap: true

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

recoveries_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    recovery_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_recoveries/Spin"
    backup:
      plugin: "nav2_recoveries/BackUp"
    wait:
      plugin: "nav2_recoveries/Wait"
    global_frame: odom
    robot_base_frame: base_link
    transform_timeout: 0.1
    simulate_ahead_time: 2.0
    max_rotational_vel: 1.0
    min_rotational_vel: 0.4
    rotational_acc_lim: 3.2
```

### Example 2: Nav2 Launch File

```python
#!/usr/bin/env python3
"""
ROS2 Launch file for Nav2 navigation stack.
Module 3 - Chapter 4
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Generate launch description for Nav2."""
    
    # Arguments
    map_yaml_file = DeclareLaunchArgument(
        'map',
        default_value='',
        description='Full path to map yaml file to load'
    )
    
    namespace = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace'
    )
    
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock'
    )
    
    autostart = DeclareLaunchArgument(
        'autostart',
        default_value='true',
        description='Automatically startup the nav2 stack'
    )
    
    # Paths
    nav2_launch_dir = FindPackageShare('nav2_bringup')
    nav2_params = PathJoinSubstitution([
        FindPackageShare('my_robot'),
        'config',
        'nav2_config_humanoid.yaml'
    ])
    
    # Map server (loads occupancy grid)
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': LaunchConfiguration('map'),
            'topic_name': 'map',
            'frame_id': 'map'
        }]
    )
    
    # AMCL localization
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_params],
        remappings=[('scan', '/scan')]
    )
    
    # Lifecycle manager (manages nav2 nodes)
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        parameters=[{
            'autostart': LaunchConfiguration('autostart'),
            'node_names': [
                'map_server',
                'amcl',
                'controller_server',
                'planner_server',
                'recoveries_server',
                'bt_navigator'
            ]
        }]
    )
    
    # Nav2 bringup
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            nav2_launch_dir, '/launch/navigation_launch.py'
        ]),
        launch_arguments={
            'namespace': LaunchConfiguration('namespace'),
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'params_file': nav2_params,
            'autostart': LaunchConfiguration('autostart'),
        }.items()
    )
    
    return LaunchDescription([
        map_yaml_file,
        namespace,
        use_sim_time,
        autostart,
        map_server,
        amcl,
        lifecycle_manager,
        nav2_bringup,
    ])


if __name__ == '__main__':
    generate_launch_description()
```

### Example 3: Nav2 Goal Publisher

```python
#!/usr/bin/env python3
"""
Send navigation goals to Nav2.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped


class Nav2GoalPublisher(Node):
    """Publish navigation goals to Nav2."""
    
    def __init__(self):
        super().__init__('nav2_goal_publisher')
        
        # Action client for Nav2
        self.action_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )
        
        self.get_logger().info('Nav2 Goal Publisher started')
    
    def send_goal(self, x, y, theta, frame_id='map'):
        """
        Send navigation goal.
        
        Args:
            x: X position in meters
            y: Y position in meters
            theta: Orientation in radians
            frame_id: Coordinate frame
        """
        # Wait for action server
        self.get_logger().info('Waiting for action server...')
        self.action_client.wait_for_server()
        
        # Create goal
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = self.create_pose_stamped(x, y, theta, frame_id)
        
        self.get_logger().info(f'Sending goal: x={x}, y={y}, theta={theta}')
        
        # Send goal
        send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        send_goal_future.add_done_callback(self.goal_response_callback)
    
    def create_pose_stamped(self, x, y, theta, frame_id):
        """Create PoseStamped message."""
        pose = PoseStamped()
        pose.header.frame_id = frame_id
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        
        # Convert theta to quaternion
        import math
        pose.pose.orientation.z = math.sin(theta / 2.0)
        pose.pose.orientation.w = math.cos(theta / 2.0)
        
        return pose
    
    def goal_response_callback(self, future):
        """Handle goal response."""
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return
        
        self.get_logger().info('Goal accepted')
        
        # Wait for result
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)
    
    def feedback_callback(self, feedback_msg):
        """Handle feedback."""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Distance remaining: {feedback.distance_remaining:.2f}m'
        )
    
    def result_callback(self, future):
        """Handle result."""
        result = future.result().result
        self.get_logger().info(f'Navigation completed: {result}')


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    publisher = Nav2GoalPublisher()
    
    # Send example goal
    publisher.send_goal(x=2.0, y=3.0, theta=1.57)
    
    # Spin until complete
    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        pass
    finally:
        publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Hands-on Lab

### Lab 4.1: Set Up Nav2 Navigation Pipeline

**Objective**: Configure and run Nav2 for autonomous navigation in simulation.

**Prerequisites**:
- ROS2 Humble with Nav2 installed
- Gazebo or Isaac Sim running
- Map file (YAML format)

**Duration**: 90 minutes

---

#### Step 1: Install Nav2

```bash
# Install Nav2 packages
sudo apt install ros-humble-nav2* ros-humble-slam-toolbox

# Verify installation
ros2 pkg list | grep nav2
```

#### Step 2: Create Map

```bash
# Option A: Use existing map
cp /path/to/map.yaml ~/ros2_ws/maps/
cp /path/to/map.pgm ~/ros2_ws/maps/

# Option B: Create map with SLAM
ros2 launch slam_toolbox online_async_launch.py
# Drive robot manually to build map
ros2 run nav2_map_server map_saver_cli -f my_map
```

#### Step 3: Configure Nav2

Create `nav2_config.yaml`:

```yaml
# Copy configuration from Example 1
```

#### Step 4: Launch Nav2

```bash
# Launch Nav2 with map
ros2 launch my_robot nav2_launch.py \
  map:=/path/to/map.yaml \
  use_sim_time:=true
```

#### Step 5: Send Navigation Goal

```bash
# Option A: Use RViz2
rviz2 -d nav2_config.rviz
# Click "2D Goal Pose" and click on map

# Option B: Use Python script
python3 nav2_goal_publisher.py --goal 2.0 3.0 1.57
```

#### Step 6: Monitor Navigation

```bash
# View robot trajectory
ros2 topic echo /trajectory

# View costmap
ros2 topic echo /local_costmap/costmap_raw

# View planned path
ros2 topic echo /plan
```

**Expected Result**:

Robot autonomously navigates to goal while avoiding obstacles. Path planned and executed successfully.

## Summary

### Key Takeaways

1. **Nav2** is the standard navigation framework for ROS2 robots

2. **Path Planning** generates global path from start to goal

3. **Obstacle Avoidance** uses local costmaps and controllers

4. **Costmaps** represent environment with obstacle costs

5. **Recovery Behaviors** handle stuck situations

### Key Terms

| Term | Definition |
|------|------------|
| **Nav2** | Navigation framework for ROS2 |
| **Costmap** | Grid representation with obstacle costs |
| **Planner** | Generates global path |
| **Controller** | Follows path while avoiding obstacles |
| **AMCL** | Adaptive Monte Carlo Localization |
| **Recovery** | Behaviors to recover from stuck situations |

## Exercises

### Exercise 4.1: Nav2 Parameter Tuning

1. Modify Nav2 parameters:
   - Robot radius
   - Inflation radius
   - Max velocity
2. **Test** navigation performance
3. **Measure** success rate
4. **Optimize** parameters

### Exercise 4.2: Obstacle Avoidance Test

1. Place obstacles in robot path
2. **Run** Nav2 navigation
3. **Observe** avoidance behavior
4. **Measure** minimum distance to obstacles
5. **Adjust** inflation parameters

### Exercise 4.3: Recovery Behavior

1. Intentionally trap robot (narrow corridor)
2. **Trigger** recovery behaviors
3. **Observe** spin, backup, wait
4. **Evaluate** recovery success rate
5. **Modify** recovery parameters

### Exercise 4.4: Multi-Goal Navigation

1. Create sequence of goals
2. **Implement** goal queue
3. **Navigate** through all goals
4. **Measure** total time and distance
5. **Optimize** goal ordering

### Exercise 4.5: Research Question

Research **Nav2 applications**:

- Warehouse robots
- Service robots
- Agricultural robots
- Search and rescue

**Write** a 500-word summary comparing Nav2 configurations across 2 domains.

---

**Next Chapter**: [Chapter 5 — Reinforcement Learning for Robots →](./chapter5-robot-reinforcement-learning.md)
