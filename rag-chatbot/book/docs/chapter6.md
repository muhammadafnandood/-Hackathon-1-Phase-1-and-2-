---
title: "Chapter 6: Sensors and Perception Systems"
sidebar_label: "Sensors & Perception"
---

# Chapter 6: Sensors and Perception Systems

## Overview of Robotic Sensors

Sensors are the foundation of robot perception, converting physical quantities into electrical signals that can be processed by the robot's control system.

## Proprioceptive Sensors

These sensors measure the robot's internal state.

### Encoders

Measure joint angles and velocities:

#### Incremental Encoders
- Output pulses as shaft rotates
- Count pulses to determine position
- Need homing routine to find absolute position
- High resolution (up to 1 million counts/rev)

#### Absolute Encoders
- Output unique code for each position
- Know position immediately on power-up
- More expensive but more robust
- Essential for safety-critical applications

### Inertial Measurement Units (IMU)

Measure body orientation and acceleration:

#### Components
- **Accelerometers**: Measure linear acceleration (3 axes)
- **Gyroscopes**: Measure angular velocity (3 axes)
- **Magnetometers**: Measure magnetic field (compass)

#### IMU Data Processing

```python
class IMUFilter:
    def __init__(self):
        self.orientation = np.array([0, 0, 0, 1])  # Quaternion
        self.bias = np.array([0, 0, 0])
    
    def update(self, gyro_data, accel_data, dt):
        # Remove gyro bias
        omega = gyro_data - self.bias
        
        # Integrate orientation
        dq = 0.5 * np.array([
            self.orientation[3] * omega[0] - self.orientation[2] * omega[1] + self.orientation[1] * omega[2],
            self.orientation[2] * omega[0] + self.orientation[3] * omega[1] - self.orientation[0] * omega[2],
            -self.orientation[1] * omega[0] + self.orientation[0] * omega[1] + self.orientation[3] * omega[2],
            -self.orientation[0] * omega[0] - self.orientation[1] * omega[1] - self.orientation[2] * omega[2]
        ])
        
        self.orientation += dq * dt
        self.orientation = self.orientation / np.linalg.norm(self.orientation)
        
        return self.orientation
```

### Force/Torque Sensors

Measure interaction forces:

- **Strain Gauge Based**: Most common, high accuracy
- **Capacitive**: High sensitivity, compact
- **Piezoelectric**: Dynamic forces only

#### Applications
- Assembly force control
- Collision detection
- Payload estimation
- Human-robot interaction

## Exteroceptive Sensors

These sensors measure the external environment.

### Vision Sensors

#### RGB Cameras

Standard color cameras:

- **Perspective Cameras**: Pinhole model
- **Fish-eye Cameras**: Wide field of view
- **Event Cameras**: Asynchronous pixel changes

#### Camera Model

Pinhole camera projection:

```
u = f_x * X/Z + c_x
v = f_y * Y/Z + c_y
```

Where:
- `(u, v)`: Image coordinates
- `(X, Y, Z)`: 3D point
- `f_x, f_y`: Focal lengths
- `c_x, c_y`: Principal point

#### Depth Cameras

Measure distance to objects:

**Stereo Cameras**
- Two cameras with known baseline
- Triangulate using disparity
- Works outdoors, passive
- Requires texture, computation intensive

**Time of Flight (ToF)**
- Measure light travel time
- Fast, compact
- Limited range, multi-path errors

**Structured Light**
- Project known pattern
- Analyze pattern distortion
- High accuracy, short range
- Sensitive to ambient light

### LiDAR (Light Detection and Ranging)

Measures distance using laser pulses:

#### Types of LiDAR

**Mechanical LiDAR**
- Rotating sensor head
- 360° field of view
- High accuracy (±2cm)
- Expensive, moving parts

**Solid-State LiDAR**
- No moving parts
- More reliable, cheaper
- Limited field of view
- Emerging technology

**Flash LiDAR**
- Single pulse illuminates scene
- Fast capture
- Lower resolution
- Short range

#### LiDAR Data Processing

```python
class LiDARProcessor:
    def __init__(self):
        self.ground_plane = None
    
    def remove_ground(self, point_cloud):
        """Remove ground points using RANSAC"""
        # Fit plane to points
        inliers, self.ground_plane = self.ransac_plane_fit(point_cloud)
        
        # Remove ground points
        non_ground = np.delete(point_cloud, inliers, axis=0)
        return non_ground
    
    def cluster_objects(self, point_cloud, eps=0.5, min_points=10):
        """Cluster points into objects using DBSCAN"""
        from sklearn.cluster import DBSCAN
        
        clustering = DBSCAN(eps=eps, min_samples=min_points)
        labels = clustering.fit_predict(point_cloud[:, :3])
        
        objects = []
        for label in np.unique(labels):
            if label != -1:  # Ignore noise
                object_points = point_cloud[labels == label]
                objects.append(object_points)
        
        return objects
```

### Tactile Sensors

Provide touch feedback:

#### Types

**Resistive Tactile Sensors**
- Measure contact pressure
- Simple, low cost
- Limited resolution

**Capacitive Tactile Sensors**
- Higher sensitivity
- Measure normal and shear forces
- More complex electronics

**Optical Tactile Sensors**
- Camera-based (e.g., GelSight)
- High resolution texture
- Measure deformation visually

#### Applications
- Grasping force control
- Texture recognition
- Slip detection
- Object identification

## Sensor Fusion

Combining multiple sensors for robust perception.

### Kalman Filter

Optimal estimator for linear systems:

