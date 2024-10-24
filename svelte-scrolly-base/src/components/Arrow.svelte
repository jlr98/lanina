<script>
	///////////////////////////////////////////////////////////
	// Credit to https://github.com/ONSvisual/svelte-scrolly //
	///////////////////////////////////////////////////////////

	export let color = "black";
  export let animation = true;

	$: arrowSvg = `<?xml version="1.0" encoding="utf-8"?>
		<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
			viewBox="0 0 26.2 15.5" style="enable-background:new 0 0 26.2 15.5;" xml:space="preserve">
		<g>
			<path fill=${color} d="M13.1,15.1c-0.5,0-1-0.2-1.4-0.6L0.9,3.7c-0.8-0.8-0.8-2,0-2.8s2-0.8,2.8,0l9.4,9.4l9.4-9.4
				c0.8-0.8,2-0.8,2.8,0s0.8,2,0,2.8L14.5,14.5C14.2,14.9,13.7,15.1,13.1,15.1z"/>
		</g>
		</svg>`;
</script>

<div class="arrow" class:short={!animation} class:bounce={animation} aria-hidden="true">
	{@html arrowSvg}
</div>

<style>
	.arrow {
		width: 48px;
		height: 48px;
	}

	.short {
		height: fit-content;
	}

	.bounce {
		-webkit-animation-duration: 2s;
		        animation-duration: 2s;
		-webkit-animation-iteration-count: infinite;
		        animation-iteration-count: infinite;
		-webkit-animation-name: bounce;
		        animation-name: bounce;
		-webkit-animation-timing-function: ease;
		        animation-timing-function: ease;
	}

	@-webkit-keyframes bounce {
		0%   { -webkit-transform: translateY(10px); transform: translateY(10px); }
		30%  { -webkit-transform: translateY(-10px); transform: translateY(-10px); }
		50%  { -webkit-transform: translateY(10px); transform: translateY(10px); }
		100% { -webkit-transform: translateY(10px); transform: translateY(10px); }
	}

	@keyframes bounce {
		0%   { -webkit-transform: translateY(10px); transform: translateY(10px); }
		30%  { -webkit-transform: translateY(-10px); transform: translateY(-10px); }
		50%  { -webkit-transform: translateY(10px); transform: translateY(10px); }
		100% { -webkit-transform: translateY(10px); transform: translateY(10px); }
	}
</style>