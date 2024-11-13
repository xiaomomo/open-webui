<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';

    export let text: string = '';
    export let isTyping: boolean;

    let storyElement: HTMLElement;

    async function typeWriter(text: string, speed = 50) {
        if (!storyElement) return;
        
        isTyping = true;
        storyElement.innerHTML = '';
        const cursor = document.createElement('span');
        cursor.className = 'typing-cursor';
        storyElement.appendChild(cursor);

        for (let i = 0; i < text.length; i++) {
            await new Promise(resolve => setTimeout(resolve, speed));
            cursor.insertAdjacentText('beforebegin', text[i]);
        }
        
        isTyping = false;
    }

    $: if (text && storyElement) {
        typeWriter(text);
    }
</script>

<div id="story-area">
    <div id="story-text" bind:this={storyElement}></div>
</div>

<style>
    #story-area {
        background: #FFF5F8;
        border-radius: 25px;
        padding: 30px;
        flex-grow: 1;
    }

    #story-text {
        font-size: 1.6em;
        line-height: 1.5;
        color: #444;
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