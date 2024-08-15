# app/services/ai/comfy_ui_service.py

import aiohttp
from urllib.parse import urljoin
from typing import AsyncGenerator, Dict, Any
from app.core.config import settings

class ComfyUIService:
    def __init__(self):
        self.base_url: str = settings.COMFYUI_BASE_URL
        self.session: aiohttp.ClientSession = None

    async def connect(self) -> None:
        """Establish a connection to the ComfyUI service."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def disconnect(self) -> None:
        """Close the connection to the ComfyUI service."""
        if self.session and not self.session.closed:
            await self.session.close()

    def _get_safe_url(self, path: str) -> str:
        """
        Construct a safe URL by joining the base URL with the given path.

        Args:
            path (str): The path to append to the base URL.

        Returns:
            str: The complete, safe URL.
        """
        return urljoin(self.base_url, path)

    async def generate_image(self, prompt: str) -> str:
        """
        Generate an image based on the given prompt.

        Args:
            prompt (str): The text prompt for image generation.

        Returns:
            str: The prompt ID for the generated image.

        Raises:
            aiohttp.ClientError: If there's an error in the API call.
        """
        await self.connect()
        url = self._get_safe_url("prompt")
        comfy_prompt = await self.create_image_generation_prompt(prompt)
        async with self.session.post(url, json=comfy_prompt) as response:
            response.raise_for_status()
            data = await response.json()
            return data['prompt_id']

    async def get_image(self, prompt_id: str) -> bytes:
        """
        Retrieve the generated image for a given prompt ID.

        Args:
            prompt_id (str): The ID of the prompt used to generate the image.

        Returns:
            bytes: The image data.

        Raises:
            aiohttp.ClientError: If there's an error in the API call.
        """
        await self.connect()
        url = self._get_safe_url("view")
        params = {"filename": prompt_id}
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.read()

    async def listen_for_updates(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Listen for updates from the ComfyUI service.

        Yields:
            Dict[str, Any]: Update messages from the ComfyUI service.
        """
        await self.connect()
        ws_url = self._get_safe_url("ws")
        async with self.session.ws_connect(ws_url) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    yield msg.json()
                elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    break
                
    async def create_image_generation_prompt(self, text_prompt: str) -> Dict[str, Any]:
        """
        Create the image generation prompt structure for ComfyUI.

        Args:
            text_prompt (str): The text prompt for image generation.

        Returns:
            Dict[str, Any]: A dictionary containing the structured prompt for ComfyUI.
        """
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