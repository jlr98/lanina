<script>
	export let theme = {"text": "#222", "background": "#fff"};
  export let src = null;
  export let alt = '';
  export let changeTime = 500;
  export let width = 200;
  export let title = '';
  export let caption = '';

  let currSrc = null;
  let currTitle = null;
  let currCaption = null;
  let hidden = false;

  $: (src, title, caption, changeSrc())

  function changeSrc() {
    hidden = true;    
    setTimeout(() => {
      currSrc = src;
      currTitle = title;
      currCaption = caption;
      hidden = false;
    }, changeTime / 2);
  }
</script>

<div class="img-container" class:hidden style="background-color: {theme['background']}; transition-duration: {changeTime / 2}ms">
  {#if currTitle}
    <h3 class='toc-exclude' style="margin: 0; color: {theme['text']}; background-color: {theme['background']}; width: 100%">{currTitle}</h3>
  {/if}
  {#if currSrc}
    <img src={currSrc} alt={alt} style="width: {width}; margin: 0 auto; max-width: fit-content;"/>
  {/if}
  {#if currCaption}
    <caption style="color: {theme['text']}; background-color: {theme['background']};">
      <div class="col-medium" style="display:flex;">
        <div class="caption">{@html currCaption}</div>
      </div>
    </caption>
  {/if}
</div>

<style>
  .img-container {
    opacity: 1;
    transition: all 1s ease-out;
    display: flex;
    flex-direction: column;
    width: fit-content;
    margin: 0 auto;
  }
  
  .hidden {
    opacity: 0;
  }

  .caption {
    flex-grow: 1;
    width: 0;
  }
</style>