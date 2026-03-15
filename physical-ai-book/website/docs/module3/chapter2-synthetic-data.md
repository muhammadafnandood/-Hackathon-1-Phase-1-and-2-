---
sidebar_label: '2. Synthetic Data & Simulation'
---

# Chapter 2: Synthetic Data and Simulation

## Learning Objectives

By the end of this chapter, you will be able to:

- Generate synthetic datasets using Isaac Sim
- Configure camera sensors (RGB, Depth, LiDAR) for data collection
- Understand domain randomization for sim-to-real transfer
- Create labeled datasets for perception training
- Implement data pipelines for robot learning

## Concept Explanation

### What is Synthetic Data?

**Synthetic data** is artificially generated data from simulation rather than real-world collection:

```
┌─────────────────────────────────────────────────────────────┐
│                  SYNTHETIC DATA GENERATION                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Real Data Collection          Synthetic Data                │
│  ────────────────────          ──────────────                │
│  • Physical robot                • Simulation                 │
│  • Real environment              • Virtual environment        │
│  • Time-consuming                • Instant generation         │
│  • Expensive                     • Low cost                   │
│  • Limited scenarios             • Infinite scenarios         │
│  • Manual labeling               • Auto-labeling              │
│  • Privacy concerns              • No privacy issues          │
│                                                              │
│  Synthetic Data Benefits:                                    │
│  ────────────────────────                                    │
│  • Perfect ground truth (depth, segmentation, pose)          │
│  • Controlled conditions (lighting, weather, occlusion)      │
│  • Rare event generation (edge cases)                        │
│  • Scalable data production                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Sensor Types in Isaac Sim

**Isaac Sim** provides multiple sensor types for data generation:

```
┌─────────────────────────────────────────────────────────────┐
│                    SENSOR TYPES                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  RGB Camera                                                  │
│  ───────────                                                 │
│  • Standard color images                                     │
│  • Configurable resolution, FPS                              │
│  • Used for: object detection, classification                │
│                                                              │
│  Depth Camera                                                │
│  ────────────                                                │
│  • Per-pixel distance measurement                            │
│  • Range: 0.1m - 100m                                        │
│  • Used for: 3D reconstruction, navigation                   │
│                                                              │
│  LiDAR                                                       │
│  ─────                                                         │
│  • 3D point cloud generation                                 │
│  • 360° or limited FOV                                       │
│  • Used for: mapping, obstacle detection                     │
│                                                              │
│  Segmentation Camera                                         │
│  ───────────────────                                         │
│  • Semantic segmentation masks                               │
│  • Instance segmentation                                     │
│  • Used for: scene understanding                             │
│                                                              │
│  Event Camera                                                │
│  ─────────────                                               │
│  • Neuromorphic vision sensor                                │
│  • High temporal resolution                                  │
│  • Used for: high-speed tracking                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Domain Randomization

**Domain randomization** is a technique to improve sim-to-real transfer:

```
┌─────────────────────────────────────────────────────────────┐
│                DOMAIN RANDOMIZATION                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Training in Simulation:                                     │
│  ──────────────────────                                      │
│  Randomize:                                                  │
│  • Lighting conditions (intensity, color, position)          │
│  • Textures (floor, walls, objects)                          │
│  • Object positions and orientations                         │
│  • Camera parameters (noise, exposure)                       │
│  • Physics parameters (friction, mass)                       │
│  • Background clutter                                        │
│                                                              │
│  Result:                                                     │
│  ───────                                                     │
│  • Model learns invariant features                           │
│  • Robust to real-world variations                           │
│  • Better generalization                                     │
│                                                              │
│  Example:                                                    │
│  ───────                                                     │
│  Train object detector with:                                 │
│  • 1000 different lighting conditions                        │
│  • 500 different textures                                    │
│  • Random object placements                                  │
│  → Model works in real world without fine-tuning            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Pipeline Architecture

**Complete synthetic data pipeline:**

```
┌─────────────────────────────────────────────────────────────┐
│              SYNTHETIC DATA PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Scene Setup                                              │
│     ────────────                                             │
│     • Import 3D models (USD format)                         │
│     • Configure lighting                                    │
│     • Set up cameras                                        │
│                                                              │
│  2. Data Generation                                          │
│     ────────────────                                         │
│     • Randomize scene parameters                            │
│     • Capture sensor data                                   │
│     • Save with metadata                                    │
│                                                              │
│  3. Data Storage                                             │
│     ────────────                                             │
│     • Organize by scenario                                  │
│     • Store annotations                                     │
│     • Version control                                       │
│                                                              │
│  4. Data Augmentation                                        │
│     ──────────────────                                       │
│     • Flip, rotate, scale                                   │
│     • Color jitter                                          │
│     • Add noise                                             │
│                                                              │
│  5. Model Training                                           │
│     ───────────────                                          │
│     • Train perception models                               │
│     • Validate on real data                                 │
│     • Iterate and improve                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Real Robotics Example

