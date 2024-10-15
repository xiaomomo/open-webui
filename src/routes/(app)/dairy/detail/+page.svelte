<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { getDiaryById } from '$lib/apis/diary';
  import { get } from 'svelte/store';

  // 创建一个变量来存储获取到的日记数据
  let diaryEntry = null;
  let error = null;

  // 获取 URL 中的 diaryId 参数
  const urlParams = get(page).url.searchParams;
  let diaryId = urlParams.get('diaryId');

  // 在组件挂载时调用 API 获取日记内容
  onMount(async () => {
    try {
      const token = 'YOUR_TOKEN_HERE'; // 替换为实际的 token
      if (diaryId) {
        diaryEntry = await getDiaryById(token, diaryId);
      } else {
        error = 'Diary ID is missing from the URL';
      }
    } catch (err) {
      error = err;
    }
  });
</script>

<!-- 显示错误信息 -->
{#if error}
  <p class="error">Failed to load diary: {error}</p>
{/if}

<!-- 显示加载中的状态 -->
{#if !diaryEntry && !error}
  <p>Loading...</p>
{/if}

<!-- 如果数据成功获取，渲染日记条目 -->
{#if diaryEntry}
  <main>
    <header class="header">
      <div class="date-container">
        <span id="date-display">{new Date(diaryEntry.timestamp * 1000).toLocaleDateString()}</span>
      </div>
    </header>

    <section class="diary-section">
      <h1 class="diary-title">Today's Adventure</h1>
      <div class="diary-content">
        <p>{diaryEntry.content}</p>
        <img src="/static/daily-report/sticker1.png" class="sticker rotated sticker-1" alt="Sticker 1">
        <img src="/static/daily-report/sticker2.png" class="sticker rotated sticker-2" alt="Sticker 2">
        <img src="/static/daily-report/sticker3.png" class="sticker rotated sticker-3" alt="Sticker 3">
      </div>
    </section>
  </main>
{/if}

<footer>
  <nav class="nav-bar">
    <button class="nav-btn">New Entry</button>
    <button class="nav-btn">Past Entries</button>
  </nav>
</footer>

<style>
  body {
    font-family: 'Comic Neue', sans-serif;
    background-color: #ffe4e1;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100vh;
  }

  .header {
    background-color: #ffccd5;
    padding: 10px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .date-container {
    font-size: 24px;
    color: #ff6f91;
    font-weight: bold;
  }

  .diary-section {
    margin: 20px;
    padding: 20px;
    background-color: #fff;
    border-radius: 20px;
    border: 2px solid #ff6f91;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    position: relative;
  }

  .diary-title {
    font-family: 'Patrick Hand', sans-serif;
    font-size: 28px;
    color: #ff6f91;
    margin-bottom: 20px;
    font-weight: bold;
  }

  .diary-content {
    font-family: 'Patrick Hand', sans-serif;
    font-size: 20px;
    color: #333;
    line-height: 1.8;
    text-align: left;
    padding: 10px;
    position: relative;
  }

  .diary-content p {
    margin-bottom: 15px;
    background-color: #fff0f5;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: relative;
  }

  .sticker {
    width: 80px;
    position: absolute;
    z-index: 2;
    opacity: 0.5;
  }

  .rotated {
    transform: rotate(var(--rotation-angle));
    transition: transform 0.3s ease-in-out;
  }

  .sticker-1 {
    top: 50px;
    left: 40px;
    --rotation-angle: -15deg;
  }

  .sticker-2 {
    top: 200px;
    right: 50px;
    --rotation-angle: 10deg;
  }

  .sticker-3 {
    top: 350px;
    left: 60px;
    --rotation-angle: -8deg;
  }

  .nav-bar {
    background-color: #ffccd5;
    padding: 10px;
    display: flex;
    justify-content: space-around;
  }

  .nav-btn {
    background-color: #ff6f91;
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .nav-btn:hover {
    background-color: #ff4f71;
  }
</style>