<script>
    export let choices = [];
    export let onSendMessage;
    export let onOptionClick;
</script>

<div class="input-section">
    {#if choices && choices.length > 0}
        <div class="options">
            {#each choices as choice}
                <button 
                    class="option-button"
                    on:click={() => onOptionClick(choice)}
                >
                    <span class="option-label">{choice.option}:</span>
                    <span class="option-content">{choice.content}</span>
                </button>
            {/each}
        </div>
    {:else}
        <div class="input-container">
            <input 
                type="text" 
                placeholder="输入你的想法..."
                on:keydown={(e) => e.key === 'Enter' && onSendMessage(e.target.value)}
            />
            <button on:click={() => onSendMessage(document.querySelector('input').value)}>
                发送
            </button>
        </div>
    {/if}
</div>

<style>
    .input-section {
        padding: 20px;
        width: 100%;
    }

    .options {
        display: flex;
        flex-direction: column;
        gap: 15px;
        align-items: center;
    }

    .option-button {
        padding: 15px 20px;
        border: none;
        border-radius: 20px;
        background: linear-gradient(145deg, #ff69b4, #87ceeb);
        color: white;
        cursor: pointer;
        transition: transform 0.2s;
        width: 80%;
        max-width: 600px;
        text-align: left;
        display: flex;
        gap: 10px;
        align-items: center;
    }

    .option-button:hover {
        transform: scale(1.02);
    }

    .option-label {
        font-weight: bold;
        font-size: 1.2em;
        min-width: 30px;
    }

    .option-content {
        flex: 1;
    }

    .input-container {
        display: flex;
        gap: 10px;
    }

    input {
        flex: 1;
        padding: 10px;
        border: 2px solid #ff69b4;
        border-radius: 20px;
        outline: none;
    }

    button {
        padding: 10px 20px;
        border: none;
        border-radius: 20px;
        background: #ff69b4;
        color: white;
        cursor: pointer;
    }
</style> 