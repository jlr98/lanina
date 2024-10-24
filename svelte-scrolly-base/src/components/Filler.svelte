<script>
	///////////////////////////////////////////////////////////
	// Credit to https://github.com/ONSvisual/svelte-scrolly //
	///////////////////////////////////////////////////////////
	
	export let theme = {"text": "#222", "background": "#fff"};
	export let center = true;
	export let wide = false;
	export let short = false;
</script>

<section style="color: {theme['text']}; background-color: {theme['background']};">
	<div class="middle" class:center class:col-medium={!wide} class:col-wide={wide} class:height-full={!short} class:short>
		<slot></slot>
	</div>
</section>

<style>
	section {
		padding: 36px 0;
	}
	.short {
		min-height: 70vh;
	}
</style>