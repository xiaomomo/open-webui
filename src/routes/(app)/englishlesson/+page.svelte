<script>
	import { onMount } from 'svelte';
	import { courses, currentPosition, completedLevels } from '$lib/stores/courseStore';
	import { fetchCourses } from '$lib/apis/englishlesson/courseApi';
	import Background from '$lib/components/englishlesson/Background.svelte';
	import CourseNode from '$lib/components/englishlesson/CourseNode.svelte';
	import Path from '$lib/components/englishlesson/Path.svelte';
	import Pony from '$lib/components/englishlesson/Pony.svelte';

	let ponyPosition = { x: 0, y: 0 };
	let mapContainer;

	onMount(async () => {
		const coursesData = await fetchCourses();
		courses.set(coursesData);
		updatePonyPosition($currentPosition);
	});

	function updatePonyPosition(nodeNumber) {
		const node = mapContainer.querySelector(`.course-node:nth-child(${nodeNumber})`);
		if (!node) return;

		const rect = node.getBoundingClientRect();
		const containerRect = mapContainer.getBoundingClientRect();

		ponyPosition = {
			x: rect.left - containerRect.left + rect.width/2 - 40,
			y: rect.top - containerRect.top + rect.height/2 - 40
		};

		node.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
	}

	function handleNodeSelect(nodeNumber) {
		if (nodeNumber <= $currentPosition + 1) {
			currentPosition.set(nodeNumber);
			completedLevels.update(set => {
				set.add(nodeNumber);
				return set;
			});
			updatePonyPosition(nodeNumber);
		}
	}
</script>

<Background />

<div class="map-wrapper">
	<div class="map-container" bind:this={mapContainer}>
		<Path courses={$courses} />
		<Pony position={ponyPosition} />

		{#each $courses as course, index}
			<CourseNode
				{course}
				{index}
				onSelect={handleNodeSelect}
			/>
		{/each}
	</div>
</div>

<style>
    /* ... styles from the original CSS ... */
</style>