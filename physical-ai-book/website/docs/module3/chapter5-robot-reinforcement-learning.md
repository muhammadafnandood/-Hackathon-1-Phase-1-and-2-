---
sidebar_label: '5. Reinforcement Learning'
---

# Chapter 5: Reinforcement Learning for Robots

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand reinforcement learning fundamentals for robot control
- Configure Isaac Gym for parallel RL training
- Train locomotion policies for bipedal robots
- Implement sim-to-real transfer techniques
- Deploy learned policies on physical robots

## Concept Explanation

### What is Reinforcement Learning?

**Reinforcement Learning (RL)** trains agents through trial and error with rewards:

```
┌─────────────────────────────────────────────────────────────┐
│              REINFORCEMENT LEARNING LOOP                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         Action (a)        ┌──────────────┐│
│  │   Agent      │──────────────────────────►│  Environment ││
│  │  (Policy π)  │                           │   (Robot)    ││
│  └──────▲───────┘                           └──────┬───────┘│
│         │                                          │         │
│         │         Reward (r) + State (s)           │         │
│         └──────────────────────────────────────────┘         │
│                                                              │
│  Goal: Maximize cumulative reward                            │
│  ─────────────────────────────                               │
│  E[R] = E[r₀ + γr₁ + γ²r₂ + ...]                            │
│                                                              │
│  Where:                                                      │
│  • π: Policy (state → action mapping)                       │
│  • r: Reward signal                                          │
│  • γ: Discount factor (0.99)                                │
│  • s: State observation                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**RL for Robotics:**

- **Control**: Learn complex motor skills
- **Adaptation**: Handle uncertain environments
- **Autonomy**: Reduce manual programming
- **Optimization**: Find better-than-human strategies

### RL Algorithms for Robotics

**Common RL algorithms:**

```
┌─────────────────────────────────────────────────────────────┐
│                  RL ALGORITHMS                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Policy Gradient Methods                                     │
│  ─────────────────────                                       │
│  • PPO (Proximal Policy Optimization)                       │
│    - Stable, sample-efficient                               │
│    - Industry standard for robotics                         │
│    - Isaac Gym default                                      │
│                                                              │
│  • SAC (Soft Actor-Critic)                                  │
│    - Off-policy, sample-efficient                           │
│    - Good for continuous control                            │
│    - Maximum entropy framework                              │
│                                                              │
│  • DDPG (Deep Deterministic Policy Gradient)                │
│    - Actor-critic architecture                              │
│    - Continuous actions                                     │
│    - Less stable than PPO                                   │
│                                                              │
│  Evolution Strategies                                        │
│  ───────────────────                                         │
│  • CMA-ES (Covariance Matrix Adaptation ES)                 │
│    - Gradient-free optimization                             │
│    - Parallel evaluation                                    │
│    - Good for high-dimensional policies                     │
│                                                              │
│  Imitation Learning                                          │
│  ──────────────────                                          │
│  • Behavioral Cloning                                       │
│    - Learn from demonstrations                              │
│    - Fast training                                          │
│    - Limited to demonstrator skill                          │
│                                                              │
│  • Inverse Reinforcement Learning                           │
│    - Learn reward function                                  │
│    - More generalizable                                     │
│    - Complex optimization                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Isaac Gym for RL Training

**Isaac Gym** provides GPU-accelerated RL training:

