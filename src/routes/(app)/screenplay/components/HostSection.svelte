<script>
    export let message;
</script>

<div class="host-section">
    <div class="host-avatar">🎭</div>
    <div class="message global-message" id="hostMessage">{message}</div>
</div>

<style>
    .host-section {
        background: rgba(255, 255, 255, 0.9);
        border: 8px solid #ff69b4;
        box-shadow: 0 8px 32px rgba(255, 105, 180, 0.3);
        z-index: 10;
        border-radius: 30px;
        margin: 20px;
    }

    .host-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #ffd700;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
    }

    #hostMessage {
        margin-top: 10px;
        font-size: 16px;
        line-height: 1.5;
        background: #fff3dc !important;
        color: #333;
    }
</style> 