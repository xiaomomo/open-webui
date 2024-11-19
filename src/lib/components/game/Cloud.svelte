<script>
    export let x;
    export let y;
</script>

<div class="cloud" style="left: {x}px; top: {y}px"></div>

<style>
    .cloud {
        width: 60px;
        height: 30px;
        background: white;
        border-radius: 15px;
        position: absolute;
        opacity: 0.8;
        z-index: 2;
    }

    .cloud::before,
    .cloud::after {
        content: '';
        position: absolute;
        background: white;
        border-radius: 50%;
    }

    .cloud::before {
        width: 25px;
        height: 25px;
        top: -10px;
        left: 15px;
    }

    .cloud::after {
        width: 20px;
        height: 20px;
        top: -5px;
        left: 35px;
    }
</style> 