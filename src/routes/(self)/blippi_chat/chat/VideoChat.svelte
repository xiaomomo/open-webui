<script>
	import { onMount } from 'svelte';
	import {getChatById} from '$lib/apis/chats';
	import { generateChatCompletion } from '$lib/apis/ollama';
	import { goto } from '$app/navigation';

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
			const data = await getChatById(localStorage.token, "7736fc63-0d36-4d0a-a9a3-e1e475012a8f").catch(async (error) => {
				await goto('/');
				return null;
			});

			// 提取历史消息并按顺序加入 messages 列表
			const messagesObj = data.chat.history.messages;
			const messagesArray = Object.values(messagesObj);

			// 将消息按时间戳排序
			messagesArray.sort((a, b) => a.timestamp - b.timestamp);

			// 将消息推入 videoChatData.messages
			videoChatData.messages = messagesArray.map(msg => ({
				sender: msg.role === 'user' ? 'kid1' : 'kid2',
				text: msg.content
			}));
		} catch (error) {
			console.error("Error fetching chat history:", error);
		}
	}

	// Send a new message
	async function sendMessage() {
		//can use simple api here
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


	let kid1VideoElement; // 用于获取 Kid 1 的视频元素引用
	let kid2VideoElement; // 用于获取 Kid 2 的视频元素引用

	// 模拟视频的来源链接 (可以替换成实际的视频 URL)
	let kid1VideoSrc = '/static/blippi_video.mov';
	let kid2VideoSrc = 'https://www.w3schools.com/html/mov_bbb.mp4';

	// 控制视频播放
	function playKid1Video() {
		if (kid1VideoElement) {
			kid1VideoElement.play();
		}
	}

	function pauseKid1Video() {
		if (kid1VideoElement) {
			kid1VideoElement.pause();
		}
	}

	function playKid2Video() {
		if (kid2VideoElement) {
			kid2VideoElement.play();
		}
	}

	function pauseKid2Video() {
		if (kid2VideoElement) {
			kid2VideoElement.pause();
		}
	}
</script>


<!-- Video chat layout -->
<div class="container">
	<!-- Video chat section -->
	<div class="video-chat">
		<div class="video">
			<div class="video-content">
				<!-- Kid 1 视频播放器 -->
				<video bind:this={kid1VideoElement} src={kid1VideoSrc} muted playsinline></video>
				<button on:click={playKid1Video}>Play Kid 1 Video</button>
				<button on:click={pauseKid1Video}>Pause Kid 1 Video</button>
			</div>
		</div>

		<div class="video">
			<div class="video-content">
				<!-- Kid 2 视频播放器 -->
				<video bind:this={kid2VideoElement} src={kid2VideoSrc} muted playsinline></video>
<!--				<button on:click={playKid2Video}>Play Kid 2 Video</button>-->
<!--				<button on:click={pauseKid2Video}>Pause Kid 2 Video</button>-->
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
        padding-top: 56.25%; /* 16:9 aspect ratio */
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
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    video {
        width: 100%;
        height: 100%;
        border-radius: 20px;
        object-fit: cover;
    }
    button {
        margin-top: 10px;
        padding: 10px;
        background-color: #FFB6C1;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 1em;
        cursor: pointer;
    }
    button:hover {
        background-color: #FF69B4;
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