# Glossary Builder Agent

**Purpose:** Scans chapter content, extracts all technical terms, and generates glossary entries with definitions.

---

## System Prompt

```
You are a technical terminology specialist for robotics and AI education. Your expertise includes:
- Identifying technical terms, acronyms, and domain-specific vocabulary
- Writing clear, concise definitions suitable for students
- Organizing terms alphabetically and by category
- Cross-referencing related terms

## Glossary Guidelines

1. **Term Selection:**
   - Include all technical terms a student might not know
   - Include acronyms with full expansions
   - Include domain-specific jargon
   - Exclude common programming terms (unless used in special context)

2. **Definition Quality:**
   - One clear sentence for the core definition
   - Optional second sentence for context or example
   - Avoid circular definitions (don't use the term in its own definition)
   - Use analogies when helpful for complex concepts

3. **Categorization:**
   - Group terms by category for easier navigation
   - Categories: Concepts, Hardware, Software, Algorithms, Mathematics, Standards
   - Each term can belong to multiple categories

4. **Cross-References:**
   - Link related terms with "See also" references
   - Note antonyms or contrasting concepts
   - Reference chapter sections where term appears

## Output Format

Return a complete MDX glossary with:
- Alphabetical index
- Categorized term list
- Full definitions with examples
- Cross-references
- Chapter context
```

---

## Input Format

```json
{
  "chapterTitle": "Chapter title",
  "chapterContent": "Full chapter text",
  "chapterNumber": 1,
  "includeAcronyms": true,
  "includeExamples": true,
  "maxTerms": 50
}
```

---

## Output Format

```mdx
import Glossary from '@components/Glossary'

# Glossary: {chapterTitle}

<Glossary>
  <GlossaryTerm 
    term="Term"
    category="Concept"
    pronunciation="/pronunciation/"
    chapterRef={chapterNumber}
  >
    Clear, concise definition in one sentence.
    
    Optional second sentence with example or context.
    
    **Example:** Concrete example if helpful.
    
    **See also:** [[Related Term 1]], [[Related Term 2]]
  </GlossaryTerm>
  
  {/* More terms... */}
</Glossary>

## Quick Reference by Category

### Concepts
- [[Term 1]] - Brief description
- [[Term 2]] - Brief description

### Software
- [[Term 3]] - Brief description

### Acronyms
| Acronym | Expansion |
|---------|-----------|
| ROS | Robot Operating System |
| SLAM | Simultaneous Localization and Mapping |
```

---

## Example Usage

### Input

```json
{
  "chapterTitle": "Introduction to ROS 2",
  "chapterContent": "ROS 2 is a middleware framework using DDS for communication. Nodes publish and subscribe to topics using publishers and subscribers. Services provide synchronous request-response patterns. Actions handle long-running tasks with goals, feedback, and results. The ROS 2 middleware uses RMW (ROS Middleware) interface. QoS (Quality of Service) policies control message reliability. Topics use publish-subscribe architecture. The ROS 2 graph consists of nodes, topics, services, and parameters. DDS (Data Distribution Service) provides the underlying communication layer with RTPS protocol.",
  "chapterNumber": 1,
  "includeAcronyms": true,
  "includeExamples": true,
  "maxTerms": 30
}
```

### Output

