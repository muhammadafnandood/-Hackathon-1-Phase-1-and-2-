/**
 * Topic Images Data
 * Maps topic keywords to relevant image URLs for the Visual Guide section
 * 
 * All images should be publicly available and properly licensed.
 * For production, replace with your own hosted images or licensed stock photos.
 */

export interface TopicImage {
  id: string;
  topic: string;
  url: string;
  alt: string;
  caption: string;
  source?: string;
}

export const topicImages: Record<string, TopicImage> = {
  // ROS 2 Architecture
  "ros2_architecture": {
    id: "ros2_arch_001",
    topic: "ROS 2 architecture",
    url: "https://docs.ros.org/en/rolling/_images/ros2-architecture.png",
    alt: "ROS 2 Architecture Diagram",
    caption: "ROS 2 layered architecture showing DDS middleware",
    source: "ROS 2 Documentation"
  },
  
  // ROS 2 Nodes
  "ros2_nodes": {
    id: "ros2_nodes_001",
    topic: "ROS 2 nodes",
    url: "https://docs.ros.org/en/rolling/_images/turtlesim_nodes.png",
    alt: "ROS 2 Nodes Communication",
    caption: "ROS 2 nodes communicating through topics",
    source: "ROS 2 Documentation"
  },
  
  // ROS 2 Topics
  "ros2_topics": {
    id: "ros2_topics_001",
    topic: "ROS 2 topics",
    url: "https://docs.ros.org/en/rolling/_images/publish_subscribe.png",
    alt: "Publish-Subscribe Pattern",
    caption: "ROS 2 publish-subscribe communication pattern",
    source: "ROS 2 Documentation"
  },
  
  // URDF
  "urdf": {
    id: "urdf_001",
    topic: "URDF",
    url: "https://classic.gazebosim.org/tutorials/tutorials/urdf_start/images/urdf_visualization.png",
    alt: "URDF Robot Model",
    caption: "URDF robot description visualization",
    source: "Gazebo Tutorials"
  },
  
  // Gazebo Simulation
  "gazebo_simulation": {
    id: "gazebo_001",
    topic: "Gazebo simulation",
    url: "https://classic.gazebosim.org/tutorials/tutorials/gazebo_basics/images/gazebo_screenshot.png",
    alt: "Gazebo Simulation Environment",
    caption: "Robot simulation in Gazebo",
    source: "Gazebo"
  },
  
  // NVIDIA Isaac Sim
  "nvidia_isaac": {
    id: "isaac_001",
    topic: "NVIDIA Isaac",
    url: "https://developer.nvidia.com/assets/isaac-sim-screenshot.png",
    alt: "NVIDIA Isaac Sim",
    caption: "Isaac Sim photorealistic robot simulation",
    source: "NVIDIA"
  },
  
  // SLAM
  "slam": {
    id: "slam_001",
    topic: "SLAM",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/SLAM_example.png/640px-SLAM_example.png",
    alt: "SLAM Map Visualization",
    caption: "SLAM-generated environment map",
    source: "Wikimedia Commons"
  },
  
  // LiDAR
  "lidar": {
    id: "lidar_001",
    topic: "LiDAR",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Lidar_point_cloud.jpg/640px-Lidar_point_cloud.jpg",
    alt: "LiDAR Point Cloud",
    caption: "LiDAR point cloud data visualization",
    source: "Wikimedia Commons"
  },
  
  // Humanoid Robot
  "humanoid_robot": {
    id: "humanoid_001",
    topic: "humanoid robot",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/ASIMO.jpg/360px-ASIMO.jpg",
    alt: "Humanoid Robot",
    caption: "ASIMO humanoid robot by Honda",
    source: "Wikimedia Commons"
  },
  
  // Bipedal Locomotion
  "bipedal_locomotion": {
    id: "bipedal_001",
    topic: "bipedal locomotion",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Bipedal_robot_walking.jpg/640px-Bipedal_robot_walking.jpg",
    alt: "Bipedal Robot Walking",
    caption: "Bipedal robot demonstrating walking gait",
    source: "Wikimedia Commons"
  },
  
  // RealSense Camera
  "realsense_camera": {
    id: "realsense_001",
    topic: "RealSense camera",
    url: "https://www.intelrealsense.com/wp-content/uploads/2020/06/d435i-product-image.jpg",
    alt: "Intel RealSense D435i",
    caption: "Intel RealSense D435i depth camera",
    source: "Intel"
  },
  
  // Jetson Orin
  "jetson_orin": {
    id: "jetson_001",
    topic: "Jetson Orin",
    url: "https://developer.nvidia.com/assets/jetson-orin-agx.jpg",
    alt: "NVIDIA Jetson Orin",
    caption: "NVIDIA Jetson Orin AGX developer kit",
    source: "NVIDIA"
  },
  
  // Nav2
  "nav2": {
    id: "nav2_001",
    topic: "Nav2",
    url: "https://navigation.ros.org/_images/nav2_stack.png",
    alt: "Nav2 Navigation Stack",
    caption: "ROS 2 Nav2 navigation architecture",
    source: "ROS 2 Navigation"
  },
  
  // VLA Model
  "vla_model": {
    id: "vla_001",
    topic: "VLA model",
    url: "https://www.google.com/static/intl/en_us/ai/images/vla-diagram.png",
    alt: "Vision-Language-Action Model",
    caption: "VLA model architecture for robotics",
    source: "Google AI"
  },
  
  // Whisper
  "whisper": {
    id: "whisper_001",
    topic: "Whisper",
    url: "https://openai.com/content/images/whisper-architecture.png",
    alt: "Whisper Speech Recognition",
    caption: "OpenAI Whisper speech recognition architecture",
    source: "OpenAI"
  },
  
  // Transformer Architecture
  "transformer_architecture": {
    id: "transformer_001",
    topic: "transformer architecture",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/The_Transformer_model.png/640px-The_Transformer_model.png",
    alt: "Transformer Architecture",
    caption: "Transformer model architecture diagram",
    source: "Wikimedia Commons"
  },
  
  // Additional Topics
  
  // IMU Sensor
  "imu": {
    id: "imu_001",
    topic: "IMU",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/IMU_sensor.jpg/640px-IMU_sensor.jpg",
    alt: "IMU Sensor",
    caption: "Inertial Measurement Unit (IMU) sensor",
    source: "Wikimedia Commons"
  },
  
  // Motor Controller
  "motor_controller": {
    id: "motor_001",
    topic: "motor controller",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Motor_controller.jpg/640px-Motor_controller.jpg",
    alt: "Motor Controller",
    caption: "Robot motor controller board",
    source: "Wikimedia Commons"
  },
  
  // Depth Camera
  "depth_camera": {
    id: "depth_001",
    topic: "depth camera",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Depth_camera.jpg/640px-Depth_camera.jpg",
    alt: "Depth Camera",
    caption: "RGB-D depth sensing camera",
    source: "Wikimedia Commons"
  },
  
  // Robot Arm
  "robot_arm": {
    id: "arm_001",
    topic: "robot arm",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Robot_arm.jpg/640px-Robot_arm.jpg",
    alt: "Robot Arm",
    caption: "6-DOF robotic manipulator arm",
    source: "Wikimedia Commons"
  },
  
  // Path Planning
  "path_planning": {
    id: "path_001",
    topic: "path planning",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Path_planning.png/640px-Path_planning.png",
    alt: "Path Planning",
    caption: "Robot path planning visualization",
    source: "Wikimedia Commons"
  },
  
  // Computer Vision
  "computer_vision": {
    id: "vision_001",
    topic: "computer vision",
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Computer_vision_example.jpg/640px-Computer_vision_example.jpg",
    alt: "Computer Vision",
    caption: "Object detection and recognition",
    source: "Wikimedia Commons"
  },
};

/**
 * Get image for a given topic keyword
 * @param keyword - The topic keyword to search for
 * @returns Matching TopicImage or undefined
 */
export function getImageForTopic(keyword: string): TopicImage | undefined {
  const normalizedKeyword = keyword.toLowerCase().replace(/[\s-]/g, '_');
  
  // Direct match
  if (topicImages[normalizedKeyword]) {
    return topicImages[normalizedKeyword];
  }
  
  // Partial match
  for (const [key, image] of Object.entries(topicImages)) {
    if (key.includes(normalizedKeyword) || normalizedKeyword.includes(key)) {
      return image;
    }
  }
  
  return undefined;
}

/**
 * Get all images matching multiple keywords
 * @param keywords - Array of topic keywords
 * @returns Array of matching TopicImages (max 6)
 */
export function getImagesForTopics(keywords: string[]): TopicImage[] {
  const matched: TopicImage[] = [];
  const seenIds = new Set<string>();
  
  for (const keyword of keywords) {
    const image = getImageForTopic(keyword);
    if (image && !seenIds.has(image.id)) {
      matched.push(image);
      seenIds.add(image.id);
    }
    
    if (matched.length >= 6) {
      break;
    }
  }
  
  return matched;
}

export default topicImages;
