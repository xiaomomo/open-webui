<script>
    export let mood = 'happy';
    
    const mascotImages = {
        happy: '/static/englishgame/mascot-happy.png',
        thinking: '/static/englishgame/mascot-thinking.png',
        excited: '/static/englishgame/mascot-excited.png',
        sad: '/static/englishgame/mascot-sad.png'
    };
</script>

<div class="mascot">
    <img 
        src={mascotImages[mood]} 
        alt="Game mascot" 
        class="bounce"
    />
</div>

<style>
    .bounce {
        animation: bounce 1s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
</style> 