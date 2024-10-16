<script>
	import { onMount } from 'svelte';

	let videoChatData = {
		kid1: { name: 'Kid 1', avatar: 'https://via.placeholder.com/40' },
		kid2: { name: 'Kid 2', avatar: 'https://via.placeholder.com/40/FFC1E3' },
		messages: []
	};
	let newMessage = '';
	let loading = false;

	// Fetch chat history on component mount
	async function fetchChatHistory() {
		try {
			const response = await fetch('/get_history_msg');
			const data = await response.json();
			videoChatData.messages = data.messages;
		} catch (error) {
			console.error("Error fetching chat history:", error);
		}
	}

	// Send a new message
	async function sendMessage() {
		if (!newMessage.trim()) return; // Prevent sending empty messages
		loading = true;

		try {
			const response = await fetch('/send_text_msg', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ text: newMessage })
			});

			if (response.ok) {
				const data = await response.json();
				videoChatData.messages.push({ sender: 'kid1', text: newMessage }); // Update the chat with the new message

				newMessage = ''; // Clear input field

				// Now, fetch response from the server
				await getMessageResponse();
			} else {
				console.error("Failed to send message");
			}
		} catch (error) {
			console.error("Error sending message:", error);
		} finally {
			loading = false;
		}
	}

	// Get the response from the backend after sending the message
	async function getMessageResponse() {
		try {
			const response = await fetch('/get_msg_response');
			const data = await response.json();

			if (data && data.text) {
				videoChatData.messages.push({ sender: 'kid2', text: data.text }); // Add Kid 2's response
			}
		} catch (error) {
			console.error("Error getting response:", error);
		}
	}

	// Fetch the chat history when the component mounts
	onMount(() => {
		fetchChatHistory();
	});
</script>

<!-- Video chat layout -->
<div class="container">
	<!-- Video chat section -->
	<div class="video-chat">
		<div class="video">
			<div class="video-content">
				<p>{videoChatData.kid1.name}'s Video</p>
			</div>
		</div>
		<div class="video">
			<div class="video-content">
				<p>{videoChatData.kid2.name}'s Video</p>
			</div>
		</div>
	</div>

	<!-- Chat section -->
	<div class="chat-section">
		<div class="chat-history">
			{#each videoChatData.messages as message}
				<div class="message {message.sender === 'kid2' ? 'sender' : ''}">
					{#if message.sender === 'kid1'}
						<img class="avatar" src={videoChatData.kid1.avatar} alt="Kid 1 Avatar">
					{/if}
					<div class="message-content">
						<div class="nickname">{message.sender === 'kid1' ? videoChatData.kid1.name : videoChatData.kid2.name}</div>
						<p>{message.text}</p>
					</div>
					{#if message.sender === 'kid2'}
						<img class="avatar" src={videoChatData.kid2.avatar} alt="Kid 2 Avatar">
					{/if}
				</div>
			{/each}
		</div>

		<!-- Input area for new messages -->
		<div class="input-area">
			<input
				type="text"
				placeholder="Type here..."
				bind:value={newMessage}
				on:keydown={(e) => e.key === 'Enter' && !loading && sendMessage()}
			/>
			<button on:click={sendMessage} disabled={loading}>😊</button>
		</div>
	</div>
</div>

<style>
    .container {
        display: flex;
        width: 100%;
        height: 100%;
    }
    .video-chat {
        flex-basis: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 10px;
        background-color: #FFF0F5;
    }
    .video {
        width: 90%;
        position: relative;
        padding-top: 56.25%;
        margin-bottom: 20px;
    }
    .video-content {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #FFF2F8;
        border-radius: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .chat-section {
        flex-basis: 50%;
        background-color: #FFF2F8;
        border-radius: 20px;
        margin: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .chat-history {
        flex: 1;
        padding: 10px;
        overflow-y: auto;
        border-bottom: 2px solid #FFC1E3;
    }
    .message, .message.sender {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .message {
        justify-content: flex-start;
    }
    .message.sender {
        justify-content: flex-end;
    }
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .message.sender .avatar {
        margin-right: 0;
        margin-left: 10px;
    }
    .message-content {
        background-color: #FFB6C1;
        padding: 10px;
        border-radius: 10px;
        color: #fff;
        font-size: 1.2em;
        text-align: left;
        max-width: 70%;
    }
    .message.sender .message-content {
        background-color: #B3E5FC;
    }
    .nickname {
        font-size: 0.9em;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .input-area {
        display: flex;
        padding: 10px;
        align-items: center;
        background-color: #FFF2F8;
        border-top: 2px solid #FFC1E3;
    }
    .input-area input {
        width: 80%;
        height: 40px;
        border-radius: 15px;
        border: 2px solid #FFB6C1;
        padding-left: 10px;
        font-size: 1em;
        outline: none;
    }
    .input-area button {
        background-color: #FFB6C1;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 1.5em;
        margin-left: 10px;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>