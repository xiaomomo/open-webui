<script lang="ts">
    export let imageUrl: string | undefined;
</script>

<div id="image-column">
    {#if imageUrl}
        <img 
            id="game-image" 
            src={imageUrl} 
            alt="Scene Image"
            class="show"
        >
    {/if}
</div>

<style>
    #image-column {
        width: 300px;
        background: #FFF5F8;
        border-radius: 25px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    #game-image {
        max-width: 100%;
        height: auto;
        border-radius: 15px;
        display: none;
    }

    #game-image.show {
        display: block;
    }
</style> 