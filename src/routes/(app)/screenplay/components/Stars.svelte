<script>
    import { onMount } from 'svelte';

    let stars = [];
    onMount(() => {
        stars = Array(100).fill().map(() => ({
            top: `${Math.random() * 100}vh`,
            left: `${Math.random() * 100}vw`,
            size: `${Math.random() * 2 + 1}px`,
            duration: `${Math.random() * 5 + 2}s`
        }));
    });
</script>

<div class="stars">
    {#each stars as star}
        <div 
            class="star" 
            style="top: {star.top}; 
                   left: {star.left}; 
                   width: {star.size}; 
                   height: {star.size}; 
                   animation-duration: {star.duration};"
        />
    {/each}
</div>

<style>
    .stars {
        position: absolute;
        width: 100%;
        height: 100%;
        background: transparent;
        z-index: 1;
    }

    .star {
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle 5s infinite;
    }

    @keyframes twinkle {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.1; }
    }
</style> 