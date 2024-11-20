<script>
    export let message = '';
</script>

<div class="system-message">
    <div class="message-bubble">
        <p>{message}</p>
    </div>
</div>

<style>
    .system-message {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5em;
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    .message-bubble {
        font-size: 1.4em;
        color: #1a365d;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
</style> 