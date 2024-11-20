<script>
    import SpeechBubble from './SpeechBubble.svelte';
    
    export let character;
    export let isActive = false;
    export let response = '';
    export let isPlayer = false;
</script>

<div class="character {isPlayer ? 'player' : 'npc'} {isActive ? 'active' : ''}"
     id={character.name}>
    <img src="/images/{character.name}.png" alt={character.name}>
    <SpeechBubble text={response} hidden={!isActive} />
</div>

<style>
    .character {
        position: relative;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .character img {
        width: 120px;
        height: 120px;
        object-fit: contain;
        filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.15));
    }

    .character.active {
        transform: scale(1.1);
        z-index: 10;
    }

    .character.npc {
        position: absolute;
        width: 140px;
        height: 140px;
    }

    .character.npc:nth-child(1) {
        left: 15%;
        top: 10%;
    }

    .character.npc:nth-child(2) {
        left: 15%;
        top: 35%;
    }

    .character.npc:nth-child(3) {
        left: 15%;
        top: 60%;
    }
</style> 