<script>
    export let character;
    export let isActive = false;
    export let messages = [];
    export let mainPlayer = '';

    // 定义一组可用的表情
    const availableEmojis = [
        '👧', '👦', '👨', '👩', '👴', '👵',  // 人物
        '🐱', '🐶', '🐰', '🐺', '🦊', '🐯',  // 动物
        '🎭', '😊', '🤔', '😄', '😎', '🤓',  // 表情
        '👑', '🎩', '🎪', '🎬', '🎮', '🎨'   // 其他
    ];

    // 使用字符串的哈希值来确定emoji，这样同一个角色总是显示相同的emoji
    function getHashCode(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash);
    }

    // 根据角色名称选择固定的emoji
    const characterEmoji = availableEmojis[getHashCode(character) % availableEmojis.length];
</script>

<div class="character-container" class:is-player={character === mainPlayer}>
    <div 
        class="character" 
        class:active={isActive}
        on:click
    >
        <div class="avatar">
            {characterEmoji}
        </div>
        <div class="name">{character}</div>
    </div>
    {#if messages.length > 0}
        {#each messages as message}
            <div class="message {character === mainPlayer ? 'player-message' : 'npc-message'}">
                {message.text}
            </div>
        {/each}
    {/if}
</div>

<style>
    .character-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin-bottom: 10px;
        align-items: flex-start;
    }

    .character-container.is-player {
        align-items: flex-end;
    }

    .is-player .character {
        flex-direction: row-reverse;
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