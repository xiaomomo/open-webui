<script lang="ts">
    export let messages: any[] = [];
    
    export function getCurrentMessages() {
        return messages;
    }

    export async function startGameChat(scene: any) {
        if (scene?.screenContent) {
            messages = [{
                type: 'host',
                text: scene.screenContent
            }];
        }
    }

    export async function submitGameMessage(message: string) {
        const messageId = Date.now().toString();
        messages = [...messages, {
            id: messageId,
            type: 'player',
            text: message
        }];
        return messageId;
    }

    export async function receiveGameResponse(text: string, type: string = 'npc') {
        messages = [...messages, {
            type,
            text
        }];
    }
</script> 