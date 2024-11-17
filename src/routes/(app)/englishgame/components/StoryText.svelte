<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';

    export let text: string = '';
    export let isTyping: boolean;

    let storyElement: HTMLElement;
    let textElement: HTMLElement;

    async function typeWriter(text: string, speed = 80) {
        if (!textElement) return;
        
        isTyping = true;
        textElement.innerHTML = '';
        const cursor = document.createElement('span');
        cursor.className = 'typing-cursor';
        textElement.appendChild(cursor);

        for (let i = 0; i < text.length; i++) {
            await new Promise(resolve => setTimeout(resolve, speed));
            cursor.insertAdjacentText('beforebegin', text[i]);
        }
        
        isTyping = false;
    }

    $: if (text && textElement) {
        typeWriter(text);
    }
</script>

<div id="story-area">
    <slot></slot>
    <div class="text-wrapper">
        <div id="text-content" bind:this={textElement} class="story-text">
        </div>
    </div>
</div>

<style>
    #story-area {
        background: #FFF5F8;
        border-radius: 25px;
        padding: 30px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .text-wrapper {
        flex-grow: 1;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #FF69B4 #FFE5EC;
    }

    .text-wrapper::-webkit-scrollbar {
        width: 8px;
    }

    .text-wrapper::-webkit-scrollbar-track {
        background: #FFE5EC;
        border-radius: 4px;
    }

    .text-wrapper::-webkit-scrollbar-thumb {
        background: #FF69B4;
        border-radius: 4px;
    }

    #text-content {
        font-size: 1.2em;
        line-height: 1.5;
        color: #444;
        width: 100%;
        padding-right: 10px;
    }

    :global(.typing-cursor) {
        display: inline-block;
        width: 3px;
        height: 1em;
        background: #FF69B4;
        margin-left: 2px;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        50% { opacity: 0; }
    }
</style> 