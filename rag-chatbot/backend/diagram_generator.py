#!/usr/bin/env python3
"""
Diagram Generator Agent

Automatically generates Mermaid diagrams for robotics and AI concepts.
Creates Docusaurus-compatible markdown with embedded Mermaid diagrams.
"""

import re
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


class DiagramType(Enum):
    """Types of diagrams supported."""
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    CLASS = "class"
    STATE = "state"
    ER = "er"
    GANTT = "gantt"
    PIE = "pie"


class ArchitectureType(Enum):
    """Predefined architecture types."""
    ROS2_PUBLISHER_SUBSCRIBER = "ros2_pubsub"
    ROS2_SERVICE_CLIENT = "ros2_service"
    ROS2_NODE_ARCHITECTURE = "ros2_node"
    RAG_PIPELINE = "rag_pipeline"
    RAG_ARCHITECTURE = "rag_architecture"
    ROBOT_PERCEPTION = "robot_perception"
    ROBOT_CONTROL_LOOP = "robot_control"
    VLA_MODEL = "vla_model"
    VLA_WORKFLOW = "vla_workflow"
    SLAM_PIPELINE = "slam_pipeline"
    NAVIGATION_STACK = "navigation"
    SENSOR_FUSION = "sensor_fusion"
    CUSTOM = "custom"


@dataclass
class DiagramConfig:
    """Configuration for diagram generation."""
    diagram_type: DiagramType = DiagramType.FLOWCHART
    direction: str = "TD"  # TD, BT, LR, RL
    title: str = ""
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    edges: List[Dict[str, Any]] = field(default_factory=list)
    subgraphs: List[Dict[str, Any]] = field(default_factory=list)
    styles: Dict[str, str] = field(default_factory=dict)
    classes: Dict[str, str] = field(default_factory=dict)


@dataclass
class GeneratedDiagram:
    """Result of diagram generation."""
    mermaid_code: str
    diagram_type: str
    title: str
    description: str
    node_count: int
    architecture_type: ArchitectureType


