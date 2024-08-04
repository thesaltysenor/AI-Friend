from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.ai.lm_client import LMStudioClient
import logging

router = APIRouter()
lm_client = LMStudioClient()

@router.get("")
async def models_endpoint():
    try:
        models = await lm_client.get_models()
        return JSONResponse(status_code=200, content=models)
    except Exception as e:
        logging.error(f"API call failed: {e}")
        raise HTTPException(status_code=500, detail=f"API call failed: {e}")