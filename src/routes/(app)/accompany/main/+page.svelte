<script type="ts">
    // 定义页面数据
    const pageData = {
      dialog: {
        text: "你好呀，小朋友！我是可爱的AI精灵，让我们一起去探索知识的奇妙世界吧！选择下面一个你喜欢的主题，开始我们的冒险吧！ ✨"
      },
      cards: [
        {
          id: 'math',
          image: 'math-planet.png',
          imageAlt: '数学星球',
          title: '数学星球',
          description: '和数字小精灵一起玩趣味数学游戏！',
          url: 'math-planet.html'
        },
        {
          id: 'science',
          image: 'science-zone.png',
          imageAlt: 'Science Zone',
          title: 'Science Zone',
          description: 'Conduct experiments and learn about the natural world.',
          url: 'science-zone.html'
        },
        {
          id: 'literature',
          image: 'literature-world.png',
          imageAlt: 'Literature World',
          title: 'Literature World',
          description: 'Read stories and improve your reading skills.',
          url: 'literature-world.html'
        }
      ]
    };

    // 渲染函数
    function renderCards() {
      const cardsContainer = document.getElementById('cards');
      cardsContainer.innerHTML = pageData.cards.map(card => `
        <div class="card" onclick="goToSector('${card.url}')">
          <img src="${card.image}" alt="${card.imageAlt}">
          <h3>${card.title}</h3>
          <p>${card.description}</p>
        </div>
      `).join('');
    }

    function renderDialog() {
      const dialogElement = document.getElementById('dialog');
      dialogElement.textContent = pageData.dialog.text;
    }

    // 页面初始化
    document.addEventListener('DOMContentLoaded', () => {
      // 渲染页面元素
      renderDialog();
      renderCards();

      const cards = document.getElementById('cards');
      
      // 设置对话显示时间（毫秒）
      const dialogDuration = 3000;
      
      // 等待对话显示完成后展示卡片
      setTimeout(() => {
        console.log('show cards');
        cards.classList.add('show');
      }, dialogDuration);
    });

    // 导航函数
    function goToSector(url) {
      window.location.href = url;
    }

    function goToAchievements() {
      window.location.href = 'achievements.html';
    }

    // 生成星星
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
      
      // 随机设置下一个流星的时间
      const nextTime = Math.random() * 1000 + 2000;
      setTimeout(createShootingStar, nextTime);
    }

    // 开始生成流星
    createShootingStar();
  </script>

<div class="body">
    <!-- Starry Background -->
    <div class="stars"></div>
  
    <div class="container">
      <div class="header">
        <button onclick="goToAchievements()">成就区</button>
      </div>
  
      <div class="pixel-container">
        <img src="robot-pixel.png" alt="AI Pixel" class="pixel" id="pixel">
        <div class="dialog" id="dialog"></div>
      </div>
  
      <div class="display-area">
        <div class="cards" id="cards"></div>
      </div>
    </div>
  
    <script>
      // 定义页面数据
      const pageData = {
        dialog: {
          text: "你好呀，小朋友！我是可爱的AI精灵，让我们一起去探索知识的奇妙世界吧！选择下面一个你喜欢的主题，开始我们的冒险吧！ ✨"
        },
        cards: [
          {
            id: 'math',
            image: 'math-planet.png',
            imageAlt: '数学星球',
            title: '数学星球',
            description: '和数字小精灵一起玩趣味数学游戏！',
            url: 'math-planet.html'
          },
          {
            id: 'science',
            image: 'science-zone.png',
            imageAlt: 'Science Zone',
            title: 'Science Zone',
            description: 'Conduct experiments and learn about the natural world.',
            url: 'science-zone.html'
          },
          {
            id: 'literature',
            image: 'literature-world.png',
            imageAlt: 'Literature World',
            title: 'Literature World',
            description: 'Read stories and improve your reading skills.',
            url: 'literature-world.html'
          }
        ]
      };
  
      // 渲染函数
      function renderCards() {
        const cardsContainer = document.getElementById('cards');
        cardsContainer.innerHTML = pageData.cards.map(card => `
          <div class="card" onclick="goToSector('${card.url}')">
            <img src="${card.image}" alt="${card.imageAlt}">
            <h3>${card.title}</h3>
            <p>${card.description}</p>
          </div>
        `).join('');
      }
  
      function renderDialog() {
        const dialogElement = document.getElementById('dialog');
        dialogElement.textContent = pageData.dialog.text;
      }
  
      // 页面初始化
      document.addEventListener('DOMContentLoaded', () => {
        // 渲染页面元素
        renderDialog();
        renderCards();
  
        const cards = document.getElementById('cards');
        
        // 设置对话显示时间（毫秒）
        const dialogDuration = 3000;
        
        // 等待对话显示完成后展示卡片
        setTimeout(() => {
          console.log('show cards');
          cards.classList.add('show');
        }, dialogDuration);
      });
  
      // 导航函数
      function goToSector(url) {
        window.location.href = url;
      }
  
      function goToAchievements() {
        window.location.href = 'achievements.html';
      }
  
      // 生成星星
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
        
        // 随机设置下一个流星的时间
        const nextTime = Math.random() * 1000 + 2000;
        setTimeout(createShootingStar, nextTime);
      }
  
      // 开始生成流星
      createShootingStar();
    </script>
  </body>

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
      width: 100px;
      height: 100px;
      transition: transform 0.3s ease;
    }

    .card:hover img {
      transform: rotate(10deg);
    }

    .card h3 {
      font-size: 20px;
      color: #fff;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    .card p {
      font-size: 16px;
      color: #fff;
    }
  </style>