### Tesla Autopilot Synthetic Data

Tesla uses synthetic data for **Autopilot vision training**:

```
┌────────────────────────────────────────────────────────┐
│         TESLA AUTOPILOT DATA GENERATION                 │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Synthetic Data Types:                                  │
│  ──────────────────────                                 │
│  • Rare scenarios (accidents, extreme weather)         │
│  • Edge cases (unusual vehicles, obstacles)            │
│  • Adversarial examples (tricky lighting)              │
│                                                         │
│  Generation Process:                                    │
│  ──────────────────                                     │
│  1. Create 3D scene of road environment                │
│  2. Place vehicles, pedestrians, obstacles             │
│  3. Vary lighting, weather, time of day                │
│  4. Render from multiple camera angles                 │
│  5. Generate perfect labels (bounding boxes, etc.)     │
│                                                         │
│  Scale:                                                 │
│  ─────                                                    │
│  • Millions of synthetic images                        │
│  • Thousands of scenarios                              │
│  • Continuous generation                               │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Architecture Overview

### Synthetic Data Generation System

```
┌─────────────────────────────────────────────────────────────┐
│          SYNTHETIC DATA GENERATION SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  Scenario    │                                           │
│  │  Generator   │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Isaac Sim   │───►│   Sensors    │───►│   Capture    │  │
│  │  Environment │    │  (Cameras)   │    │   Engine     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                              │               │
│                                              ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Dataset     │◄───│  Annotation  │◄───│   Storage    │  │
│  │  (COCO)      │    │   Export     │    │   (HDF5)     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Example 1: Synthetic Data Generation Script

