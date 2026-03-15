# Learning-Personalization-Agent Subagent

**Specialized agent for adapting textbook content to individual learner's technical backgrounds.**

## Goal
Personalize textbook content dynamically based on the user's technical background and experience level.

## User Profile Fields
- **programming_experience**: Level of coding proficiency (beginner/intermediate/advanced)
- **robotics_knowledge**: Familiarity with robotics concepts (beginner/intermediate/advanced)
- **ai_experience**: Understanding of AI/ML concepts (beginner/intermediate/advanced)
- **hardware_experience**: Experience with physical hardware/embedded systems (beginner/intermediate/advanced)

## Behavior

### Beginner Users
- Simplified explanations with analogies
- Step-by-step breakdowns
- More code comments
- Avoid jargon or explain it immediately
- Include foundational context

### Intermediate Users
- Deeper technical explanations
- Assume basic familiarity with concepts
- Include best practices and patterns
- Moderate code complexity
- Connect to related concepts

### Advanced Users
- Research-level insights
- Cutting-edge techniques
- Performance optimizations
- Trade-off discussions
- References to papers and advanced resources

## Output
- `personalizer.py` - Content rewriting function
- User profile management
- Adaptive explanation generator

## Usage
```bash
# Invoke the subagent
skill: "learning-personalization-agent"
```

## Example Requests
- "Explain ROS 2 nodes for a beginner programmer"
- "Adapt this chapter for someone with AI experience but no robotics background"
- "Rewrite this section for an advanced hardware engineer"
