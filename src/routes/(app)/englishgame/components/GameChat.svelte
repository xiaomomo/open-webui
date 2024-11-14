<script lang="ts">
    import { page } from '$app/stores';
    import { createNewChat, updateChatById } from '$lib/apis/chats';
    import { getLessonUnit } from '$lib/apis/englishlesson/courseApi';
    import { v4 as uuidv4 } from 'uuid';

    let messages = {};
    let currentMessageId = null;

    async function submitGameMessage(content: string) {
        // Create user message
        const userMessageId = uuidv4();
        const userMessage = {
            id: userMessageId,
            parentId: currentMessageId,
            childrenIds: [],
            role: 'user',
            content: content,
            timestamp: Math.floor(Date.now() / 1000)
        };

        // Update messages
        if (currentMessageId) {
            messages[currentMessageId].childrenIds.push(userMessageId);
        }
        messages[userMessageId] = userMessage;
        currentMessageId = userMessageId;

        // Save to chat history
        await saveChatHistory();

        return userMessageId;
    }

    async function receiveGameResponse(content: string, parentMessageId: string) {
        // Create assistant message
        const responseMessageId = uuidv4();
        const responseMessage = {
            id: responseMessageId,
            parentId: parentMessageId,
            childrenIds: [],
            role: 'assistant',
            content: content,
            timestamp: Math.floor(Date.now() / 1000)
        };

        // Update messages
        messages[parentMessageId].childrenIds.push(responseMessageId);
        messages[responseMessageId] = responseMessage;
        currentMessageId = responseMessageId;

        // Save to chat history
        await saveChatHistory();

        return responseMessageId;
    }

    async function saveChatHistory() {
        const lessonUnitId = $page.url.searchParams.get('lessonUnitId');
        if (!lessonUnitId) return;

        try {
            // Create or update chat with current history
            const chatData = {
                title: `English Game - Lesson ${lessonUnitId}`,
                history: {
                    messages,
                    currentId: currentMessageId
                },
                lessonUnitId
            };

            if (!currentChatId) {
                const newChat = await createNewChat(localStorage.token, chatData);
                currentChatId = newChat.id;
            } else {
                await updateChatById(localStorage.token, currentChatId, chatData);
            }
        } catch (error) {
            console.error('Error saving chat history:', error);
        }
    }

    let currentChatId = null;

    export async function startGameChat(currentScene: any) {
        const userMessageId = await submitGameMessage(JSON.stringify(currentScene));
        await receiveGameResponse(JSON.stringify(currentScene), userMessageId);
    }

    export function getCurrentMessages() {
        return messages;
    }

    export function getCurrentMessageId() {
        return currentMessageId;
    }
</script> 