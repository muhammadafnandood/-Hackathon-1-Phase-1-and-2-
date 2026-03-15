---
sidebar_label: '4. Unity Robot Visualization'
---

# Chapter 4: Unity Robot Visualization

## Learning Objectives

By the end of this chapter, you will be able to:

- Set up Unity for robotics visualization with ROS#
- Implement high-fidelity rendering for robot models
- Configure camera systems for human-robot interaction
- Build immersive 3D scenes for robot simulation
- Integrate Gazebo physics with Unity visualization
- Create Python scripts for data streaming to Unity

## Concept Explanation

### Why Unity for Robotics?

While Gazebo excels at physics simulation, **Unity** provides superior visual rendering:

```
┌─────────────────────────────────────────────────────────────┐
│                  GAZEBO vs UNITY                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GAZEBO                      UNITY                           │
│  ───────                     ───────                         │
│  • Physics-first             • Rendering-first              │
│  • Accurate dynamics         • Photorealistic graphics      │
│  • ROS native                • ROS# bridge required         │
│  • Basic materials           • HDRP/URP rendering           │
│  • Fast simulation           • Higher quality, slower       │
│  • Research standard         • Industry adoption            │
│                                                              │
│  BEST PRACTICE: Use both!                                    │
│  ────────────────                                            │
│  • Gazebo for physics and sensors                            │
│  • Unity for visualization and HRI                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Unity Rendering Pipelines

Unity offers three rendering pipelines:

**1. Built-in Render Pipeline:**
- Legacy pipeline (Unity 2019 and earlier)
- Compatible with most assets
- Limited customization

**2. Universal Render Pipeline (URP):**
- Optimized for performance
- Cross-platform support
- Good for VR/AR applications

**3. High Definition Render Pipeline (HDRP):**
- Photorealistic quality
- Ray tracing support
- Best for high-end visualization

```
┌─────────────────────────────────────────────────────────────┐
│              UNITY RENDERING COMPARISON                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Built-in          URP               HDRP                   │
│  ──────────        ───               ────                   │
│  [Basic]    →     [Good]     →      [Photorealistic]        │
│                                                              │
│  • Standard          • Mobile/VR       • Ray tracing        │
│    lighting          • Fast            • Global             │
│  • No ray tracing    • Customizable      illumination       │
│  • Legacy            • Good quality    • 8K textures        │
│                                                              │
│  Recommendation: Use HDRP for robotics visualization         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### ROS# Integration

**ROS#** (ROS Sharp) is a Unity package for ROS communication:

```
┌─────────────────────────────────────────────────────────────┐
│                    ROS# ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Unity Scene              ROS# Bridge         ROS2 Network   │
│  ───────────              ───────────         ────────────   │
│                                                              │
│  ┌──────────┐           ┌──────────┐        ┌──────────┐   │
│  │  Robot   │◄─────────►│  ROS#    │◄──────►│  ROS2    │   │
│  │  Visual  │  Unity    │  Bridge  │ ROS2   │  Nodes   │   │
│  └──────────┘  Internal └──────────┘ Topics └──────────┘   │
│                                                              │
│  Supported Message Types:                                    │
│  • std_msgs (String, Int32, Float64, etc.)                  │
│  • geometry_msgs (Twist, Pose, Point)                       │
│  • sensor_msgs (Image, LaserScan, Imu)                      │
│  • nav_msgs (Odometry, Path)                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Camera Systems for HRI

**Human-Robot Interaction (HRI)** requires realistic camera systems:

**Camera Types:**

| Type | Purpose | Configuration |
|------|---------|---------------|
| **First-Person** | Robot's view | Mounted on robot head |
| **Third-Person** | External observation | Follows robot |
| **Orbital** | 360° inspection | Rotates around robot |
| **Fixed** | Surveillance | Stationary positions |

**Camera Properties:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMERA PROPERTIES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Field of View (FOV)       Depth of Field                   │
│  ───────────────────       ────────────────                 │
│  • Wide (90-120°): VR      • Focus distance                 │
│  • Normal (60-75°): Human  • Aperture (f-stop)             │
│  • Narrow (30-45°): Zoom   • Blur effect                    │
│                                                              │
│  Resolution                  Frame Rate                      │
│  ──────────                  ───────────                     │
│  • 1080p (1920×1080)        • 30 FPS (standard)             │
│  • 4K (3840×2160)           • 60 FPS (smooth)               │
│  • 8K (7680×4320)           • 90+ FPS (VR)                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Scene Building

**Building immersive scenes** requires attention to detail:

**Scene Elements:**

```
┌─────────────────────────────────────────────────────────────┐
│                    SCENE ELEMENTS                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Environment           2. Lighting                        │
│     ────────────             ─────────                       │
│     • Floor/ground           • Directional (sun)            │
│     • Walls                  • Point lights                 │
│     • Ceiling                • Spotlights                   │
│     • Props (furniture)      • Ambient lighting             │
│                                                              │
│  3. Materials               4. Post-Processing               │
│     ──────────                ────────────────               │
│     • PBR materials          • Bloom                        │
│     • Textures (4K)          • Color grading                │
│     • Normal maps            • Ambient occlusion            │
│     • Reflection probes      • Depth of field               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Gazebo-Unity Integration