class MermaidDiagramGenerator:
    """
    Generates Mermaid diagrams for robotics and AI concepts.
    """
    
    # Color palettes for different component types
    COLOR_PALETTES = {
        "ros2": {
            "node": "#4CAF50",
            "topic": "#FF9800",
            "service": "#2196F3",
            "message": "#9C27B0",
            "default": "#607D8B",
        },
        "rag": {
            "user": "#E3F2FD",
            "embedding": "#FFF3E0",
            "database": "#E8F5E9",
            "llm": "#F3E5F5",
            "output": "#FFEBEE",
        },
        "robotics": {
            "sensor": "#4CAF50",
            "processing": "#2196F3",
            "control": "#FF9800",
            "actuator": "#F44336",
            "environment": "#9E9E9E",
        },
        "vla": {
            "vision": "#4CAF50",
            "language": "#2196F3",
            "fusion": "#FF9800",
            "action": "#F44336",
        },
    }
    
    def __init__(self):
        """Initialize the diagram generator."""
        self.default_direction = "TD"
        self.default_style = """
    style {{fill: transparent, stroke: #333, stroke-width: 1px}}
"""
    
    def _create_node(self, id: str, label: str, shape: str = "rect") -> str:
        """Create a node definition."""
        shapes = {
            "rect": f"[{label}]",
            "rounded": f"({label})",
            "circle": f"(({label}))",
            "diamond": f"{{{label}}}",
            "hexagon": f"{{{{{label}}}}}",
            "trapezoid": f"[/{label}/]",
            "cylinder": f"[({label})]",
        }
        return f"    {id}{shapes.get(shape, f'[{label}]')}"
    
    def _create_edge(self, source: str, target: str, 
                     label: str = "", style: str = "solid") -> str:
        """Create an edge definition."""
        styles = {
            "solid": "-->",
            "dashed": "-.->",
            "dotted": "-.->",
            "thick": "==>",
            "bidirectional": "<-->",
        }
        edge_style = styles.get(style, "-->")
        
        if label:
            return f"    {source} {edge_style}|{label}| {target}"
        return f"    {source} {edge_style} {target}"
    
    def _create_subgraph(self, id: str, title: str, 
                         nodes: List[str], direction: str = "") -> str:
        """Create a subgraph definition."""
        lines = [f"    subgraph {id}[\"{title}\"]"]
        if direction:
            lines.append(f"        direction {direction}")
        for node in nodes:
            lines.append(f"        {node}")
        lines.append("    end")
        return "\n".join(lines)
    
    def _apply_style(self, node_id: str, color: str, 
                     text_color: str = "#fff") -> str:
        """Create a style definition."""
        return f"    style {node_id} fill:{color},color:{text_color}"
    
    def generate_ros2_pubsub_diagram(self) -> GeneratedDiagram:
        """Generate ROS 2 Publisher-Subscriber architecture diagram."""
        mermaid = """graph LR
    subgraph ROS2_Network["ROS 2 Network"]
        direction LR
        
        subgraph Node1["Node 1"]
            P1[Publisher]
        end
        
        subgraph Node2["Node 2"]
            S1[Subscriber]
        end
        
        subgraph Node3["Node 3"]
            S2[Subscriber]
        end
        
        T[("Topic: /sensor_data")]
    end
    
    P1 -->|Publishes| T
    T -->|Subscribes| S1
    T -->|Subscribes| S2
    
    style Node1 fill:#4CAF50,color:#fff
    style Node2 fill:#2196F3,color:#fff
    style Node3 fill:#2196F3,color:#fff
    style T fill:#FF9800,color:#fff
    style P1 fill:#81C784
    style S1 fill:#64B5F6
    style S2 fill:#64B5F6"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="ROS 2 Publisher-Subscriber Pattern",
            description="Shows how multiple nodes can publish and subscribe to topics in ROS 2",
            node_count=7,
            architecture_type=ArchitectureType.ROS2_PUBLISHER_SUBSCRIBER,
        )
    
    def generate_ros2_service_diagram(self) -> GeneratedDiagram:
        """Generate ROS 2 Service-Client architecture diagram."""
        mermaid = """sequenceDiagram
    participant Client as Client Node
    participant Service as Service Node
    
    Client->>Service: Service Request
    Note over Service: Processing...
    Service-->>Client: Service Response
    
    rect rgb(200, 230, 255)
        Note over Client,Service: Synchronous Communication
    end"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="sequence",
            title="ROS 2 Service-Client Pattern",
            description="Shows synchronous request-response communication in ROS 2",
            node_count=2,
            architecture_type=ArchitectureType.ROS2_SERVICE_CLIENT,
        )
    
    def generate_rag_pipeline_diagram(self) -> GeneratedDiagram:
        """Generate RAG chatbot pipeline diagram."""
        mermaid = """graph TD
    User[("User Query")] --> Embed[Embedding Model]
    
    subgraph Retrieval["Retrieval Phase"]
        Embed --> Search[("Vector Search<br/>Qdrant")]
        Search --> Rank[Rank Results]
        Rank --> Retrieve[Retrieve Top-K Chunks]
    end
    
    subgraph Generation["Generation Phase"]
        Retrieve --> Context[Build Context]
        Context --> Prompt[Construct Prompt]
        Prompt --> LLM[("LLM<br/>GPT")]
        LLM --> Answer[Generate Answer]
    end
    
    Answer --> Output[("Response + Sources")]
    
    style User fill:#E3F2FD
    style Embed fill:#FFF3E0
    style Retrieval fill:#E8F5E9
    style Generation fill:#F3E5F5
    style LLM fill:#FFEBEE
    style Output fill:#E0F2F1"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="RAG Chatbot Pipeline",
            description="Complete flow from user query to generated answer with sources",
            node_count=11,
            architecture_type=ArchitectureType.RAG_PIPELINE,
        )
    
    def generate_rag_architecture_diagram(self) -> GeneratedDiagram:
        """Generate RAG system architecture diagram."""
        mermaid = """graph LR
    subgraph Frontend["Frontend"]
        UI[User Interface]
        Chat[Chat Component]
    end
    
    subgraph Backend["Backend API"]
        API[FastAPI Server]
        RAG[RAG Pipeline]
    end
    
    subgraph Data["Data Layer"]
        Qdrant[("Qdrant<br/>Vector DB")]
        Docs[Document Store]
    end
    
    subgraph External["External Services"]
        OpenAI[("OpenAI<br/>API")]
    end
    
    UI --> Chat
    Chat --> API
    API --> RAG
    RAG --> Qdrant
    RAG --> OpenAI
    
    style Frontend fill:#E3F2FD
    style Backend fill:#FFF3E0
    style Data fill:#E8F5E9
    style External fill:#FCE4EC"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="RAG System Architecture",
            description="High-level architecture showing all components and their relationships",
            node_count=9,
            architecture_type=ArchitectureType.RAG_ARCHITECTURE,
        )
    
    def generate_robot_perception_diagram(self) -> GeneratedDiagram:
        """Generate robot perception pipeline diagram."""
        mermaid = """graph TD
    subgraph Sensors["Sensors"]
        Camera[("Camera<br/>RGB-D")]
        LiDAR[("LiDAR<br/>3D Points")]
        IMU[("IMU<br/>Orientation")]
    end
    
    subgraph Preprocessing["Preprocessing"]
        Calib[Sensor Calibration]
        Filter[Noise Filtering]
        Sync[Time Synchronization]
    end
    
    subgraph Fusion["Sensor Fusion"]
        Fuse[Data Fusion]
        Localize[Localization]
    end
    
    subgraph Perception["Perception"]
        Detect[Object Detection]
        Segment[Semantic Segmentation]
        Track[Multi-Object Tracking]
    end
    
    subgraph Output["World Model"]
        State[("World State<br/>Representation")]
    end
    
    Camera --> Calib
    LiDAR --> Calib
    IMU --> Sync
    Calib --> Filter
    Filter --> Fuse
    Sync --> Fuse
    Fuse --> Localize
    Localize --> Detect
    Detect --> Segment
    Segment --> Track
    Track --> State
    
    style Sensors fill:#E3F2FD
    style Preprocessing fill:#FFF3E0
    style Fusion fill:#E8F5E9
    style Perception fill:#F3E5F5
    style Output fill:#FFEBEE"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="Robot Perception Pipeline",
            description="Complete perception pipeline from raw sensor data to world model",
            node_count=15,
            architecture_type=ArchitectureType.ROBOT_PERCEPTION,
        )
    
    def generate_robot_control_loop_diagram(self) -> GeneratedDiagram:
        """Generate robot control loop diagram."""
        mermaid = """graph LR
    subgraph Control_Loop["Control Loop (100Hz)"]
        Sense[("Sense<br/>Read Sensors")]
        Plan[("Plan<br/>Compute Action")]
        Act[("Act<br/>Execute Command")]
    end
    
    Environment[("Environment<br/>Robot State")]
    
    Sense --> Plan
    Plan --> Act
    Act --> Environment
    Environment --> Sense
    
    style Control_Loop fill:#E8F5E9
    style Sense fill:#4CAF50,color:#fff
    style Plan fill:#2196F3,color:#fff
    style Act fill:#FF9800,color:#fff
    style Environment fill:#9E9E9E,color:#fff"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="Robot Control Loop",
            description="Classic sense-plan-act control loop for robotics",
            node_count=5,
            architecture_type=ArchitectureType.ROBOT_CONTROL_LOOP,
        )
    
    def generate_vla_model_diagram(self) -> GeneratedDiagram:
        """Generate Vision-Language-Action model architecture diagram."""
        mermaid = """graph LR
    subgraph Inputs["Input Encoders"]
        Vision[("Vision<br/>ViT Encoder")]
        Language[("Language<br/>LLM Encoder")]
        Proprio[("Proprioception<br/>Joint States")]
    end
    
    subgraph Fusion["Multimodal Fusion"]
        CrossAttn[Cross-Attention<br/>Layers]
        Fusion[Fusion<br/>Transformer]
    end
    
    subgraph Output["Action Output"]
        ActionHead[("Action<br/>Head")]
        Traj[Trajectory<br/>Points]
    end
    
    Vision --> CrossAttn
    Language --> CrossAttn
    Proprio --> Fusion
    CrossAttn --> Fusion
    Fusion --> ActionHead
    ActionHead --> Traj
    
    style Inputs fill:#E3F2FD
    style Fusion fill:#FFF3E0
    style Output fill:#E8F5E9
    style Vision fill:#4CAF50,color:#fff
    style Language fill:#2196F3,color:#fff
    style ActionHead fill:#FF9800,color:#fff"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="Vision-Language-Action (VLA) Model Architecture",
            description="VLA model that takes vision, language, and proprioception to output robot actions",
            node_count=9,
            architecture_type=ArchitectureType.VLA_MODEL,
        )
    
    def generate_vla_workflow_diagram(self) -> GeneratedDiagram:
        """Generate VLA training and inference workflow diagram."""
        mermaid = """graph TD
    subgraph Training["Training Phase"]
        Data[("Robot<br/>Demonstrations")]
        Preprocess[Preprocess &<br/>Augment]
        Train[Train VLA<br/>Model]
        Validate[Validate &<br/>Fine-tune]
    end
    
    subgraph Inference["Inference Phase"]
        Obs[("Observation<br/>Image + Text")]
        Encode[Encode<br/>Inputs]
        Predict[Predict<br/>Actions]
        Execute[Execute on<br/>Robot]
    end
    
    Data --> Preprocess
    Preprocess --> Train
    Train --> Validate
    
    Obs --> Encode
    Encode --> Predict
    Predict --> Execute
    
    style Training fill:#E3F2FD
    style Inference fill:#E8F5E9"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="VLA Model Training and Inference Workflow",
            description="End-to-end workflow from data collection to robot execution",
            node_count=10,
            architecture_type=ArchitectureType.VLA_WORKFLOW,
        )
    
    def generate_slam_pipeline_diagram(self) -> GeneratedDiagram:
        """Generate SLAM pipeline diagram."""
        mermaid = """graph TD
    Sensors[("Raw Sensor<br/>Data")] --> Preprocess[Preprocessing<br/>& Filtering]
    Preprocess --> Features[Feature<br/>Extraction]
    Features --> Match[Feature<br/>Matching]
    Match --> LoopClosure[Loop Closure<br/>Detection]
    Match --> PoseEst[Pose<br/>Estimation]
    PoseEst --> Optimize[Graph<br/>Optimization]
    LoopClosure --> Optimize
    Optimize --> MapUpdate[Map<br/>Update]
    MapUpdate --> Output[("Dense<br/>Map")]
    
    style Sensors fill:#4CAF50,color:#fff
    style Output fill:#2196F3,color:#fff"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="SLAM Pipeline",
            description="Simultaneous Localization and Mapping pipeline",
            node_count=10,
            architecture_type=ArchitectureType.SLAM_PIPELINE,
        )
    
    def generate_navigation_stack_diagram(self) -> GeneratedDiagram:
        """Generate robot navigation stack diagram."""
        mermaid = """graph TD
    Goal[("Goal<br/>Pose")] --> GlobalPlanner[Global<br/>Planner]
    GlobalPlanner --> GlobalPath[Global<br/>Path]
    
    subgraph Local_Planning["Local Planning"]
        LocalCostmap[Local<br/>Costmap]
        LocalPlanner[Local<br/>Planner]
    end
    
    subgraph Recovery["Recovery Behaviors"]
        Rotate[Rotate in<br/>Place]
        Backup[Back<br/>Up]
    end
    
    GlobalPath --> LocalPlanner
    LocalCostmap --> LocalPlanner
    LocalPlanner --> CmdVel[("Velocity<br/>Commands")]
    
    LocalPlanner -.->|Blocked| Recovery
    Recovery -.-> LocalPlanner
    
    style Goal fill:#4CAF50,color:#fff
    style CmdVel fill:#F44336,color:#fff
    style Local_Planning fill:#E3F2FD
    style Recovery fill:#FFEBEE"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="Robot Navigation Stack",
            description="Navigation2 stack showing global and local planning",
            node_count=10,
            architecture_type=ArchitectureType.NAVIGATION_STACK,
        )
    
    def generate_sensor_fusion_diagram(self) -> GeneratedDiagram:
        """Generate sensor fusion architecture diagram."""
        mermaid = """graph LR
    subgraph Raw_Sensors["Raw Sensors"]
        Cam[Camera]
        Lidar[LiDAR]
        Radar[Radar]
        IMU[IMU]
    end
    
    subgraph Calibration["Calibration"]
        ExtCalib[Extrinsic<br/>Calibration]
        TimeSync[Time<br/>Synchronization]
    end
    
    subgraph Fusion_Level["Fusion Level"]
        Early[Early/<br/>Low-Level]
        Late[Late/<br/>High-Level]
    end
    
    subgraph Output["Fused Output"]
        Objects[Detected<br/>Objects]
        Tracking[Multi-Object<br/>Tracking]
    end
    
    Cam --> ExtCalib
    Lidar --> ExtCalib
    Radar --> ExtCalib
    IMU --> TimeSync
    ExtCalib --> Early
    TimeSync --> Early
    Early --> Late
    Late --> Objects
    Late --> Tracking
    
    style Raw_Sensors fill:#E3F2FD
    style Calibration fill:#FFF3E0
    style Fusion_Level fill:#E8F5E9
    style Output fill:#F3E5F5"""
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type="flowchart",
            title="Multi-Sensor Fusion Architecture",
            description="Shows how multiple sensors are calibrated and fused",
            node_count=12,
            architecture_type=ArchitectureType.SENSOR_FUSION,
        )
    
    def generate_custom_diagram(self, config: DiagramConfig) -> GeneratedDiagram:
        """Generate a custom diagram based on configuration."""
        lines = [f"{config.diagram_type.value} {config.direction}"]
        
        # Add subgraphs
        for subgraph in config.subgraphs:
            lines.append(self._create_subgraph(
                subgraph["id"],
                subgraph.get("title", ""),
                subgraph.get("nodes", []),
                subgraph.get("direction", "")
            ))
        
        # Add nodes
        for node in config.nodes:
            lines.append(self._create_node(
                node["id"],
                node.get("label", node["id"]),
                node.get("shape", "rect")
            ))
        
        # Add edges
        for edge in config.edges:
            lines.append(self._create_edge(
                edge["source"],
                edge["target"],
                edge.get("label", ""),
                edge.get("style", "solid")
            ))
        
        # Add styles
        for node_id, color in config.styles.items():
            lines.append(self._apply_style(node_id, color))
        
        mermaid = "\n".join(lines)
        
        return GeneratedDiagram(
            mermaid_code=mermaid,
            diagram_type=config.diagram_type.value,
            title=config.title,
            description="Custom generated diagram",
            node_count=len(config.nodes),
            architecture_type=ArchitectureType.CUSTOM,
        )
    
    def generate(self, architecture_type: ArchitectureType, 
                 config: Optional[DiagramConfig] = None) -> GeneratedDiagram:
        """
        Generate a diagram for the specified architecture type.
        
        Args:
            architecture_type: Type of architecture to diagram
            config: Optional custom configuration
        
        Returns:
            GeneratedDiagram with mermaid code and metadata
        """
        generators = {
            ArchitectureType.ROS2_PUBLISHER_SUBSCRIBER: self.generate_ros2_pubsub_diagram,
            ArchitectureType.ROS2_SERVICE_CLIENT: self.generate_ros2_service_diagram,
            ArchitectureType.RAG_PIPELINE: self.generate_rag_pipeline_diagram,
            ArchitectureType.RAG_ARCHITECTURE: self.generate_rag_architecture_diagram,
            ArchitectureType.ROBOT_PERCEPTION: self.generate_robot_perception_diagram,
            ArchitectureType.ROBOT_CONTROL_LOOP: self.generate_robot_control_loop_diagram,
            ArchitectureType.VLA_MODEL: self.generate_vla_model_diagram,
            ArchitectureType.VLA_WORKFLOW: self.generate_vla_workflow_diagram,
            ArchitectureType.SLAM_PIPELINE: self.generate_slam_pipeline_diagram,
            ArchitectureType.NAVIGATION_STACK: self.generate_navigation_stack_diagram,
            ArchitectureType.SENSOR_FUSION: self.generate_sensor_fusion_diagram,
        }
        
        if architecture_type in generators:
            return generators[architecture_type]()
        elif architecture_type == ArchitectureType.CUSTOM and config:
            return self.generate_custom_diagram(config)
        else:
            raise ValueError(f"Unknown architecture type: {architecture_type}")
    
    def to_markdown(self, diagram: GeneratedDiagram, 
                    include_description: bool = True) -> str:
        """
        Convert a generated diagram to Docusaurus-compatible markdown.
        
        Args:
            diagram: GeneratedDiagram object
            include_description: Whether to include description text
        
        Returns:
            Markdown string with embedded Mermaid diagram
        """
        lines = []
        
        # Add title
        if diagram.title:
            lines.append(f"### {diagram.title}")
            lines.append("")
        
        # Add description
        if include_description and diagram.description:
            lines.append(diagram.description)
            lines.append("")
        
        # Add Mermaid code block
        lines.append(f"```mermaid")
        lines.append(diagram.mermaid_code)
        lines.append("```")
        
        return "\n".join(lines)
    
    def generate_all_diagrams(self) -> List[GeneratedDiagram]:
        """Generate all predefined diagrams."""
        diagrams = []
        
        for arch_type in ArchitectureType:
            if arch_type != ArchitectureType.CUSTOM:
                try:
                    diagram = self.generate(arch_type)
                    diagrams.append(diagram)
                except Exception as e:
                    print(f"Error generating {arch_type}: {e}")
        
        return diagrams
    
    def save_diagrams_to_file(self, output_path: str, 
                               diagrams: Optional[List[GeneratedDiagram]] = None) -> str:
        """
        Save diagrams to a markdown file.
        
        Args:
            output_path: Path to output file
            diagrams: List of diagrams to save (or generate all if None)
        
        Returns:
            Path to saved file
        """
        if diagrams is None:
            diagrams = self.generate_all_diagrams()
        
        content = "# Robotics & AI Diagrams\n\n"
        content += "Auto-generated Mermaid diagrams for textbook content.\n\n"
        content += "---\n\n"
        
        for diagram in diagrams:
            content += self.to_markdown(diagram)
            content += "\n\n---\n\n"
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_file)


