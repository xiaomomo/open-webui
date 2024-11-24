<script>
    import Character from './Character.svelte';

    export let messages = [];
    export let activeCharacter = null;
    export let onCharacterClick;

    const characters = ['喵喵', '旺旺', '兔兔'];
</script>

<div class="game-area">
    <div class="npc-section">
        {#each characters as character}
            <Character
                {character}
                isActive={activeCharacter === character}
                messages={messages.filter(m => m.type === 'npc' && m.character === character)}
                on:click={() => onCharacterClick(character)}
            />
        {/each}
    </div>
    <div class="player-section">
        <Character
            character="小侦探"
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