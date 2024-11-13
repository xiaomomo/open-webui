<script lang="ts">
    import type { Choice } from '$lib/apis/englishgame/englishGameApi';
    
    export let choices: Choice[];
    export let onSelect: (choiceId: string) => void;
</script>

<div id="choices-container">
    {#each choices as choice}
        <button 
            class="choice-button"
            on:click={() => onSelect(choice.id)}
        >
            {choice.text}
        </button>
    {/each}
</div>

<style>
    #choices-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .choice-button {
        background: linear-gradient(135deg, #FFB6C1, #FF69B4);
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        margin: 10px;
        font-size: 1.2em;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .choice-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4);
    }
</style> 