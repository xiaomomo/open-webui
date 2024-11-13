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

    let currentScene: Scene | null = null;
    let inputValue = '';
    let isTyping = false;
    let lessonDetail: any = null;

    async function loadLessonDetail() {
        let lessonUnitId = $page.url.searchParams.get('lessonUnitId');
        if (!lessonUnitId) return;

        try {
            lessonDetail = await getLessonUnit(lessonUnitId);
            // Initialize first scene
            const formData = {
                lessonId: lessonDetail.id,
                type: 'start'
            };
            currentScene = await getGameResponse(formData);
        } catch (error) {
            console.error('Error loading lesson:', error);
        }
    }
    
    onMount(loadLessonDetail);

    async function handleInput() {
        if (!inputValue.trim() || !currentScene) return;
        
        try {
            const formData = {
                lessonId: lessonDetail.id,
                sceneId: currentScene.id,
                input: inputValue,
                type: 'input'
            };

            const response = await getGameResponse(formData);
            console.log('Response received:', response); // Debug log
            currentScene = response;
            inputValue = '';
        } catch (error) {
            console.error('Error handling input:', error);
        }
    }

    async function handleChoice(choiceId: string) {
        if (!currentScene) return;

        try {
            const formData = {
                lessonId: lessonDetail.id,
                sceneId: currentScene.id,
                choiceId: choiceId,
                type: 'choice'
            };

            const response = await getGameResponse(formData);
            currentScene = response;
        } catch (error) {
            console.error('Error handling choice:', error);
        }
    }
</script>

<div id="game-container">
    <GameTitle {lessonDetail} />
    
    <div id="content-area">
        <div id="story-column">
            {#if currentScene}
                <StoryText 
                    text={currentScene.text} 
                    bind:isTyping 
                />
            {/if}
        </div>
        
        <GameImage imageUrl={currentScene?.image} />
    </div>

    <div id="interaction-area">
        {#if currentScene?.type === 'choice' && !isTyping}
            <ChoiceButtons 
                choices={currentScene.choices || []} 
                onSelect={handleChoice} 
            />
        {/if}

        {#if currentScene?.type === 'input' && !isTyping}
            <InputField 
                bind:value={inputValue} 
                onSubmit={handleInput} 
            />
        {/if}
    </div>
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
    }

    #content-area {
        display: flex;
        gap: 30px;
        flex-grow: 1;
        margin-bottom: 30px;
    }

    #story-column {
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    #interaction-area {
        min-height: 120px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
</style>