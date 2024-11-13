from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessonModel, FredisaLessons
from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.utils import get_admin_user, get_verified_user
import logging

log = logging.getLogger(__name__)
router = APIRouter()

class GameResponse(BaseModel):
    lesson_id: str
    scene_id: Optional[str] = None
    user_input: Optional[str] = None
    choice_id: Optional[str] = None
    action_type: str

@router.post("/complateresponse")
async def complateresponse(form_data: GameResponse):
    try:
        log.info(f"Processing game response: {form_data}")
        
        # Handle different types of responses
        if form_data.action_type == 'start':
            # Return initial scene
            return {
                "id": "start",
                "text": "Welcome! Let's begin the lesson.",
                "type": "input"
            }
            
        elif form_data.action_type == 'input':
            # Process input and return next scene
            return {
                "id": "next_scene",
                "text": f"You entered: {form_data.user_input}",
                "type": "choice",
                "choices": [
                    {"id": "1", "text": "Option 1"},
                    {"id": "2", "text": "Option 2"}
                ]
            }
            
        elif form_data.action_type == 'choice':
            # Process choice and return next scene
            return {
                "id": "final_scene",
                "text": f"You chose option {form_data.choice_id}",
                "type": "input"
            }
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid response type"
        )
            
    except Exception as e:
        log.error(f"Error processing game response: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
