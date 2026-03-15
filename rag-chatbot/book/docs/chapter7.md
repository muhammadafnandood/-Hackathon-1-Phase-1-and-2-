---
title: "Chapter 7: Motion Planning and Control"
sidebar_label: "Motion Planning"
---

# Chapter 7: Motion Planning and Control

## Introduction to Motion Planning

Motion planning is the computation of a sequence of actions that moves a robot from an initial state to a goal state while avoiding obstacles and satisfying constraints.

## Configuration Space

###基本概念

**Configuration (q)**: Complete specification of robot position

**Configuration Space (C-space)**: Set of all possible configurations

**Obstacles in C-space (C_obs)**: Configurations that cause collision

**Free Space (C_free)**: C_space - C_obs

### Example: 2-Link Planar Arm

```
q = [θ1, θ2]
C_space = [0, 2π] × [0, 2π]

Forward Kinematics:
x = L1*cos(θ1) + L2*cos(θ1 + θ2)
y = L1*sin(θ1) + L2*sin(θ1 + θ2)
```

## Sampling-Based Planning

### Rapidly-Exploring Random Trees (RRT)

Builds a tree by randomly sampling configuration space:

```python
class RRT:
    def __init__(self, start, goal, bounds, step_size=0.1, max_iter=10000):
        self.start = start
        self.goal = goal
        self.bounds = bounds  # [(min1, max1), (min2, max2), ...]
        self.step_size = step_size
        self.max_iter = max_iter
        self.tree = [start]
        self.parent = {tuple(start): None}
    
    def sample(self):
        """Random configuration in bounds"""
        return [np.random.uniform(low, high) for low, high in self.bounds]
    
    def nearest(self, config):
        """Find nearest tree node to sample"""
        min_dist = float('inf')
        nearest_node = None
        
        for node in self.tree:
            dist = np.linalg.norm(np.array(node) - np.array(config))
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
        
        return nearest_node
    
    def steer(self, from_config, to_config):
        """Move from_config toward to_config by step_size"""
        direction = np.array(to_config) - np.array(from_config)
        direction = direction / np.linalg.norm(direction)
        new_config = np.array(from_config) + self.step_size * direction
        return new_config.tolist()
    
    def is_collision_free(self, config):
        """Check if configuration is in free space"""
        # Implement collision checking
        return True
    
    def plan(self):
        for i in range(self.max_iter):
            # Sample random configuration
            random_config = self.sample()
            
            # Find nearest tree node
            nearest_node = self.nearest(random_config)
            
            # Steer toward sample
            new_config = self.steer(nearest_node, random_config)
            
            # Check collision
            if self.is_collision_free(new_config):
                # Add to tree
                self.tree.append(new_config)
                self.parent[tuple(new_config)] = nearest_node
                
                # Check if goal reached
                if np.linalg.norm(np.array(new_config) - np.array(self.goal)) < self.step_size:
                    return self.extract_path(new_config)
        
        return None
    
    def extract_path(self, end_config):
        """Extract path from start to end_config"""
        path = []
        current = end_config
        
        while current is not None:
            path.append(current)
            current = self.parent.get(tuple(current))
        
        return path[::-1]  # Reverse to get start-to-goal path
```

### RRT* (Optimal RRT)

Asymptotically optimal version of RRT:

```python
class RRTStar(RRT):
    def __init__(self, *args, rewiring_radius=1.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.rewiring_radius = rewiring_radius
        self.cost = {tuple(self.start): 0}
    
    def cost_to_reach(self, config):
        """Cost from start to config"""
        return self.cost.get(tuple(config), float('inf'))
    
    def plan(self):
        for i in range(self.max_iter):
            random_config = self.sample()
            nearest_node = self.nearest(random_config)
            new_config = self.steer(nearest_node, random_config)
            
            if self.is_collision_free(new_config):
                # Find neighbors
                neighbors = self.find_neighbors(new_config)
                
                # Choose best parent
                best_parent = nearest_node
                best_cost = self.cost_to_reach(nearest_node) + self.distance(nearest_node, new_config)
                
                for neighbor in neighbors:
                    new_cost = self.cost_to_reach(neighbor) + self.distance(neighbor, new_config)
                    if new_cost < best_cost and self.is_collision_free_path(neighbor, new_config):
                        best_parent = neighbor
                        best_cost = new_cost
                
                # Add to tree
                self.tree.append(new_config)
                self.parent[tuple(new_config)] = best_parent
                self.cost[tuple(new_config)] = best_cost
                
                # Rewire tree
                for neighbor in neighbors:
                    new_cost = best_cost + self.distance(new_config, neighbor)
                    if new_cost < self.cost_to_reach(neighbor):
                        if self.is_collision_free_path(new_config, neighbor):
                            self.parent[tuple(neighbor)] = new_config
                            self.cost[tuple(neighbor)] = new_cost
                
                # Check goal
                if np.linalg.norm(np.array(new_config) - np.array(self.goal)) < self.step_size:
                    return self.extract_path(new_config)
        
        return None
```