```python
#!/usr/bin/env python3
"""
Synthetic Data Generation with Isaac Sim
Module 3 - Chapter 2

Generates labeled image dataset for object detection.
"""

import omni.isaac.core
from omni.isaac.core import SimulationContext
from omni.isaac.core.utils.stage import open_stage
from omni.isaac.core.utils.prims import define_prim
from omni.isaac.sensor import Camera
import numpy as np
import json
import os
from datetime import datetime


class SyntheticDataGenerator:
    """Generate synthetic dataset with Isaac Sim."""
    
    def __init__(self, output_dir='./synthetic_dataset'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'annotations'), exist_ok=True)
        
        # Dataset metadata
        self.annotations = {
            'images': [],
            'annotations': [],
            'categories': [
                {'id': 1, 'name': 'box'},
                {'id': 2, 'name': 'cylinder'},
                {'id': 3, 'name': 'sphere'}
            ]
        }
        self.image_id = 0
        self.annotation_id = 0
    
    def setup_scene(self):
        """Setup Isaac Sim scene."""
        # Open stage
        open_stage("omniverse://nucleus/Isaac/Isaac/Samples/ROS2/Scenario/simple_world.usd")
        
        # Create camera
        self.camera = Camera(
            prim_path="/World/Camera",
            position=[0, 0, 2],
            orientation=[0, 0, 0, 1],
            frequency=30
        )
        
        # Configure camera
        self.camera.set_focal_length(24)
        self.camera.set_focus_distance(1.0)
    
    def randomize_scene(self):
        """Randomize scene parameters for domain randomization."""
        # Random lighting
        # (Implementation depends on specific scene setup)
        
        # Random object positions
        # (Implementation depends on objects in scene)
        
        # Random textures
        # (Implementation depends on material system)
        
        pass
    
    def capture_frame(self):
        """Capture single frame with annotations."""
        # Get RGB image
        rgb_image = self.camera.get_rgba()
        
        # Get depth image
        depth_image = self.camera.get_depth()
        
        # Get segmentation
        segmentation = self.camera.get_semantic_segmentation()
        
        # Save images
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        rgb_path = os.path.join(self.output_dir, 'images', f'{timestamp}_rgb.png')
        depth_path = os.path.join(self.output_dir, 'images', f'{timestamp}_depth.png')
        seg_path = os.path.join(self.output_dir, 'images', f'{timestamp}_seg.png')
        
        # Save (implementation depends on image format)
        # ...
        
        # Create annotation
        annotation = {
            'image_id': self.image_id,
            'file_name': f'{timestamp}_rgb.png',
            'width': rgb_image.shape[1],
            'height': rgb_image.shape[0],
            'depth_file': f'{timestamp}_depth.png',
            'seg_file': f'{timestamp}_seg.png',
            'objects': []  # Extract from segmentation
        }
        
        self.annotations['images'].append(annotation)
        self.image_id += 1
        
        return annotation
    
    def generate_dataset(self, num_frames=1000):
        """Generate complete dataset."""
        print(f"Generating {num_frames} frames...")
        
        for i in range(num_frames):
            # Randomize scene
            self.randomize_scene()
            
            # Step simulation
            omni.isaac.core.utils.viewports.set_camera_view()
            
            # Capture frame
            annotation = self.capture_frame()
            
            if i % 100 == 0:
                print(f"Progress: {i}/{num_frames}")
        
        # Save annotations
        with open(os.path.join(self.output_dir, 'annotations', 'dataset.json'), 'w') as f:
            json.dump(self.annotations, f, indent=2)
        
        print(f"Dataset saved to {self.output_dir}")


def main():
    """Main entry point."""
    generator = SyntheticDataGenerator(output_dir='./synthetic_dataset')
    
    # Initialize
    sim = SimulationContext()
    generator.setup_scene()
    sim.reset()
    
    # Generate
    generator.generate_dataset(num_frames=1000)
    
    sim.stop()


if __name__ == '__main__':
    main()
```

### Example 2: Domain Randomization Configuration

