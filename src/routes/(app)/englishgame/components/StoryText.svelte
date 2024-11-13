<script lang="ts">
    export let text: string;
    export let isTyping: boolean;

    async function typeWriter(text: string, speed = 50) {
        isTyping = true;
        const storyText = document.getElementById('story-text');
        if (!storyText) return;
        
        storyText.innerHTML = '';
        const cursor = document.createElement('span');
        cursor.className = 'typing-cursor';
        storyText.appendChild(cursor);

        for (let i = 0; i < text.length; i++) {
            await new Promise(resolve => setTimeout(resolve, speed));
            cursor.insertAdjacentText('beforebegin', text[i]);
        }
        
        isTyping = false;
    }

    $: if (text) {
        typeWriter(text);
    }
</script>

<div id="story-area">
    <div id="story-text"></div>
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
</style> 