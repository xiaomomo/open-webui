<script>
		import { onMount } from 'svelte';
    import confetti from 'canvas-confetti';
    
    onMount(() => {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    });
</script> 