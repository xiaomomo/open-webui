<script lang="ts">
    export let volume: number;
</script>

<div class="volume-control">
    <input 
        type="range" 
        min="0" 
        max="1" 
        step="0.1" 
        bind:value={volume}
    />
</div>

<style>
    .volume-control {
        position: fixed;
        top: 60px;
        right: 20px;
        z-index: 100;
    }
    
    input[type="range"] {
        width: 100px;
        transform: rotate(-90deg);
    }
</style> 