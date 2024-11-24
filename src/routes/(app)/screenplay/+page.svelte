<script>
    import Stars from './components/Stars.svelte';
    import HostSection from './components/HostSection.svelte';
    import GameArea from './components/GameArea.svelte';
    import InputSection from './components/InputSection.svelte';

    let hostMessage = '欢迎来到奇妙剧本杀！今天我们要解开一个有趣的谜题...';
    let messages = [];
    let activeCharacter = null;

    const responses = {
        '喵喵': ['喵~我刚才在晒太阳呢', '我看到旺旺在花园里跑来跑去', '这件事我也很困惑...'],
        '旺旺': ['汪！我在追一只蝴蝶', '我闻到了奇怪的味道', '我看到有人在偷偷摸摸...'],
        '兔兔': ['其实我看到了一些线索...', '我在吃胡萝卜的时候发现...', '要不要检查一下这个地方？']
    };

    function getRandomResponse(character) {
        const characterResponses = responses[character];
        return characterResponses[Math.floor(Math.random() * characterResponses.length)];
    }

    function handleCharacterClick(character) {
        activeCharacter = character;
        const response = getRandomResponse(character);
        messages = [...messages, { type: 'npc', character, text: response }];
        hostMessage = `${character}说话了！让我们听听看...`;

        setTimeout(() => {
            messages = messages.filter(m => m.text !== response);
        }, 5000);
    }

    function handleOptionClick(option) {
        const targetNPC = option.includes('喵喵') ? '喵喵' : 
                         option.includes('旺旺') ? '旺旺' : '兔兔';
        
        messages = [...messages, { type: 'player', text: option }];
        hostMessage = '这是个有趣的观点！';

        setTimeout(() => {
            const response = getRandomResponse(targetNPC);
            messages = [...messages, { type: 'npc', character: targetNPC, text: response }];
        }, 1000);
    }

    function handleSendMessage(text) {
        messages = [...messages, { type: 'player', text }];
        hostMessage = '让我们继续调查...';
    }
</script>

<div class="body">
    <Stars />
    <HostSection message={hostMessage} />
    <GameArea
        {messages}
        {activeCharacter}
        onCharacterClick={handleCharacterClick}
    />
    <InputSection
        onSendMessage={handleSendMessage}
        onOptionClick={handleOptionClick}
    />
</div>

<style>
    :global(*) {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    :global(body) {
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }

    .body {
        font-family: 'Rounded Mplus 1c', 'Comic Sans MS', cursive, sans-serif;
        background: linear-gradient(to bottom, #000, #1a1a1a);
        margin: 0;
        padding: 0;
        width: 100%;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        color: #fff;
        position: relative;
        overflow: hidden;
    }

    :global(.host-section), :global(.game-area), :global(.input-section) {
        background: rgba(255, 255, 255, 0.9);
        border: 8px solid #ff69b4;
        box-shadow: 0 8px 32px rgba(255, 105, 180, 0.3);
        z-index: 10;
        border-radius: 30px;
        margin: 20px;
    }

    :global(.message) {
        position: relative;
        background: linear-gradient(145deg, #ff69b4, #87ceeb);
        border: 5px solid #fff;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        color: #333;
        border-radius: 15px;
        padding: 10px;
        margin: 10px;
        max-width: 80%;
        opacity: 0;
        transform: translateY(20px);
        animation: fadeIn 0.5s ease forwards;
        width: fit-content;
        transform-origin: left center;
        transition: all 0.3s ease;
    }

    :global(.npc-message) {
        margin-left: 60px;
        background: linear-gradient(145deg, #87ceeb, #ff69b4);
        animation: messagePopup 0.3s ease forwards;
    }

    :global(.player-message) {
        margin-right: 60px;
        background: #dcffe4;
        align-self: flex-end;
        color: #333;
        transform-origin: right center;
    }

    @keyframes fadeIn {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes messagePopup {
        0% {
            transform: scale(0.8);
            opacity: 0;
        }
        100% {
            transform: scale(1.1);
            opacity: 1;
        }
    }

    :global(.message::after) {
        content: '';
        position: absolute;
        bottom: -10px;
        border-width: 10px 10px 0;
        border-style: solid;
    }

    :global(.npc-message::after) {
        left: 20px;
        border-color: #e8f4ff transparent;
    }

    :global(.player-message::after) {
        right: 20px;
        border-color: #dcffe4 transparent;
    }
</style>
