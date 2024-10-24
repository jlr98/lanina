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

<footer style="color: {theme['text']}; background-color: {bgcolor ? bgcolor : theme['background']}; {style}" class:short>
	<div class="v-padded col-footer middle" style="position: relative" class:short class:tall-footer={!short}>
		<div class:center>
			<slot></slot>
    </div>
	</div>
</footer>

<style>
  .tall-footer {
    min-height: 30vh;
  }
  .short {
    min-height: 15vh;
  }
  .v-padded {
    box-sizing: border-box;
    padding: 40px 0;
  }
  .col-footer {
    width: 95%;
  }
</style>