```
┌─────────────────────────────────────────────────────────────┐
│              ISAAC GYM ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              GPU Parallel Environments                │   │
│  │                                                       │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐       ┌──────┐        │   │
│  │  │ Env  │  │ Env  │  │ Env  │  ...  │ Env  │        │   │
│  │  │  1   │  │  2   │  │  3   │       │  N   │        │   │
│  │  └──────┘  └──────┘  └──────┘       └──────┘        │   │
│  │                                                       │   │
│  │  • 1000s of environments                             │   │
│  │  • GPU physics (PhysX)                               │   │
│  │  • GPU rendering                                     │   │
│  │  • Direct tensor access                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↕                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              RL Framework (PyTorch)                   │   │
│  │                                                       │   │
│  │  • PPO implementation                                │   │
│  │  • GPU tensor operations                             │   │
│  │  • Distributed training                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Training Speed:                                             │
│  ───────────────                                             │
│  • 100x faster than CPU simulation                          │
│  • Humanoid walking: ~1 hour (vs. days)                     │
│  • Quadruped locomotion: ~30 minutes                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Benefits:**

- **Massive Parallelization**: 1000s of environments on single GPU
- **End-to-End GPU**: No CPU-GPU transfer bottleneck
- **PyTorch Integration**: Direct tensor access
- **Domain Randomization**: Built-in support

### Training Locomotion Policies

**Bipedal walking** is a challenging RL problem:

```
┌─────────────────────────────────────────────────────────────┐
│          BIPEDAL LOCOMOTION TRAINING                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  State Space (Observations):                                 │
│  ───────────────────────                                     │
│  • Joint positions (12-20 DOF)                              │
│  • Joint velocities                                         │
│  • Base orientation (IMU)                                   │
│  • Base angular velocity                                    │
│  • Commanded velocity                                       │
│  • Phase information (for gaits)                            │
│                                                              │
│  Action Space:                                               │
│  ────────────                                                │
│  • Joint torques (Nm)                                       │
│  • Joint position targets                                   │
│  • Typically 12-20 continuous actions                       │
│                                                              │
│  Reward Function:                                            │
│  ───────────────                                             │
│  r_total = w₁*r_forward + w₂*r_energy + w₃*r_stability      │
│            + w₄*r_height + w₅*r_joint_limit                 │
│                                                              │
│  Where:                                                      │
│  • r_forward: Reward for forward motion                     │
│  • r_energy: Penalty for high torque/speed                  │
│  • r_stability: Penalty for falling                         │
│  • r_height: Reward for maintaining height                  │
│  • r_joint_limit: Penalty for extreme angles                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Sim-to-Real Transfer

**Sim-to-real** transfers learned policies to physical robots:

```
┌─────────────────────────────────────────────────────────────┐
│              SIM-TO-REAL TRANSFER                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Challenge: Reality Gap                                      │
│  ─────────────────────                                       │
│  • Simulation ≠ Reality                                     │
│  • Inaccurate physics                                       │
│  • Sensor noise                                             │
│  • Unmodeled dynamics                                       │
│                                                              │
│  Solutions:                                                  │
│  ──────────                                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Domain Randomization                                 │   │
│  │  • Randomize physical parameters                     │   │
│  │    - Mass, friction, damping                         │   │
│  │  • Randomize visual appearance                       │   │
│  │    - Textures, lighting                              │   │
│  │  • Randomize sensor noise                            │   │
│  │  • Policy learns robust behavior                     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  System Identification                                │   │
│  │  • Measure real robot parameters                     │   │
│  │  • Update simulation model                           │   │
│  │  • Reduce reality gap                                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Progressive Training                                 │   │
│  │  • Train in simulation                               │   │
│  │  • Fine-tune on real robot                           │   │
│  │  • Start simple, increase difficulty                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Success Metrics:                                            │
│  ───────────────                                             │
│  • Same task performance in sim and real                    │
│  • Minimal real-world training needed                       │
│  • Robust to environmental changes                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Boston Atlas RL Training

Boston Dynamics uses **RL for Atlas parkour**:

```
┌────────────────────────────────────────────────────────┐
│           ATLAS RL-BASED CONTROL                        │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Task: Parkour (jumping, running, flipping)            │
│  ─────────────────────────────────                      │
│                                                         │
│  Training Approach:                                     │
│  ──────────────────                                     │
│  • Simulation: Custom physics engine                   │
│  • Algorithm: Model-based RL + MPC                     │
│  • Parallel: 100s of environments                      │
│  • Training time: Weeks                                │
│                                                         │
│  Sim-to-Real Transfer:                                  │
│  ──────────────────                                     │
│  • System identification                               │
│  • Progressive difficulty                              │
│  • Safety constraints                                  │
│  • Human supervision                                   │
│                                                         │
│  Results:                                               │
│  ───────                                                │
│  • Backflip from crouch                                │
│  • 180° jump turn                                      │
│  • Running jump over obstacles                         │
│  • Robust to pushes and slips                          │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Complete RL Training Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│              RL TRAINING PIPELINE                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Environment Setup                                        │
│     ────────────────────                                     │
│     ┌──────────────┐                                        │
│     │ Robot URDF   │                                        │
│     │ + Task Def   │                                        │
│     │ + Rewards    │                                        │
│     └──────────────┘                                        │
│                                                              │
│  2. Training (Isaac Gym)                                     │
│     ────────────────                                         │
│     ┌──────────────┐    ┌──────────────┐                   │
│     │  GPU Envs    │───►│  PPO Trainer │                   │
│     │  (Parallel)  │    │  (PyTorch)   │                   │
│     └──────────────┘    └──────────────┘                   │
│                                                              │
│  3. Policy Export                                            │
│     ─────────────                                            │
│     ┌──────────────┐                                        │
│     │  Neural Net  │                                        │
│     │  (ONNX)      │                                        │
│     └──────────────┘                                        │
│                                                              │
│  4. Deployment                                               │
│     ────────────                                             │
│     ┌──────────────┐    ┌──────────────┐                   │
│     │  Real Robot  │◄───│  Policy      │                   │
│     │              │    │  Execution   │                   │
│     └──────────────┘    └──────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Isaac Gym RL Training Script

