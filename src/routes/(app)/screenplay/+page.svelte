<script lang="ts">
    import { onMount, tick } from 'svelte';
    import Stars from './components/Stars.svelte';
    import HostSection from './components/HostSection.svelte';
    import GameArea from './components/GameArea.svelte';
    import InputSection from './components/InputSection.svelte';
    import GameChat from '../englishgame/components/GameChat.svelte';
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

    onMount(async () => {
        // 先初始化 GameChat
        if (!gameChat) {
            await tick();
            gameChat = new GameChat({
                target: document.createElement('div'),
                props: {}
            });
        }
        
        // 然获取剧本数据
        await fetchScreenplay();
    });

    async function fetchScreenplay() {
        isLoading = true;
        try {
            const response = await fetch(`${WEBUI_API_BASE_URL}/screenplay/getScreenPlay`);
            const data = await response.json();
            screenplay = JSON.parse(data);
            
            // 使用 startGameChat 来初始化游戏对话
            if (gameChat) {
                await gameChat.startGameChat(screenplay);
            }
            
            title = screenplay.title;
            characters = screenplay.characters;
            mainPlayer = screenplay.characters.find(char => char.isMainPlayer === "true")?.name || "侦探";
            
            const firstScene = screenplay.scenes.find(scene => scene.sceneNumber === 1);
            if (firstScene) {
                hostMessage = firstScene.screenContent;
                playerChoices = firstScene.playerChoice || [];
                processScene(firstScene);
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
        playerChoices = [];
        showInputSection = false;

        // 获取所有对话历史
        const chatHistory = gameChat ? gameChat.getCurrentMessages() : [];
        
        try {
            const prompt = `
            you are a screenplay host, you need to answer the player's question and guide the player to the next scene.
            the following is the chat history:
            ${JSON.stringify(chatHistory)}
            It's important to note that your answer should only be in json format like this:
                {
                            "playerChoiceEvaluate":"give evaluate of playerChoice", //exist if has user choice
                            "sceneNumber": "5",
                            "screenContent": "",
                            "charactersBehavior":[
                                {
                                "charactersName":"",
                                "behaviorType":"thinking/speaking/motion",
                                "behaviorContent":""
                                }
                            ]
                            "whatNextPlayerShouldDo":""
                            "questionBehaviorShouldAction": {
                                "question":"",
                                "answerType":"choose/input"
                                "playerChoice": [
                                {
                                    "option": "",
                                    "chinese": ""
                                }
                            ]
                            }

                }
            `;

            // 发送请求获取下一个场景
            const response = await fetch(`${WEBUI_API_BASE_URL}/qwenproxy/get_ai_response?prompt=${prompt}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const responseData = await response.text(); // 先获取原始文本
            // 先尝试解析一次，然后再解析内部的 JSON 字符串
            const parsedOnce = JSON.parse(responseData.replace(/\\n/g, ''));
            const nextSceneData = typeof parsedOnce === 'string' ? JSON.parse(parsedOnce) : parsedOnce;
            console.log(nextSceneData); // 用于调试

            if (gameChat) {
                await gameChat.submitGameMessage(JSON.stringify(nextSceneData));
            }

            currentSceneIndex = parseInt(nextSceneData.sceneNumber) - 1;
            processScene(nextSceneData);

        } catch (error) {
            console.error('Error fetching next scene:', error);
            hostMessage = '抱歉，发生了一些错误...';
        }
    }

    function handleSendMessage(text) {
        messages = [...messages, { type: 'player', text }];
        hostMessage = '让我们继续调查...';
    }

    // 首先定义 sleep 函数
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // 重构后的异步处理函数
    async function processScene(scene) {
        // 如果有 playerChoiceEvaluate，先展示它
        if (scene.playerChoiceEvaluate) {
            hostMessage = scene.playerChoiceEvaluate;
            await sleep(1000); // 等待一秒
        }
        // 然后展示 screenContent
        hostMessage = scene.screenContent;
        // 延迟 1 秒
        await sleep(1000);

        // 处理 NPC 对话
        if (scene.charactersBehavior) {
            for (const dialog of scene.playerBehavior) {
                //todo 这里有问题啊
                messages = [...messages, {
                    type: 'npc',
                    character: dialog.charactersName,
                    text: dialog.behaviorContent
                }];
                await sleep(1000);
            }

            // 如果有动作，等待 1 秒后显示
            if (scene.whatNextMainPlayerShouldDo) {
                await sleep(1000);
                hostMessage = scene.whatNextMainPlayerShouldDo.question;
                playerChoices = scene.whatNextMainPlayerShouldDo.playerChoice || [];
                showInputSection = true;
            }
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
        <GameChat bind:this={gameChat} />
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
