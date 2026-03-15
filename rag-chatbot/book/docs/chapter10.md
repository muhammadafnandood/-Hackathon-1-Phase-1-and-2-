---
title: "Chapter 10: Digital Twins and Simulation"
sidebar_label: "Digital Twins"
---

# Chapter 10: Digital Twins and Simulation

## What are Digital Twins?

A digital twin is a virtual representation of a physical robot or system that mirrors its real-world counterpart. Digital twins enable testing, optimization, and monitoring without risking physical hardware.

## Benefits of Digital Twins

### Development

- **Rapid Prototyping**: Test designs before building
- **Algorithm Development**: Validate control strategies
- **Safety Testing**: Test failure modes safely
- **Cost Reduction**: Reduce physical prototyping costs

### Operations

- **Predictive Maintenance**: Detect issues before failure
- **Performance Optimization**: Tune parameters virtually
- **Remote Monitoring**: Track system health
- **Training**: Safe operator training environment

### Lifecycle Management

- **Design Iteration**: Quick design modifications
- **What-if Analysis**: Test scenarios
- **Documentation**: Living system model
- **Knowledge Preservation**: Capture institutional knowledge

## Simulation Platforms

### Gazebo

Popular robotics simulator with ROS integration:

```python
import gazebo_ros
from gazebo_msgs.srv import SpawnEntity, DeleteEntity
from geometry_msgs.msg import Pose

class GazeboSimulation:
    def __init__(self):
        self.spawn_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnEntity)
        self.delete_client = rospy.ServiceProxy('/gazebo/delete_model', DeleteEntity)
    
    def spawn_robot(self, robot_name, urdf_string, initial_pose):
        """Spawn robot in simulation"""
        spawn_request = SpawnEntityRequest()
        spawn_request.model_name = robot_name
        spawn_request.model_xml = urdf_string
        spawn_request.robot_namespace = ""
        spawn_request.initial_pose = initial_pose
        spawn_request.reference_frame = "world"
        
        response = self.spawn_client(spawn_request)
        return response.success
    
    def set_joint_state(self, joint_name, position, velocity, effort):
        """Set joint state"""
        pub = rospy.Publisher('/gazebo/set_joint_state', JointState)
        
        joint_state = JointState()
        joint_state.name = [joint_name]
        joint_state.position = [position]
        joint_state.velocity = [velocity]
        joint_state.effort = [effort]
        
        pub.publish(joint_state)
    
    def get_link_state(self, link_name):
        """Get link state"""
        client = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
        response = client(link_name, "world")
        return response.link_state
```

### MuJoCo

Physics engine optimized for robotics and RL:

```python
import mujoco
import numpy as np

class MuJoCoSimulation:
    def __init__(self, model_path):
        # Load model
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)
        
        # Simulation parameters
        self.timestep = self.model.opt.timestep
    
    def step(self, controls):
        """Advance simulation by one step"""
        # Set controls
        self.data.ctrl = controls
        
        # Step simulation
        mujoco.mj_step(self.model, self.data)
        
        return self.get_state()
    
    def get_state(self):
        """Get full simulation state"""
        return {
            'qpos': self.data.qpos.copy(),
            'qvel': self.data.qvel.copy(),
            'qacc': self.data.qacc.copy(),
            'time': self.data.time,
            'contact': self.data.contact,
        }
    
    def set_state(self, qpos, qvel):
        """Set simulation state"""
        self.data.qpos = qpos
        self.data.qvel = qvel
        mujoco.mj_forward(self.model, self.data)
    
    def render(self, viewer):
        """Render simulation"""
        viewer.render()
    
    def add_disturbance(self, body_name, force):
        """Apply external force"""
        body_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, body_name)
        self.data.xfrc_applied[body_id, :3] = force
```

### PyBullet

Physics engine for robotics and ML:

```python
import pybullet as p
import pybullet_data

class PyBulletSimulation:
    def __init__(self, gui=True):
        if gui:
            self.client_id = p.connect(p.GUI)
        else:
            self.client_id = p.connect(p.DIRECT)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        self.timestep = 1./240.
    
    def load_robot(self, urdf_path, base_position=[0, 0, 0], base_orientation=[0, 0, 0, 1]):
        """Load robot from URDF"""
        robot_id = p.loadURDF(
            urdf_path,
            basePosition=base_position,
            baseOrientation=base_orientation,
            useFixedBase=False,
            flags=p.URDF_USE_SELF_COLLISION
        )
        
        # Get joint information
        num_joints = p.getNumJoints(robot_id)
        self.joint_info = [p.getJointInfo(robot_id, i) for i in range(num_joints)]
        
        return robot_id
    
    def load_plane(self):
        """Load ground plane"""
        return p.loadURDF("plane.urdf")
    
    def load_object(self, urdf_path, position, orientation=[0, 0, 0, 1]):
        """Load object"""
        return p.loadURDF(urdf_path, position, orientation)
    
    def set_joint_position(self, robot_id, joint_index, position):
        """Set joint position"""
        p.setJointMotorControl2(
            robot_id,
            joint_index,
            p.POSITION_CONTROL,
            targetPosition=position
        )
    
    def get_joint_state(self, robot_id, joint_index):
        """Get joint state"""
        return p.getJointState(robot_id, joint_index)
    
    def get_base_position(self, robot_id):
        """Get robot base position"""
        pos, orn = p.getBasePositionAndOrientation(robot_id)
        return pos, orn
    
    def step_simulation(self):
        """Step simulation"""
        p.stepSimulation()
    
    def get_camera_image(self, camera_position, camera_target, up_vector=[0, 0, 1],
                        width=640, height=480, fov=60):
        """Get camera image"""
        view_matrix = p.computeViewMatrix(
            cameraEyePosition=camera_position,
            cameraTargetPosition=camera_target,
            cameraUpVector=up_vector
        )
        
        projection_matrix = p.computeProjectionMatrixFOV(
            fov=fov,
            aspect=float(width)/float(height),
            nearVal=0.01,
            farVal=100.0
        )
        
        return p.getCameraImage(
            width=width,
            height=height,
            viewMatrix=view_matrix,
            projectionMatrix=projection_matrix
        )
    
    def apply_external_force(self, object_id, link_id, force, position):
        """Apply external force"""
        p.applyExternalForce(
            object_id,
            link_id,
            forceObj=force,
            posObj=position,
            flags=p.WORLD_FRAME
        )
```

## Sim-to-Real Transfer

### Domain Randomization

```python
class DomainRandomizer:
    def __init__(self, simulation):
        self.sim = simulation
        self.original_params = {}
    
    def randomize_friction(self, min_friction=0.5, max_friction=2.0):
        """Randomize contact friction"""
        friction = np.random.uniform(min_friction, max_friction)
        
        # Change friction for all contact surfaces
        for i in range(self.sim.model.ngeom):
            self.sim.model.geom_friction[i, 0] = friction
        
        return friction
    
    def randomize_mass(self, body_name, min_scale=0.8, max_scale=1.2):
        """Randomize body mass"""
        scale = np.random.uniform(min_scale, max_scale)
        body_id = mujoco.mj_name2id(
            self.sim.model, 
            mujoco.mjtObj.mjOBJ_BODY, 
            body_name
        )
        
        # Scale mass
        self.sim.model.body_mass[body_id] *= scale
        
        return scale
    
    def randomize_visual(self, texture_path):
        """Randomize visual appearance"""
        # Load random texture
        texture_id = mujoco.mj_loadTexture(self.sim.model, texture_path)
        
        return texture_id
    
    def randomize_lighting(self):
        """Randomize lighting conditions"""
        for i in range(self.sim.model.nlight):
            # Random position
            self.sim.model.light_pos[i, :3] = np.random.uniform(-5, 5, 3)
            
            # Random intensity
            self.sim.model.light_intensity[i] = np.random.uniform(0.5, 1.5)
    
    def randomize_all(self):
        """Apply all randomizations"""
        params = {
            'friction': self.randomize_friction(),
            'mass_scale': self.randomize_mass('robot_base'),
            'lighting': 'randomized'
        }
        
        return params
```

### System Identification

Learn real robot parameters from data:

```python
class SystemIdentification:
    def __init__(self, real_robot, simulation):
        self.real = real_robot
        self.sim = simulation
        self.params_to_identify = ['mass', 'friction', 'damping']
    
    def collect_data(self, n_episodes=10):
        """Collect data from real robot"""
        trajectories = []
        
        for _ in range(n_episodes):
            # Execute random actions
            actions = np.random.uniform(-1, 1, self.real.n_actions)
            
            trajectory = {
                'states': [],
                'actions': [],
                'next_states': []
            }
            
            state = self.real.reset()
            
            for _ in range(100):
                next_state, reward, done, _ = self.real.step(actions)
                
                trajectory['states'].append(state)
                trajectory['actions'].append(actions)
                trajectory['next_states'].append(next_state)
                
                state = next_state
                
                if done:
                    break
            
            trajectories.append(trajectory)
        
        return trajectories
    
    def optimize_parameters(self, trajectories):
        """Optimize simulation parameters to match real data"""
        from scipy.optimize import minimize
        
        def objective(params):
            # Set simulation parameters
            self.set_sim_params(params)
            
            # Simulate same actions
            total_error = 0
            
            for traj in trajectories:
                self.sim.reset()
                sim_states = []
                
                for action in traj['actions']:
                    sim_state = self.sim.step(action)
                    sim_states.append(sim_state)
                
                # Compare with real states
                for real_state, sim_state in zip(traj['states'], sim_states):
                    error = np.linalg.norm(real_state - sim_state)
                    total_error += error
            
            return total_error / len(trajectories)
        
        # Initial parameters
        x0 = [1.0, 0.5, 0.1]  # mass, friction, damping
        
        # Optimize
        result = minimize(objective, x0, method='Nelder-Mead')
        
        return result.x
    
    def set_sim_params(self, params):
        """Set simulation parameters"""
        mass_scale, friction, damping = params
        
        # Apply to simulation
        # ... implementation depends on simulator
```

## Digital Twin Architecture

### Real-Time Synchronization

```python
class DigitalTwin:
    def __init__(self, physical_robot, simulation):
        self.physical = physical_robot
        self.simulation = simulation
        self.sync_frequency = 100  # Hz
        self.state_history = []
    
    def synchronize(self):
        """Sync simulation with physical robot"""
        # Get physical state
        physical_state = self.physical.get_full_state()
        
        # Update simulation
        self.simulation.set_state(
            physical_state['qpos'],
            physical_state['qvel']
        )
        
        # Store for analysis
        self.state_history.append({
            'time': time.time(),
            'physical': physical_state,
            'simulation': self.simulation.get_state()
        })
    
    def predict(self, actions, horizon=10):
        """Predict future states"""
        predictions = []
        
        # Save current state
        saved_state = self.simulation.get_state()
        
        # Roll forward in simulation
        for i in range(horizon):
            next_state = self.simulation.step(actions[i])
            predictions.append(next_state)
        
        # Restore state
        self.simulation.set_state(saved_state['qpos'], saved_state['qvel'])
        
        return predictions
    
    def detect_anomalies(self, threshold=0.1):
        """Detect anomalies between physical and simulated behavior"""
        if len(self.state_history) < 10:
            return False
        
        # Compare recent trajectories
        physical_traj = [s['physical'] for s in self.state_history[-10:]]
        sim_traj = [s['simulation'] for s in self.state_history[-10:]]
        
        # Compute difference
        differences = []
        for p, s in zip(physical_traj, sim_traj):
            diff = np.linalg.norm(p['qpos'] - s['qpos'])
            differences.append(diff)
        
        avg_diff = np.mean(differences)
        
        return avg_diff > threshold
    
    def run_parallel(self):
        """Run digital twin in parallel with physical robot"""
        while True:
            # Get physical command
            command = self.physical.get_command()
            
            # Execute in simulation
            sim_result = self.simulation.step(command)
            
            # Execute on physical
            physical_result = self.physical.execute(command)
            
            # Compare and log
            error = np.linalg.norm(sim_result - physical_result)
            
            if error > 0.1:
                print(f"Warning: Large sim-real gap: {error}")
            
            # Sync periodically
            self.synchronize()
            
            time.sleep(1.0 / self.sync_frequency)
```

## Summary

Digital twins enable safe, efficient robot development and operation. By maintaining a virtual counterpart synchronized with the physical robot, we can predict, optimize, and monitor system behavior.