```python
#!/usr/bin/env python3
"""
Reinforcement Learning Training with Isaac Gym
Module 3 - Chapter 5

Train bipedal walking policy using PPO.
"""

import isaacgym
from isaacgym import gymtorch, gymapi
import torch
import torch.nn as nn
from torch.distributions import Normal
import numpy as np
from collections import deque
import time


class BipedalEnv:
    """Bipedal robot environment for RL training."""
    
    def __init__(self, num_envs=1024, device='cuda'):
        self.num_envs = num_envs
        self.device = device
        
        # Initialize gym
        self.gym = isaacgym.gymapi.acquire_gym()
        
        # Create environments
        self.envs = []
        self.actors = []
        self._create_envs()
        
        # Get state tensors
        self.root_states = self.gym.acquire_actor_root_state_tensor(self.sim)
        self.dof_states = self.gym.acquire_dof_state_tensor(self.sim)
        self.contact_states = self.gym.acquire_net_contact_force_tensor(self.sim)
        
        # Parse tensors
        self.root_states = gymtorch.wrap_tensor(self.root_states)
        self.dof_states = gymtorch.wrap_tensor(self.dof_states)
        self.contact_states = gymtorch.wrap_tensor(self.contact_states)
        
        # Action/observation dimensions
        self.num_obs = 48  # Joint positions, velocities, base orientation, etc.
        self.num_actions = 12  # Joint torques
        
        # Domain randomization
        self.randomize = True
    
    def _create_envs(self):
        """Create parallel environments."""
        # Load robot URDF
        asset_root = "assets"
        assetFile = "bipedal_robot.urdf"
        
        asset_options = gymapi.AssetOptions()
        asset_options.fix_base_link = False
        asset_options.default_dof_drive_mode = gymapi.DOF_MODE_POS
        
        robot_asset = self.gym.load_asset(self.sim, assetRoot, assetFile, asset_options)
        
        # Create environments
        for i in range(self.num_envs):
            env = self.gym.create_env(
                self.sim,
                gymapi.Vec3(-5, -5, 0),
                gymapi.Vec3(5, 5, 5),
                gymapi.Vec3(10, 10, 10)
            )
            
            # Add robot
            pose = gymapi.Transform()
            pose.p = gymapi.Vec3(0, 0, 1.0)
            pose.r = gymapi.Quat(0, 0, 0, 1)
            
            actor = self.gym.create_actor(env, robot_asset, pose, "robot", i, 0)
            
            self.envs.append(env)
            self.actors.append(actor)
    
    def reset(self):
        """Reset all environments."""
        # Randomize initial states
        self.root_states[:, 0:3] += torch.randn_like(self.root_states[:, 0:3]) * 0.1
        self.root_states[:, 7:13] = 0  # Zero velocity
        
        self.gym.set_actor_root_state_tensor(self.sim, self.root_states)
        
        # Get initial observations
        return self._get_observations()
    
    def step(self, actions):
        """
        Take action step.
        
        Args:
            actions: Tensor of shape (num_envs, num_actions)
        
        Returns:
            obs, rewards, dones, info
        """
        # Apply actions
        self.dof_states[:, 0:self.num_actions] = actions
        self.gym.set_dof_state_tensor(self.sim, self.dof_states)
        
        # Step simulation
        self.gym.simulate(self.sim)
        
        # Get new state
        self.gym.fetch_results(self.sim, True)
        self.gym.refresh_dof_state_tensor(self.sim)
        self.gym.refresh_actor_root_state_tensor(self.sim)
        
        # Compute rewards
        rewards = self._compute_reward()
        
        # Check dones (fallen)
        dones = self._check_dones()
        
        # Get observations
        obs = self._get_observations()
        
        return obs, rewards, dones, {}
    
    def _compute_reward(self):
        """Compute reward function."""
        rewards = torch.zeros(self.num_envs, device=self.device)
        
        # Reward for forward motion
        forward_vel = self.root_states[:, 7]  # X velocity
        rewards += 1.0 * torch.clamp(forward_vel, 0, 1.0)
        
        # Penalty for high torque
        torques = torch.abs(self.dof_states[:, 0:self.num_actions])
        rewards -= 0.0001 * torch.sum(torques, dim=1)
        
        # Penalty for falling
        base_height = self.root_states[:, 2]
        rewards -= 10.0 * (base_height < 0.5).float()
        
        # Reward for maintaining height
        rewards += 1.0 * torch.clamp(base_height - 0.8, 0, 0.2)
        
        return rewards
    
    def _check_dones(self):
        """Check if episodes are done (robot fell)."""
        base_height = self.root_states[:, 2]
        base_orientation = self.root_states[:, 3:7]
        
        # Done if too low or too tilted
        done_low = base_height < 0.3
        done_tilt = torch.abs(base_orientation[:, 0]) > 0.5
        
        dones = (done_low | done_tilt).float()
        return dones
    
    def _get_observations(self):
        """Get observations for policy."""
        obs = torch.cat([
            self.dof_states[:, 0:self.num_actions],  # Joint positions
            self.dof_states[:, self.num_actions:],    # Joint velocities
            self.root_states[:, 3:7],                 # Base orientation
            self.root_states[:, 10:13],               # Base angular velocity
        ], dim=-1)
        
        return obs


class PPOAgent:
    """PPO RL Agent."""
    
    def __init__(self, num_obs, num_actions, device='cuda'):
        self.device = device
        
        # Actor-Critic network
        self.actor = nn.Sequential(
            nn.Linear(num_obs, 256),
            nn.ELU(),
            nn.Linear(256, 128),
            nn.ELU(),
            nn.Linear(128, num_actions)
        ).to(device)
        
        self.critic = nn.Sequential(
            nn.Linear(num_obs, 256),
            nn.ELU(),
            nn.Linear(256, 128),
            nn.ELU(),
            nn.Linear(128, 1)
        ).to(device)
        
        # Action distribution
        self.log_std = nn.Parameter(torch.zeros(num_actions)).to(device)
        
        # Optimizers
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=3e-4)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=1e-3)
    
    def select_action(self, obs):
        """Select action using current policy."""
        mean = self.actor(obs)
        std = torch.exp(self.log_std)
        
        dist = Normal(mean, std)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum(dim=-1)
        
        return action, log_prob
    
    def evaluate(self, obs, actions):
        """Evaluate actions for PPO update."""
        mean = self.actor(obs)
        std = torch.exp(self.log_std)
        
        dist = Normal(mean, std)
        log_prob = dist.log_prob(actions).sum(dim=-1)
        entropy = dist.entropy().sum(dim=-1)
        
        value = self.critic(obs)
        
        return log_prob, entropy, value
    
    def update(self, obs, actions, old_log_probs, returns, advantages):
        """PPO update step."""
        # PPO parameters
        clip_epsilon = 0.2
        value_coef = 0.5
        entropy_coef = 0.01
        
        # Evaluate current policy
        log_probs, entropy, values = self.evaluate(obs, actions)
        
        # PPO loss
        ratio = torch.exp(log_probs - old_log_probs)
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1-clip_epsilon, 1+clip_epsilon) * advantages
        actor_loss = -torch.min(surr1, surr2).mean()
        
        # Critic loss
        critic_loss = ((returns - values) ** 2).mean()
        
        # Total loss
        loss = actor_loss + value_coef * critic_loss - entropy_coef * entropy.mean()
        
        # Update actor
        self.actor_optimizer.zero_grad()
        loss.backward()
        self.actor_optimizer.step()
        
        # Update critic
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        return loss.item()


def train_rl():
    """Main training loop."""
    # Parameters
    num_envs = 1024
    max_iterations = 1000
    steps_per_iter = 1000
    gamma = 0.99
    lam = 0.95
    
    # Initialize
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    env = BipedalEnv(num_envs=num_envs, device=device)
    agent = PPOAgent(num_obs=48, num_actions=12, device=device)
    
    # Training loop
    for iteration in range(max_iterations):
        # Collect trajectories
        obs_buffer = []
        action_buffer = []
        reward_buffer = []
        log_prob_buffer = []
        done_buffer = []
        
        obs = env.reset()
        
        for step in range(steps_per_iter):
            # Select action
            action, log_prob = agent.select_action(obs)
            
            # Step environment
            next_obs, reward, done, info = env.step(action)
            
            # Store
            obs_buffer.append(obs)
            action_buffer.append(action)
            reward_buffer.append(reward)
            log_prob_buffer.append(log_prob)
            done_buffer.append(done)
            
            obs = next_obs
        
        # Convert to tensors
        obs_batch = torch.cat(obs_buffer, dim=0)
        action_batch = torch.cat(action_buffer, dim=0)
        reward_batch = torch.cat(reward_buffer, dim=0)
        log_prob_batch = torch.cat(log_prob_buffer, dim=0)
        done_batch = torch.cat(done_buffer, dim=0)
        
        # Compute returns and advantages
        returns = compute_returns(reward_batch, done_batch, gamma)
        advantages = compute_advantages(reward_batch, done_batch, agent, gamma, lam)
        
        # Update policy
        loss = agent.update(obs_batch, action_batch, log_prob_batch, returns, advantages)
        
        # Log progress
        avg_reward = reward_batch.mean().item()
        print(f"Iteration {iteration}: Loss={loss:.3f}, Avg Reward={avg_reward:.3f}")
        
        # Save checkpoint
        if iteration % 100 == 0:
            torch.save({
                'actor': agent.actor.state_dict(),
                'critic': agent.critic.state_dict(),
                'iteration': iteration
            }, f'checkpoint_iter_{iteration}.pt')


def compute_returns(rewards, dones, gamma):
    """Compute discounted returns."""
    returns = []
    R = 0
    
    for reward, done in zip(reversed(rewards), reversed(dones)):
        R = reward + gamma * R * (1 - done)
        returns.insert(0, R)
    
    return torch.stack(returns)


def compute_advantages(rewards, dones, agent, gamma, lam):
    """Compute GAE advantages."""
    # Simplified implementation
    returns = compute_returns(rewards, dones, gamma)
    
    with torch.no_grad():
        values = agent.critic(torch.cat([rewards], dim=-1))
    
    advantages = returns - values.squeeze()
    
    return advantages


if __name__ == '__main__':
    train_rl()
```