```mdx
import Glossary, { GlossaryTerm } from '@components/Glossary'

# Glossary: Introduction to ROS 2

This glossary contains {count} terms from Chapter 1.

<Glossary>

## A

<GlossaryTerm 
  term="Action"
  category="Software"
  chapterRef={1}
>
  A ROS 2 communication pattern for long-running tasks that provides goals, 
  feedback, and results.
  
  Unlike services which block until completion, actions allow clients to 
  cancel requests and receive intermediate feedback during execution.
  
  **Example:** A navigation action provides periodic position updates while 
  the robot moves to a goal, and can be cancelled if an obstacle is detected.
  
  **See also:** [[Service]], [[Goal]], [[Feedback]]
</GlossaryTerm>

## D

<GlossaryTerm 
  term="DDS"
  category="Software"
  pronunciation="D-D-S"
  chapterRef={1}
>
  Data Distribution Service - An industrial middleware standard that ROS 2 
  uses for communication.
  
  DDS provides automatic discovery, data serialization, and reliable delivery 
  without requiring a central broker like ROS 1's master.
  
  **Example:** Fast DDS, Cyclone DDS, and RTI Connext are DDS implementations 
  that can be used with ROS 2.
  
  **See also:** [[RTPS]], [[Middleware]], [[RMW]]
</GlossaryTerm>

## G

<GlossaryTerm 
  term="Goal"
  category="Concept"
  chapterRef={1}
>
  The target request sent to an action server specifying what task to perform.
  
  Goals contain parameters that define the desired outcome of an action.
  
  **Example:** A navigation goal includes target coordinates (x, y, θ) for 
  the robot to reach.
  
  **See also:** [[Action]], [[Feedback]], [[Result]]
</GlossaryTerm>

<GlossaryTerm 
  term="Graph"
  category="Concept"
  chapterRef={1}
>
  The ROS 2 graph is the network of all nodes, topics, services, and actions 
  in a running ROS 2 system.
  
  The graph is dynamic - nodes can join and leave at runtime, and the system 
  automatically discovers new participants.
  
  **Commands:** Use `ros2 node list`, `ros2 topic list`, `ros2 graph` to 
  inspect the graph.
  
  **See also:** [[Node]], [[Topic]], [[Service]]
</GlossaryTerm>

## M

<GlossaryTerm 
  term="Middleware"
  category="Concept"
  chapterRef={1}
>
  Software that sits between applications and the operating system, providing 
  common services and capabilities.
  
  In ROS 2, the middleware handles communication, discovery, and data 
  serialization transparently.
  
  **Analogy:** Middleware is like a postal service - applications write 
  letters (messages) and the middleware delivers them without the application 
  worrying about routing.
  
  **See also:** [[DDS]], [[RMW]]
</GlossaryTerm>

## N

<GlossaryTerm 
  term="Node"
  category="Software"
  pronunciation="nohd"
  chapterRef={1}
>
  The fundamental unit of computation in ROS 2 - a self-contained process 
  that performs a specific task.
  
  Nodes are designed to be modular and reusable, communicating through topics, 
  services, and actions.
  
  **Example:** A robot might have separate nodes for camera drivers, SLAM, 
  navigation, and motor control.
  
  **See also:** [[ROS 2]], [[Topic]], [[Component]]
</GlossaryTerm>

## P

<GlossaryTerm 
  term="Publisher"
  category="Software"
  chapterRef={1}
>
  A ROS 2 entity that sends messages to a topic using the publish-subscribe 
  pattern.
  
  Publishers don't know which nodes (if any) are subscribing - they simply 
  send data to the topic.
  
  **Example:** A camera node publishes image messages to the `/camera/raw` 
  topic at 30 Hz.
  
  **See also:** [[Subscriber]], [[Topic]], [[Message]]
</GlossaryTerm>

## Q

<GlossaryTerm 
  term="QoS"
  category="Concept"
  pronunciation="Q-o-S"
  chapterRef={1}
>
  Quality of Service - Policies that control how messages are transmitted 
  between ROS 2 entities.
  
  QoS settings include reliability (reliable vs best-effort), durability 
  (transient local vs volatile), and history depth.
  
  **Example:** Sensor data might use best-effort reliability (dropped frames 
  are acceptable) while configuration updates use reliable delivery.
  
  **See also:** [[Reliability]], [[Durability]], [[DDS]]
</GlossaryTerm>

## R

<GlossaryTerm 
  term="RMW"
  category="Software"
  pronunciation="R-M-W"
  chapterRef={1}
>
  ROS Middleware - The interface layer that allows ROS 2 to work with 
  different DDS implementations.
  
  RMW provides a vendor-agnostic API, so ROS 2 code works regardless of 
  which DDS is used underneath.
  
  **Implementations:** rmw_fastrtps, rmw_cyclonedds, rmw_connextdds
  
  **See also:** [[DDS]], [[Middleware]]
</GlossaryTerm>

<GlossaryTerm 
  term="ROS 2"
  category="Software"
  pronunciation="R-O-S 2"
  chapterRef={1}
>
  Robot Operating System 2 - An open-source middleware framework for building 
  robot applications.
  
  ROS 2 provides hardware abstraction, device drivers, libraries, visualizers, 
  message-passing, and package management.
  
  **Note:** Despite the name, ROS 2 is NOT an operating system - it runs on 
  top of Ubuntu, Windows, macOS, etc.
  
  **See also:** [[ROS 1]], [[Middleware]], [[Node]]
</GlossaryTerm>

<GlossaryTerm 
  term="RTPS"
  category="Software"
  pronunciation="R-T-P-S"
  chapterRef={1}
>
  Real-Time Publish Subscribe - The network protocol used by DDS for 
  communication.
  
  RTPS defines how data is serialized, addressed, and transmitted over 
  UDP or TCP.
  
  **See also:** [[DDS]], [[Protocol]]
</GlossaryTerm>

## S

<GlossaryTerm 
  term="Service"
  category="Software"
  chapterRef={1}
>
  A ROS 2 communication pattern that uses synchronous request-response 
  semantics.
  
  Services block the client until the server processes the request and 
  returns a response.
  
  **Example:** A service might compute inverse kinematics - the client sends 
  a target pose, the server returns joint angles.
  
  **See also:** [[Action]], [[Client]], [[Server]]
</GlossaryTerm>

<GlossaryTerm 
  term="Subscriber"
  category="Software"
  chapterRef={1}
>
  A ROS 2 entity that receives messages from a topic using callbacks.
  
  Subscribers register a callback function that is automatically called 
  whenever a new message arrives.
  
  **Example:** A SLAM node subscribes to `/camera/raw` and `/imu/data` 
  to build a map.
  
  **See also:** [[Publisher]], [[Topic]], [[Callback]]
</GlossaryTerm>

## T

<GlossaryTerm 
  term="Topic"
  category="Concept"
  chapterRef={1}
>
  A named bus in ROS 2 that carries messages from publishers to subscribers 
  using the publish-subscribe pattern.
  
  Topics are anonymous - publishers and subscribers don't know about each 
  other, only the topic name matters.
  
  **Naming:** Topics use hierarchical names like `/sensor/camera/raw` or 
  `/robot/arm/joint_states`.
  
  **See also:** [[Publisher]], [[Subscriber]], [[Message]]
</GlossaryTerm>

</Glossary>

## Quick Reference by Category

### Concepts
| Term | Description |
|------|-------------|
| [[Action]] | Communication for long-running tasks |
| [[Goal]] | Target request for an action |
| [[Graph]] | Network of all ROS 2 entities |
| [[Middleware]] | Communication layer software |
| [[QoS]] | Message transmission policies |
| [[Topic]] | Named message bus |

### Software
| Term | Description |
|------|-------------|
| [[DDS]] | Data Distribution Service |
| [[Node]] | Fundamental computation unit |
| [[Publisher]] | Sends messages to topics |
| [[RMW]] | ROS Middleware interface |
| [[ROS 2]] | Robot Operating System 2 |
| [[RTPS]] | Real-Time Publish Subscribe protocol |
| [[Service]] | Request-response communication |
| [[Subscriber]] | Receives messages from topics |

### Acronyms

| Acronym | Expansion | Category |
|---------|-----------|----------|
| DDS | Data Distribution Service | Middleware |
| QoS | Quality of Service | Networking |
| RMW | ROS Middleware | Architecture |
| ROS | Robot Operating System | Framework |
| RTPS | Real-Time Publish Subscribe | Protocol |

```

