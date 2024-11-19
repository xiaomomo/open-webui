<script>
    export let x;
    export let y;

    // Generate a random number between 1-5 when component is created
    const iconNumber = Math.floor(Math.random() * 5) + 1;
    const iconPath = `/static/englishgame/icon${iconNumber}.png`;
</script>

<div class="mushroom" style="left: {x}px; top: {y}px">
    <img src={iconPath} alt="decoration icon" />
</div>

<style>
    .mushroom {
        width: 40px;  /* Adjust size as needed */
        height: 40px;
        position: absolute;
        z-index: 1;
        transition: transform 0.3s ease;
    }

    .mushroom img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    /* Optional: Add hover effect */
    .mushroom:hover {
        transform: scale(1.1);
    }
</style> 