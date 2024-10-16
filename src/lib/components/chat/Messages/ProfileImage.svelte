<script lang="ts">
	import { settings } from '$lib/stores';
	import ProfileImageBase from './ProfileImageBase.svelte';

	export let className = 'size-8';
	export let src = '';
	export let animationSrc = '';
	export let speaking = false;
</script>

<div class={`flex-shrink-0 ${($settings?.chatDirection ?? 'LTR') === 'LTR' ? 'mr-3' : 'ml-3'}`}>
	<ProfileImageBase {src} {className} {animationSrc} speaking={speaking}/>
</div>