```python
#!/usr/bin/env python3
"""
Domain Randomization Configuration
Define parameters to randomize for sim-to-real transfer.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class LightingRandomization:
    """Randomize lighting conditions."""
    intensity_range: tuple = (0.5, 2.0)  # Multiplier
    color_temperature_range: tuple = (3000, 6500)  # Kelvin
    position_offset: tuple = (-2.0, 2.0)  # Meters
    shadow_enabled: bool = True


@dataclass
class TextureRandomization:
    """Randomize surface textures."""
    floor_materials: List[str] = None
    wall_materials: List[str] = None
    object_materials: List[str] = None
    
    def __post_init__(self):
        if self.floor_materials is None:
            self.floor_materials = ['concrete', 'tile', 'wood', 'carpet']
        if self.wall_materials is None:
            self.wall_materials = ['paint', 'brick', 'drywall']
        if self.object_materials is None:
            self.object_materials = ['metal', 'plastic', 'rubber']


@dataclass
class ObjectRandomization:
    """Randomize object properties."""
    position_range: tuple = (-5.0, 5.0)  # Meters
    rotation_range: tuple = (0, 360)  # Degrees
    scale_range: tuple = (0.8, 1.2)  # Multiplier


@dataclass
class CameraRandomization:
    """Randomize camera parameters."""
    noise_std: float = 0.01  # Gaussian noise
    exposure_range: tuple = (0.5, 2.0)
    focal_length_range: tuple = (20, 35)  # mm
    position_jitter: float = 0.05  # Meters


class DomainRandomizer:
    """Apply domain randomization to scene."""
    
    def __init__(self, config: Dict):
        self.lighting_config = LightingRandomization(**config.get('lighting', {}))
        self.texture_config = TextureRandomization(**config.get('texture', {}))
        self.object_config = ObjectRandomization(**config.get('object', {}))
        self.camera_config = CameraRandomization(**config.get('camera', {}))
    
    def randomize_lighting(self, light_prim):
        """Apply random lighting."""
        intensity = np.random.uniform(*self.lighting_config.intensity_range)
        # Apply to light primitive
        # light_prim.GetAttribute('intensity').Set(intensity)
    
    def randomize_textures(self):
        """Apply random textures."""
        floor_mat = np.random.choice(self.texture_config.floor_materials)
        wall_mat = np.random.choice(self.texture_config.wall_materials)
        # Apply materials to scene
    
    def randomize_objects(self, object_prims):
        """Apply random object transformations."""
        for prim in object_prims:
            # Random position
            x = np.random.uniform(*self.object_config.position_range)
            y = np.random.uniform(*self.object_config.position_range)
            # Random rotation
            rot_z = np.random.uniform(*self.object_config.rotation_range)
            # Apply transformation
            # prim.SetTranslation([x, y, 0])
            # prim.SetRotation([0, 0, rot_z])
    
    def apply_all(self, scene_elements):
        """Apply all randomization to scene."""
        self.randomize_lighting(scene_elements.get('light'))
        self.randomize_textures()
        self.randomize_objects(scene_elements.get('objects', []))


# Example usage
if __name__ == '__main__':
    config = {
        'lighting': {
            'intensity_range': (0.5, 2.0),
            'color_temperature_range': (3000, 6500)
        },
        'texture': {
            'floor_materials': ['concrete', 'tile', 'wood']
        },
        'object': {
            'position_range': (-3.0, 3.0)
        },
        'camera': {
            'noise_std': 0.01
        }
    }
    
    randomizer = DomainRandomizer(config)
    # randomizer.apply_all(scene_elements)
```

### Example 3: Dataset Export to COCO Format

```python
#!/usr/bin/env python3
"""
Export synthetic dataset to COCO format for training.
"""

import json
import os
from typing import Dict, List


class COCOExporter:
    """Export dataset to COCO format."""
    
    def __init__(self):
        self.dataset = {
            'info': {},
            'licenses': [],
            'images': [],
            'annotations': [],
            'categories': []
        }
    
    def add_image(self, image_info: Dict):
        """Add image to dataset."""
        self.dataset['images'].append(image_info)
    
    def add_annotation(self, annotation: Dict):
        """Add annotation to dataset."""
        self.dataset['annotations'].append(annotation)
    
    def add_category(self, category: Dict):
        """Add category to dataset."""
        self.dataset['categories'].append(category)
    
    def save(self, output_path: str):
        """Save dataset to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(self.dataset, f, indent=2)
        print(f"Dataset saved to {output_path}")


def convert_to_coco(isaac_annotations: Dict, output_path: str):
    """Convert Isaac Sim annotations to COCO format."""
    exporter = COCOExporter()
    
    # Add info
    exporter.dataset['info'] = {
        'description': 'Synthetic dataset from Isaac Sim',
        'version': '1.0',
        'year': 2024
    }
    
    # Add categories
    for cat in isaac_annotations['categories']:
        exporter.add_category(cat)
    
    # Add images and annotations
    for image in isaac_annotations['images']:
        exporter.add_image({
            'id': image['image_id'],
            'file_name': image['file_name'],
            'width': image['width'],
            'height': image['height']
        })
        
        # Convert object annotations to COCO format
        for obj in image.get('objects', []):
            exporter.add_annotation({
                'id': obj['id'],
                'image_id': image['image_id'],
                'category_id': obj['category_id'],
                'bbox': obj['bbox'],  # [x, y, width, height]
                'area': obj['bbox'][2] * obj['bbox'][3],
                'iscrowd': 0
            })
    
    exporter.save(output_path)


if __name__ == '__main__':
    # Load Isaac annotations
    with open('synthetic_dataset/annotations/dataset.json', 'r') as f:
        isaac_data = json.load(f)
    
    # Convert
    convert_to_coco(isaac_data, 'synthetic_dataset/annotations/coco_format.json')
```

