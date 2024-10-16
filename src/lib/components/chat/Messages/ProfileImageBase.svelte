<style>
  .blippi-animated {
  				position: relative;
  				margin: 0 auto;
  				animation: none; /* No animation initially */
    }
    .animate-speaking {
            animation: bounce 1s infinite;
    }

  @keyframes bounce {
      0%, 100% {
          transform: translateY(0);
      }
      50% {
          transform: translateY(-10px);
      }
  }
</style>

<script lang="ts">
	import { WEBUI_BASE_URL } from '$lib/constants';

	export let className = 'size-8';
	export let src = `${WEBUI_BASE_URL}/static/favicon.png`;
	export let animationSrc = "";
	export let speaking = false;
</script>

<img
	crossorigin="anonymous"
	src={src === ''
		? `${WEBUI_BASE_URL}/static/favicon.png`
		: src.startsWith(WEBUI_BASE_URL) ||
			  src.startsWith('https://www.gravatar.com/avatar/') ||
			  src.startsWith('data:') ||
			  src.startsWith('/')
			? src
			: `/user.png`}
	class="{className} object-cover rounded-full -translate-y-[1px] {speaking ? 'animate-speaking' : 'blippi-animated'}"
	alt="profile"
	draggable="false"
/>