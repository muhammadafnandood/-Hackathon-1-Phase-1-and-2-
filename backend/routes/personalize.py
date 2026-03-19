"""
Personalization endpoint for customizing chapter content based on user profile.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import httpx
import os

router = APIRouter(prefix="/api", tags=["personalization"])

# Qwen/OpenAI API configuration
QWEN_API_KEY = os.getenv("QWEN_API_KEY", os.getenv("OPENAI_API_KEY", ""))
QWEN_API_URL = os.getenv("QWEN_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")


class UserProfile(BaseModel):
    """User profile with learning preferences and background."""
    experience_level: str = "beginner"
    software_background: str = ""
    hardware_background: str = ""
    learning_goal: str = ""


class PersonalizeChapterRequest(BaseModel):
    """Request body for chapter personalization."""
    chapter_content: str
    user_profile: Dict[str, Any]


class PersonalizeChapterResponse(BaseModel):
    """Response body for chapter personalization."""
    personalized_content: str


def build_system_prompt(profile: Dict[str, Any]) -> str:
    """
    Build the system prompt for the AI based on user profile.
    
    Args:
        profile: User profile dictionary with experience_level, backgrounds, and goals
        
    Returns:
        Formatted system prompt for the personalization AI
    """
    experience_level = profile.get("experience_level", "beginner")
    software_bg = profile.get("software_background", "none")
    hardware_bg = profile.get("hardware_background", "none")
    learning_goal = profile.get("learning_goal", "general understanding")
    
    # Base system prompt
    system_prompt = """You are a textbook personalization engine for a Physical AI and Robotics course.

Your task is to rewrite the given chapter content based on the student's profile below.

GENERAL GUIDELINES:
- Keep all code blocks COMPLETELY UNCHANGED - do not modify any code
- Keep all MDX formatting intact (admonitions, tabs, mermaid diagrams, etc.)
- Preserve all section headings and structure
- Maintain technical accuracy while adjusting explanation depth

ADAPTATION RULES BY EXPERIENCE LEVEL:

"""
    
    # Add experience-level specific instructions
    if experience_level == "beginner":
        system_prompt += """FOR BEGINNERS:
- Add relatable analogies for complex concepts (e.g., "ROS 2 nodes are like apps on your phone")
- Explain all technical jargon in simple terms when first introduced
- Add more concrete, real-world examples
- Break down complex sentences into simpler ones
- Add "Why this matters" explanations before technical details
- Include step-by-step mental models for abstract concepts
- Define acronyms on first use
"""
    elif experience_level == "intermediate":
        system_prompt += """FOR INTERMEDIATE LEARNERS:
- Balance theory with practical applications
- Assume basic programming knowledge but explain robotics-specific concepts
- Include both conceptual explanations and implementation details
- Add "Under the hood" insights for important mechanisms
- Connect new concepts to common programming patterns
- Provide context about when to use different approaches
"""
    else:  # advanced
        system_prompt += """FOR ADVANCED LEARNERS:
- Skip basic introductions and get straight to technical depth
- Add deeper technical details about implementation and trade-offs
- Include additional code samples showing advanced patterns
- Discuss performance considerations and optimization strategies
- Mention edge cases, common pitfalls in production, and debugging tips
- Reference industry best practices and real-world architectures
- Add notes about scalability and system design considerations
"""
    
    # Add background-specific customization
    system_prompt += f"""
STUDENT BACKGROUND:
- Experience Level: {experience_level.upper()}
- Software Background: {software_bg if software_bg else 'Not specified'}
- Hardware Background: {hardware_bg if hardware_bg else 'Not specified'}
- Learning Goal: {learning_goal if learning_goal else 'General understanding of Physical AI and Robotics'}

"""
    
    # Add background-specific notes
    if software_bg and software_bg.lower() != "none":
        system_prompt += f"""- When relevant, connect concepts to their software background: {software_bg}
"""
    
    if hardware_bg and hardware_bg.lower() != "none":
        system_prompt += f"""- When relevant, connect concepts to their hardware background: {hardware_bg}
