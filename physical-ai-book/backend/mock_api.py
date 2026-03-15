"""
Simple mock RAG API for testing the chatbot UI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="Mock RAG API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class Source(BaseModel):
    chapter_id: str
    heading: str = ""
    score: float


class ChatResponse(BaseModel):
    response: str
    sources: list[Source]
    session_id: str
    model: str = "mock-gpt"


# Mock responses for common questions
MOCK_RESPONSES = {
    "ros": {
        "response": """ROS 2 (Robot Operating System) is a flexible framework for writing robot software. It provides tools and libraries to create robot applications.

**Key Concepts:**
- **Nodes**: Independent processes that communicate
- **Topics**: Named buses for exchanging messages
- **Services**: Synchronous request/response communication
- **Actions**: Goal-oriented long-running tasks

In this textbook, you'll learn to set up ROS 2 nodes for humanoid robot control.""",
        "sources": [
            {"chapter_id": "Chapter1", "heading": "Introduction to ROS 2", "score": 0.92},
            {"chapter_id": "Chapter3", "heading": "Robot Communication Patterns", "score": 0.85},
        ]
    },
    "simulation": {
        "response": """The textbook covers multiple simulation environments for humanoid robots:

**Webots**: Professional robot simulation with physics engine
**Gazebo**: Open-source 3D simulator with ROS integration
**Isaac Sim**: NVIDIA's GPU-accelerated simulation platform

Each simulator has its strengths. Webots is great for beginners, while Isaac Sim offers photorealistic rendering.""",
        "sources": [
            {"chapter_id": "Chapter5", "heading": "Simulation Environments", "score": 0.88},
            {"chapter_id": "Chapter6", "heading": "Physics Engines", "score": 0.79},
        ]
    },
    "vl": {
        "response": """Vision-Language-Action (VLA) models combine:

1. **Vision**: Processing camera/sensor input
2. **Language**: Understanding natural language commands
3. **Action**: Generating robot motor commands

Our textbook teaches you to implement VLA models using transformers and pre-trained models like RT-2 or OpenVLA.""",
        "sources": [
            {"chapter_id": "Chapter8", "heading": "Vision-Language Models", "score": 0.91},
            {"chapter_id": "Chapter9", "heading": "Action Generation", "score": 0.83},
        ]
    },
    "default": {
        "response": """That's a great question! Based on the Physical AI textbook content, I can help you understand various topics including:

- **ROS 2** setup and programming
- **Robot simulation** with Webots/Gazebo
- **AI/ML** for robot perception
- **Vision-Language-Action** models
- **Humanoid robot** control systems

Could you be more specific about what you'd like to learn?""",
        "sources": [
            {"chapter_id": "Chapter1", "heading": "Getting Started", "score": 0.75},
        ]
    }
}


@app.get("/")
async def root():
    return {"name": "Mock RAG API", "version": "1.0.0", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    message_lower = request.message.lower()

    # Simple keyword matching for mock responses
    if "ros" in message_lower or "robot operating" in message_lower:
        mock = MOCK_RESPONSES["ros"]
    elif "simul" in message_lower or "webots" in message_lower or "gazebo" in message_lower:
        mock = MOCK_RESPONSES["simulation"]
    elif "vla" in message_lower or "vision-language" in message_lower or "action model" in message_lower:
        mock = MOCK_RESPONSES["vl"]
    else:
        mock = MOCK_RESPONSES["default"]

    return ChatResponse(
        response=mock["response"],
        sources=[Source(**s) for s in mock["sources"]],
        session_id="mock-session-123"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
