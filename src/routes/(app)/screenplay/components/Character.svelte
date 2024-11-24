<script>
    export let character;
    export let isActive = false;
    export let messages = [];

    const emojis = {
        '喵喵': '🐱',
        '旺旺': '🐶',
        '兔兔': '🐰',
        '小侦探': '👦'
    };
</script>

<div class="character-container">
    <div 
        class="character" 
        class:active={isActive}
        on:click
    >
        <div class="avatar">
            {emojis[character]}
        </div>
        <div class="name">{character}</div>
    </div>
    {#each messages as message}
        <div class="message {character === '小侦探' ? 'player-message' : 'npc-message'}">
            {message.text}
        </div>
    {/each}
</div>

<style>
    .character-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin-bottom: 10px;
    }

    .character {
        padding: 10px;
        background: linear-gradient(145deg, #ff69b4, #87ceeb);
        border: 5px solid #fff;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
        width: fit-content;
        color: #333;
        transform-origin: center;
    }

    .character:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    }

    .character.active {
        transform: scale(1.2);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }

    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #ffb6c1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }

    .name {
        color: #333;
        font-weight: bold;
    }
</style> 