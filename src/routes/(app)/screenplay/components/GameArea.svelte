<script>
    import Character from './Character.svelte';

    export let messages = [];
    export let activeCharacter = null;
    export let onCharacterClick;
    export let characters;
    export let mainPlayer;
</script>

<div class="game-area">
    <div class="npc-section">
        {#each characters.filter(char => char.isMainPlayer === "false") as character}
            <Character
                character={character.name}
                isActive={activeCharacter === character.name}
                messages={messages.filter(m => m.type === 'npc' && m.character === character.name)}
                on:click={() => onCharacterClick(character.name)}
            />
        {/each}
    </div>
    <div class="player-section">
        <Character
            character={mainPlayer}
            messages={messages.filter(m => m.type === 'player')}
        />
    </div>
</div>

<style>
    .game-area {
        display: flex;
        flex: 1;
        padding: 20px;
        gap: 20px;
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