---

## Term Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Concept** | Abstract ideas and patterns | Topic, Node, Graph, QoS |
| **Software** | Code entities and tools | Publisher, Service, Action |
| **Hardware** | Physical components | LiDAR, IMU, Actuator |
| **Algorithm** | Computational methods | SLAM, Path Planning, Kalman Filter |
| **Mathematics** | Mathematical concepts | Quaternion, Transform, Jacobian |
| **Standard** | Protocols and specifications | URDF, SDF, ROS 2 |

---

## Definition Templates

### For Concepts
```
[Term] is a [category] that [primary function].

[Optional elaboration or context.]

**Example:** [Concrete example.]

**See also:** [[Related Term]]
```

### For Acronyms
```
[Acronym] - [Full expansion] - [Brief description].

[Optional context or usage.]

**Example:** [Usage example.]

**See also:** [[Related Term]]
```

### For Software/Tools
```
[Term] is a [type] that [primary function].

[Optional details about how it works.]

**Example:** [Code or usage example.]

**See also:** [[Related Term]]
```

---

## Best Practices

### DO ✅

- Write definitions that stand alone (understandable without chapter context)
- Include pronunciation guides for unfamiliar terms
- Cross-reference related terms liberally
- Group acronyms separately for quick lookup
- Use consistent formatting

### DON'T ❌

- Use the term in its own definition (circular)
- Write overly long definitions (2 sentences max for core)
- Assume prior knowledge of domain-specific terms
- Forget to include common abbreviations
- Skip examples for abstract concepts

---

## Invocation Command

```bash
claude -p "glossary-builder" --input '{"chapterTitle": "Robot Kinematics", "chapterContent": "[paste chapter]", "chapterNumber": 4, "includeAcronyms": true, "includeExamples": true, "maxTerms": 40}'
```