## Hands-on Lab

### Lab 2.1: Generate Synthetic Dataset

**Objective**: Create a synthetic dataset for humanoid robot perception using Isaac Sim.

**Prerequisites**:
- Isaac Sim installed (Chapter 1)
- Python 3.8+
- NumPy, OpenCV installed

**Duration**: 90 minutes

---

#### Step 1: Setup Data Generation Script

Create `generate_data.py`:

```python
# Copy Example 1 from above
```

#### Step 2: Configure Domain Randomization

Create `randomization_config.yaml`:

```yaml
lighting:
  intensity_range: [0.5, 2.0]
  color_temperature_range: [3000, 6500]

texture:
  floor_materials: [concrete, tile, wood, carpet]
  wall_materials: [paint, brick, drywall]

object:
  position_range: [-3.0, 3.0]
  rotation_range: [0, 360]

camera:
  noise_std: 0.01
  exposure_range: [0.5, 2.0]
```

#### Step 3: Run Data Generation

```bash
# Generate 1000 frames
python3 generate_data.py --num-frames 1000 --config randomization_config.yaml
```

#### Step 4: Verify Dataset

```bash
# Check output structure
ls -la synthetic_dataset/
ls -la synthetic_dataset/images/ | head
cat synthetic_dataset/annotations/dataset.json | head -50
```

#### Step 5: Visualize Dataset

```python
import cv2
import json
import matplotlib.pyplot as plt

# Load annotations
with open('synthetic_dataset/annotations/dataset.json') as f:
    data = json.load(f)

# Display sample images
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

for i, image in enumerate(data['images'][:4]):
    img = cv2.imread(f"synthetic_dataset/images/{image['file_name']}")
    axes[i//2, i%2].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[i//2, i%2].set_title(image['file_name'])

plt.tight_layout()
plt.savefig('dataset_samples.png')
```

**Expected Result**:

Dataset with 1000+ images, depth maps, segmentation masks, and COCO-format annotations.

## Summary

### Key Takeaways

1. **Synthetic Data** enables scalable, labeled dataset generation for robot perception

2. **Domain Randomization** improves sim-to-real transfer by training on varied conditions

3. **Isaac Sim Sensors** provide RGB, depth, segmentation, and LiDAR data

4. **COCO Format** is standard for object detection datasets

5. **Data Pipelines** automate generation, storage, and export

### Key Terms

| Term | Definition |
|------|------------|
| **Synthetic Data** | Artificially generated data from simulation |
| **Domain Randomization** | Technique to improve sim-to-real transfer |
| **COCO Format** | Standard dataset format for object detection |
| **Semantic Segmentation** | Per-pixel class labeling |
| **Instance Segmentation** | Per-pixel object instance labeling |

## Exercises

### Exercise 2.1: Dataset Analysis

1. Generate 1000 synthetic images
2. **Analyze** distribution of:
   - Object sizes
   - Lighting conditions
   - Camera distances
3. **Plot** histograms
4. **Report** findings

### Exercise 2.2: Domain Randomization Study

1. Train object detector with 3 randomization levels:
   - No randomization
   - Limited randomization
   - Full randomization
2. **Test** on real images
3. **Compare** accuracy
4. **Document** results

### Exercise 2.3: Multi-Sensor Dataset

1. Generate dataset with:
   - RGB camera
   - Depth camera
   - LiDAR
2. **Synchronize** data streams
3. **Export** in unified format
4. **Visualize** all modalities

### Exercise 2.4: Data Augmentation

1. Apply augmentations to synthetic data:
   - Random flip
   - Color jitter
   - Gaussian noise
   - Occlusion
2. **Measure** impact on training
3. **Compare** with and without augmentation

### Exercise 2.5: Research Question

Research **synthetic data for robotics**:

- What companies use synthetic data?
- What are the limitations?
- How much real data is needed for fine-tuning?

**Write** a 500-word summary with examples.

---

**Next Chapter**: [Chapter 3 — Visual SLAM →](./chapter3-visual-slam.md)