```python
class KalmanFilter:
    def __init__(self, F, H, Q, R, P0, x0):
        self.F = F  # State transition model
        self.H = H  # Observation model
        self.Q = Q  # Process noise covariance
        self.R = R  # Measurement noise covariance
        self.P = P0  # Estimate error covariance
        self.x = x0  # State estimate
    
    def predict(self):
        # Predict state
        self.x = self.F @ self.x
        
        # Predict error covariance
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        return self.x, self.P
    
    def update(self, z):
        # Innovation
        y = z - self.H @ self.x
        
        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman gain
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update state
        self.x = self.x + K @ y
        
        # Update error covariance
        I = np.eye(len(self.x))
        self.P = (I - K @ self.H) @ self.P
        
        return self.x, self.P
```

### Extended Kalman Filter (EKF)

For nonlinear systems:

```python
class ExtendedKalmanFilter:
    def __init__(self, f, h, Q, R, P0, x0):
        self.f = f  # Nonlinear state transition
        self.h = h  # Nonlinear observation
        self.Q = Q
        self.R = R
        self.P = P0
        self.x = x0
    
    def jacobian(self, func, x, dx=1e-6):
        """Numerical Jacobian computation"""
        n = len(x)
        J = np.zeros((len(func(x)), n))
        
        for i in range(n):
            x_plus = x.copy()
            x_plus[i] += dx
            x_minus = x.copy()
            x_minus[i] -= dx
            
            J[:, i] = (func(x_plus) - func(x_minus)) / (2 * dx)
        
        return J
    
    def update(self, z):
        # Linearize around current estimate
        H = self.jacobian(self.h, self.x)
        
        # Innovation
        y = z - self.h(self.x)
        
        # Innovation covariance
        S = H @ self.P @ H.T + self.R
        
        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)
        
        # Update
        self.x = self.x + K @ y
        I = np.eye(len(self.x))
        self.P = (I - K @ H) @ self.P
        
        return self.x
```

### Particle Filter

For non-Gaussian distributions:

```python
class ParticleFilter:
    def __init__(self, n_particles, initial_state, noise):
        self.n_particles = n_particles
        self.particles = np.tile(initial_state, (n_particles, 1))
        self.weights = np.ones(n_particles) / n_particles
        self.noise = noise
    
    def predict(self, control):
        # Move particles with motion model
        for i in range(self.n_particles):
            self.particles[i] = self.motion_model(
                self.particles[i], 
                control, 
                self.noise
            )
    
    def update(self, measurement):
        # Update weights based on measurement likelihood
        for i in range(self.n_particles):
            predicted_measurement = self.observation_model(self.particles[i])
            error = measurement - predicted_measurement
            self.weights[i] = np.exp(-0.5 * error.T @ np.linalg.inv(self.noise) @ error)
        
        # Normalize weights
        self.weights /= np.sum(self.weights)
        
        # Resample
        self.resample()
    
    def resample(self):
        indices = np.random.choice(
            range(self.n_particles), 
            size=self.n_particles, 
            p=self.weights
        )
        self.particles = self.particles[indices]
        self.weights = np.ones(self.n_particles) / self.n_particles
    
    def get_estimate(self):
        return np.average(self.particles, weights=self.weights, axis=0)
```

## Computer Vision for Robotics

### Object Detection

#### Traditional Methods

- **Feature Detection**: SIFT, SURF, ORB
- **Template Matching**: Compare with known templates
- **Color Segmentation**: Threshold in color space

#### Deep Learning Methods

**YOLO (You Only Look Once)**
- Real-time detection
- Single neural network
- Good for robotics applications

```python
import cv2
import torch

class ObjectDetector:
    def __init__(self, model_path, confidence_threshold=0.5):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        self.confidence_threshold = confidence_threshold
    
    def detect(self, image):
        results = self.model(image)
        detections = results.pandas().xyxy[0]
        
        # Filter by confidence
        detections = detections[detections['confidence'] > self.confidence_threshold]
        
        return detections
```

### Semantic Segmentation

Classify every pixel:

- **U-Net**: Encoder-decoder architecture
- **DeepLab**: Atrous convolution
- **Mask R-CNN**: Instance segmentation

### Visual SLAM

Simultaneous Localization and Mapping:

#### ORB-SLAM

Popular visual SLAM system:

1. **Feature Extraction**: ORB features
2. **Tracking**: Match features frame to frame
3. **Local Mapping**: Build map from features
4. **Loop Closure**: Detect and close loops
5. **Global Bundle Adjustment**: Optimize map

## Perception Pipeline

### Complete Perception Stack

```python
class PerceptionStack:
    def __init__(self):
        self.camera = Camera()
        self.lidar = LiDAR()
        self.imu = IMU()
        self.object_detector = ObjectDetector()
        self.tracker = MultiObjectTracker()
    
    def process_frame(self):
        # Get sensor data
        image = self.camera.get_image()
        point_cloud = self.lidar.get_scan()
        imu_data = self.imu.get_data()
        
        # Detect objects
        detections = self.object_detector.detect(image)
        
        # Associate with point cloud
        for detection in detections:
            detection_3d = self.project_to_3d(detection, point_cloud)
        
        # Track over time
        tracks = self.tracker.update(detections)
        
        # Fuse with IMU for motion compensation
        compensated_tracks = self.compensate_motion(tracks, imu_data)
        
        return {
            'objects': compensated_tracks,
            'point_cloud': point_cloud,
            'imu': imu_data
        }
```

## Summary

Robust perception requires combining multiple sensor modalities with sophisticated algorithms. Modern robots use deep learning for high-level perception combined with classical filtering for state estimation.
