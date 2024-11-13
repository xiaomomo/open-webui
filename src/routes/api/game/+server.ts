import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

// Example game scenes (in real app, this would be in a database)
const gameScenes = {
    start: {
        id: 'start',
        text: "Welcome to Ponyville! 🏰 You're a new pony in town. What's your favorite color? This will help determine what kind of pony you are!",
        type: 'input',
        nextScene: 'chooseName'
    },
    chooseName: {
        id: 'chooseName',
        text: "That's a wonderful color! Now, what would you like your pony name to be?",
        type: 'input',
        nextScene: 'meetTwilight'
    },
    meetTwilight: {
        id: 'meetTwilight',
        text: "Hello! I'm Twilight Sparkle. What would you like to do?",
        type: 'choice',
        choices: [
            { id: 'magic', text: "Learn about magic 📚", nextScene: 'learnMagic' },
            { id: 'explore', text: "Explore Ponyville 🏘️", nextScene: 'explorePonyville' },
            { id: 'friends', text: "Make new friends 👋", nextScene: 'makeFriends' }
        ]
    }
    // Add more scenes as needed
};

export const POST: RequestHandler = async ({ request }) => {
    const data = await request.json();
    const { action, sceneId, input, choiceId } = data;

    switch (action) {
        case 'start':
            return json(gameScenes.start);

        case 'input':
            const inputScene = gameScenes[sceneId];
            if (!inputScene || !inputScene.nextScene) {
                throw new Error('Invalid scene');
            }
            return json(gameScenes[inputScene.nextScene]);

        case 'choice':
            const choiceScene = gameScenes[sceneId];
            if (!choiceScene || !choiceScene.choices) {
                throw new Error('Invalid scene');
            }
            const selectedChoice = choiceScene.choices.find(c => c.id === choiceId);
            if (!selectedChoice || !selectedChoice.nextScene) {
                throw new Error('Invalid choice');
            }
            return json(gameScenes[selectedChoice.nextScene]);

        default:
            throw new Error('Invalid action');
    }
}; 