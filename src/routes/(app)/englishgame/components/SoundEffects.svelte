<script lang="ts">
    export let enabled = true;
    
    function toggleSound() {
        enabled = !enabled;
    }
</script>

<button class="sound-toggle" on:click={toggleSound}>
    {#if enabled}
        🔊
    {:else}
        🔇
    {/if}
</button>

<style>
    .sound-toggle {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 24px;
        padding: 10px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .sound-toggle:hover {
        background: rgba(255, 255, 255, 1);
    }
</style> 