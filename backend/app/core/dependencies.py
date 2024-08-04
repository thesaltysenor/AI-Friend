# app/core/dependencies.py

import asyncio
import os
from app.services.ai.comfy_ui_service import ComfyUIService
from app.core.config import settings


comfy_ui_service = ComfyUIService()

async def get_prediction(input_text: str):
    # Assuming the backend directory is structured correctly under the project root
    node_script_path = os.path.join(os.path.dirname(__file__), 'lm_client.ts')
    cmd = ['node', node_script_path, input_text]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return stdout.decode()
    else:
        error_msg = stderr.decode()
        print(f"Error running lm_client.ts: {error_msg}")
        return None

def get_comfy_ui_service():
    return ComfyUIService(settings.COMFYUI_BASE_URL)