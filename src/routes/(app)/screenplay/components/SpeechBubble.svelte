<script>
    export let text = '';
    export let hidden = false;
</script>

<div class="speech-bubble" class:hidden>
    <p>{text}</p>
</div>

<style>
    .speech-bubble {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 16px 24px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        font-size: 1.1em;
        color: #1a365d;
        max-width: 300px;
        position: absolute;
        left: 120%;
        top: 50%;
        transform: translateY(-50%);
    }

    .hidden {
        display: none;
    }
</style> 