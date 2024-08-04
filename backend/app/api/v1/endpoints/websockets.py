from fastapi import APIRouter, WebSocket, Depends
from app.services.ai.comfy_ui_service import ComfyUIService
from app.core.dependencies import get_comfy_ui_service

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    comfy_ui: ComfyUIService = Depends(get_comfy_ui_service)
):
    await websocket.accept()
    await comfy_ui.listen_for_updates(websocket)