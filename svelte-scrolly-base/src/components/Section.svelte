<script>
	///////////////////////////////////////////////////////////
	// Credit to https://github.com/ONSvisual/svelte-scrolly //
	///////////////////////////////////////////////////////////

	export let theme = {text: '#222', background: '#fff'};
	export let col = 'medium';
</script>

<section style={`color: ${theme["text"]}; background-color: ${theme["background"]};`}>
	<div class="col-{col}">
		<slot></slot>
	</div>
</section>