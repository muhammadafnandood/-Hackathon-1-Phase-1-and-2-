"""
User-related Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class HardwareAvailability(BaseModel):
    """Hardware availability schema for user profile."""
    
    hasRobot: bool = Field(default=False, description="User has physical robot")
    hasROS2: bool = Field(default=False, description="User has ROS2 installed")
    hasGPU: bool = Field(default=False, description="User has GPU for AI training")
    simulationOnly: bool = Field(default=True, description="User will use simulation only")


class UserProfileBase(BaseModel):
    """Base schema for user profile."""
    
    programming_level: str = Field(
        ...,
        min_length=1,
        max_length=20,
        pattern=r"^(beginner|intermediate|advanced)$",
        description="User programming experience level"
    )
    ai_knowledge: str = Field(
        ...,
        min_length=1,
        max_length=20,
        pattern=r"^(none|basic|intermediate|advanced)$",
        description="User AI/ML knowledge level"
    )
    hardware_availability: HardwareAvailability = Field(
        default_factory=HardwareAvailability,
        description="Hardware access details"
    )
    learning_pace: str = Field(
        default="normal",
        pattern=r"^(slow|normal|fast)$",
        description="Preferred learning speed"
    )
    preferred_explanation_style: str = Field(
        default="both",
        pattern=r"^(conceptual|practical|both)$",
        description="Conceptual vs practical preference"
    )


class UserProfileCreate(UserProfileBase):
    """Schema for creating a user profile."""
    
    user_id: UUID = Field(..., description="Auth user ID")


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    
    programming_level: Optional[str] = Field(
        None,
        pattern=r"^(beginner|intermediate|advanced)$",
        description="User programming experience level"
    )
    ai_knowledge: Optional[str] = Field(
        None,
        pattern=r"^(none|basic|intermediate|advanced)$",
        description="User AI/ML knowledge level"
    )
    hardware_availability: Optional[HardwareAvailability] = Field(
        None,
        description="Hardware access details"
    )
    learning_pace: Optional[str] = Field(
        None,
        pattern=r"^(slow|normal|fast)$",
        description="Preferred learning speed"
    )
    preferred_explanation_style: Optional[str] = Field(
        None,
        pattern=r"^(conceptual|practical|both)$",
        description="Conceptual vs practical preference"
    )


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Profile ID")
    user_id: UUID = Field(..., description="Auth user ID")
    created_at: datetime = Field(..., description="Profile creation timestamp")
    updated_at: datetime = Field(..., description="Last profile update timestamp")


class UserProgressResponse(BaseModel):
    """Schema for user progress response."""
    
    totalChapters: int = Field(..., description="Total chapters in system")
    completedChapters: int = Field(..., description="Number of completed chapters")
    inProgressChapters: int = Field(..., description="Number of chapters in progress")
    chapters: List["ChapterProgress"] = Field(default_factory=list)


class ChapterProgress(BaseModel):
    """Schema for individual chapter progress."""
    
    chapterId: str = Field(..., description="Chapter identifier")
    title: str = Field(..., description="Chapter title")
    status: str = Field(..., pattern=r"^(not_started|in_progress|completed)$")
    completedAt: Optional[datetime] = Field(None, description="Completion timestamp")
    timeSpentSeconds: int = Field(default=0, description="Time spent on chapter")


# Update forward references
UserProfileResponse.model_rebuild()