### Example 2: Policy Deployment Script

```python
#!/usr/bin/env python3
"""
Deploy trained RL policy to real robot.
"""

import torch
import torch.nn as nn
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
import numpy as np


class DeployedPolicy(nn.Module):
    """Deployed policy network."""
    
    def __init__(self, num_obs=48, num_actions=12):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(num_obs, 256),
            nn.ELU(),
            nn.Linear(256, 128),
            nn.ELU(),
            nn.Linear(128, num_actions)
        )
    
    def forward(self, x):
        return self.network(x)


class PolicyExecutor(Node):
    """Execute RL policy on real robot."""
    
    def __init__(self):
        super().__init__('policy_executor')
        
        # Load policy
        self.policy = DeployedPolicy()
        checkpoint = torch.load('checkpoint_final.pt')
        self.policy.load_state_dict(checkpoint['actor'])
        self.policy.eval()
        
        # Subscribers
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )
        
        # Publishers
        self.cmd_pub = self.create_publisher(
            Float64MultiArray,
            '/joint_commands',
            10
        )
        
        # State
        self.joint_positions = None
        self.joint_velocities = None
        self.base_orientation = None
        
        self.get_logger().info('Policy Executor started')
    
    def joint_callback(self, msg: JointState):
        """Process joint state feedback."""
        self.joint_positions = np.array(msg.position)
        self.joint_velocities = np.array(msg.velocity)
        
        # Execute policy
        self.execute_policy()
    
    def execute_policy(self):
        """Execute policy to get actions."""
        if self.joint_positions is None:
            return
        
        # Build observation
        obs = np.concatenate([
            self.joint_positions,
            self.joint_velocities,
            # Add base orientation from IMU (placeholder)
            [0, 0, 0, 1],
            [0, 0, 0]
        ])
        
        # Convert to tensor
        obs_tensor = torch.FloatTensor(obs).unsqueeze(0)
        
        # Get action
        with torch.no_grad():
            action = self.policy(obs_tensor)
        
        # Publish command
        cmd_msg = Float64MultiArray()
        cmd_msg.data = action.numpy().flatten().tolist()
        self.cmd_pub.publish(cmd_msg)


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    executor = PolicyExecutor()
    
    try:
        rclpy.spin(executor)
    except KeyboardInterrupt:
        pass
    finally:
        executor.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Hands-on Lab

### Lab 5.1: Train Bipedal Walking with RL

**Objective**: Train a bipedal walking policy using Isaac Gym and PPO.

**Prerequisites**:
- Isaac Gym installed
- PyTorch with CUDA support
- Bipedal robot URDF model

**Duration**: 120 minutes

---

#### Step 1: Setup Isaac Gym Environment

```bash
# Install Isaac Gym
# Download from NVIDIA website

