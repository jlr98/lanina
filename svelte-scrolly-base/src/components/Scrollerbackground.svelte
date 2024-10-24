<script>
  import ImgGrid from "./Imggrid.svelte";
  import Graph from "./Graphnina.svelte";
  import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

  const COMPONENT_OPTIONS = {
    'imggrid': ImgGrid,
    'graph': Graph 
  }

  export let bgStates = [];
  export let bgShowing = '';
  export let offsetTop = '0px';

  $: currComp = bgStates.find(s => s.showWhen === bgShowing);
</script>

{#if currComp}
  {#key currComp.showWhen}
    <div
      style='margin-top: {offsetTop};'
      out:fly={{ duration: 250, x: '100vw', easing: quintOut }}
      in:fly={{ delay: 250, duration: 250, x: '100vw', easing: quintOut }}
    >
      <svelte:component this={COMPONENT_OPTIONS[currComp.type]} {...currComp.props} />
    </div>
  {/key}
{/if}