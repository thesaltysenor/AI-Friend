# app/services/ai/comfy_ui_service.py

import aiohttp
from typing import AsyncGenerator, Dict, Any
from app.core.config import settings

class ComfyUIService:
    def __init__(self):
        self.base_url = settings.COMFYUI_BASE_URL
        self.session = None

    async def connect(self):
        self.session = aiohttp.ClientSession()

    async def disconnect(self):
        if self.session:
            await self.session.close()

    async def generate_image(self, prompt: str) -> str:
        comfy_prompt = await self.create_image_generation_prompt(prompt)
        async with self.session.post(f"{self.base_url}/prompt", json=comfy_prompt) as response:
            data = await response.json()
            return data['prompt_id']

    async def get_image(self, prompt_id: str) -> bytes:
        async with self.session.get(f"{self.base_url}/view?filename={prompt_id}") as response:
            return await response.read()

    async def listen_for_updates(self) -> AsyncGenerator[Dict[str, Any], None]:
        async with self.session.ws_connect(f"{self.base_url}/ws") as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    yield msg.json()
                elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    break
                
    async def create_image_generation_prompt(self, text_prompt):
        return {
            "prompt": {
                "3": {
                    "inputs": {
                        "text": text_prompt,
                        "clip": ["4", 0]
                    },
                    "class_type": "CLIPTextEncode"
                },
                "4": {
                    "inputs": {
                        "ckpt_name": settings.COMFYUI_CHECKPOINT
                    },
                    "class_type": "CheckpointLoaderSimple"
                },
                "5": {
                    "inputs": {
                        "seed": settings.COMFYUI_SEED,
                        "steps": settings.COMFYUI_STEPS,
                        "cfg": settings.COMFYUI_CFG_SCALE,
                        "sampler_name": settings.COMFYUI_SAMPLER_NAME,
                        "scheduler": settings.COMFYUI_SCHEDULER,
                        "denoise": settings.COMFYUI_DENOISE,
                        "model": ["4", 0],
                        "positive": ["3", 0],
                        "negative": ["6", 0],
                        "latent_image": ["7", 0]
                    },
                    "class_type": "KSampler"
                },
                "6": {
                    "inputs": {
                        "text": settings.COMFYUI_NEGATIVE_PROMPT,
                        "clip": ["4", 0]
                    },
                    "class_type": "CLIPTextEncode"
                },
                "7": {
                    "inputs": {
                        "width": settings.COMFYUI_WIDTH,
                        "height": settings.COMFYUI_HEIGHT,
                        "batch_size": settings.COMFYUI_BATCH_SIZE
                    },
                    "class_type": "EmptyLatentImage"
                },
                "8": {
                    "inputs": {
                        "samples": ["5", 0],
                        "vae": ["4", 2]
                    },
                    "class_type": "VAEDecode"
                },
                "9": {
                    "inputs": {
                        "filename_prefix": settings.COMFYUI_FILENAME_PREFIX,
                        "images": ["8", 0]
                    },
                    "class_type": "SaveImage"
                }
            }
        }