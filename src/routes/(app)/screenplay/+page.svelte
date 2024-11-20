<script>
    import { onMount } from 'svelte';
    import SystemMessage from './components/SystemMessage.svelte';
    import Character from './components/Character.svelte';
    import DialogOptions from './components/DialogOptions.svelte';

    let currentScene = 'start';
    let currentDialog = {};
    let characters = [];
    
    async function fetchGameData() {
        try {
            const response = await fetch('/api/screenplay/data');
            const data = await response.json();
            characters = data.characters;
            currentDialog = data.currentDialog;
        } catch (error) {
            console.error('Failed to fetch game data:', error);
        }
    }

    async function handleOptionSelect(option) {
        try {
            const response = await fetch('/api/screenplay/select', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    option,
                    currentScene
                })
            });
            const data = await response.json();
            currentDialog = data.dialog;
            currentScene = data.scene;
        } catch (error) {
            console.error('Failed to process selection:', error);
        }
    }

    onMount(fetchGameData);
</script>

<div class="game-container">
    <SystemMessage message={currentDialog.systemMessage} />

    <div class="game-scene">
        <div class="scene-background">
            <img src="/images/scene1.jpg" alt="游戏场景">
        </div>

        <div class="npc-area">
            {#each characters.filter(char => !char.isPlayer) as character}
                <Character 
                    {character}
                    isActive={currentDialog.activeNPC === character.name}
                    response={currentDialog.npcResponse}
                />
            {/each}
        </div>

        <div class="player-area">
            {#each characters.filter(char => char.isPlayer) as character}
                <Character 
                    {character}
                    isPlayer={true}
                    response={currentDialog.playerResponse}
                    isActive={currentDialog.playerResponse !== ""}
                />
            {/each}
        </div>
    </div>

    <DialogOptions 
        options={currentDialog.options || []}
        onSelect={handleOptionSelect}
    />
</div>

<style>
    .game-container {
        width: 100%;
        height: 100vh;
        display: flex;
        flex-direction: column;
        background: linear-gradient(120deg, #f6f9fc 0%, #e9f2ff 100%);
        font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
        padding: 20px;
        gap: 20px;
    }

    .game-scene {
        flex: 1;
        position: relative;
        border-radius: 24px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
    }

    .scene-background img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
</style> 