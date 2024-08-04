# app/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatInputMessage(BaseModel):
    role: str
    content: str
    user_id: str

class ChatInput(BaseModel):
    messages: List[ChatInputMessage]
    model: str
    temperature: float = 0.7
    max_tokens: int = 150
    ai_personality_id: Optional[int] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    is_active: bool

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class AIPersonalityCreate(BaseModel):
    name: str
    description: str
    personality_traits: str
    character_type: str = "default"
    available: bool = True

class AIPersonalityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    personality_traits: str
    character_type: str
    available: bool

class AIPersonalityUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    description: Optional[str] = None
    personality_traits: Optional[str] = None
    character_type: Optional[str] = None
    available: Optional[bool] = None

class IntentCreate(BaseModel):
    intent_name: str
    description: str

class IntentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    intent_name: str
    description: str

class IntentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    intent_name: Optional[str] = None
    description: Optional[str] = None

class InteractionCreate(BaseModel):
    user_id: int
    ai_personality_id: Optional[int] = None
    interaction_type: str

class InteractionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    ai_personality_id: int
    interaction_type: str
    timestamp: datetime

class InteractionUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    interaction_type: Optional[str] = None

class EntityCreate(BaseModel):
    entity_name: str
    intent_id: int

class EntityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    entity_name: str
    intent_id: int

class EntityUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    entity_name: Optional[str] = None
    intent_id: Optional[int] = None

class FeedbackCreate(BaseModel):
    user_id: str
    session_id: int
    message_id: str
    rating: int

class FeedbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: str
    session_id: int
    message_id: str
    rating: int

class FeedbackUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    rating: Optional[int] = None

class MessageCreate(BaseModel):
    role: str
    content: str
    user_id: str
    relevance: float = 1.0

class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: str
    content: str
    timestamp: float
    user_id: str
    relevance: float

class MessageUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role: Optional[str] = None
    content: Optional[str] = None
    relevance: Optional[float] = None

class SessionCreate(BaseModel):
    user_id: int
    status: str

class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime]
    status: str

class SessionUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    end_time: Optional[datetime] = None
    status: Optional[str] = None

class UserPreferenceCreate(BaseModel):
    user_id: int
    preference_type: str
    preference_value: str

class UserPreferenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    preference_type: str
    preference_value: str

class UserPreferenceUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    preference_value: Optional[str] = None
    
class ImageGenerationRequest(BaseModel):
    prompt: str
    ai_personality_id: Optional[int] = None

class ImageGenerationResponse(BaseModel):
    prompt_id: str
    message: str

class ImageRetrievalResponse(BaseModel):
    image_data: str  # Base64 encoded image data

class WSMessage(BaseModel):
    type: str
    data: Dict[str, Any]