**Integration approaches:**

```
┌─────────────────────────────────────────────────────────────┐
│              GAZEBO-UNITY INTEGRATION METHODS                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Method 1: Topic Bridge                                      │
│  ────────────────────                                        │
│  Gazebo → ROS2 Topics → ROS# → Unity                        │
│  • Simple to implement                                       │
│  • Real-time synchronization                                 │
│  • Network overhead                                          │
│                                                              │
│  Method 2: Shared Memory                                     │
│  ───────────────────                                         │
│  Gazebo ↔ Shared Memory ↔ Unity                             │
│  • Low latency                                               │
│  • Same machine only                                         │
│  • Complex setup                                             │
│                                                              │
│  Method 3: Unity as Sensor                                   │
│  ────────────────────────                                    │
│  Gazebo (physics) → Unity (rendering) → Back to Gazebo      │
│  • Best of both worlds                                       │
│  • Requires tight coupling                                   │
│  • Research projects (e.g., Unity Robotics Hub)             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Tesla Optimus Visualization

Tesla uses Unity-like rendering for **Optimus humanoid** visualization:

```
┌────────────────────────────────────────────────────────┐
│          TESLA OPTIMUS VISUALIZATION PIPELINE           │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Simulation → Rendering → Neural Network Training      │
│      ↓           ↓              ↓                       │
│  Physics    Photorealistic   Vision-based             │
│  Engine     Visualization    Perception               │
│                                                         │
│  Key Features:                                          │
│  • HDRP rendering for realistic lighting               │
│  • Synthetic data generation for AI training           │
│  • Digital twin mirroring physical robot               │
│  • Real-time teleoperation interface                   │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete Visualization Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│              UNITY VISUALIZATION PIPELINE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ROS2 Topics    →    ROS# Bridge    →    Unity Components   │
│  ────────────        ────────────        ──────────────────  │
│                                                              │
│  /cmd_vel           RosSubscriber        RobotController    │
│  (Twist)            (C# Script)          (Motor Control)    │
│                                                              │
│  /joint_states      RosSubscriber        Animator           │
│  (JointState)       (C# Script)          (Rig Control)      │
│                                                              │
│  /camera/image      RosSubscriber        RenderTexture      │
│  (Image)            (C# Script)          (Display)          │
│                                                              │
│  /scan              RosSubscriber        LineRenderer       │
│  (LaserScan)        (C# Script)          (LiDAR Viz)        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Unity C# ROS# Subscriber

```csharp
// RobotController.cs
using UnityEngine;
using ROSBridgeLib;
using ROSBridgeLib.std_msgs;
using ROSBridgeLib.geometry_msgs;

public class RobotController : ROSBridgeSocket
{
    [Header("Robot Settings")]
    public GameObject robotModel;
    public float maxSpeed = 2.0f;
    public float maxRotation = 180.0f;
    
    [Header("Debug")]
    public bool showDebugInfo = true;
    
    private Vector3 linearVelocity = Vector3.zero;
    private float angularVelocity = 0.0f;
    
    void Start()
    {
        // Connect to ROS bridge
        Connect("ws://localhost:9090");
        
        // Subscribe to velocity commands
        Subscribe<TwistMsg>("/cmd_vel");
        
        Debug.Log("Robot Controller started");
    }
    
    void OnMessage(ROSMessage msg)
    {
        if (msg is TwistMsg twist)
        {
            linearVelocity = new Vector3(
                twist.Linear.X,
                twist.Linear.Y,
                twist.Linear.Z
            );
            
            angularVelocity = twist.Angular.Z;
            
            if (showDebugInfo)
            {
                Debug.Log($"Received cmd_vel: linear={linearVelocity}, angular={angularVelocity}");
            }
        }
    }
    
    void Update()
    {
        // Apply velocity to robot
        if (robotModel != null)
        {
            // Linear movement
            Vector3 movement = linearVelocity * maxSpeed * Time.deltaTime;
            robotModel.transform.Translate(movement);
            
            // Angular rotation
            float rotation = angularVelocity * maxRotation * Time.deltaTime;
            robotModel.transform.Rotate(0, rotation, 0);
        }
    }
    
    void OnGUI()
    {
        if (showDebugInfo)
        {
            GUILayout.BeginArea(new Rect(10, 10, 300, 100));
            GUILayout.Label($"Connected: {IsConnected()}");
            GUILayout.Label($"Linear: {linearVelocity}");
            GUILayout.Label($"Angular: {angularVelocity}");
            GUILayout.EndArea();
        }
    }
}
```

### Example 2: Unity Camera Controller

```csharp
// CameraController.cs
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [Header("Target")]
    public Transform target;  // Robot to follow
    
    [Header("Camera Settings")]
    public float followDistance = 5.0f;
    public float followHeight = 2.0f;
    public float rotationSpeed = 5.0f;
    public float zoomSpeed = 2.0f;
    
    [Header("Limits")]
    public float minDistance = 2.0f;
    public float maxDistance = 10.0f;
    
    private float currentDistance;
    private float currentAngle;
    
    void Start()
    {
        currentDistance = followDistance;
        currentAngle = 0.0f;
    }
    
    void LateUpdate()
    {
        if (target == null) return;
        
        // Handle mouse input for rotation
        if (Input.GetMouseButton(1))  // Right mouse button
        {
            float mouseX = Input.GetAxis("Mouse X");
            currentAngle += mouseX * rotationSpeed;
        }
        
        // Handle scroll for zoom
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        currentDistance -= scroll * zoomSpeed;
        currentDistance = Mathf.Clamp(currentDistance, minDistance, maxDistance);
        
        // Calculate camera position
        float angleRad = currentAngle * Mathf.Deg2Rad;
        Vector3 offset = new Vector3(
            Mathf.Sin(angleRad) * currentDistance,
            followHeight,
            -Mathf.Cos(angleRad) * currentDistance
        );
        
        // Position camera
        transform.position = target.position + offset;
        transform.LookAt(target.position);
    }
    
    void OnGUI()
    {
        // Camera control instructions
        GUILayout.BeginArea(new Rect(Screen.width - 200, 10, 190, 80));
        GUILayout.Label("Camera Controls:");
        GUILayout.Label("- Right drag: Rotate");
        GUILayout.Label("- Scroll: Zoom");
        GUILayout.EndArea();
    }
}
```

### Example 3: Python Data Streaming to Unity

```python
#!/usr/bin/env python3
"""
Stream robot data from ROS2 to Unity via WebSocket.
"""
import asyncio
import websockets
import json
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu, Image
from geometry_msgs.msg import PoseStamped
import numpy as np


class UnityStreamer(Node):
    """Stream robot data to Unity visualization."""
    
    def __init__(self):
        super().__init__('unity_streamer')
        
        # Subscribers
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )
        
        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )
        
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/robot_pose',
            self.pose_callback,
            10
        )
        
        # WebSocket clients
        self.unity_clients = set()
        
        # Latest data
        self.latest_data = {
            'joints': {},
            'imu': {},
            'pose': {}
        }
        
        self.get_logger().info('Unity Streamer started')
    
    def joint_callback(self, msg: JointState):
        """Process joint states."""
        self.latest_data['joints'] = {
            name: float(position)
            for name, position in zip(msg.name, msg.position)
        }
        
        self.broadcast_data()
    
    def imu_callback(self, msg: Imu):
        """Process IMU data."""
        self.latest_data['imu'] = {
            'orientation': [
                msg.orientation.x,
                msg.orientation.y,
                msg.orientation.z,
                msg.orientation.w
            ],
            'angular_velocity': [
                msg.angular_velocity.x,
                msg.angular_velocity.y,
                msg.angular_velocity.z
            ],
            'linear_acceleration': [
                msg.linear_acceleration.x,
                msg.linear_acceleration.y,
                msg.linear_acceleration.z
            ]
        }
        
        self.broadcast_data()
    
    def pose_callback(self, msg: PoseStamped):
        """Process robot pose."""
        self.latest_data['pose'] = {
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
        
        self.broadcast_data()
    
    def broadcast_data(self):
        """Broadcast latest data to all Unity clients."""
        if not self.unity_clients:
            return
        
        message = json.dumps(self.latest_data)
        
        # Send to all connected clients
        for client in list(self.unity_clients):
            asyncio.create_task(self.send_to_client(client, message))
    
    async def send_to_client(self, websocket, message):
        """Send message to WebSocket client."""
        try:
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            self.unity_clients.discard(websocket)
            self.get_logger().info('Unity client disconnected')
    
    async def handle_client(self, websocket, path):
        """Handle WebSocket client connection."""
        self.unity_clients.add(websocket)
        self.get_logger().info(f'Unity client connected: {websocket.remote_address}')
        
        try:
            async for message in websocket:
                # Handle messages from Unity (if any)
                self.get_logger().debug(f'Received from Unity: {message}')
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.unity_clients.discard(websocket)
    
    async def run_server(self):
        """Run WebSocket server."""
        server = await websockets.serve(self.handle_client, "localhost", 8765)
        self.get_logger().info('WebSocket server started on ws://localhost:8765')
        await server.wait_closed()


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    streamer = UnityStreamer()
    
    # Run ROS2 spinner and WebSocket server concurrently
    import threading
    
    def spin_ros():
        rclpy.spin(streamer)
    
    ros_thread = threading.Thread(target=spin_ros)
    ros_thread.start()
    
    # Run WebSocket server
    try:
        asyncio.run(streamer.run_server())
    except KeyboardInterrupt:
        pass
    finally:
        streamer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 4: Unity LiDAR Visualization

```csharp
// LidarVisualizer.cs
using UnityEngine;
using System.Collections.Generic;
using ROSBridgeLib;
using ROSBridgeLib.sensor_msgs;

public class LidarVisualizer : ROSBridgeSocket
{
    [Header("Visualization Settings")]
    public GameObject pointPrefab;
    public Material pointMaterial;
    public float pointSize = 0.05f;
    public Color closeColor = Color.red;
    public Color farColor = Color.green;
    
    [Header("LiDAR Settings")]
    public float minRange = 0.1f;
    public float maxRange = 10.0f;
    
    private List<GameObject> points = new List<GameObject>();
    private Transform lidarTransform;
    
    void Start()
    {
        Connect("ws://localhost:9090");
        Subscribe<LaserScanMsg>("/scan");
        
        // Create parent object for points
        GameObject parent = new GameObject("LiDAR Points");
        lidarTransform = parent.transform;
    }
    
    void OnMessage(ROSMessage msg)
    {
        if (msg is LaserScanMsg scan)
        {
            UpdatePoints(scan);
        }
    }
    
    void UpdatePoints(LaserScanMsg scan)
    {
        // Clear old points
        foreach (var point in points)
        {
            Destroy(point);
        }
        points.Clear();
        
        float[] ranges = scan.Ranges;
        float angleMin = scan.AngleMin;
        float angleIncrement = scan.AngleIncrement;
        
        // Create new points
        for (int i = 0; i < ranges.Length; i++)
        {
            float range = ranges[i];
            
            // Skip invalid readings
            if (range < minRange || range > maxRange)
                continue;
            
            // Calculate position
            float angle = angleMin + i * angleIncrement;
            Vector3 position = new Vector3(
                Mathf.Cos(angle) * range,
                0,
                Mathf.Sin(angle) * range
            );
            
            // Create point
            GameObject point = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            point.transform.position = lidarTransform.position + position;
            point.transform.localScale = Vector3.one * pointSize;
            point.transform.parent = lidarTransform;
            
            // Color by distance
            float t = (range - minRange) / (maxRange - minRange);
            point.GetComponent<Renderer>().material = new Material(pointMaterial);
            point.GetComponent<Renderer>().material.color = Color.Lerp(closeColor, farColor, t);
            
            points.Add(point);
        }
    }
    
    void OnDestroy()
    {
        Disconnect();
    }
}
```

## Hands-on Lab

### Lab 4.1: Visualize Gazebo Robot in Unity

**Objective**: Create a Unity scene that visualizes a robot simulated in Gazebo.

**Prerequisites**:
- Unity 2021 LTS or later installed
- ROS# package downloaded
- Gazebo simulation from Chapter 2 running

**Duration**: 90 minutes

---

#### Step 1: Setup Unity Project

```bash
# Create new Unity project
# Open Unity Hub → New Project → 3D (HDRP)
# Name: "Robot Visualization"
```

#### Step 2: Import ROS# Package

1. Download ROS# from GitHub:
   ```bash
   git clone https://github.com/siemens/ros-sharp.git
   ```

2. In Unity:
   - Assets → Import Package → Custom Package
   - Select `ros-sharp/Unity3D/ros-sharp.unitypackage`
   - Import all

#### Step 3: Create Robot Scene

1. **Create ground plane**:
   - GameObject → 3D Object → Plane
   - Scale: (10, 1, 10)

2. **Import robot model**:
   - Export URDF to FBX (use Blender or urdf-importer)
   - Drag FBX into Unity Assets
   - Add to scene

3. **Add lighting**:
   - GameObject → Light → Directional Light
   - Intensity: 1.5
   - Rotation: (50, -30, 0)

#### Step 4: Create ROS# Subscriber

Create `RobotController.cs`:

```csharp
// Copy code from Example 1 above
```

#### Step 5: Setup ROS Bridge

On Ubuntu (same machine as Gazebo):

```bash
# Install rosbridge
sudo apt install ros-humble-rosbridge-suite

# Launch rosbridge
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

#### Step 6: Configure Unity Connection

In Unity Inspector for RobotController:
- **WebSocket URL**: `ws://localhost:9090`
- **Robot Model**: Drag robot GameObject
- **Max Speed**: 2.0
- **Max Rotation**: 180

#### Step 7: Add Camera Controller

1. Create `CameraController.cs`:
   ```csharp
   // Copy code from Example 2
   ```

2. Attach to Main Camera
3. Set target to robot

#### Step 8: Run Complete System

Terminal 1 - Gazebo:
```bash
ros2 launch my_robot gazebo_launch.py
```

Terminal 2 - ROS Bridge:
```bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

Terminal 3 - Velocity Publisher:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"
```

Unity - Press Play

**Expected Result**:

Robot moves in Unity when velocity commands are published. Camera follows robot smoothly.

## Summary

### Key Takeaways

1. **Unity Rendering**: HDRP provides photorealistic visualization for robotics

2. **ROS# Integration**: Unity can subscribe to ROS2 topics via WebSocket bridge

3. **Camera Systems**: Implement orbital, follow, and first-person cameras for HRI

4. **Scene Building**: Combine environment, lighting, materials, and post-processing

5. **Gazebo-Unity Bridge**: Stream data from Gazebo physics to Unity rendering

### Key Terms

| Term | Definition |
|------|------------|
| **HDRP** | High Definition Render Pipeline |
| **ROS#** | ROS Sharp - Unity ROS communication library |
| **WebSocket** | Protocol for Unity-ROS2 communication |
| **HRI** | Human-Robot Interaction |
| **Post-Processing** | Visual effects applied after rendering |

## Exercises

### Exercise 4.1: Material Creation

1. Create PBR materials in Unity for:
   - Metal (robot body)
   - Rubber (wheels/tires)
   - Plastic (sensors)
2. Apply materials to robot model
3. **Screenshot** the result

### Exercise 4.2: Camera System

1. Implement three camera modes:
   - First-person (robot view)
   - Third-person (follow)
   - Top-down (overhead)
2. Add keyboard shortcuts to switch cameras
3. **Record** a video demo

### Exercise 4.3: LiDAR Visualization

1. Implement Example 4 (LiDAR Visualizer)
2. Test with Gazebo LiDAR data
3. **Compare** visualization with RViz2

### Exercise 4.4: Scene Enhancement

1. Add props to scene (tables, chairs, walls)
2. Configure lighting for different times of day
3. Add post-processing effects (bloom, color grading)
4. **Document** your scene design

### Exercise 4.5: Research Question

Research **digital twin visualization** in industry:

- How do companies use Unity for robot visualization?
- What are the benefits over traditional tools?
- What is the future of photorealistic simulation?

**Write** a 400-word summary with examples.

---

**Next Chapter**: [Chapter 5 — Building the Digital Twin →](./chapter5-building-digital-twin.md)
