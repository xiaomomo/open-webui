<script lang="ts">
    export let value: string;
    export let onSubmit: () => void;
</script>

<div id="player-input" class="show">
    <input
        type="text"
        id="input-field"
        bind:value
        on:keypress={(e) => e.key === 'Enter' && onSubmit()}
        placeholder="Type your answer..."
        autocomplete="off"
    >
</div>

<style>
    #player-input {
        width: 100%;
    }

    #input-field {
        width: 100%;
        padding: 15px 25px;
        border: 2px solid #FF9ECD;
        border-radius: 25px;
        font-size: 1.2em;
        outline: none;
        transition: border-color 0.3s;
    }

    #input-field:focus {
        border-color: #FF69B4;
    }
</style> 