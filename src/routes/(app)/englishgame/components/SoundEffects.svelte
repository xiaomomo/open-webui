<script>
    export let enabled = true;
    
    const sounds = {
        correct: new Audio('/static/englishgame/correct.mp3'),
        wrong: new Audio('/static/englishgame/wrong.mp3'),
        click: new Audio('/static/englishgame/click.mp3')
    };
    
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