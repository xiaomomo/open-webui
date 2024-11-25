<script lang="ts">
    import { onMount } from 'svelte';
    import Stars from './components/Stars.svelte';
    import HostSection from './components/HostSection.svelte';
    import GameArea from './components/GameArea.svelte';
    import InputSection from './components/InputSection.svelte';
    import GameChat from './components/GameChat.svelte';
    import { WEBUI_API_BASE_URL } from '$lib/constants';

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
    let showInputSection = false;
    let playerChoices = [];
    let gameChat: GameChat;

    async function fetchScreenplay() {
        isLoading = true;
        try {
            const response = await fetch(`${WEBUI_API_BASE_URL}/screenplay/getScreenPlay`);
            const data = await response.json();
            screenplay = JSON.parse(data);
            
            title = screenplay.title;
            characters = screenplay.characters;
            mainPlayer = screenplay.characters.find(char => char.isMainPlayer === "true")?.name || "侦探";
            
            const firstScene = screenplay.scenes.find(scene => scene.sceneNumber === 1);
            if (firstScene) {
                hostMessage = firstScene.screenContent;
                playerChoices = firstScene.playerChoice || [];
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

    async function handleOptionClick(choice) {
        // 记录玩家选择
        if (gameChat) {
            await gameChat.submitGameMessage(`${choice.option}: ${choice.content}`);
        }

        hostMessage = choice.consequence;
        if (gameChat) {
            gameChat.receiveGameResponse(choice.consequence, 'host'); // 记录选择的结果
        }

        // 选择后清空选项，隐藏输入区
        playerChoices = [];
        showInputSection = false;

        // 获取所有对话历史
        const chatHistory = gameChat ? gameChat.getCurrentMessages() : [];
        
        try {
            // 准备请求数据
            const requestData = {
                currentSceneIndex,
                selectedChoice: choice,
                chatHistory,
                screenplay: screenplay.id
            };

            // 发送请求获取下一个场景
            const response = await fetch(`${WEBUI_API_BASE_URL}/screenplay/nextScene`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error('Failed to fetch next scene');
            }

            const nextSceneData = await response.json();
            currentSceneIndex = nextSceneData.sceneNumber - 1;
            displaySceneDialogues(nextSceneData);

        } catch (error) {
            console.error('Error fetching next scene:', error);
            hostMessage = '抱歉，发生了一些错误...';
        }
    }

    function handleSendMessage(text) {
        messages = [...messages, { type: 'player', text }];
        hostMessage = '让我们继续调查...';
    }

    function displaySceneDialogues(scene) {
        // 先展示 host-message
        hostMessage = scene.screenContent;
        if (gameChat) {
            gameChat.startGameChat(scene); // 记录初始的 screenContent
        }

        // 延迟 1 秒后再开始展示 NPC 对话
        setTimeout(() => {
            if (scene.playerBehavior && scene.playerBehavior.dialogue) {
                const totalDialogues = scene.playerBehavior.dialogue.length;
                let displayedCount = 0;

                scene.playerBehavior.dialogue.forEach((dialog, index) => {
                    setTimeout(() => {
                        messages = [...messages, {
                            type: 'npc',
                            character: dialog.character,
                            text: dialog.content
                        }];
                        
                        if (gameChat) {
                            gameChat.receiveGameResponse(dialog.content, 'npc'); // 记录 NPC 对话
                        }
                        
                        displayedCount++;
                        
                        if (displayedCount === totalDialogues && scene.playerBehavior.actions) {
                            setTimeout(() => {
                                hostMessage = scene.playerBehavior.actions;
                                if (gameChat) {
                                    gameChat.receiveGameResponse(scene.playerBehavior.actions, 'host'); // 记录 actions
                                }
                                playerChoices = scene.playerChoice || [];
                                showInputSection = true;
                            }, 1000);
                        }
                    }, index * 1000);
                });
            }
        }, 1000);
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
        <GameChat bind:this={gameChat} hidden />
    {/if}
    {#if showInputSection}
        <InputSection
            choices={playerChoices}
            onSendMessage={handleSendMessage}
            onOptionClick={handleOptionClick}
        />
    {/if}
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