def generate_diagram(architecture_type: str) -> str:
    """
    Convenience function to generate a diagram.
    
    Args:
        architecture_type: Name of architecture type
    
    Returns:
        Markdown string with embedded Mermaid diagram
    """
    generator = MermaidDiagramGenerator()
    
    try:
        arch_enum = ArchitectureType(architecture_type)
    except ValueError:
        raise ValueError(f"Unknown architecture type: {architecture_type}")
    
    diagram = generator.generate(arch_enum)
    return generator.to_markdown(diagram)


# Example usage
if __name__ == "__main__":
    generator = MermaidDiagramGenerator()
    
    # Generate RAG pipeline diagram
    rag_diagram = generator.generate(ArchitectureType.RAG_PIPELINE)
    print("=" * 60)
    print("RAG PIPELINE DIAGRAM")
    print("=" * 60)
    print(generator.to_markdown(rag_diagram))
    
    # Generate VLA model diagram
    vla_diagram = generator.generate(ArchitectureType.VLA_MODEL)
    print("\n" + "=" * 60)
    print("VLA MODEL DIAGRAM")
    print("=" * 60)
    print(generator.to_markdown(vla_diagram))
    
    # Save all diagrams
    output_file = generator.save_diagrams_to_file("docs/generated-diagrams.md")
    print(f"\n✓ All diagrams saved to: {output_file}")