### Probabilistic Roadmaps (PRM)

Builds a graph of feasible configurations:

```python
class PRM:
    def __init__(self, n_samples=100, connection_radius=0.5):
        self.n_samples = n_samples
        self.connection_radius = connection_radius
        self.roadmap = []
        self.edges = []
    
    def sample_configurations(self, bounds):
        """Generate random collision-free configurations"""
        configs = []
        
        while len(configs) < self.n_samples:
            config = [np.random.uniform(low, high) for low, high in bounds]
            
            if self.is_collision_free(config):
                configs.append(config)
        
        return configs
    
    def build_roadmap(self, bounds):
        """Build probabilistic roadmap"""
        # Sample configurations
        self.roadmap = self.sample_configurations(bounds)
        
        # Connect nearby configurations
        for i, config1 in enumerate(self.roadmap):
            for j, config2 in enumerate(self.roadmap[i+1:], i+1):
                distance = np.linalg.norm(np.array(config1) - np.array(config2))
                
                if distance < self.connection_radius:
                    if self.is_collision_free_path(config1, config2):
                        self.edges.append((i, j))
    
    def query(self, start, goal):
        """Find path from start to goal"""
        # Add start and goal to roadmap
        start_idx = len(self.roadmap)
        self.roadmap.append(start)
        
        goal_idx = len(self.roadmap)
        self.roadmap.append(goal)
        
        # Connect start and goal to roadmap
        for i, config in enumerate(self.roadmap[:-2]):
            if np.linalg.norm(np.array(config) - np.array(start)) < self.connection_radius:
                if self.is_collision_free_path(config, start):
                    self.edges.append((i, start_idx))
            
            if np.linalg.norm(np.array(config) - np.array(goal)) < self.connection_radius:
                if self.is_collision_free_path(config, goal):
                    self.edges.append((i, goal_idx))
        
        # Search graph (A* or Dijkstra)
        path_indices = self.dijkstra(start_idx, goal_idx)
        
        return [self.roadmap[i] for i in path_indices]
```

## Trajectory Generation

### Point-to-Point Motion

#### Linear Interpolation

```python
def linear_trajectory(q_start, q_end, duration, n_points):
    """Generate linear trajectory in joint space"""
    trajectory = []
    
    for i in range(n_points):
        t = i / (n_points - 1)
        q = q_start + t * (q_end - q_start)
        trajectory.append(q)
    
    return trajectory
```

#### Cubic Polynomial

Smooth trajectory with velocity constraints:

```python
def cubic_trajectory(q_start, q_end, v_start, v_end, duration, n_points):
    """
    Cubic polynomial trajectory: q(t) = a0 + a1*t + a2*t^2 + a3*t^3
    
    Constraints:
    q(0) = q_start, q(duration) = q_end
    v(0) = v_start, v(duration) = v_end
    """
    # Solve for coefficients
    T = duration
    
    a0 = q_start
    a1 = v_start
    a2 = (3*(q_end - q_start)/T**2) - (2*v_start/T) - (v_end/T)
    a3 = (-2*(q_end - q_start)/T**3) + (v_start/T**2) + (v_end/T**2)
    
    trajectory = []
    
    for i in range(n_points):
        t = i * duration / (n_points - 1)
        q = a0 + a1*t + a2*t**2 + a3*t**3
        v = a1 + 2*a2*t + 3*a3*t**2
        a = 2*a2 + 6*a3*t
        
        trajectory.append({'position': q, 'velocity': v, 'acceleration': a})
    
    return trajectory
```

#### Quintic Polynomial

Smooth trajectory with acceleration constraints:

```python
def quintic_trajectory(q_start, q_end, v_start, v_end, a_start, a_end, duration, n_points):
    """
    Quintic polynomial: q(t) = a0 + a1*t + a2*t^2 + a3*t^3 + a4*t^4 + a5*t^5
    """
    T = duration
    
    # Build system of equations
    A = np.array([
        [1, 0, 0, 0, 0, 0],
        [T, T**2, T**3, T**4, T**5, T**6],
        [0, 1, 0, 0, 0, 0],
        [0, 2*T, 3*T**2, 4*T**3, 5*T**4, 6*T**5],
        [0, 0, 2, 0, 0, 0],
        [0, 0, 6*T, 12*T**2, 20*T**3, 30*T**4]
    ])
    
    b = np.array([q_start, q_end, v_start, v_end, a_start, a_end])
    
    coefficients = np.linalg.solve(A, b)
    
    trajectory = []
    
    for i in range(n_points):
        t = i * duration / (n_points - 1)
        q = sum(coefficients[j] * t**j for j in range(6))
        v = sum(j * coefficients[j] * t**(j-1) for j in range(1, 6))
        a = sum(j * (j-1) * coefficients[j] * t**(j-2) for j in range(2, 6))
        
        trajectory.append({'position': q, 'velocity': v, 'acceleration': a})
    
    return trajectory
```