# Install dependencies
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
pip install numpy tensorboard
```

#### Step 2: Prepare Robot Model

```bash
# Copy robot URDF to assets folder
cp bipedal_robot.urdf ~/isaacgym/assets/

# Verify URDF is valid
check_urdf bipedal_robot.urdf
```

#### Step 3: Configure Training

Create `train_config.yaml`:

```yaml
env:
  num_envs: 1024
  num_obs: 48
  num_actions: 12

training:
  max_iterations: 1000
  steps_per_iter: 1000
  gamma: 0.99
  lam: 0.95
  lr_actor: 0.0003
  lr_critic: 0.001

policy:
  hidden_sizes: [256, 128]
  activation: elu

domain_randomization:
  enabled: true
  mass_range: [0.8, 1.2]
  friction_range: [0.5, 1.5]
```

#### Step 4: Run Training

```bash
# Start training
python3 train_rl.py --config train_config.yaml

# Monitor with TensorBoard
tensorboard --logdir=logs/
```

#### Step 5: Monitor Training Progress

```bash
# Watch training metrics
# Open http://localhost:6006 in browser

# Check reward progression
# Target: > 50 average reward
```

#### Step 6: Test Trained Policy

```bash
# Run policy in simulation
python3 test_policy.py --checkpoint checkpoint_iter_1000.pt

