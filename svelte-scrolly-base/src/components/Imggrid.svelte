<script>
  import Imgmodal from "./Imgmodal.svelte";

	export let theme = {"text": "#222", "background": "#fff"};
  export let width = '100%';
  export let height = 'calc(100vh - 110px)';
  export let rows = 1;
  export let cols = 1;
  export let imgs = [];
  export let gap = 0;

  let selectedImage = { src: '', alt: ''};
  let showModal = false;
</script>

<div class='img-grid-container' style='--rows: {rows}; --cols: {cols}; --width: {width}; --height: {height}; --gap: {gap}px'>
  {#if imgs.length}
    {#each imgs.slice(0, rows*cols) as imgObj}
      <div class="img-container" style="background-color: {theme['background']}; grid-column: span {imgObj.gridColSpan || 1}; grid-row: span {imgObj.gridRowSpan || 1}">
        {#if imgObj.title}
          <h3 class='toc-exclude' style="height: 22px; margin: 0; color: {theme['text']}; background-color: {theme['background']}; width: 100%">{imgObj.title}</h3>
        {/if}
        {#if imgObj.src}
          <div>
            {#if imgObj.src.split('.')[1] === 'mp4'}
              <video
                controls
                muted
                height='100%'
                width='100%'
              >
                <source src={imgObj.src} type='video/mp4'>
                Your browser does not support playing this video.
              </video>
            {:else}
              <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
              <img src={imgObj.src} alt={imgObj.alt || ''} title={imgObj.hoverText || ''} on:click={() => {
                showModal = !showModal;
                selectedImage = imgObj;
              }}/>
            {/if}
          </div>
        {:else}
          <div class='not-available'>Image Not Available</div>
        {/if}
        {#if imgObj.caption}
          <caption style="color: {theme['text']}; background-color: {theme['background']};">
            <div class="col-medium" style="display:flex;">
              <div class="caption">{@html imgObj.caption}</div>
            </div>
          </caption>
        {/if}
      </div>
    {/each}

    <Imgmodal bind:showModal>
      <img src={selectedImage.src} alt={selectedImage.alt || ''} />
    </Imgmodal>
  {:else}
    <div class='not-available'>Images Not Available</div>
  {/if}
</div>

<style>
  .img-grid-container {
    display: grid;
    grid-template-columns: repeat(var(--cols), calc(var(--width) / var(--cols) - (var(--gap) * (var(--cols) - 1) / var(--cols))));
    grid-template-rows: repeat(var(--rows), calc(var(--height) / var(--rows) - (var(--gap) * (var(--rows) - 1) / var(--rows))));
    max-width: var(--width);
    max-height: var(--height);
    gap: var(--gap);
  }

  .img-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }

  .img-container > div {
    flex: 1;
    min-height: 0;
  }

  .img-container > div > img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  
  .caption {
    flex-grow: 1;
    width: 0;
  }

  .not-available {
    color: rgb(150,150,150);
    font-style: italic;
    text-align: center;
  }
</style>