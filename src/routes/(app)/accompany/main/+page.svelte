<script lang="ts">
    import { onMount, tick } from 'svelte';
    import GameChat from '../../englishgame/components/GameChat.svelte';
    import { WEBUI_API_BASE_URL } from '$lib/constants';
    import { synthesizeSoVITSSpeech } from '$lib/apis/audio';
    import { config, settings } from '$lib/stores';

    let gameChat: GameChat;
    let showCards = false;

    // Add pageData object
    let pageData = {
        dialog: {
            text: "Welcome! I'm your AI companion..."  // Default welcome message
        },
        cards: [
            {
                image: "/robot-pixel.png",
                imageAlt: "Chat",
                description: "Let's chat!",
                url: "/chat"
            },
            {
                image: "/game-pixel.png",
                imageAlt: "Game",
                description: "Play a game",
                url: "/game"
            }
            // Add more cards as needed
        ]
    };

    onMount(async () => {
        // Initialize GameChat
        if (!gameChat) {
            await tick();
            gameChat = new GameChat({
                target: document.createElement('div'),
                props: {}
            });
        }

        // Start initial chat
        await startInitialChat();

        // Show cards after delay
        setTimeout(() => {
            showCards = true;
        }, 3000);

        // Generate stars array instead of DOM manipulation
        stars = Array.from({ length: 100 }, () => ({
            top: `${Math.random() * 100}vh`,
            left: `${Math.random() * 100}vw`,
            width: `${Math.random() * 2 + 1}px`,
            height: `${Math.random() * 2 + 1}px`,
            duration: `${Math.random() * 5 + 2}s`
        }));

        // Start shooting stars
        createShootingStar();
    });

    async function startInitialChat() {
        if (gameChat) {
            const initialMessage = await gameChat.submitGameMessage("Start new accompany session");
            
            try {
                const prompt = `
                you are an AI companion, you need to respond to the player with a warm welcome message.
                It's important to note that your answer should only be in json format like this:
                    {
                        "screenContent": "",
                        "charactersBehavior":[
                            {
                            "charactersName":"AI",
                            "behaviorType":"speaking",
                            "behaviorContent":""
                            }
                        ]
                    }
                `;

                const response = await fetch(`${WEBUI_API_BASE_URL}/qwenproxy/get_ai_response?prompt=${prompt}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                const responseData = await response.text();
                const parsedResponse = JSON.parse(responseData.replace(/\\n/g, ''));
                const aiResponse = typeof parsedResponse === 'string' ? JSON.parse(parsedResponse) : parsedResponse;

                if (gameChat) {
                    await gameChat.submitGameMessage(JSON.stringify(aiResponse));
                }

                // Update dialog text with AI response
                if (aiResponse.charactersBehavior?.[0]?.behaviorContent) {
                    pageData.dialog.text = aiResponse.charactersBehavior[0].behaviorContent;
                    await playTextToSpeech(pageData.dialog.text);
                }

            } catch (error) {
                console.error('Error getting AI response:', error);
                // Set fallback message if there's an error
                pageData.dialog.text = "Hello! I'm here to help you.";
            }
        }
    }

    async function playTextToSpeech(text: string) {
        try {
            const defaultVoice = $settings?.audio?.tts?.defaultVoice;
            const configVoice = $config?.audio?.tts?.voice;
            const selectedVoice = defaultVoice === configVoice
                ? ($settings?.audio?.tts?.voice ?? configVoice)
                : configVoice;

            if (selectedVoice) {
                const audio = await synthesizeSoVITSSpeech(
                    localStorage.token,
                    selectedVoice,
                    text
                );

                if (audio) {
                    const blob = await audio.blob();
                    const blobUrl = URL.createObjectURL(blob);
                    const audioElement = new Audio(blobUrl);
                    await audioElement.play();
                }
            }
        } catch (error) {
            console.error('TTS Error:', error);
        }
    }

    let stars = [];
    let shootingStars = [];

    function createShootingStar() {
        const star = {
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            id: Date.now()
        };
        
        shootingStars = [...shootingStars, star];
        
        // Remove star after animation
        setTimeout(() => {
            shootingStars = shootingStars.filter(s => s.id !== star.id);
        }, 3000);

        // Schedule next star
        setTimeout(createShootingStar, Math.random() * 1000 + 2000);
    }

    function goToSector(url) {
        window.location.href = url;
    }

    function goToAchievements() {
        window.location.href = 'achievements.html';
    }
</script>

<div class="body">
    <!-- Starry Background -->
    <div class="stars">
        {#each stars as star}
            <div class="star" 
                style="top: {star.top}; 
                       left: {star.left}; 
                       width: {star.width}; 
                       height: {star.height}; 
                       animation-duration: {star.duration};">
            </div>
        {/each}
        {#each shootingStars as star (star.id)}
            <div class="shooting-star" 
                style="left: {star.left}; 
                       top: {star.top};">
            </div>
        {/each}
    </div>

    <div class="container">
      <div class="header">
        <button onclick="goToAchievements()">成就区</button>
      </div>
  
      <div class="pixel-container">
        <img src="/robot-pixel.png" alt="AI Pixel" class="pixel" id="pixel">
        <div class="dialog" id="dialog">{pageData.dialog.text}</div>
      </div>
  
      <div class="display-area">
        <div class="cards" class:show={showCards}>
            {#each pageData.cards as card}
                <div class="card" on:click={() => goToSector(card.url)}>
                    <img src={card.image} alt={card.imageAlt}>
                    <p>{card.description}</p>
                </div>
            {/each}
        </div>
      </div>
    </div>
  </div>

<style>
    .body {
      font-family: 'Rounded Mplus 1c', 'Comic Sans MS', cursive, sans-serif;
      background: linear-gradient(to bottom, #000, #1a1a1a);
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      overflow: hidden;
      position: relative;
      color: #fff;
      width: 100%;
    }

    /* Starry Background */
    .stars {
      position: absolute;
      width: 100%;
      height: 100%;
      background: transparent;
      z-index: 1;
    }

    .star {
      position: absolute;
      background: white;
      border-radius: 50%;
      animation: twinkle 5s infinite;
    }

    @keyframes twinkle {
      0%, 100% {
        opacity: 1;
      }
      50% {
        opacity: 0.1;
      }
    }

    /* 添加流星样式 */
    .shooting-star {
      position: absolute;
      width: 100px;
      height: 2px;
      background: linear-gradient(90deg, white, transparent);
      transform: rotate(225deg);
      animation: shooting 3s linear;
      z-index: 2;
    }

    @keyframes shooting {
      0% {
        transform: translateX(-200px) translateY(-200px) rotate(225deg);
        opacity: 1;
      }
      100% {
        transform: translateX(2000px) translateY(2000px) rotate(225deg);
        opacity: 0;
      }
    }

    /* Container */
    .container {
      display: flex;
      width: 90%;
      max-width: 1200px;
      padding: 20px;
      background: rgba(255, 255, 255, 0.9);
      border-radius: 30px;
      border: 8px solid #ff69b4;
      box-shadow: 0 8px 32px rgba(255, 105, 180, 0.3);
      position: relative;
      z-index: 10;
      height: 70%; /* 自动适应内容高度 */
    }

    .header {
      position: absolute;
      top: 10px;
      right: 10px;
      display: flex;
      align-items: center;
    }

    .header button {
      background: #ff69b4;
      font-size: 18px;
      padding: 12px 24px;
      border-radius: 25px;
      border: 3px solid #fff;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .header button:hover {
      background: #ff1493;
      transform: scale(1.1);
      transition: all 0.3s ease;
    }

    .pixel-container {
      width: 40%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    .pixel {
      width: 200px;
      animation: bounce 2s infinite;
    }

    @keyframes bounce {
      0%, 100% {
        transform: translateY(0);
      }
      50% {
        transform: translateY(-20px);
      }
    }

    .dialog {
      max-width: 300px;
      background: #ff69b4;
      border: 5px solid #fff;
      border-radius: 20px;
      padding: 25px;
      font-size: 18px;
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
      color: #fff;
      line-height: 1.5;
    }

    .display-area {
      width: 60%;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .cards {
      display: flex;
      flex-direction: column;
      gap: 20px;
      height: 80%;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.8s ease;
      visibility: hidden;
    }

    .cards.show {
      opacity: 1;
      transform: translateY(0);
      visibility: visible;
    }

    .card {
      background: linear-gradient(145deg, #ff69b4, #87ceeb);
      border-radius: 20px;
      padding: 20px;
      width: 200px;
      height: 200px;
      transition: all 0.3s ease;
      border: 5px solid #fff;
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
      cursor: pointer;
    }

    .card:hover {
      transform: translateY(-10px) scale(1.05);
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    }

    .card img {
      width: 80px;
      height: 80px;
      transition: transform 0.3s ease;
    }

    .card:hover img {
      transform: rotate(10deg);
    }

    .card p {
      font-size: 16px;
      color: #fff;
    }
  </style>