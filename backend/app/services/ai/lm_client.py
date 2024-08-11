# app/services/lm_client.py
import datetime
import httpx
import logging
from typing import List, Dict, Union
from app.models.messages import Message
from app.schemas import ChatInputMessage
from app.core.config import settings

class LMStudioClient:
    def __init__(self, client: httpx.AsyncClient = None):
        self.client = client
        self._client_created = client is None
        if self._client_created:
            self.client = httpx.AsyncClient(
                base_url=settings.get_current_api_base_url,
                timeout=httpx.Timeout(300.0, connect=60.0)
            )

    async def close(self):
        if self._client_created and not self.client.is_closed:
            await self.client.aclose()
        
    async def get_models(self) -> Dict:
        try:
            response = await self.client.get("/models")
            response.raise_for_status()
            data = response.json()
            logging.debug(f"LM Studio API response: {data}")
            return data
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    async def create_chat_completion(self, messages: List[Union[ChatInputMessage, dict]], model: str, temperature: float, max_tokens: int, stream: bool = False) -> Message:
        payload = {
            "model": model,
            "messages": [
                {"role": message.role, "content": message.content} if isinstance(message, ChatInputMessage) else message
                for message in messages
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("choices") and len(data["choices"]) > 0:
                message_data = data["choices"][0]["message"]
                return Message(
                    role=message_data["role"],
                    content=message_data["content"],
                    user_id="assistant",  # Or use a default user ID
                    timestamp=datetime.datetime.now().timestamp(),
                    relevance=1.0
                )
            else:
                raise ValueError("Unexpected response format: missing or empty choices")
            
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP status error occurred: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logging.error(f"Request failed: {e}")
            raise
        except ValueError as e:
            logging.error(f"Unexpected response format: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise
   