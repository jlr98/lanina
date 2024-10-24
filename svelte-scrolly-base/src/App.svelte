<script>
	import { onMount } from "svelte";
  let id = {}; // Object to hold visible section IDs of Scroller components
	let idPrev = {}; // Object to keep track of previous IDs, to compare for changes
	onMount(() => {
		idPrev = {...id};
	});
  
//Actions

	// Code to run Scroller actions when new caption IDs come into view
	function runActions(codes = []) {
    codes.forEach(code => {
      if (id[code] != idPrev[code]) {
				if (actions[code][id[code]]) {
					actions[code][id[code]].forEach(([stateName, newStateValue]) => (state[stateName] = newStateValue));
				}
				idPrev[code] = id[code];
			}
		});
	}
	$: id && runActions(Object.keys(actions)); // Run above code when 'id' object changes
</script>
<style global>
  html, body {
    position: relative;
    width: 100%;
    height: 100%;
  }

  body {
    color: #222;
    background-color: #fff;
    margin: 0;
    padding: 0;
    -webkit-box-sizing: border-box;
            box-sizing: border-box;
    font-family: "Helvetica Neue", "Arial", sans-serif;
    font-size: 21px;
    line-height: 1.5;
    word-wrap: break-word;
  }

  a {
    color: #206095;
  }

  a:hover {
    color: #323132;
  }

  label {
    display: block;
  }

  input, button, select, textarea {
    font-family: inherit;
    font-size: inherit;
    -webkit-padding: 0.4em 0;
    padding: 0.4em;
    margin: 0 0 0.5em 0;
    -webkit-box-sizing: border-box;
            box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 2px;
  }

  input:disabled {
    color: #ccc;
  }

  button {
    color: #333;
    background-color: #f4f4f4;
    outline: none;
  }

  button:disabled {
    color: #999;
  }

  button:not(:disabled):active {
    background-color: #ddd;
  }

  button:focus {
    border-color: #666;
  }

  header, section, nav, footer, figure, caption {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-pack: center;
        -ms-flex-pack: center;
            justify-content: center;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 54px;
    line-height: 1.3;
    margin: 30px 0 0 0;
  }

  h2 {
    font-size: 30px;
    margin: 40px 0 -20px 0;
  }

  h3 {
    font-size: 22px;
    margin: 40px 0 -10px 0;
  }

  p {
    margin: 30px 0 0 0;
  }

  img {
    max-width: 100%;
    height: auto;
    vertical-align: middle;
  }

  blockquote {
    margin: 30px 0 6px 0;
    font-size: 30px;
    color: #777;
  }

  small {
    font-size: 14px;
  }

  /* CLASSES */

  .col-full {
    width: 100%;
  }


  .col-extra-wide {
    width: 100%;
    max-width: 1280px;
    margin: 0 24px;
  }

  .col-wide {
    width: 100%;
    max-width: 980px;
    margin: 0 24px;
  }

  .col-medium {
    width: 100%;
    max-width: 680px;
    margin: 0 24px;
  }

  .col-narrow {
    width: 100%;
    max-width: 540px;
    margin: 0 24px;
  }

  .height-full {
    min-height: 100vh;
  }

  .height-full-minus-title {
    min-height: calc(100vh - 60px);
  }

  .center {
    text-align: center;
  }

  .middle {
    height: 100%;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
        -ms-flex-direction: column;
            flex-direction: column;
    -webkit-box-pack: center;
        -ms-flex-pack: center;
            justify-content: center;
  }

  .caption {
    margin-top: 8px;
    text-align: left;
    font-size: 14px;
    color: #777;
  }

  .scroll-shadows {
    overflow-y: auto;
    border: 1px solid rgb(220,220,220);

    background:
      /* Shadow Cover TOP */
      linear-gradient(
        white 20%,
        rgba(255, 255, 255, 0)
      ) center top,
      
      /* Shadow Cover BOTTOM */
      linear-gradient(
        rgba(255, 255, 255, 0), 
        white 80%
      ) center bottom,
      
      /* Shadow TOP */
      linear-gradient(
        rgba(100, 100, 100, 0.3) 20%,
        rgba(0, 0, 0, 0)
      ) center top,
      
      /* Shadow BOTTOM */
      linear-gradient(
        rgba(0, 0, 0, 0) 20%,
        rgba(100, 100, 100, 0.3)
      ) center bottom;
    
    background-repeat: no-repeat;
    background-size: 100% 40px, 100% 40px, 100% 14px, 100% 14px;
    background-attachment: local, local, scroll, scroll;
  }
</style>