"""
    
    # Final instructions
    system_prompt += """
OUTPUT FORMAT:
- Return ONLY the rewritten MDX content
- Do not include any introductory text, explanations, or meta-commentary
- Do not wrap the output in markdown code blocks
- Preserve the exact structure of the original content
- Keep all YAML front matter unchanged if present

Remember: Your goal is to make the content optimally suited for THIS specific student while maintaining all technical accuracy and educational value."""

    return system_prompt


async def call_qwen_api(messages: list, temperature: float = 0.7) -> str:
    """
    Call Qwen API (or OpenAI-compatible endpoint) for content generation.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        temperature: Sampling temperature for generation
        
    Returns:
        Generated content as string
        
    Raises:
        HTTPException: If API call fails
    """
    if not QWEN_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Qwen/OpenAI API key not configured. Please set QWEN_API_KEY or OPENAI_API_KEY environment variable."
        )
    
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": QWEN_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 4000,
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                QWEN_API_URL,
                headers=headers,
                json=payload,
            )
            
            if response.status_code != 200:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('error', 'Unknown error')}"
                except:
                    error_msg += f": {response.text[:200]}"
                raise HTTPException(status_code=500, detail=error_msg)
            
            result = response.json()
            
            if not result.get("choices") or len(result["choices"]) == 0:
                raise HTTPException(status_code=500, detail="No response generated from AI")
            
            content = result["choices"][0]["message"]["content"]
            
            # Strip any markdown code block wrappers if present
            if content.startswith("```mdx"):
                content = content[5:]
            elif content.startswith("```markdown"):
                content = content[11:]
            elif content.startswith("```"):
                content = content[3:]
            
            if content.endswith("```"):
                content = content[:-3]
            
            return content.strip()
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI service timeout. Please try again in a few moments."
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to AI service: {str(e)}"
        )


@router.post("/personalize-chapter", response_model=PersonalizeChapterResponse)
async def personalize_chapter(request: PersonalizeChapterRequest) -> PersonalizeChapterResponse:
    """
    Personalize chapter content based on user profile.
    
    This endpoint takes chapter content and a user profile, then uses AI
    to rewrite the content in a way that's optimized for that specific user's
    background, experience level, and learning goals.
    
    Args:
        request: PersonalizeChapterRequest with chapter_content and user_profile
        
    Returns:
        PersonalizeChapterResponse with personalized_content
        
    Raises:
        HTTPException: If content is empty, profile is invalid, or AI service fails
    """
    # Validate input
    if not request.chapter_content or not request.chapter_content.strip():
        raise HTTPException(
            status_code=400,
            detail="Chapter content cannot be empty"
        )
    
    if len(request.chapter_content) > 50000:
        raise HTTPException(
            status_code=400,
            detail="Chapter content is too large. Maximum 50,000 characters allowed."
        )
    
    # Extract and validate profile
    profile = request.user_profile
    
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="User profile is required"
        )
    
    experience_level = profile.get("experience_level", "beginner")
    if experience_level not in ["beginner", "intermediate", "advanced"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid experience level: {experience_level}. Must be 'beginner', 'intermediate', or 'advanced'."
        )
    
    # Build system prompt
    system_prompt = build_system_prompt(profile)
    
    # Prepare messages for Qwen API
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Here is the chapter content to personalize:\n\n{request.chapter_content}"
        }
    ]
    
    # Call Qwen API
    personalized_content = await call_qwen_api(messages)
    
    return PersonalizeChapterResponse(
        personalized_content=personalized_content
    )


@router.get("/personalize-chapter/health")
async def personalize_health_check() -> Dict[str, Any]:
    """
    Health check endpoint for personalization service.
    
    Returns:
        Status information including API configuration
    """
    return {
        "status": "healthy",
        "service": "personalization",
        "api_configured": bool(QWEN_API_KEY),
        "api_url": QWEN_API_URL[:50] + "..." if QWEN_API_URL else None,
        "model": QWEN_MODEL,
    }
