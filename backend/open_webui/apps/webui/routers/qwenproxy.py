from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import dashscope
from dashscope import Generation
import os
import json
import logging

log = logging.getLogger(__name__)
router = APIRouter()

# Make sure your API key is set
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

@router.get("/get_ai_response")
async def get_ai_response(prompt: str):

    fallback_response = {
        "id": "error",
        "text": "Sorry, there was an error. Please try again.",
        "type": "input"
    }

    try:
        # Call DashScope API
        response = Generation.call(
            model='qwen-max',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        
        log.info(f"DashScope API Response: {response}")
        
        # Validate response structure
        if not response or not hasattr(response, 'output'):
            log.error("Invalid response structure")
            return fallback_response

        return response.output.text

    except Exception as e:
        log.error(f"Error getting AI response: {str(e)}")
        return fallback_response