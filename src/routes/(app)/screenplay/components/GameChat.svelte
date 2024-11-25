<script lang="ts">
    export let messages: any[] = [];
    
    export function getCurrentMessages() {
        return messages;
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

		export async function receiveServerResponse(text: string, type: string = 'server') {
			const messageId = Date.now().toString();
			messages = [...messages, {
				id: messageId,
				type,
				text
			}];
		}
</script> 