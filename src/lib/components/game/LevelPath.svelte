<script>
    export let pathData;
</script>

<svg class="level-path" width="100%" height="100%">
    <path d={pathData} />
</svg>

<style>
    .level-path {
        position: absolute;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }

    .level-path path {
        fill: none;
        stroke: rgba(255, 255, 255, 0.8);
        stroke-width: 4;
        stroke-dasharray: 8 8;
    }
</style> 