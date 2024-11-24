<script>
    import Character from './Character.svelte';

    export let messages = [];
    export let activeCharacter = null;
    export let characters = [];
    export let mainPlayer = '';
    export let onCharacterClick;
</script>

<div class="game-area">
    <div class="characters">
        {#each characters as character}
            <Character
                character={character.name}
                isActive={character.name === activeCharacter}
                messages={messages.filter(m => m.character === character.name)}
                {mainPlayer}
                on:click={() => onCharacterClick(character.name)}
            />
        {/each}
    </div>
</div>

<style>
    .game-area {
        display: flex;
        flex: 1;
        padding: 20px;
        gap: 20px;
        height: 60vh;
        overflow-y: auto;
    }

    .characters {
        width: 100%;
        display: flex;
        flex-direction: column;
    }

    .game-area::-webkit-scrollbar {
        width: 8px;
    }

    .game-area::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }

    .game-area::-webkit-scrollbar-thumb {
        background: rgba(255, 105, 180, 0.5);
        border-radius: 4px;
    }

    .game-area::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 105, 180, 0.7);
    }

    .npc-section {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .player-section {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
</style> 