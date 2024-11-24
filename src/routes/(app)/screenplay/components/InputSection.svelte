<script>
    export let onSendMessage;
    export let onOptionClick;
    
    let inputValue = '';

    function handleSend() {
        if (!inputValue.trim()) return;
        onSendMessage(inputValue);
        inputValue = '';
    }

    const options = ['我觉得是喵喵干的！', '让我问问旺旺', '兔兔看起来很可疑'];
</script>

<div class="input-section">
    <div class="input-group">
        <input 
            type="text" 
            placeholder="输入你的想法..." 
            bind:value={inputValue}
            on:keydown={e => e.key === 'Enter' && handleSend()}
        >
        <button on:click={handleSend}>发送</button>
    </div>
    <div class="options-group">
        {#each options as option}
            <div class="option-btn" on:click={() => onOptionClick(option)}>
                {option}
            </div>
        {/each}
    </div>
</div>

<style>
    .input-section {
        padding: 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px 20px 0 0;
    }

    .input-group {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
    }

    input {
        flex: 1;
        padding: 10px;
        border: 5px solid #ff69b4;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        font-size: 16px;
        color: #333;
    }

    button {
        padding: 10px 20px;
        background: #ff69b4;
        border: 3px solid #fff;
        color: #fff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    button:hover {
        background: #ff1493;
        transform: scale(1.1);
    }

    .options-group {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
    }

    .option-btn {
        padding: 8px 15px;
        background: #e0e0e0;
        border: 3px solid #fff;
        color: #333;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .option-btn:hover {
        background: #ffd700;
        transform: scale(1.1);
    }

    /* 确保输入框在移动设备上也有良好的显示 */
    @media (max-width: 768px) {
        .input-group {
            flex-direction: column;
        }

        .options-group {
            justify-content: center;
        }

        .option-btn {
            width: 100%;
            text-align: center;
        }
    }
</style> 