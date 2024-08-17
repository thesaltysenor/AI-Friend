# app/schemas.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    id: int
    is_active: bool

class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenData(BaseSchema):
    user_id: Optional[str] = None

class CharacterBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: str
    personality_traits: str
    character_type: str = "default"
    available: bool = True

class CharacterCreate(CharacterBase):
    pass

class CharacterRead(CharacterBase):
    id: int

class CharacterUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    personality_traits: Optional[str] = None
    character_type: Optional[str] = None
    available: Optional[bool] = None

class ChatInputMessage(BaseSchema):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    user_id: str

class ChatInput(BaseSchema):
    messages: List[ChatInputMessage]
    model: str
    temperature: float = Field(0.7, ge=0, le=1)
    max_tokens: int = Field(150, gt=0)
    character_id: Optional[int] = None

class ConversationIntentBase(BaseSchema):
    conversation_intent_name: str
    description: str

class ConversationIntentCreate(ConversationIntentBase):
    pass

class ConversationIntentRead(ConversationIntentBase):
    id: int

class ConversationIntentUpdate(BaseSchema):
    conversation_intent_name: Optional[str] = None
    description: Optional[str] = None

class InteractionBase(BaseSchema):
    user_id: int
    character_id: Optional[int] = None
    interaction_type: str

class InteractionCreate(InteractionBase):
    pass

class InteractionRead(InteractionBase):
    id: int
    timestamp: datetime

class InteractionUpdate(BaseSchema):
    interaction_type: Optional[str] = None

class EntityBase(BaseSchema):
    entity_name: str
    conversation_intent_id: int

class EntityCreate(EntityBase):
    pass

class EntityRead(EntityBase):
    id: int

class EntityUpdate(BaseSchema):
    entity_name: Optional[str] = None
    conversation_intent_id: Optional[int] = None

class FeedbackBase(BaseSchema):
    user_id: str
    session_id: int
    message_id: str
    rating: int = Field(..., ge=1, le=5)

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackRead(FeedbackBase):
    id: int

class FeedbackUpdate(BaseSchema):
    rating: Optional[int] = Field(None, ge=1, le=5)

class MessageBase(BaseSchema):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    user_id: str
    relevance: float = Field(1.0, ge=0, le=1)

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: str
    timestamp: float

class MessageUpdate(BaseSchema):
    role: Optional[str] = Field(None, pattern="^(user|assistant|system)$")
    content: Optional[str] = None
    relevance: Optional[float] = Field(None, ge=0, le=1)

class SessionBase(BaseSchema):
    user_id: int
    status: str

class SessionCreate(SessionBase):
    pass

class SessionRead(SessionBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None

class SessionUpdate(BaseSchema):
    end_time: Optional[datetime] = None
    status: Optional[str] = None

class UserPreferenceBase(BaseSchema):
    user_id: int
    preference_type: str
    preference_value: str

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceRead(UserPreferenceBase):
    id: int

class UserPreferenceUpdate(BaseSchema):
    preference_value: Optional[str] = None

class ImageGenerationRequest(BaseSchema):
    prompt: str = Field(..., min_length=1)
    character_id: Optional[int] = None

class ImageGenerationResponse(BaseSchema):
    prompt_id: str
    message: str

class ImageRetrievalResponse(BaseSchema):
    image_data: str  # Base64 encoded image data

class WSMessage(BaseSchema):
    type: str
    data: Dict[str, Any]