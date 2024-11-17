<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import type { Scene } from '$lib/apis/englishlesson/gameApi';
	import { getLessonUnit } from '$lib/apis/englishlesson/courseApi';
	import { getGameResponse } from '$lib/apis/englishlesson/gameApi';
	import GameTitle from './components/GameTitle.svelte';
	import StoryText from './components/StoryText.svelte';
	import GameImage from './components/GameImage.svelte';
	import ChoiceButtons from './components/ChoiceButtons.svelte';
	import InputField from './components/InputField.svelte';
	import LoadingSpinner from './components/LoadingSpinner.svelte';
	import ConfettiEffect from './components/ConfettiEffect.svelte';
	import CharacterMascot from './components/CharacterMascot.svelte';
	import SoundEffects from './components/SoundEffects.svelte';
	import GameChat from './components/GameChat.svelte';
	import { synthesizeSoVITSSpeech } from '$lib/apis/audio';
	import { config, models, settings, user } from '$lib/stores';
	import BackgroundMusic from './components/BackgroundMusic.svelte';

	let currentScene: Scene | null = null;
	let inputValue = '';
	let isTyping = false;
	let lessonDetail: any = null;
	let isLoading = false;
	let showConfetti = false;
	let mascotMood = 'happy'; // Can be: happy, thinking, excited, etc.
	let soundEnabled = true;
	let gameChat: GameChat;
	let bgMusicVolume = 0.3;
	let bgMusic: HTMLAudioElement;
	let backgroundMusicComponent: any;
	
	async function loadLessonDetail() {
		isLoading = true;
		let lessonUnitId = $page.url.searchParams.get('lessonUnitId');
		if (!lessonUnitId) return;

		try {
			lessonDetail = await getLessonUnit(lessonUnitId);
			// Initialize first scene
			const formData = {
				lessonId: lessonDetail.id,
				type: 'start',
				courseContent: lessonDetail.lesson_json,
				courseQuestions: lessonDetail.question_json,
				lessonImg: lessonDetail.lesson_img
			};
			currentScene = await getGameResponse(formData);
		} catch (error) {
			console.error('Error loading lesson:', error);
		} finally {
			isLoading = false;
		}
	}

	onMount(async () => {
		await loadLessonDetail();
		if (gameChat) {
			await gameChat.startGameChat(currentScene);
		}
		backgroundMusicComponent?.startMusic();
	});

	async function handleGameResponse(formData: any, userMessage: string) {
		isLoading = true;
		try {
			const response = await getGameResponse(formData);
			currentScene = response;

			try {
				const defaultVoice = $settings?.audio?.tts?.defaultVoice;
				const configVoice = $config?.audio?.tts?.voice;
				const selectedVoice = defaultVoice === configVoice
					? ($settings?.audio?.tts?.voice ?? configVoice)
					: configVoice;

				if (selectedVoice) {
					if (bgMusic) {
						const originalVolume = bgMusic.volume;
						bgMusic.volume = 0.1;
					}

					const audio = await synthesizeSoVITSSpeech(
						localStorage.token,
						selectedVoice,
						response.text
					);

					if (audio) {
						const blob = await audio.blob();
						const blobUrl = URL.createObjectURL(blob);
						const audioElement = new Audio(blobUrl);
						
						audioElement.onended = () => {
							if (bgMusic) {
								bgMusic.volume = bgMusicVolume;
							}
						};
						
						
						audioElement.play();
					}
				}
			} catch (error) {
				console.error('TTS Error:', error);
				if (bgMusic) {
					bgMusic.volume = bgMusicVolume;
				}
			}

			if (gameChat) {
				const userMessageId = await gameChat.submitGameMessage(userMessage);
				await gameChat.receiveGameResponse(response.text, userMessageId);
			}

			return response;
		} catch (error) {
			console.error('Error handling game response:', error);
			throw error;
		} finally {
			isLoading = false;
		}
	}

	async function handleInput() {
		if (!inputValue.trim() || !currentScene) return;

		try {
			const formData = {
				lessonId: lessonDetail.id,
				sceneId: currentScene.id,
				input: inputValue,
				type: 'input',
				messages: gameChat.getCurrentMessages(),
				courseContent: lessonDetail.lesson_json,
				courseQuestions: lessonDetail.question_json
			};

			await handleGameResponse(formData, inputValue);
			inputValue = '';
		} catch (error) {
			console.error('Error handling input:', error);
		}
	}

	async function handleChoice(choiceId: string) {
		if (!currentScene || !gameChat) return;

		try {
			const formData = {
				lessonId: lessonDetail.id,
				sceneId: currentScene.id,
				choiceId: choiceId,
				type: 'choice',
				messages: gameChat.getCurrentMessages(),
				courseContent: lessonDetail.lesson_json,
				courseQuestions: lessonDetail.question_json
			};

			await handleGameResponse(formData, choiceId);
			
			showConfetti = true;
			mascotMood = 'excited';
			setTimeout(() => showConfetti = false, 2000);
		} catch (error) {
			console.error('Error handling choice:', error);
		}
	}

	function handleStartGame() {
		backgroundMusicComponent?.startMusic();
		// ... rest of your start game logic
	}
</script>

<BackgroundMusic 
	bind:this={backgroundMusicComponent}
	enabled={true} 
	volume={bgMusicVolume}
	bind:audio={bgMusic}
/>
<div id="game-container">
	<div class="title-container">
		<GameTitle {lessonDetail} />
	</div>

	<div id="content-area">
		<div id="story-column">
			<div class="story-content">
				{#if currentScene && !isLoading}
					<StoryText
						text={currentScene.text}
						bind:isTyping
					>
						<div class="mascot-container">
							<CharacterMascot mood={mascotMood} />
						</div>
					</StoryText>
				{:else}
					<LoadingSpinner show={true}>
						<div class="mascot-container">
							<CharacterMascot mood="thinking" />
						</div>
					</LoadingSpinner>
				{/if}
				<GameChat bind:this={gameChat} />
			</div>
		</div>

		<GameImage imageUrl={currentScene?.image || lessonDetail?.lesson_img} />
	</div>

	<div id="interaction-area">
		{#if currentScene?.type === 'choice' && !isTyping && !isLoading}
			<ChoiceButtons
				choices={currentScene.choices || []}
				onSelect={handleChoice}
			/>
		{/if}

		{#if currentScene?.type === 'input' && !isTyping && !isLoading}
			<InputField
				bind:value={inputValue}
				onSubmit={handleInput}
			/>
		{/if}
	</div>

	{#if showConfetti}
		<ConfettiEffect />
	{/if}
</div>

<style>
    #game-container {
        background: white;
        border-radius: 40px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        padding: 40px;
        max-width: 900px;
        width: 100%;
        min-height: 700px;
        display: flex;
        flex-direction: column;
        position: relative;
    }

    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 30px;
        width: 100%;
    }

    #content-area {
        display: flex;
        gap: 30px;
        flex-grow: 1;
        margin-bottom: 30px;
        height: 500px;
    }

    #story-column {
        flex: 1;
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    #interaction-area {
        min-height: 120px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .story-content {
        background-color: #FFF2F4;
        border-radius: 20px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .mascot-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 20px;
        flex-shrink: 0;
    }

    :global(.mascot) {
        width: 120px;
        height: 120px;
    }

    :global(.sound-toggle) {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 100;
    }
</style>