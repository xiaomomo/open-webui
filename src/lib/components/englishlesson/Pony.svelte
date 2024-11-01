<script>
	export let position = { x: 0, y: 0 };
</script>

<div
	class="pony"
	style="left: {position.x}px; top: {position.y}px"
></div>

<style>
    .pony {
        position: absolute;
        width: 80px;
        height: 80px;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50,20 C30,20 20,40 20,50 C20,70 35,80 50,80 C65,80 80,70 80,50 C80,40 70,20 50,20" fill="%23FF69B4"/><circle cx="40" cy="45" r="5" fill="white"/><circle cx="38" cy="44" r="2" fill="black"/><path d="M45,60 Q50,65 55,60" stroke="white" fill="none" stroke-width="2"/><path d="M15,40 Q25,20 40,25" fill="%23FF69B4"/></svg>');
        background-size: contain;
        transition: all 0.8s ease;
        z-index: 100;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
</style>