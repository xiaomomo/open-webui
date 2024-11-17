<script lang="ts">
    export let enabled = true;
    export let volume = 0.3;
    
    let audio: HTMLAudioElement;
    let hasInteracted = false;
    
    const bgMusicUrl = '/static/englishgame/background-music.mp3';
    
    // Initialize audio without autoplay
    function initAudio() {
        audio = new Audio(bgMusicUrl);
        audio.loop = true;
        audio.volume = volume;
    }
    
    // Function to start music after user interaction
    export function startMusic() {
        if (audio && enabled && !hasInteracted) {
            hasInteracted = true;
            audio.play().catch(err => console.error('Audio playback failed:', err));
        }
    }
    
    $: if (audio && enabled !== undefined && hasInteracted) {
        if (enabled) {
            audio.play().catch(err => console.error('Audio playback failed:', err));
        } else {
            audio.pause();
        }
    }
    
    $: if (audio && volume !== undefined) {
        audio.volume = volume;
    }
</script>

<svelte:head>
    <audio 
        bind:this={audio} 
        src={bgMusicUrl}
        preload="auto"
        on:canplaythrough={initAudio}
    />
</svelte:head> 