<script lang="ts">
    import { onMount, tick, onDestroy } from 'svelte';
    import Stars from './components/Stars.svelte';
    import HostSection from './components/HostSection.svelte';
    import GameArea from './components/GameArea.svelte';
    import InputSection from './components/InputSection.svelte';
    import GameChat from '../englishgame/components/GameChat.svelte';
    import { WEBUI_API_BASE_URL } from '$lib/constants';
    import { synthesizeSoVITSSpeech } from '$lib/apis/audio';
    import { config, settings } from '$lib/stores';

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
    let showStartButton = false;
    let isSceneReady = false;
    let playerChoices = [];
    let gameChat: GameChat;
    let audioCache = new Map();
    let aiResponseCache = new Map();

    // 添加 window 类型声明
    declare global {
        interface Window {
            startScene: () => void;
        }
    }

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
                await gameChat.submitGameMessage(screenplay);
            }
            
            title = screenplay.title;
            characters = screenplay.characters;
            mainPlayer = screenplay.characters.find(char => 
                char.isMainPlayer === "true" || char.isMainPlayer === true
            )?.name || "侦探";
            
            const firstScene = screenplay.scenes[0];
            if (firstScene) {
                hostMessage = firstScene.screenContent;
                playerChoices = firstScene.playerChoice || [];
                processScene(firstScene);
            }

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

    async function handleCharacterClick(character) {
        activeCharacter = character;
        const response = getNextResponse(character, currentSceneIndex + 1);
        messages = [...messages, { type: 'npc', character, text: response }];
        hostMessage = `${character}说话了！让我们���听看...`;
        await playTextToSpeech(character, response);
    }

    async function handleOptionClick(choice) {
        // 记录玩家选择
        if (gameChat) {
            await gameChat.submitGameMessage(`screenIndexOption${currentSceneIndex}:${choice.option}: ${choice.content}`);
        }

        hostMessage = "正在处理...";
        playerChoices = [];
        showInputSection = false;

        try {
            // 尝试从缓存获取响应
            const cacheKey = `${choice.option}:${choice.content}`;
            let nextSceneData = aiResponseCache.get(cacheKey);

            // 如果缓存中没有，实时获取
            if (!nextSceneData) {
                hostMessage = "机器人在思考...";
                nextSceneData = await preloadAIResponse(choice);
            }

            if (nextSceneData) {
                if (gameChat) {
                    await gameChat.submitGameMessage(JSON.stringify(nextSceneData));
                }

                currentSceneIndex = parseInt(nextSceneData.sceneNumber) - 1;
                processScene(nextSceneData);
            }

        } catch (error) {
            console.error('Error handling option click:', error);
            hostMessage = '抱歉，发生了一些错误...';
        }
    }

    function handleSendMessage(text) {
        messages = [...messages, { type: 'player', text }];
        hostMessage = '让我们继续调查...';
    }

    // 首先定义 sleep 函数
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // 修改预加载函数
    async function preloadAudio(role: string, text: string): Promise<string> {
        const cacheKey = `${role}:${text}`;
        
        try {
            // 检查缓存
            const cachedUrl = audioCache.get(cacheKey);
            if (cachedUrl) {
                return cachedUrl;
            }

            const defaultVoice = $settings?.audio?.tts?.defaultVoice;
            const configVoice = $config?.audio?.tts?.voice;
            const selectedVoice = defaultVoice === configVoice
                ? ($settings?.audio?.tts?.voice ?? configVoice)
                : configVoice;

            if (selectedVoice) {
                // 根据角色选择不同的语音配置
                const voicePrompt = role === 'host' ? 'BLIPPI' : 'LITTLE_PONY';
                
                const audio = await synthesizeSoVITSSpeech(
                    localStorage.token,
                    selectedVoice,
                    text,
                    undefined,
                    'zh',
                    voicePrompt
                );

                if (audio) {
                    const blob = await audio.blob();
                    const blobUrl = URL.createObjectURL(blob);
                    audioCache.set(cacheKey, blobUrl);
                    return blobUrl;
                }
            }
        } catch (error) {
            console.error('Audio preload error:', error);
        }
        return null;
    }

    // 修改播放函数
    async function playTextToSpeech(role: string, text: string) {
        try {
            const cacheKey = `${role}:${text}`;
            let blobUrl = audioCache.get(cacheKey);
            
            if (!blobUrl) {
                // 如果缓存中没有，实时获取
                blobUrl = await preloadAudio(role, text);
            }

            if (blobUrl) {
                const audioElement = new Audio(blobUrl);
                await new Promise((resolve) => {
                    audioElement.addEventListener('ended', () => {
                        resolve(true);
                    });
                    audioElement.play();
                });
            }
        } catch (error) {
            console.error('TTS Error:', error);
        }
    }

    // 修改场景预加载函数
    async function preloadSceneAudio(scene) {
        const audioPromises = [];

        // 收集所有需要预加载的文本
        if (scene.playerChoiceEvaluate) {
            audioPromises.push(preloadAudio('host', scene.playerChoiceEvaluate));
        }
        
        audioPromises.push(preloadAudio('host', scene.screenContent));

        if (scene.charactersBehavior) {
            scene.charactersBehavior.forEach(dialog => {
                audioPromises.push(preloadAudio(
                    dialog.charactersName,
                    dialog.behaviorContent
                ));
            });

            if (scene.whatNextMainPlayerShouldDo) {
                audioPromises.push(preloadAudio(
                    'host',
                    scene.whatNextMainPlayerShouldDo.question
                ));
                
                const choices = scene.whatNextMainPlayerShouldDo.playerChoice || [];
                choices.forEach(choice => {
                    audioPromises.push(preloadAudio(
                        'host',
                        `选项 ${choice.option}： ${choice.content}`
                    ));
                });
            }
        }

        // 并行预加载所有音频
        await Promise.all(audioPromises);
    }

    // 添加预加载AI响应的函数
    async function preloadAIResponse(choice) {
        const messages: Record<string | number, string> = gameChat.getCurrentMessages();
            
        messages["screenIndexOption" + currentSceneIndex + ":" + choice.option] = choice.content;
        const prompt = `
            you are a screenplay host, you need to answer the player's question and guide the player to the next scene.
            the following is the chat history:
            ${JSON.stringify(messages)}
            It's important to note that your answer should only be in json format like this:
                {
                            "playerChoiceEvaluate":"give evaluate of playerChoice",
                            "sceneNumber": "5",
                            "screenContent": "",
                            "charactersBehavior":[
                                {
                                "charactersName":"",
                                "behaviorType":"thinking/speaking/motion",
                                "behaviorContent":""
                                }
                            ]
                            "whatNextMainPlayerShouldDo": {
                                "question":"",
                                "answerType":"choose/input"
                                "playerChoice": [
                                {
                                    "option": "",
                                    "content": ""
                                }
                            ]
                            }

                }
            `;

        try {
            const response = await fetch(`${WEBUI_API_BASE_URL}/qwenproxy/get_ai_response?prompt=${encodeURIComponent(prompt)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const responseData = await response.text();
            const parsedOnce = JSON.parse(responseData.replace(/\\n/g, ''));
            const nextSceneData = typeof parsedOnce === 'string' ? JSON.parse(parsedOnce) : parsedOnce;
            
            // 缓存响应
            const cacheKey = `${choice.option}:${choice.content}`;
            aiResponseCache.set(cacheKey, nextSceneData);
            
            // 预加载这个场景的音频
            await preloadSceneAudio(nextSceneData);
            
            return nextSceneData;
        } catch (error) {
            console.error('Error preloading AI response:', error);
            return null;
        }
    }

    // 修改 processScene 函数，添加选项预加载
    async function processScene(scene) {
        // 只在第一个场景显示开始按钮
        showStartButton = currentSceneIndex === 0;
        isSceneReady = false;

        // 在这里定义 startScene 函数
        window.startScene = () => {}; // 初始化为空函数

        // AI 响应预加载
        if (scene.whatNextMainPlayerShouldDo) {
            playerChoices = scene.whatNextMainPlayerShouldDo.playerChoice || [];
            const preloadPromises = playerChoices.map(choice => preloadAIResponse(choice));
            Promise.all(preloadPromises).catch(error => {
                console.error('Error preloading choices:', error);
            });
        }
        isSceneReady = true;

        // 等待用户点击开始按钮
        if (currentSceneIndex === 0) {
            await new Promise<void>(resolve => {
                window.startScene = () => {
                    showStartButton = false;
                    resolve();
                };
            });
        }

        // 预加载音频
        await preloadSceneAudio(scene);

        // 继续原有的场景处理逻辑
        if (scene.playerChoiceEvaluate) {
            hostMessage = scene.playerChoiceEvaluate;
            await playTextToSpeech('host', scene.playerChoiceEvaluate);
        }
        
        hostMessage = scene.screenContent;
        await playTextToSpeech('host', scene.screenContent);

        if (scene.charactersBehavior) {
            messages = [];
            for (const dialog of scene.charactersBehavior) {
                messages = [...messages, {
                    type: 'npc',
                    character: dialog.charactersName,
                    text: dialog.behaviorContent
                }];
                await playTextToSpeech(dialog.charactersName, dialog.behaviorContent);
            }
            messages = [];

            if (scene.whatNextMainPlayerShouldDo) {
                hostMessage = scene.whatNextMainPlayerShouldDo.question;
                await playTextToSpeech('host', scene.whatNextMainPlayerShouldDo.question);
                playerChoices = scene.whatNextMainPlayerShouldDo.playerChoice || [];
                showInputSection = true;

                for (const choice of playerChoices) {
                    const choiceText = `选项 ${choice.option}： ${choice.content}`;
                    await playTextToSpeech('host', choiceText);
                }

            }
        }
    }

    // 在组件卸载时清理缓存
    onDestroy(() => {
        audioCache.forEach(blobUrl => {
            URL.revokeObjectURL(blobUrl);
        });
        audioCache.clear();
        aiResponseCache.clear();
    });
</script>

<div class="body">
    <Stars />
    <HostSection 
        message={hostMessage}
        {title}
    />
    {#if showStartButton && currentSceneIndex === 0}
        <div class="start-button-container">
            <button 
                class="start-button" 
                on:click={() => window.startScene()} 
                disabled={!isSceneReady}
            >
                {isSceneReady ? '开始游戏' : '加载中...'}
            </button>
        </div>
    {/if}
    {#if !isLoading && characters.length > 0}
        <GameArea
            {messages}
            {activeCharacter}
            {characters}
            {mainPlayer}
            onCharacterClick={handleCharacterClick}
        />
        
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

    .start-button-container {
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
    }

    .start-button {
        background: linear-gradient(145deg, #ff69b4, #87ceeb);
        border: 3px solid #fff;
        border-radius: 15px;
        padding: 12px 24px;
        font-size: 1.2em;
        color: #fff;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }

    .start-button:hover:not(:disabled) {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    .start-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }
</style>
