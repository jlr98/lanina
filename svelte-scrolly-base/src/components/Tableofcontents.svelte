<script>
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  
  // CSS selector that matches all headings to list in the ToC.
  // You can try out selectors in the dev console of your live page to make sure they return what you want by passing it into [...document.querySelectorAll(headingSelector)].
  // The default selector :is(h2, h3, h4):not(.toc-exclude) excludes h5 and h6 headings as well as any node with a class of toc-exclude.
  // For example <h2 class="toc-exclude">Section Title</h2> will not be listed.
  //   Credit to https://github.com/janosh/svelte-toc for this bit of logic.
  export let headingSelector = ':is(h2, h3, h4):not(.toc-exclude)';
  export let btnBgColor = '#FF4949';
  export let btnTextColor = 'white';
  export let tableBgColor = 'white';
  export let tableTextColor = 'black';
  export let scrollPaddingTop = '70px';
  export let indentAmount = 30;

  let isOpen = false;
  let headings = [];

  function handleOpen() {
    const headingsList= [...document.querySelectorAll(headingSelector)];
    const lowestIndentLevel = Math.min(...headingsList.map(h => parseInt(h.tagName[1])));
    const usedIds = [];
    headings = headingsList.map((h) => {
      let id = h.id;
      if (!id) {
        id = encodeURI(h.innerText.split(' ').join('_'));
      }
      
      let num = 2;
      let tempId = id;
      while (usedIds.includes(tempId)) {
        tempId = id + '_' + String(num++);
      }
      id = tempId;
      h.id = id;
      usedIds.push(id);

      return {
        text: h.textContent,
        indent: (parseInt(h.tagName[1]) - lowestIndentLevel) * indentAmount,
        scrollTo: `#${id}`
      };
    });

    isOpen = true;
  }

  function handleClose() {
    isOpen = false;
    headings = [];
  }

  function handleToTop() {
    window.scrollTo({ top: 0 });
    handleClose();
  }

  onMount(() =>  {
    const html = document.getElementsByTagName('html')[0];
    html.style.scrollPaddingTop = scrollPaddingTop;
  });
</script>

<div id='toc-opener-container'>
  <button
    aria-haspopup="menu"
    id='toc-opener'
    on:click={handleOpen}
    style='background-color: {btnBgColor};'
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      viewBox="0 0 124.5 25.7"
      fill={btnTextColor}
      >
      <g transform='translate(-5.7 5.1) rotate(90 13.1 7.75)'>
        <path id='arrow' d="M13.1,15.1c-0.5,0-1-0.2-1.4-0.6L0.9,3.7c-0.8-0.8-0.8-2,0-2.8s2-0.8,2.8,0l9.4,9.4l9.4-9.4
          c0.8-0.8,2-0.8,2.8,0s0.8,2,0,2.8L14.5,14.5C14.2,14.9,13.7,15.1,13.1,15.1z"/>
      </g>

      <text x='23' y='18' font-size='20' font-weight='bold'>Jump To</text>

      <g transform='translate(104 5.1) rotate(-90 13.1 7.75)'>
        <use href='#arrow' />
      </g>
    </svg>
  </button>
</div>

{#if isOpen}
  <button transition:fade={{duration: 400}} id='toc-closer' aria-label='Close' on:click|self={handleClose}>
    <div
      role='menu'
      id='toc-container'
      class='popup'
      style='--textColor: {tableTextColor}; --bgColor: {tableBgColor}'
      transition:fade={{duration: 400}}
    >
      <h2 class='toc-exclude' style='text-align: center;'>Table of Contents</h2>
      <button class='toc-exclude to-top' style='--btnBgColor: {btnBgColor}; --btnTextColor: {btnTextColor};' on:click={handleToTop}>To Top</button>
    
      <ol>
        {#each headings as heading}
          <li style='margin-left: {heading.indent}px;'><a href={heading.scrollTo} on:click={handleClose}>{heading.text}</a></li>
        {/each}
      </ol>
    </div>
  </button>
{/if}

<style lang="scss">
  :global(html) {
    scroll-behavior: smooth;
  }

  #toc-opener-container {
    position: fixed;
    right: -15px;
    bottom: max(130px, 30vh);
    height: 0;
    width: 0;
    transition: all 0.25s ease-out;
    z-index: 5;
    transform-origin: top center;

    #toc-opener {
      border: none;
      padding: 22px 12px 6px;
      width: 120px;
      height: 45px;
      display: flex;
      justify-content: center;
      align-items: center;
      transform: rotate(90deg);
      transform-origin: top left;

      &:hover {
        cursor: pointer;
      }
    }

    &:hover {
      cursor: pointer;
      transform: translateY(-15px) scale(1.2);
    }
  }

  #toc-closer {
    background-color: rgba(100,100,100,0.5);
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    border: none;
    padding: 0;
    margin: 0;
    z-index: 6;
    font-size: 30px;
  }

  #toc-container {
    height: fit-content;
    width: fit-content;
    padding: 6px 12px 18px;
    border: 1px solid black;
    border-radius: 6px;
    background-color: var(--bgColor);
    font-size: 1em;
    color: var(--textColor);

    h2 {
      font-size: 0.8em;
      margin: 10px 0px 0px;
    }
    
    .to-top {
      background-color: var(--btnBgColor);
      color: var(--btnTextColor);
      border: none;
      font-size: 0.6em;
      border-radius: 4px;
      margin: 12px 0px 16px;

      &:hover {
        cursor: pointer;
      }
    }

    ol {
      padding: 0;
      margin: 0;

      li {
        margin: 0;
        list-style-type: none;
        text-align: left;
        font-size: 0.6em;

        a {
          display: inline-block;
          width: min(fit-content, 80vw);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          text-decoration: none;
        }
      }
    }
  }

  .popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    transition: visibility 0.4s ease-out;
    box-shadow: 3px 3px 4px 3px rgba(175,175,175,0.2);
  }

  @media screen and (max-width: 400px) {
    #toc-container {
      font-size: 0.8em;

      ol > li > a {
        max-width: 200px;
      }
    }
  }
</style>