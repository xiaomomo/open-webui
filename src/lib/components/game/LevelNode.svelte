<script>
    export let x;
    export let y;
    export let index;
    export let isLocked;
    export let onClick;
    export let course;
</script>

<div
    class="level {isLocked ? 'locked' : ''}"
    style="left: {x - 60}px; top: {y - 60}px"
    on:click={onClick}
>
    <div class="level-content">
        <div class="unit-text">{course.unit}</div>
    </div>
</div>

<style>
    .level {
        width: 120px;
        height: 120px;
        position: absolute;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1;
    }

    .level-content {
        width: 100px;
        height: 100px;
        background: linear-gradient(145deg, #9d47e5, #8a2be2);
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4),
                   inset 0 2px 2px rgba(255, 255, 255, 0.4),
                   inset 0 -2px 2px rgba(0, 0, 0, 0.2);
    }

    .unit-text {
        color: white;
        font-weight: bold;
        font-size: 0.85em;
        text-align: center;
        word-break: break-word;
        line-height: 1.2;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        max-width: 90%;
    }

    .level:not(.locked):hover .level-content {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6),
                   inset 0 2px 2px rgba(255, 255, 255, 0.4),
                   inset 0 -2px 2px rgba(0, 0, 0, 0.2);
    }

    .level.locked .level-content {
        background: linear-gradient(145deg, #d4d4d4, #cccccc);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1),
                   inset 0 2px 2px rgba(255, 255, 255, 0.4),
                   inset 0 -2px 2px rgba(0, 0, 0, 0.1);
        cursor: not-allowed;
    }

    .level:not(.locked):active .level-content {
        transform: scale(0.95);
        transition: transform 0.1s ease;
    }
</style> 