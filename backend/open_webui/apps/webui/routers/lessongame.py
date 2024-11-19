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

class CourseContent(BaseModel):
    unit: str
    objectives: list[str]
    lesson_story: str
    vocabulary: list
    key_sentences: list

class GameResponse(BaseModel):
    lesson_id: str
    scene_id: Optional[str] = None
    user_input: Optional[str] = None
    choice_id: Optional[str] = None
    action_type: str
    messages: Optional[list] = None
    course_content: Optional[CourseContent] = None
    course_questions: Optional[list] = None

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
        
        # Convert messages to conversation format
        conversation_history = ""
        if form_data.messages:
            for msg in form_data.messages:
                role = "Assistant" if msg.get("isBot") else "User"
                conversation_history += f"{role}: {msg.get('content', '')}\n"
        
        # Format course content and questions for the prompt
        course_content = json.dumps(form_data.course_content.dict() if form_data.course_content else {}, indent=2)
        course_questions = json.dumps(form_data.course_questions if form_data.course_questions else [], indent=2)
        
        # Unified prompt combining My Little Pony theme with game mechanics
        prompt = f"""You're a My Little Pony text adventure game made for kids. You're designed to be really fun, so lots of kids like to play.

        Current game state:
        - Action Type: {form_data.action_type}
        - User Input: {form_data.user_input if form_data.user_input else 'None'}
        - Choice Selected: {form_data.choice_id if form_data.choice_id else 'None'}

        Previous conversation:
        {conversation_history}

        The game is around her adventure, where players will make choices based on the course content and questions provided.

        The game content are:
        <CourseContent>
        {course_content}
        </CourseContent>

        The game challenge are:
        <CourseQuestions>
        {course_questions}
        </CourseQuestions>

        The game is suitable for fans of My Little Pony, combining fun, exploration, and decision-making elements that reflect the values of friendship and learning. It includes various paths and endings based on players' choices throughout the adventure.

        Use simple sentences to move the story forward. After 5 game challenges finish, the game will be over with congratulations.

        Generate an appropriate game response in JSON format. The response should:
        1. For new conversations, provide a welcoming message with type "input"
        2. For user inputs, provide feedback and present choices with type "choice"
        3. For user choices, provide feedback and continue the conversation with type "input"

        Response must be in this JSON format:
        {{
            "id": "<scene_id>",
            "text": "<response text>",
            "type": "input" or "choice",
            "choices": [                    // Include only if type is "choice"
                {{"id": "1", "text": "<option 1>"}},
                {{"id": "2", "text": "<option 2>"}}
            ]
        }}

        Make the response fun, engaging, and suitable for kids learning English through My Little Pony adventures."""

        print(f"lesson game Prompt: {prompt}")
        try:
            # Call DashScope API with error handling
            response = Generation.call(
                model='qwen-max',
                messages=[
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
