<script lang="ts">
	import { v4 as uuidv4 } from 'uuid';
	import { chats, config, settings, user as _user, mobile, currentChatPage } from '$lib/stores';
	import { tick, getContext, onMount, createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	import { toast } from 'svelte-sonner';
	import { getChatList, updateChatById } from '$lib/apis/chats';
	import { copyToClipboard, findWordIndices } from '$lib/utils';

	import Message from './Messages/Message.svelte';
	import Loader from '../common/Loader.svelte';
	import Spinner from '../common/Spinner.svelte';

	import ChatPlaceholder from './ChatPlaceholder.svelte';

	const i18n = getContext('i18n');

	export let chatId = '';
	export let user = $_user;

	export let prompt;
	export let history = {};
	export let selectedModels;

	let messages = [];

	export let sendPrompt: Function;
	export let continueResponse: Function;
	export let regenerateResponse: Function;
	export let mergeResponses: Function;
	export let chatActionHandler: Function;
	export let showMessage: Function = () => {};

	export let readOnly = false;

	export let bottomPadding = false;
	export let autoScroll;

	let messagesCount = 20;
	let messagesLoading = false;

	const loadMoreMessages = async () => {
		// scroll slightly down to disable continuous loading
		const element = document.getElementById('messages-container');
		element.scrollTop = element.scrollTop + 100;

		messagesLoading = true;
		messagesCount += 20;

		await tick();

		messagesLoading = false;
	};

	$: if (history.currentId) {
		let _messages = [];

		let message = history.messages[history.currentId];
		while (message && _messages.length <= messagesCount) {
			_messages.unshift({ ...message });
			message = message.parentId !== null ? history.messages[message.parentId] : null;
		}

		messages = _messages;
	} else {
		messages = [];
	}

	$: if (autoScroll && bottomPadding) {
		(async () => {
			await tick();
			scrollToBottom();
		})();
	}

	const scrollToBottom = () => {
		const element = document.getElementById('messages-container');
		element.scrollTop = element.scrollHeight;
	};

	const updateChatHistory = async () => {
		await tick();
		history = history;
		await updateChatById(localStorage.token, chatId, {
			history: history,
			messages: messages
		});

		currentChatPage.set(1);
		await chats.set(await getChatList(localStorage.token, $currentChatPage));
	};

	const showPreviousMessage = async (message) => {
		if (message.parentId !== null) {
			let messageId =
				history.messages[message.parentId].childrenIds[
					Math.max(history.messages[message.parentId].childrenIds.indexOf(message.id) - 1, 0)
				];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		} else {
			let childrenIds = Object.values(history.messages)
				.filter((message) => message.parentId === null)
				.map((message) => message.id);
			let messageId = childrenIds[Math.max(childrenIds.indexOf(message.id) - 1, 0)];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		}

		await tick();

		if ($settings?.scrollOnBranchChange ?? true) {
			const element = document.getElementById('messages-container');
			autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	};

	const showNextMessage = async (message) => {
		if (message.parentId !== null) {
			let messageId =
				history.messages[message.parentId].childrenIds[
					Math.min(
						history.messages[message.parentId].childrenIds.indexOf(message.id) + 1,
						history.messages[message.parentId].childrenIds.length - 1
					)
				];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		} else {
			let childrenIds = Object.values(history.messages)
				.filter((message) => message.parentId === null)
				.map((message) => message.id);
			let messageId =
				childrenIds[Math.min(childrenIds.indexOf(message.id) + 1, childrenIds.length - 1)];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		}

		await tick();

		if ($settings?.scrollOnBranchChange ?? true) {
			const element = document.getElementById('messages-container');
			autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	};

	const rateMessage = async (messageId, rating) => {
		history.messages[messageId].annotation = {
			...history.messages[messageId].annotation,
			rating: rating
		};

		await updateChatHistory();
	};

	const editMessage = async (messageId, content, submit = true) => {
		if (history.messages[messageId].role === 'user') {
			if (submit) {
				// New user message
				let userPrompt = content;
				let userMessageId = uuidv4();

				let userMessage = {
					id: userMessageId,
					parentId: history.messages[messageId].parentId,
					childrenIds: [],
					role: 'user',
					content: userPrompt,
					...(history.messages[messageId].files && { files: history.messages[messageId].files }),
					models: selectedModels
				};

				let messageParentId = history.messages[messageId].parentId;

				if (messageParentId !== null) {
					history.messages[messageParentId].childrenIds = [
						...history.messages[messageParentId].childrenIds,
						userMessageId
					];
				}

				history.messages[userMessageId] = userMessage;
				history.currentId = userMessageId;

				await tick();
				await sendPrompt(userPrompt, userMessageId);
			} else {
				// Edit user message
				history.messages[messageId].content = content;
				await updateChatHistory();
			}
		} else {
			if (submit) {
				// New response message
				const responseMessageId = uuidv4();
				const message = history.messages[messageId];
				const parentId = message.parentId;

				const responseMessage = {
					...message,
					id: responseMessageId,
					parentId: parentId,
					childrenIds: [],
					content: content,
					timestamp: Math.floor(Date.now() / 1000) // Unix epoch
				};

				history.messages[responseMessageId] = responseMessage;
				history.currentId = responseMessageId;

				// Append messageId to childrenIds of parent message
				if (parentId !== null) {
					history.messages[parentId].childrenIds = [
						...history.messages[parentId].childrenIds,
						responseMessageId
					];
				}

				await updateChatHistory();
			} else {
				// Edit response message
				history.messages[messageId].originalContent = history.messages[messageId].content;
				history.messages[messageId].content = content;
				await updateChatHistory();
			}
		}
	};

	const deleteMessage = async (messageId) => {
		const messageToDelete = history.messages[messageId];
		const parentMessageId = messageToDelete.parentId;
		const childMessageIds = messageToDelete.childrenIds ?? [];

		// Collect all grandchildren
		const grandchildrenIds = childMessageIds.flatMap(
			(childId) => history.messages[childId]?.childrenIds ?? []
		);

		// Update parent's children
		if (parentMessageId && history.messages[parentMessageId]) {
			history.messages[parentMessageId].childrenIds = [
				...history.messages[parentMessageId].childrenIds.filter((id) => id !== messageId),
				...grandchildrenIds
			];
		}

		// Update grandchildren's parent
		grandchildrenIds.forEach((grandchildId) => {
			if (history.messages[grandchildId]) {
				history.messages[grandchildId].parentId = parentMessageId;
			}
		});

		// Delete the message and its children
		[messageId, ...childMessageIds].forEach((id) => {
			delete history.messages[id];
		});

		await tick();

		showMessage({ id: parentMessageId });

		// Update the chat
		await updateChatHistory();
	};

	//todo 怎么根据message的交互触发这些事件
	let showChatContainer = true;
	let showConfirmation = false;

	function handleConfirm() {
		showConfirmation = true;
		setTimeout(() => {
			showConfirmation = false;
		}, 3000);
	}

	function handleCancel() {
		showChatContainer = false;
	}
</script>

<style>
    .lesson-question-tip {
        background-color: #fff0f6;
        width: 80%;
        max-width: 600px;
        margin: 40px auto;
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        font-family: 'Jost', sans-serif;
        box-shadow: 0 6px 20px rgba(255, 102, 178, 0.3);
        animation: slide-in 0.5s ease-out;
    }

    @keyframes slide-in {
        0% {
            transform: translateY(-20%);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }

    .lesson-question-tip-message {
        font-size: 28px;
        margin-bottom: 25px;
        color: #ff66b2;
        font-weight: bold;
        border: 3px dashed #ff66b2;
        padding: 12px;
        border-radius: 20px;
        background-color: #fff;
    }

    .lesson-question-tip-button-container {
        display: flex;
        justify-content: center;
        margin-top: 25px;
    }

    .lesson-question-tip-button {
        background-color: #ff66b2;
        border: none;
        color: white;
        padding: 12px 26px;
        border-radius: 20px;
        font-size: 20px;
        cursor: pointer;
        margin: 0 8px;
        transition: background-color 0.3s, transform 0.2s;
        box-shadow: 0 4px 10px rgba(255, 102, 178, 0.4);
    }

		/**贴纸样式**/
    .confirmation-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.5);
        animation: firework-burst 1s ease-out forwards;
        opacity: 0;
    }

    .firework-burst {
        width: 100%;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .firework-spark {
        position: absolute;
        width: 20px;
        height: 20px;
        background-color: #ff00ff;
        border-radius: 50%;
        animation: firework-spark 1s ease-out forwards;
    }

    .firework-spark:nth-child(1) {
        top: 50%;
        left: 50%;
        animation-delay: 0.1s;
    }

    .firework-spark:nth-child(2) {
        top: 50%;
        left: 50%;
        animation-delay: 0.2s;
    }

    /* 省略剩余 8 个 .firework-spark 的样式 */

    @keyframes firework-burst {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        50% {
            transform: scale(1.2);
            opacity: 1;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }

    @keyframes firework-spark {
        0% {
            transform: translate(-50%, -50%) scale(0);
        }
        50% {
            transform: translate(-50%, -150%) scale(1);
        }
        100% {
            transform: translate(-50%, -300%) scale(0);
        }
    }
		/**明天继续让AI增强**/

</style>
<div class="h-full flex pt-8">
	{#if Object.keys(history?.messages ?? {}).length == 0}
		<ChatPlaceholder
			modelIds={selectedModels}
			submitPrompt={async (p) => {
				let text = p;

				if (p.includes('{{CLIPBOARD}}')) {
					const clipboardText = await navigator.clipboard.readText().catch((err) => {
						toast.error($i18n.t('Failed to read clipboard contents'));
						return '{{CLIPBOARD}}';
					});

					text = p.replaceAll('{{CLIPBOARD}}', clipboardText);
				}

				prompt = text;

				await tick();

				const chatInputElement = document.getElementById('chat-textarea');
				if (chatInputElement) {
					prompt = p;

					chatInputElement.style.height = '';
					chatInputElement.style.height = Math.min(chatInputElement.scrollHeight, 200) + 'px';
					chatInputElement.focus();

					const words = findWordIndices(prompt);

					if (words.length > 0) {
						const word = words.at(0);
						chatInputElement.setSelectionRange(word?.startIndex, word.endIndex + 1);
					}
				}

				await tick();
			}}
		/>
	{:else}
		<div class="w-full pt-2">
			{#key chatId}
				<div class="w-full">
					{#if messages.at(0)?.parentId !== null}
						<Loader
							on:visible={(e) => {
								console.log('visible');
								if (!messagesLoading) {
									loadMoreMessages();
								}
							}}
						>
							<div class="w-full flex justify-center py-1 text-xs animate-pulse items-center gap-2">
								<Spinner className=" size-4" />
								<div class=" ">Loading...</div>
							</div>
						</Loader>
					{/if}

					{#each messages as message, messageIdx (message.id)}
						<Message
							{chatId}
							bind:history
							messageId={message.id}
							idx={messageIdx}
							{user}
							{showPreviousMessage}
							{showNextMessage}
							{editMessage}
							{deleteMessage}
							{rateMessage}
							{regenerateResponse}
							{continueResponse}
							{mergeResponses}
							{readOnly}
							on:submit={async (e) => {
								dispatch('submit', e.detail);
							}}
							on:action={async (e) => {
								if (typeof e.detail === 'string') {
									await chatActionHandler(chatId, e.detail, message.model, message.id);
								} else {
									const { id, event } = e.detail;
									await chatActionHandler(chatId, id, message.model, message.id, event);
								}
							}}
							on:update={() => {
								updateChatHistory();
							}}
							on:scroll={() => {
								if (autoScroll) {
									const element = document.getElementById('messages-container');
									autoScroll =
										element.scrollHeight - element.scrollTop <= element.clientHeight + 50;
									setTimeout(() => {
										scrollToBottom();
									}, 100);
								}
							}}
							on:play_blippi_animation={() => {
								console.log("Messages play_blippi_animation");
								dispatch('play_blippi_animation');
							}}
							on:pause_blippi_animation={() => {
								console.log("Messages pause_blippi_animation");
								dispatch('pause_blippi_animation');
							}}
						/>
					{/each}

					{#if showChatContainer}
						<div class="lesson-question-tip">
							<div class="lesson-question-tip-message">Let's do a test together</div>
							<div class="lesson-question-tip-button-container">
								<button class="lesson-question-tip-button" on:click={handleConfirm}>Confirm</button>
								<button class="lesson-question-tip-button" on:click={handleCancel}>Cancel</button>
							</div>
						</div>
					{/if}

					{#if showConfirmation}
						<div class="confirmation-container">
							<div class="firework-burst">
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
								<div class="firework-spark"></div>
							</div>
						</div>
					{/if}

				</div>
				<div class="pb-12" />
				{#if bottomPadding}
					<div class="  pb-6" />
				{/if}
			{/key}
		</div>
	{/if}
</div>
