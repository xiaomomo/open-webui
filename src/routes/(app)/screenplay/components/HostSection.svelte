<script>
    export let message;
    export let title;
</script>

<div class="host-section">
    <div class="header">
        <div class="host-avatar">🎭</div>
        {#if title}
            <div class="title">{title}</div>
        {/if}
    </div>
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
        padding: 20px;
    }

    .header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 10px;
    }

    .host-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: #ffd700;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        flex-shrink: 0;
    }

    .title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        background: linear-gradient(45deg, #ff69b4, #87ceeb);
        padding: 8px 15px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    #hostMessage {
        margin-top: 10px;
        font-size: 16px;
        line-height: 1.5;
        background: #fff3dc !important;
        color: #333;
        padding: 15px;
        border-radius: 15px;
    }
</style> 