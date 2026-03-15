# Unity Installation Guide for Robotics Visualization

This guide walks you through installing Unity 2021+ with HDRP for robotics visualization.

## System Requirements

- **OS**: Windows 10/11, Ubuntu 20.04+, or macOS 11+
- **CPU**: Intel i7 or AMD equivalent
- **RAM**: 16 GB minimum, 32 GB recommended
- **GPU**: NVIDIA GTX 1060 or better with 6GB VRAM
- **Storage**: 50 GB free space

## Step 1: Download Unity Hub

### Windows/macOS

1. Visit [unity.com/download](https://unity.com/download)
2. Click "Download for [your OS]"
3. Run the installer
4. Sign in or create a Unity account

### Ubuntu/Linux

```bash
# Download Unity Hub
wget -q https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage -O unity-hub.AppImage

# Make executable
chmod +x unity-hub.AppImage

# Run Unity Hub
./unity-hub.AppImage
```

## Step 2: Install Unity Editor

1. Open Unity Hub
2. Go to **Installs** → **Install Editor**
3. Select **Unity 2021.3 LTS** or later
4. Click **Next**

## Step 3: Add Required Modules

During installation, select these modules:

- [x] **Unity Hub**
- [x] **Unity Editor**
- [x] **Documentation** (optional)
- [x] **Standard Assets** (optional)

Click **Install** and wait for download (may take 30-60 minutes).

## Step 4: Create HDRP Project

1. Open Unity Hub
2. Click **New Project**
3. Select **High Definition Render Pipeline (HDRP)**
4. Name: `RobotVisualization`
5. Location: Choose a directory
6. Click **Create Project**

## Step 5: Install ROS# Package

### Option A: Via Package Manager (Recommended)

1. In Unity: **Window** → **Package Manager**
2. Click **+** (top left)
3. Select **Add package from git URL**
4. Enter: `https://github.com/siemens/ros-sharp.git?path=/RosSharp2`
5. Click **Add**

### Option B: Manual Installation

```bash
# Clone ROS# repository
git clone https://github.com/siemens/ros-sharp.git

# Copy Unity package
cp -r ros-sharp/Unity3D/* /path/to/your/project/Assets/
```

## Step 6: Configure ROS# Bridge

1. In Unity, create empty GameObject: **GameObject** → **Create Empty**
2. Name it `RosBridge`
3. Add component: **Add Component** → `RosBridge`
4. Configure:
   - **WebSocket URL**: `ws://localhost:9090`
   - **Fixed Update Rate**: `100`

## Step 7: Verify Installation

### Test Scene

1. Create a simple scene with:
   - 3D object (cube or sphere)
   - Directional light
   - Camera

2. Press **Play** button

3. Verify:
   - Object renders correctly
   - No console errors
   - Frame rate > 30 FPS

### ROS# Test

1. Start ROS bridge on Ubuntu:

```bash
sudo apt install ros-humble-rosbridge-suite
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

2. In Unity, press **Play**
3. Check Console for "Connected to ROS bridge" message

## Troubleshooting

### Issue: Unity won't start on Linux

```bash
# Install required dependencies
sudo apt install -y libxcb1 libxkbcommon-x11-0 libdbus-1-3
```

### Issue: HDRP not rendering correctly

1. Go to **Edit** → **Project Settings** → **Graphics**
2. Set **Scriptable Render Pipeline Asset** to `HDRenderPipelineAsset`

### Issue: ROS# not connecting

1. Verify ROS bridge is running: `netstat -an | grep 9090`
2. Check firewall settings
3. Verify WebSocket URL is correct

### Issue: Low frame rate

1. Reduce resolution in Game view
2. Lower quality settings: **Edit** → **Project Settings** → **Quality**
3. Disable vsync for testing

## Next Steps

- Follow Chapter 4 tutorials for robot visualization
- Import your robot model (FBX format)
- Attach ROS# subscriber scripts
- Test with Gazebo simulation

## Resources

- [Unity Documentation](https://docs.unity3d.com/)
- [HDRP Documentation](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@latest)
- [ROS# GitHub](https://github.com/siemens/ros-sharp)
- [Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub)
