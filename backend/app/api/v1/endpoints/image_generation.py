# app/api/v1/endpoints/image_generation.py

from fastapi import APIRouter, Depends, HTTPException, WebSocket
from app.services.ai.comfy_ui_service import ComfyUIService
from app.core.dependencies import get_comfy_ui_service
from app.schemas import ImageGenerationRequest, ImageGenerationResponse, ImageRetrievalResponse, WSMessage
import base64

router = APIRouter()

@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    comfy_ui: ComfyUIService = Depends(get_comfy_ui_service)
):
    try:
        prompt_id = await comfy_ui.generate_image(request.prompt, request.ai_personality_id)
        return ImageGenerationResponse(
            prompt_id=prompt_id,
            message=f"Image generation started for prompt: '{request.prompt}'"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start image generation: {str(e)}")

@router.get("/{prompt_id}", response_model=ImageRetrievalResponse)
async def get_image(prompt_id: str, comfy_ui: ComfyUIService = Depends(get_comfy_ui_service)):
    try:
        image_data = await comfy_ui.get_image(prompt_id)
        # Convert image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        return ImageRetrievalResponse(image_data=base64_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    comfy_ui: ComfyUIService = Depends(get_comfy_ui_service)
):
    await websocket.accept()
    try:
        async for message in comfy_ui.listen_for_updates():
            await websocket.send_json(WSMessage(type="update", data=message).dict())
    except Exception as e:
        await websocket.send_json(WSMessage(type="error", data={"message": str(e)}).dict())
    finally:
        await websocket.close()