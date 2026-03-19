"""
Urdu translation endpoint with Neon Postgres caching.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import os
import asyncpg
import uuid

router = APIRouter(prefix="/api", tags=["translation"])

# Qwen/OpenAI API configuration
QWEN_API_KEY = os.getenv("QWEN_API_KEY", os.getenv("OPENAI_API_KEY", ""))
QWEN_API_URL = os.getenv("QWEN_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

# Neon Postgres configuration
DATABASE_URL = os.getenv("DATABASE_URL", "")


class TranslateUrduRequest(BaseModel):
    """Request body for Urdu translation."""
    chapter_id: str
    chapter_content: str
    chapter_title: str


class TranslateUrduResponse(BaseModel):
    """Response body for Urdu translation."""
    urdu_content: str
    is_cached: bool = False


def get_urdu_system_prompt() -> str:
    """
    Get the system prompt for Urdu translation.
    
    Returns:
        System prompt string with translation rules
    """
    return """You are an expert Urdu translator for technical education, specializing in Physical AI and Robotics textbooks.

Your task is to translate the given textbook chapter from English to Urdu while following these strict rules:

## TRANSLATION RULES (MUST FOLLOW):

1. **Code Blocks**: Keep ALL code blocks exactly as they are in English. Do NOT translate:
   - Python code
   - Bash commands
   - YAML configurations
   - JSON data
   - XML/URDF definitions
   - Any text inside ``` code blocks

2. **Technical Terms**: Keep these in English with Urdu explanation in brackets on FIRST USE ONLY:
   - ROS 2 (روس 2)
   - URDF (یو آر ڈی ایف)
   - LiDAR (لائڈار)
   - SLAM (سلیَم - Simultaneous Localization and Mapping)
   - IMU (آئی ایم یو - Inertial Measurement Unit)
   - GPS (جی پی ایس)
   - Python (پائیتھن)
   - API (اے پی آئی)
   - Node (نوڈ - کمپیوٹنگ کی اکائی)
   - Topic (ٹاپک - میسج بران)
   - Publisher (پبلشر - میسج بھیجنے والا)
   - Subscriber (سبسکرائبر - میسج وصول کرنے والا)
   
   After first use, you can use the English term alone.

3. **Writing Style**:
   - Write in standard Urdu Nastaliq script
   - Use simple Urdu vocabulary suitable for Pakistani university students
   - Avoid overly Persianized or Arabicized Urdu
   - Use clear, educational tone
   - Write numbers in English (1, 2, 3) not Urdu (۱، ۲، ۳)

4. **MDX Formatting**: Keep ALL formatting intact:
   - Headings: #, ##, ### must remain exactly as structure
   - Bold text: **text** should stay bold (translate content only)
   - Lists: -, 1. must maintain structure
   - Code blocks: ```language ... ``` keep completely unchanged
   - Links: [text](url) - translate link text only, keep URL
   - Images: ![alt](src) - translate alt text only
   - Admonitions: :::note, :::tip, :::warning keep structure
   - Tabs: <Tabs> components keep structure

5. **Mathematical Content**: 
   - Keep LaTeX math expressions unchanged: $...$ and $$...$$
   - Keep equations in English

6. **Output Format**:
   - Return ONLY the translated MDX content
   - Do NOT include any introductory text
   - Do NOT include explanations or meta-commentary
   - Do NOT wrap in markdown code blocks

## EXAMPLE TRANSFORMATION:

Input:
```markdown
# Introduction to ROS 2

ROS 2 is a middleware framework for robotics. It uses a publish-subscribe pattern.

```python
import rclpy
from rclpy.node import Node
```

**Key Concept**: Nodes communicate through topics.
```

Output:
```markdown
# ROS 2 کا تعارف

ROS 2 (روس 2) روبوٹکس کے لیے ایک مڈل ویئر فریم ورک ہے۔ یہ پبلش سبسکرائب پیٹرن استعمال کرتا ہے۔

```python
import rclpy
from rclpy.node import Node
```

