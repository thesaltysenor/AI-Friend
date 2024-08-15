# app/api/v1/endpoints/models.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from app.services.ai.lm_client import LMStudioClient
from app.core.dependencies import get_lm_client
import logging

router = APIRouter()

@router.get("")
async def models_endpoint(lm_client: LMStudioClient = Depends(get_lm_client)):
    try:
        models = await lm_client.get_models()
        return JSONResponse(status_code=status.HTTP_200_OK, content=models)
    except Exception as e:
        logging.error(f"API call failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"API call failed: {e}")