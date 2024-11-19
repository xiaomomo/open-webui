<script>
	import { onMount } from 'svelte';
	import { courses, currentPosition, completedLevels } from '$lib/stores/courseStore';
	import { fetchCourses } from '$lib/apis/englishlesson/courseApi';
	import Cloud from '$lib/components/game/Cloud.svelte';
	import Mushroom from '$lib/components/game/Mushroom.svelte';
	import LevelNode from '$lib/components/game/LevelNode.svelte';
	import LevelPath from '$lib/components/game/LevelPath.svelte';
	import { goto } from '$app/navigation';

	let gameContainer;
	let width;
	let height;

	function calculatePointOnCurve(t) {
		const amplitude = 0.2;
		const frequency = 3;
		
		const x = width * (
			0.5 + 
			amplitude * Math.sin(frequency * Math.PI * t) + 
			0.1 * Math.sin(2 * frequency * Math.PI * t)
		);
		
		const y = height * (0.02 + 0.95 * t);
		
		return { x, y };
	}

	function generateSafePosition() {
		let x, y, attempts = 0;
		do {
			x = Math.random() * width;
			y = Math.random() * height;
			attempts++;
		} while (isNearPath(x, y) && attempts < 50);
		return { x, y };
	}

	function isNearPath(x, y) {
		for(let t = 0; t <= 1; t += 0.01) {
			const pathPoint = calculatePointOnCurve(t);
			const distance = Math.sqrt(
				Math.pow(x - pathPoint.x, 2) + 
				Math.pow(y - pathPoint.y, 2)
			);
			if (distance < 50) {
				return true;
			}
		}
		return false;
	}

	let positions = [];
	let pathData = '';
	let clouds = [];
	let mushrooms = [];

	onMount(async () => {
		const coursesData = await fetchCourses();
		courses.set(coursesData);
		
		width = window.innerWidth;
		height = gameContainer.offsetHeight;

		positions = $courses.map((_, index) => {
			const t = index / ($courses.length - 1);
			return calculatePointOnCurve(t);
		});

		pathData = `M ${positions[0].x} ${positions[0].y}`;
		for(let i = 1; i < positions.length; i++) {
			const prevPos = positions[i-1];
			const currentPos = positions[i];
			const cpX = (prevPos.x + currentPos.x) / 2;
			pathData += ` Q ${cpX} ${prevPos.y}, ${currentPos.x} ${currentPos.y}`;
		}

		clouds = Array(10).fill().map(() => generateSafePosition());
		mushrooms = Array(20).fill().map(() => generateSafePosition());
	});

	function handleNodeSelect(index) {
		currentPosition.set(index);
		completedLevels.update(set => {
			set.add(index);
			return set;
		});

		const lessonUnitId = $courses[index].id;
		goto(`/englishgame?lessonUnitId=${lessonUnitId}`);
	}
</script>

<div id="gameContainer" bind:this={gameContainer}>
	<div id="levelPath">
		{#each clouds as pos}
			<Cloud x={pos.x} y={pos.y} />
		{/each}

		{#each mushrooms as pos}
			<Mushroom x={pos.x} y={pos.y} />
		{/each}

		<LevelPath {pathData} />

		{#each $courses as course, index}
			{#if positions[index]}
				<LevelNode
					x={positions[index].x}
					y={positions[index].y}
					{index}
					{course}
					onClick={() => handleNodeSelect(index)}
				/>
			{/if}
		{/each}
	</div>
</div>

<style>
	#gameContainer {
		width: 100vw;
		height: 300vh;
		background: linear-gradient(45deg, #ff9eb5, #ffc0cb);
		position: relative;
		overflow-x: hidden;
		overflow-y: auto;
	}
</style>