**اہم تصور**: نوڈز ٹاپکس کے ذریعے رابطہ کرتے ہیں۔
```

Remember: Your translation should make technical concepts accessible to Urdu-speaking students while maintaining complete technical accuracy."""


async def get_cached_translation(chapter_id: str) -> Optional[str]:
    """
    Check Neon Postgres cache for existing translation.
    
    Args:
        chapter_id: Unique identifier for the chapter
        
    Returns:
        Cached Urdu content if found, None otherwise
    """
    if not DATABASE_URL:
        return None
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        result = await conn.fetchrow(
            "SELECT urdu_content FROM urdu_translations WHERE chapter_id = $1",
            chapter_id
        )
        
        await conn.close()
        
        if result:
            return result["urdu_content"]
        
        return None
    except Exception as e:
        print(f"Cache lookup error: {e}")
        return None


async def save_translation_to_cache(chapter_id: str, urdu_content: str) -> bool:
    """
    Save translation to Neon Postgres cache.
    
    Args:
        chapter_id: Unique identifier for the chapter
        urdu_content: Translated Urdu content
        
    Returns:
        True if saved successfully, False otherwise
    """
    if not DATABASE_URL:
        return False
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        await conn.execute(
            """
            INSERT INTO urdu_translations (chapter_id, urdu_content)
            VALUES ($1, $2)
            ON CONFLICT (chapter_id) DO UPDATE SET
                urdu_content = $2,
                created_at = NOW()
            """,
            chapter_id,
            urdu_content
        )
        
        await conn.close()
        return True
    except Exception as e:
        print(f"Cache save error: {e}")
        return False


async def call_translation_api(content: str) -> str:
    """
    Call Qwen/OpenAI API for Urdu translation.
    
    Args:
        content: English content to translate
        
    Returns:
        Translated Urdu content
        
    Raises:
        HTTPException: If API call fails
    """
    if not QWEN_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Translation API key not configured. Please set QWEN_API_KEY or OPENAI_API_KEY."
        )
    
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json",
    }
    
    system_prompt = get_urdu_system_prompt()
    
    payload = {
        "model": QWEN_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate this chapter to Urdu:\n\n{content}"}
        ],
        "temperature": 0.3,  # Lower temperature for more consistent translations
        "max_tokens": 8000,
    }
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                QWEN_API_URL,
                headers=headers,
                json=payload,
            )
            
            if response.status_code != 200:
                error_msg = f"Translation API failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('error', 'Unknown error')}"
                except:
                    error_msg += f": {response.text[:200]}"
                raise HTTPException(status_code=500, detail=error_msg)
            
            result = response.json()
            
            if not result.get("choices") or len(result["choices"]) == 0:
                raise HTTPException(status_code=500, detail="No translation generated")
            
            urdu_content = result["choices"][0]["message"]["content"]
            
            # Strip any markdown code block wrappers
            if urdu_content.startswith("```mdx"):
                urdu_content = urdu_content[5:]
            elif urdu_content.startswith("```markdown"):
                urdu_content = urdu_content[11:]
            elif urdu_content.startswith("```"):
                urdu_content = urdu_content[3:]
            
            if urdu_content.endswith("```"):
                urdu_content = urdu_content[:-3]
            
            return urdu_content.strip()
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Translation service timeout. Please try again."
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to translation service: {str(e)}"
        )


@router.post("/translate-urdu", response_model=TranslateUrduResponse)
async def translate_urdu(request: TranslateUrduRequest) -> TranslateUrduResponse:
    """
    Translate chapter content to Urdu with caching.
    
    This endpoint:
    1. Checks the Neon Postgres cache for existing translation
    2. If found, returns cached version immediately
    3. If not found, calls Qwen API for translation
    4. Saves new translation to cache
    5. Returns Urdu content
    
    Args:
        request: TranslateUrduRequest with chapter_id, chapter_content, chapter_title
        
    Returns:
        TranslateUrduResponse with urdu_content and is_cached flag
        
    Raises:
        HTTPException: If content is empty or translation fails
    """
    # Validate input
    if not request.chapter_content or not request.chapter_content.strip():
        raise HTTPException(
            status_code=400,
            detail="Chapter content cannot be empty"
        )
    
    if len(request.chapter_content) > 100000:
        raise HTTPException(
            status_code=400,
            detail="Chapter content too large. Maximum 100,000 characters."
        )
    
    # Step 1: Check cache
    cached_content = await get_cached_translation(request.chapter_id)
    
    if cached_content:
        return TranslateUrduResponse(
            urdu_content=cached_content,
            is_cached=True
        )
    
    # Step 2: Cache miss - call translation API
    urdu_content = await call_translation_api(request.chapter_content)
    
    # Step 3: Save to cache (async, don't wait)
    await save_translation_to_cache(request.chapter_id, urdu_content)
    
    return TranslateUrduResponse(
        urdu_content=urdu_content,
        is_cached=False
    )


@router.get("/translate-urdu/health")
async def translate_health_check() -> Dict[str, Any]:
    """
    Health check for translation service.
    
    Returns:
        Status information including cache and API configuration
    """
    cache_configured = bool(DATABASE_URL)
    api_configured = bool(QWEN_API_KEY)
    
    return {
        "status": "healthy",
        "service": "urdu-translation",
        "cache_configured": cache_configured,
        "api_configured": api_configured,
        "model": QWEN_MODEL,
    }
