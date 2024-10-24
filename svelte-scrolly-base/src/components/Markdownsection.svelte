<script>
  import { marked } from 'marked';

  export let markdownFilePath = null;
  export let theme = {text: '#222'};
	export let col = 'medium';
  export let dataId = '';
  export let sectionId = '';
  export let sectionClass = '';
  export let sectionStyle = {};

  // External links get opened in new tab
  const renderer = new marked.Renderer();
  const linkRenderer = renderer.link;
  renderer.link = (href, title, text) => {
    const localLink = href.startsWith(`${location.protocol}//${location.hostname}`);
    const html = linkRenderer.call(renderer, href, title, text);
    return localLink ? html : html.replace(/^<a /, `<a target="_blank" rel="noreferrer noopener nofollow" `);
  };
  
  let markdown = null;
  async function loadMarkdown() {
    const path = markdownFilePath || dataId;
		markdown = path ? await fetch('./markdown/' + path + '.md').then(r => r.text()).then(t => marked(t, { renderer })) : null;
  }

  function stringifyStyle(obj) {
    let str = '';
    Object.entries(obj).forEach(([k,v]) => str += ` ${k}: ${v};`);
    return str;
  }
  
  $: extraStyle = stringifyStyle(sectionStyle);
  $: markdownFilePath, loadMarkdown();
</script>

<section id={sectionId} class={'markdown-section ' + sectionClass} data-id={dataId} style={`color: ${theme["text"]}; ${extraStyle}`}>
	<div class="col-{col}">
    {#if markdown}
      {@html markdown}
    {:else}
      <slot />
    {/if}
	</div>
</section>