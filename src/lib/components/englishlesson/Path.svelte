<script>
	export let courses;

	$: pathD = generatePath(courses);

	function generatePath(courses) {
		let d = "M100,80 ";
		courses.forEach((_, index) => {
			const y = 80 + Math.sin(index * 0.5) * 150;
			d += `${index === 0 ? 'M' : 'L'} ${250 + (index * 300)},${y} `;
		});
		return d;
	}
</script>

<svg class="path">
	<path class="path-line" d={pathD}/>
</svg>

<style>
    .path {
        position: absolute;
        top: 100px;
        left: 50px;
        width: calc(100% - 100px);
        height: 80%;
        pointer-events: none;
    }

    .path-line {
        stroke: #FF69B4;
        stroke-width: 12;
        stroke-linecap: round;
        stroke-dasharray: 15;
        fill: none;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        animation: drawPath 2s forwards;
    }

    @keyframes drawPath {
        from { stroke-dashoffset: 1000; }
        to { stroke-dashoffset: 0; }
    }
</style>