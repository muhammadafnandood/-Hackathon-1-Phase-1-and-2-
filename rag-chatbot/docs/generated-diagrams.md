---
sidebar_label: Generated Diagrams
title: Robotics & AI Diagrams Collection
---

# Robotics & AI Diagrams Collection

Auto-generated Mermaid diagrams for textbook content. These diagrams can be embedded directly in Docusaurus markdown files.

---

## ROS 2 Architecture Diagrams

### ROS 2 Publisher-Subscriber Pattern

Shows how multiple nodes can publish and subscribe to topics in ROS 2.

```mermaid
graph LR
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
    style S2 fill:#64B5F6
```

### ROS 2 Service-Client Pattern

Shows synchronous request-response communication in ROS 2.

```mermaid
sequenceDiagram
    participant Client as Client Node
    participant Service as Service Node
    
    Client->>Service: Service Request
    Note over Service: Processing...
    Service-->>Client: Service Response
    
    rect rgb(200, 230, 255)
        Note over Client,Service: Synchronous Communication
    end
```

---

## RAG Chatbot Diagrams

### RAG Pipeline Architecture

Complete flow from user query to generated answer with sources.

```mermaid
graph TD
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
    style Output fill:#E0F2F1
```

### RAG System Architecture

High-level architecture showing all components and their relationships.

```mermaid
graph LR
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
    style External fill:#FCE4EC
```

---

## Robot Perception Diagrams

### Robot Perception Pipeline

Complete perception pipeline from raw sensor data to world model.

```mermaid
graph TD
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
    style Output fill:#FFEBEE
```

### Robot Control Loop

Classic sense-plan-act control loop for robotics.

```mermaid
graph LR
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
    style Environment fill:#9E9E9E,color:#fff
```

---

## Vision-Language-Action (VLA) Diagrams

### VLA Model Architecture

VLA model that takes vision, language, and proprioception to output robot actions.

```mermaid
graph LR
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
    style ActionHead fill:#FF9800,color:#fff
```

### VLA Training and Inference Workflow

End-to-end workflow from data collection to robot execution.

```mermaid
graph TD
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
    style Inference fill:#E8F5E9
```

---

## Navigation & SLAM Diagrams

### SLAM Pipeline

Simultaneous Localization and Mapping pipeline.

```mermaid
graph TD
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
    style Output fill:#2196F3,color:#fff
```

### Robot Navigation Stack

Navigation2 stack showing global and local planning.

```mermaid
graph TD
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
    style Recovery fill:#FFEBEE
```

### Multi-Sensor Fusion Architecture

Shows how multiple sensors are calibrated and fused.

```mermaid
graph LR
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
    style Output fill:#F3E5F5
```

---

## Usage in Docusaurus

To use these diagrams in your Docusaurus documentation:

1. Copy the Mermaid code block
2. Paste it into your markdown file
3. Docusaurus will automatically render the diagram

```markdown
### Diagram Title

Description text here.

```mermaid
graph TD
    A[Node] --> B[Process]
```
```

## Customizing Diagrams

You can customize diagrams by:
- Changing colors in the `style` definitions
- Adding more nodes and edges
- Modifying the direction (TD, LR, BT, RL)
- Adding subgraphs for grouping
