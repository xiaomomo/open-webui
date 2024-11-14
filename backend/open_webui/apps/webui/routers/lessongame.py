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
        
        # Default fallback response
        fallback_response = {
            "id": "error",
            "text": "Sorry, there was an error. Please try again.",
            "type": "input"
        }
        
        # Construct prompt based on action type
        if form_data.action_type == 'start':
            prompt = """Generate a game scene response in JSON format with the following structure:
            {
                "id": "start",
                "text": "<welcome message>",
                "type": "input"
            }
            Make it welcoming and engaging for an English learning game."""
            
        elif form_data.action_type == 'input':
            prompt = f"""Based on user input: "{form_data.user_input}", generate a game scene response in JSON format:
            {{
                "id": "next_scene",
                "text": "<response based on user input>",
                "type": "choice",
                "choices": [
                    {{"id": "1", "text": "<option 1>"}},
                    {{"id": "2", "text": "<option 2>"}}
                ]
            }}
            Make the response educational and interactive."""
            
        elif form_data.action_type == 'choice':
            prompt = f"""Based on user choice {form_data.choice_id}, generate a game scene response in JSON format:
            {{
                "id": "final_scene",
                "text": "<response based on user choice>",
                "type": "input"
            }}
            Provide feedback that encourages learning."""

        try:
            # Call DashScope API with error handling
            response = Generation.call(
                model='qwen-plus',
                messages=[
                    {'role': 'system', 'content': 'You are an English learning game assistant. Provide responses in valid JSON format only.'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            
            # Debug logging
            log.info(f"DashScope API Response: {response}")
            
            # Validate response structure
            if not response or not hasattr(response, 'output'):
                log.error("Invalid response structure")
                return fallback_response
            
            # Get the text content from the response
            ai_text = response.output.text
            log.error(f"AI text response: {ai_text}")
            
            try:
                # Parse the JSON from the text content
                parsed_response = json.loads(ai_text)
                
                # Validate required fields
                if not all(key in parsed_response for key in ['id', 'text', 'type']):
                    log.error(f"Missing required fields in parsed response: {parsed_response}")
                    return fallback_response
                
                log.info(f"Successfully parsed response: {parsed_response}")
                return parsed_response
                
            except json.JSONDecodeError as je:
                log.error(f"JSON parsing error: {str(je)}")
                return fallback_response
                
        except Exception as api_error:
            log.error(f"DashScope API error: {str(api_error)}")
            return fallback_response
            
    except Exception as e:
        log.error(f"Error processing game response: {str(e)}")
        return fallback_response
