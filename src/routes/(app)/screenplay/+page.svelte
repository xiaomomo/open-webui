<script>
    import { onMount } from 'svelte';
    import Stars from './components/Stars.svelte';
    import HostSection from './components/HostSection.svelte';
    import GameArea from './components/GameArea.svelte';
    import InputSection from './components/InputSection.svelte';

    let hostMessage = '欢迎来到奇妙剧本杀！今天我们要解开一个有趣的谜题...';
    let title = '';
    let messages = [];
    let activeCharacter = null;
    let characters = [];
    let mainPlayer = '';
    let screenplay = null;
    let responses = {};
    let currentSceneIndex = 0;
    let isLoading = true;

    async function fetchScreenplay() {
        isLoading = true;
        try {
            const response = await fetch('http://localhost:8080/api/v1/screenplay/getScreenPlay');
            const data = await response.json();
            screenplay = JSON.parse(data);
            
            title = screenplay.title;
            characters = screenplay.characters;
            mainPlayer = screenplay.characters.find(char => char.isMainPlayer === "true")?.name || "小侦探";
            
            const firstScene = screenplay.scenes.find(scene => scene.sceneNumber === 1);
            if (firstScene) {
                hostMessage = firstScene.screenContent;
                displaySceneDialogues(firstScene);
            }
            
            responses = screenplay.scenes.reduce((acc, scene) => {
                if (!acc[scene.sceneNumber]) {
                    acc[scene.sceneNumber] = [];
                }
                scene.playerBehavior.dialogue.forEach(dialog => {
                    acc[scene.sceneNumber].push({
                        character: dialog.character,
                        content: dialog.content
                    });
                });
                return acc;
            }, {});

        } catch (error) {
            console.error('Error fetching screenplay:', error);
            hostMessage = '清晨的阳光透过窗户照进房间...';
            title = '默认剧本';
            characters = [
                { name: '小红帽', isMainPlayer: "false" },
                { name: '妈妈', isMainPlayer: "false" },
                { name: '奶奶', isMainPlayer: "false" },
                { name: '狼', isMainPlayer: "false" }
            ];
            mainPlayer = "小红帽";
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        fetchScreenplay();
    });

    function getNextResponse(character, sceneNumber = 1) {
        const sceneDialogues = responses[sceneNumber] || [];
        const characterDialogues = sceneDialogues.filter(d => d.character === character);
        
        const nextDialogue = characterDialogues.find(d => 
            !messages.some(m => m.character === character && m.text === d.content)
        );
        
        return nextDialogue?.content || `${character}沉默不语...`;
    }

    function handleCharacterClick(character) {
        activeCharacter = character;
        const response = getNextResponse(character, currentSceneIndex + 1);
        messages = [...messages, { type: 'npc', character, text: response }];
        hostMessage = `${character}说话了！让我们听听看...`;
    }

    function handleOptionClick(option) {
        const targetNPC = option.includes('喵喵') ? '喵喵' : 
                         option.includes('旺旺') ? '旺旺' : '兔兔';
        
        messages = [...messages, { type: 'player', text: option }];
        hostMessage = '这是个有趣的观点！';

        setTimeout(() => {
            const response = getNextResponse(targetNPC);
            messages = [...messages, { type: 'npc', character: targetNPC, text: response }];
        }, 1000);
    }

    function handleSendMessage(text) {
        messages = [...messages, { type: 'player', text }];
        hostMessage = '让我们继续调查...';
    }

    function displaySceneDialogues(scene) {
        if (scene.playerBehavior && scene.playerBehavior.dialogue) {
            scene.playerBehavior.dialogue.forEach((dialog, index) => {
                setTimeout(() => {
                    messages = [...messages, {
                        type: 'npc',
                        character: dialog.character,
                        text: dialog.content
                    }];
                }, index * 1000);
            });
        }
    }
</script>

<div class="body">
    <Stars />
    <HostSection 
        message={hostMessage}
        {title}
    />
    {#if !isLoading && characters.length > 0}
        <GameArea
            {messages}
            {activeCharacter}
            {characters}
            {mainPlayer}
            onCharacterClick={handleCharacterClick}
        />
    {/if}
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
