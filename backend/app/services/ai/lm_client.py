# ai-friend/backend/app/services/ai/lm_client.py
from app.core.exceptions import APIException
import datetime
import httpx
import logging
from typing import List, Dict, Union, Optional
from app.models import Message
from app.schemas.schemas import ChatInputMessage
from app.core.config import settings

class LMStudioClient:
    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self.client = client
        self._client_created = client is None
        if self._client_created:
            self.client = httpx.AsyncClient(
                base_url=settings.CURRENT_API_BASE_URL,
                timeout=httpx.Timeout(300.0, connect=60.0)
            )

    async def close(self) -> None:
        """Close the client session if it was created by this instance."""
        if self._client_created and not self.client.is_closed:
            await self.client.aclose()
        
    async def get_models(self) -> Dict:
        """
        Retrieve available models from the LM Studio API.

        Returns:
            Dict: A dictionary containing information about available models.

        Raises:
            HTTPException: If there's an error in the API call.
        """
        try:
            response = await self.client.get("/models")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP status error occurred: {e.response.text}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    async def prepare_chat_messages(self, messages: List[Union[ChatInputMessage, dict]]) -> List[dict]:
        return [
            {"role": msg.role, "content": msg.content} if isinstance(msg, ChatInputMessage) else msg
            for msg in messages
        ]

    async def process_chat_response(self, response_data: dict) -> Message:
        if response_data.get("choices") and len(response_data["choices"]) > 0:
            message_data = response_data["choices"][0]["message"]
            return Message(
                role=message_data["role"],
                content=message_data["content"],
                user_id="assistant",
                timestamp=datetime.datetime.now().timestamp(),
                relevance=1.0
            )
        else:
            raise ValueError("Unexpected response format: missing or empty choices")

    async def create_chat_completion(
        self, 
        messages: List[Union[ChatInputMessage, dict]], 
        model: str, 
        temperature: float, 
        max_tokens: int, 
        stream: bool = False
    ) -> Message:
        payload = {
            "model": model,
            "messages": await self.prepare_chat_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return await self.process_chat_response(data)
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP status error occurred: {e.response.status_code} - {e.response.text}")
            raise APIException(f"LM Studio API returned an error: {e.response.status_code}") from e
        except ValueError as e:
            logging.error(f"Unexpected response format: {e}")
            raise APIException("Unexpected response format from LM Studio API") from e
        except httpx.TimeoutException as e:
            logging.error(f"Request to LM Studio API timed out: {e}")
            raise APIException("Request to LM Studio API timed out") from e
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise APIException("An unexpected error occurred while communicating with LM Studio API") from e