from app.core.config import settings

__version__ = "0.1.0"  # Or whatever version your app is at

# Initialize ComfyUIService here
from app.services.ai.comfy_ui_service import ComfyUIService
comfy_ui_service = ComfyUIService()

__all__ = ["settings", "comfy_ui_service"]