<script lang="ts">
    interface LessonDetail {
        unit: string;
        emoji_start?: string;
        emoji_end?: string;
    }

    export let lessonDetail: LessonDetail | null = null;
</script>

<div id="title">
    <span>{lessonDetail?.emoji_start || '🦄'}</span>
    {lessonDetail?.unit || 'Loading...'}
    <span>{lessonDetail?.emoji_end || '🌈'}</span>
</div>

<style>
    #title {
        text-align: left;
        margin-bottom: 30px;
        font-size: 2.8em;
        color: #FF69B4;
        display: flex;
        align-items: center;
        gap: 15px;
    }
</style> 


