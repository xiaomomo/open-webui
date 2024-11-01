<script>
	import { currentPosition, completedLevels } from '../../stores/courseStore';
	import { spring } from 'svelte/motion';

	export let course;
	export let index;
	export let onSelect;

	let isHovered = false;
	let element;

	const scale = spring(1, {
		stiffness: 0.1,
		damping: 0.15
	});

	$: isActive = $currentPosition === index + 1;
	$: isCompleted = $completedLevels.has(index + 1);
	$: isSelectable = index + 1 <= $currentPosition + 1;

	function handleMouseenter() {
		if (isSelectable) {
			isHovered = true;
			scale.set(1.05);
		}
	}

	function handleMouseleave() {
		isHovered = false;
		scale.set(1);
	}

	// Generate cute decorative elements programmatically
	const generateStars = () => {
		const stars = [];
		for (let i = 0; i < 5; i++) {
			stars.push({
				top: Math.random() * 100 + '%',
				left: Math.random() * 100 + '%',
				animationDelay: Math.random() * 2 + 's'
			});
		}
		return stars;
	};

	const stars = generateStars();

	const goChat = () => {
		//todo 传入内容啊,怎么交互到chat里？
		// create a chat and start it
		console.log("go chat!")
	};

</script>

<div
	bind:this={element}
	class="course-node"
	class:active={isActive}
	class:completed={isCompleted}
	class:selectable={isSelectable}
	class:hover={isHovered}
	style="
        left: {250 + (index * 300)}px;
        transform: scale({$scale});
    "
	on:click={ goChat}
	on:mouseenter={handleMouseenter}
	on:mouseleave={handleMouseleave}
>
	<!-- Decorative elements -->
	{#each stars as star}
		<div
			class="star"
			style="top: {star.top}; left: {star.left}; animation-delay: {star.animationDelay}"
		></div>
	{/each}

	<!-- Course content -->
	<div class="content-wrapper">
		<div class="level-badge">
			<div class="badge-inner">
				Level {index + 1}
				{#if isCompleted}
					<div class="checkmark">✓</div>
				{/if}
			</div>
		</div>

		<div class="emoji-container">
			<div class="emoji-icon" class:bounce={isHovered}>
				<img src="/assets/images/emojis/emoji_{course.emoji}.png" />
			</div>
			{#if isActive}
				<div class="current-indicator">
					<div class="arrow">↓</div>
					<div class="pulse"></div>
				</div>
			{/if}
		</div>

		<h2 class="course-title">{course.unit}</h2>
		<p class="course-description">{course.description || "descriptiondescriptiondescription"}</p>

		<!--{#if isSelectable && !isCompleted}-->
		<!--	<div class="start-button" class:bounce={isHovered}>-->
		<!--		Start Learning!-->
		<!--	</div>-->
		<!--{/if}-->
	</div>

	<!-- Decorative cloud background -->
	<div class="cloud-bg"></div>
</div>

<style>
    .course-node {
        position: absolute;
        width: 240px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 25px;
        box-shadow:
                0 8px 32px rgba(0,0,0,0.1),
                0 4px 8px rgba(0,0,0,0.05);
        cursor: pointer;
        transition: all 0.3s;
        border: 4px solid #FF69B4;
        overflow: hidden;
    }

    .content-wrapper {
        position: relative;
        z-index: 2;
    }

    .cloud-bg {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background:
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.8) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255,255,255,0.8) 0%, transparent 50%);
        z-index: 1;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .hover .cloud-bg {
        opacity: 1;
    }

    .level-badge {
        position: absolute;
        top: -15px;
        right: -15px;
        background: #FF69B4;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform-origin: center;
    }

    .badge-inner {
        text-align: center;
        font-size: 0.9em;
    }

    .checkmark {
        font-size: 1.2em;
        color: #90EE90;
        text-shadow: 0 0 8px white;
        animation: pop 0.3s ease-out;
    }

    .emoji-container {
        position: relative;
        height: 80px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
    }

    .emoji-icon {
        font-size: 3em;
        transition: transform 0.3s;
    }

    .bounce {
        animation: bounce 0.6s ease infinite;
    }

    .current-indicator {
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
    }

    .arrow {
        font-size: 1.5em;
        color: #FF69B4;
        animation: bounceArrow 0.6s ease infinite;
    }

    .pulse {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 40px;
        height: 40px;
        background: rgba(255,105,180,0.2);
        border-radius: 50%;
        animation: pulse 2s ease-out infinite;
    }

    .star {
        position: absolute;
        width: 15px;
        height: 15px;
        background:
                radial-gradient(circle at 50% 50%, #FFD700, transparent 60%),
                radial-gradient(circle at 50% 50%, rgba(255,215,0,0.5), transparent 70%);
        border-radius: 50%;
        animation: twinkle 3s ease-in-out infinite;
    }

    .start-button {
        background: #FF69B4;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        text-align: center;
        margin-top: 15px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .start-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    .course-title {
        font-size: 1.4em;
        margin: 10px 0;
        color: #FF1493;
        text-align: center;
    }

    .course-description {
        font-size: 0.9em;
        color: #666;
        text-align: center;
        margin-bottom: 10px;
    }

    .active {
        background: #FFF0F5;
        border-color: #FF1493;
        box-shadow:
                0 12px 40px rgba(255,105,180,0.2),
                0 8px 16px rgba(255,105,180,0.15);
    }

    .completed {
        border-color: #90EE90;
    }

    .selectable:hover {
        box-shadow:
                0 16px 48px rgba(0,0,0,0.15),
                0 12px 24px rgba(0,0,0,0.1);
    }

    :not(.selectable) {
        filter: grayscale(0.7);
        opacity: 0.7;
        cursor: not-allowed;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    @keyframes bounceArrow {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    @keyframes pulse {
        0% {
            transform: translate(-50%, -50%) scale(0.5);
            opacity: 0.8;
        }
        100% {
            transform: translate(-50%, -50%) scale(2);
            opacity: 0;
        }
    }

    @keyframes twinkle {
        0%, 100% { opacity: 0.2; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.2); }
    }

    @keyframes pop {
        0% { transform: scale(0); }
        70% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
</style>