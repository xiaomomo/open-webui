<script lang="ts">
    export let show: boolean = false;
</script>

<div class="loading-container">
    <slot></slot>
    <div class="loading-content">
        <div class="dots">• • •</div>
        <div class="spinner"></div>
        <div class="loading-text">AI is thinking...</div>
    </div>
</div>

<style>
    .loading-container {
        background: #FFF5F8;
        border-radius: 25px;
        padding: 30px;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: 100%;
    }

    .loading-content {
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }

    .loading-text {
        color: #FF69B4;
        font-size: 1.2em;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #FFD1DC;
        border-top: 4px solid #FF69B4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    .dots {
        color: #FF69B4;
        font-size: 2em;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style> 