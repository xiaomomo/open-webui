import { WEBUI_API_BASE_URL } from '$lib/constants';

export interface Choice {
	id: string;
	text: string;
	nextScene?: string;
}

export interface Scene {
    id: string;
    text: string;
    type: 'input' | 'choice';
    choices?: Array<{
        id: string;
        text: string;
    }>;
    image?: string;
}

export async function getGameResponse(formData) {
    try {
        // Convert the form data to match the backend model
        const requestBody = {
            lesson_id: formData.lessonId,
            scene_id: formData.sceneId,
            user_input: formData.input,
            choice_id: formData.choiceId,
            action_type: formData.type
        };

        const response = await fetch(`${WEBUI_API_BASE_URL}/lessongame/complateresponse`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get game response');
        }

        return await response.json();
    } catch (error) {
        console.error('Error getting game response:', error);
        throw error;
    }
} 