## Control Systems

### PID Control

Proportional-Integral-Derivative controller:

```python
class PIDController:
    def __init__(self, kp, ki, kd, integral_limit=10, output_limit=100):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_limit = integral_limit
        self.output_limit = output_limit
        
        self.integral = 0
        self.previous_error = 0
    
    def update(self, setpoint, measurement, dt):
        error = setpoint - measurement
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term (with anti-windup)
        self.integral += error * dt
        self.integral = np.clip(self.integral, -self.integral_limit, self.integral_limit)
        i_term = self.ki * self.integral
        
        # Derivative term
        derivative = (error - self.previous_error) / dt
        d_term = self.kd * derivative
        
        self.previous_error = error
        
        # Combine terms
        output = p_term + i_term + d_term
        output = np.clip(output, -self.output_limit, self.output_limit)
        
        return output
    
    def reset(self):
        self.integral = 0
        self.previous_error = 0
```

### Computed Torque Control

Model-based control for manipulators:

```python
class ComputedTorqueController:
    def __init__(self, robot_model, kp, kd):
        self.robot_model = robot_model
        self.kp = kp
        self.kd = kd
    
    def compute_torque(self, q_desired, qd_desired, qdd_desired, q_actual, qd_actual):
        """
        Compute joint torques using computed torque method
        
        τ = M(q)(qdd_d + kd*(qd_d - qd) + kp*(q_d - q)) + C(q, qd) + G(q)
        """
        error = q_desired - q_actual
        error_rate = qd_desired - qd_actual
        
        # Desired acceleration with feedback
        qdd_command = qdd_desired + self.kd * error_rate + self.kp * error
        
        # Get robot dynamics
        M = self.robot_model.mass_matrix(q_actual)
        C = self.robot_model.coriolis(q_actual, qd_actual)
        G = self.robot_model.gravity(q_actual)
        
        # Compute torque
        tau = M @ qdd_command + C + G
        
        return tau
```

### Operational Space Control

Control in task space rather than joint space:

```python
class OperationalSpaceController:
    def __init__(self, robot_model, kp_task, kd_task):
        self.robot_model = robot_model
        self.kp_task = kp_task
        self.kd_task = kd_task
    
    def compute_torque(self, x_desired, xd_desired, xdd_desired, q, qd):
        """
        Compute joint torques for task space control
        
        τ = J^T * (Λ * (xdd_d + kd*(xd_d - xd) + kp*(x_d - x)) + p) + b
        """
        # Forward kinematics
        x = self.robot_model.forward_kinematics(q)
        J = self.robot_model.jacobian(q)
        Jdot = self.robot_model.jacobian_derivative(q, qd)
        
        # Task space error
        error = x_desired - x
        error_rate = xd_desired - J @ qd
        
        # Operational space inertia
        M = self.robot_model.mass_matrix(q)
        Lambda = np.linalg.inv(J @ np.linalg.inv(M) @ J.T)
        
        # Task space force
        F_task = self.kp_task * error + self.kd_task * error_rate
        
        # Joint torques
        tau = J.T @ F_task
        
        # Add dynamics compensation
        C = self.robot_model.coriolis(q, qd)
        G = self.robot_model.gravity(q)
        tau += C + G
        
        return tau
```

## Whole-Body Control

### Quadratic Programming Formulation

Optimize multiple objectives with constraints:

```python
import cvxpy as cp

class WholeBodyController:
    def __init__(self, robot):
        self.robot = robot
        self.n_joints = robot.n_joints
    
    def compute_joint_accelerations(self, q, qd, tasks, constraints):
        """
        Solve QP for whole-body control
        
        minimize: ||W_task * (J*qdd + Jdot*qd - xdd_ref)||^2 + ||W_reg * qdd||^2
        subject to: constraints
        """
        qdd = cp.Variable(self.n_joints)
        
        # Build objective
        objective = 0
        
        for task in tasks:
            J = task['jacobian'](q)
            Jdot = task['jacobian_dot'](q, qd)
            xdd_ref = task['acceleration_ref']
            W = task['weight']
            
            task_error = J @ qdd + Jdot @ qd - xdd_ref
            objective += cp.sum_squares(W @ task_error)
        
        # Regularization
        objective += cp.sum_squares(0.01 * qdd)
        
        # Add constraints
        constraints_list = []
        
        for constraint in constraints:
            constraints_list.append(constraint(q, qd, qdd))
        
        # Solve QP
        problem = cp.Problem(cp.Minimize(objective), constraints_list)
        problem.solve()
        
        return qdd.value
```

## Summary

Motion planning and control are fundamental to robotics. Sampling-based planners handle high-dimensional spaces, while sophisticated controllers ensure accurate trajectory tracking despite dynamics and disturbances.