# Record video
python3 record_video.py --checkpoint checkpoint_final.pt
```

#### Step 7: Export Policy

```bash
# Export to ONNX format
python3 export_policy.py --checkpoint checkpoint_final.pt --output policy.onnx
```

**Expected Result**:

Bipedal robot learns to walk forward. Training reward increases over iterations. Policy exported for deployment.

## Summary

### Key Takeaways

1. **Reinforcement Learning** trains robots through trial and error with rewards

2. **Isaac Gym** enables GPU-accelerated parallel RL training (1000s of environments)

3. **PPO** is the standard algorithm for robotics RL

4. **Sim-to-Real Transfer** requires domain randomization and system identification

5. **Deployment** exports trained policy to ONNX for real robot execution

### Key Terms

| Term | Definition |
|------|------------|
| **RL** | Reinforcement Learning |
| **PPO** | Proximal Policy Optimization |
| **Isaac Gym** | GPU-accelerated RL training platform |
| **Domain Randomization** | Technique for sim-to-real transfer |
| **Policy** | Neural network mapping states to actions |
| **Reward Function** | Signal defining task objective |

## Exercises

### Exercise 5.1: Reward Function Design

1. Modify reward function components:
   - Forward velocity weight
   - Energy penalty
   - Stability penalty
2. **Train** policies with different weights
3. **Compare** walking quality
4. **Optimize** reward weights

### Exercise 5.2: Domain Randomization Study

1. Train with 3 randomization levels:
   - No randomization
   - Limited randomization
   - Full randomization
2. **Test** in perturbed simulation
3. **Measure** robustness
4. **Analyze** sim-to-real gap

### Exercise 5.3: Network Architecture

1. Experiment with network sizes:
   - Small: [64, 32]
   - Medium: [256, 128]
   - Large: [512, 256]
2. **Compare** sample efficiency
3. **Measure** final performance
4. **Analyze** compute requirements

### Exercise 5.4: Sim-to-Real Transfer

1. Train policy in simulation
2. Deploy to physical robot (or high-fidelity sim)
3. **Measure** performance degradation
4. **Implement** fine-tuning
5. **Document** transfer process

### Exercise 5.5: Research Assignment

Research **RL for humanoid robots**:

- Boston Dynamics Atlas
- Tesla Optimus
- Agility Robotics Digit
- Apptronik Apollo

**Write** a 600-word summary comparing RL approaches across 2 robots.

---

**Module 3 Complete!** 🎉

You have learned:
- NVIDIA Isaac platform for AI robotics
- Synthetic data generation
- Visual SLAM for localization
- Nav2 for autonomous navigation
- Reinforcement learning for robot control

**Next Module**: [Module 4 — Vision Language Action →](../module4/chapter1-vla-intro.md)
