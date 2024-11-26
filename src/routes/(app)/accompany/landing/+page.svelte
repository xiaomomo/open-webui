<style>
    .body {
      font-family: 'Comic Sans MS', cursive, sans-serif;
      background: linear-gradient(to bottom, #000, #1a1a1a);
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      overflow: hidden;
      position: relative;
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

    /* Container */
    .container {
      text-align: center;
      max-width: 400px;
      padding: 20px;
      background: rgba(255, 255, 255, 0.8);
      border-radius: 20px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
      position: relative;
      z-index: 10;
    }

    .cutscene {
      position: relative;
      padding: 20px;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      border-radius: 10px;
      margin-bottom: 20px;
    }

    .cutscene img {
      width: 100px;
      margin-bottom: 10px;
      animation: flyIn 3s forwards;
    }

    .cutscene h2 {
      font-size: 20px;
      margin-bottom: 10px;
    }

    .cutscene p {
      font-size: 14px;
      line-height: 1.5;
    }

    .mission {
      position: relative;
      padding: 20px;
      background: rgba(255, 255, 255, 0.8);
      border-radius: 10px;
      margin-bottom: 20px;
    }

    .mission h2 {
      font-size: 20px;
      color: #ff69b4;
      margin-bottom: 10px;
    }

    .mission p {
      font-size: 14px;
      line-height: 1.5;
    }

    .start-button {
      padding: 10px 20px;
      font-size: 16px;
      color: #fff;
      background-color: #ff69b4;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s;
    }

    .start-button:hover {
      background-color: #ff1493;
    }

    /* Memory Bubbles */
    .memory-bubbles {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 10;
      display: none;
    }

    .memory-bubble {
      position: absolute;
      background: radial-gradient(circle, #ff69b4, #ff1493);
      border-radius: 50%;
      box-shadow: 0 0 10px rgba(255, 105, 180, 0.5);
      animation: scatter 5s forwards;
    }

    @keyframes scatter {
      0% {
        transform: scale(0) translate(0, 0);
        opacity: 1;
      }
      100% {
        transform: scale(1) translate(calc(var(--x) * 100vw), calc(var(--y) * 100vh));
        opacity: 0;
      }
    }

    @keyframes flyIn {
      0% {
        transform: translate(-100%, -100%) scale(0);
        opacity: 0;
      }
      100% {
        transform: translate(0, 0) scale(1);
        opacity: 1;
      }
    }

    @keyframes crash {
      0% {
        transform: scale(1);
      }
      50% {
        transform: scale(1.2) rotate(20deg);
      }
      100% {
        transform: scale(1) rotate(0deg);
      }
    }

    .crash-animation {
      animation: crash 2s forwards;
    }

    .loading-message {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      background: rgba(255, 255, 255, 0.8);
      border-radius: 10px;
      padding: 20px;
      display: none;
    }

    .loading-message img {
      width: 100px;
      margin-bottom: 10px;
    }

    .loading-message h2 {
      font-size: 20px;
      color: #ff69b4;
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
  </style>

<div class="body">
    <!-- Starry Background -->
    <div class="stars"></div>
  
    <div class="container">
      <div class="cutscene">
        <img src="robot-pixel.png" alt="Pixel Robot Flying In" class="pixel-image" id="flying-robot">
        <h2>Pixel’s Crash Landing</h2>
        <p>Oh no! Pixel's spaceship crashed on a distant planet. His memory bubbles scattered everywhere. Without them, he can't remember how to get home.</p>
      </div>
  
      <div class="mission">
        <h2>Mission: Help Pixel Recover Knowledge Bubbles</h2>
        <p>To help Pixel, you need to solve challenges and collect memory bubbles. Each bubble contains important information that will guide you through the adventure.</p>
      </div>
  
      <button class="start-button" onclick="startAdventure()">Start Adventure</button>
    </div>
  
    <div class="memory-bubbles" id="memory-bubbles"></div>
    <div class="loading-message" id="loading-message">
      <img src="robot-pixel-loading.png" alt="Pixel Robot Loading" class="pixel-image">
      <h2>Loading...</h2>
    </div>
  
    
</div>

  <script type="ts">
    // Generate stars
    const starsContainer = document.querySelector('.stars');
    for (let i = 0; i < 100; i++) {
      const star = document.createElement('div');
      star.classList.add('star');
      star.style.top = `${Math.random() * 100}vh`;
      star.style.left = `${Math.random() * 100}vw`;
      star.style.width = `${Math.random() * 2 + 1}px`;
      star.style.height = `${Math.random() * 2 + 1}px`;
      star.style.animationDuration = `${Math.random() * 5 + 2}s`;
      starsContainer.appendChild(star);
    }

    // Generate memory bubbles
    const memoryBubbles = document.getElementById('memory-bubbles');
    for (let i = 0; i < 20; i++) {
      const bubble = document.createElement('div');
      bubble.classList.add('memory-bubble');
      bubble.style.width = `${Math.random() * 10 + 10}px`;
      bubble.style.height = `${Math.random() * 10 + 10}px`;
      bubble.style.setProperty('--x', Math.random() - 0.5);
      bubble.style.setProperty('--y', Math.random() - 0.5);
      memoryBubbles.appendChild(bubble);
    }

    // Animation sequence for the robot
    const flyingRobot = document.getElementById('flying-robot');

    flyingRobot.addEventListener('animationend', () => {
      flyingRobot.src = 'robot-pixel copy.png';
      flyingRobot.classList.add('crash-animation');
    });

    function startAdventure() {      
      window.location.href = "main.html";
    }

    // 创建流星函数
    function createShootingStar() {
      const shootingStar = document.createElement('div');
      shootingStar.classList.add('shooting-star');
      
      // 随机起始位置
      shootingStar.style.left = `${Math.random() * 100}%`;
      shootingStar.style.top = `${Math.random() * 100}%`;
      
      document.body.appendChild(shootingStar);
      
      // 动画结束后移除流星元素
      shootingStar.addEventListener('animationend', () => {
        shootingStar.remove();
      });
      
      // 随机设置下一个流星的时
      const nextTime = Math.random() * 1000 + 2000;
      setTimeout(createShootingStar, nextTime);
    }

    // 开始生成流星
    createShootingStar();
  </script>