<script>
  ///////////////////////////////////////////////////////////
	// Credit to https://github.com/ONSvisual/svelte-scrolly //
	///////////////////////////////////////////////////////////
  
  export let theme = {"text": "#222", "background": "#fff"};
  export let bgimage = null;
  export let bgcolor = null;
  export let bgfixed = false;
  export let center = true;
  export let short = false;

  let style = '';

  if (bgimage) {
    style += `background-image: url(${bgimage});`;
  } else {
    style += 'background-image: none;';
  }

  if (bgfixed) {
    style += ' background-attachment: fixed;';
  }
</script>

<header style="color: {theme['text']}; background-color: {bgcolor ? bgcolor : theme['background']}; {style}" class:short>
	<div class="v-padded col-wide middle" style="position: relative" class:short class:height-full={!short}>
		<div class:center>
			<slot></slot>
    </div>
	</div>
</header>

<style>
  .short {
    min-height: 85vh;
  }
  .v-padded {
    box-sizing: border-box;
    padding: 40px 0;
  }
</style>