<script context='module'>
  let counter = 0;
</script>

<script>
  export let bgColor = 'white';
  export let textColor = 'black';
  export let value;
  export let options;
  export let label = '';
  export let borderColor = 'rgb(150,150,150)';
  export let labelColor = 'default';
  export let labelBGColor = 'default';
  export let labelOffset = '-0.8em';
  export let fontSize = '16px';
  let id = 'selector_' + counter++;
</script>

<div class='selector-container' style='background-color: {bgColor}; border: 1px solid {borderColor}; font-size: {fontSize};'>
  {#if label}
    <label style='background-color: {labelBGColor}; color: {labelColor}; top: {labelOffset};' for={id}>{label}</label>
  {/if}

  <select style='color: {textColor};' id={id} on:change={(e) => value = options.find(({value}) => value === e.target.value)}>
    {#each options as option (option.value)}
      <option style='color: {textColor};' value={option.value}>{option.name}</option>
    {/each}
  </select>
</div>

<style>
  .selector-container {
    position: relative;
    border-radius: 5px;
    margin-top: 1em;
  }

  label {
    font-size: 0.7em;
    position: absolute;
    left: 7px;
    background-color: white;
    padding: 0px 3px;
  }

  select {
    background-color: transparent;
    border: none;
    font-size: 1em;
    padding: 8px 3px 4px;
  }

  select:hover {
    cursor: pointer;
  }
</style>