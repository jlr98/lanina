<script>
  ///////////////////////////////////////////////////////////
	// Credit to https://github.com/ONSvisual/svelte-scrolly //
	///////////////////////////////////////////////////////////

  export let theme = {"text": "#222", "background": "#fff", "muted": "#777"};
  export let hr = true;
</script>

<section style="color: {theme['text']}; background-color: {theme['background']};">
	<div class="col-medium">
    {#if hr}
    <hr style="color: {theme['muted']}"/>
    {:else}
    <hr style="color: {theme['muted']}; border: none;"/>
    {/if}
	</div>
</section>

<style>
  hr {
    width: 75px;
    border: none;
    border-top: 2px solid;
    margin: 40px auto -10px auto;
  }
</style>

