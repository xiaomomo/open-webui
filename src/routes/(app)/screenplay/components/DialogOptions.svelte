<script>
    export let options = [];
    export let onSelect;
</script>

<div class="dialog-options">
    {#each options as option}
        <button 
            class="option-button" 
            on:click={() => onSelect(option)}
        >
            {option}
        </button>
    {/each}
</div>

<style>
    .dialog-options {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        backdrop-filter: blur(8px);
    }

    .option-button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 16px 24px;
        border-radius: 16px;
        font-size: 1.1em;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
        cursor: pointer;
    }

    .option-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
</style> 