<script>
  export let date = '';
  export let sectionTitle = '';
</script>

<header>
  <div id='header-content'>
    <div id='header-content-left'>
      <h1 class='toc-exclude'>La Niña Impacts and Outlook</h1>
    </div>
    <div id='noaa-bird'>
      <svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="104px" viewBox="0 13 200.000000 117.000000" preserveAspectRatio="xMidYMid meet">
        <g transform="translate(0.000000,117.000000) scale(0.100000,-0.100000)" fill="#fff" stroke="none">
          <path d="M250 973 c-54 -37 -100 -108 -100 -155 0 -34 34 -66 77 -73 74 -11
            122 -46 246 -178 192 -204 291 -258 523 -285 l69 -8 -50 -26 c-41 -21 -121
            -52 -195 -75 -11 -3 -9 -8 10 -18 73 -38 140 -28 294 46 114 54 206 85 284 94
            51 7 53 8 36 26 -15 17 -27 18 -103 13 l-86 -7 100 52 c138 72 205 128 319
            272 55 68 130 156 168 195 l69 71 -31 26 c-39 33 -67 41 -131 35 -59 -6 -129
            -50 -175 -111 -17 -23 -62 -100 -99 -172 -108 -209 -197 -318 -280 -345 -48
            -16 -129 -8 -191 19 -91 41 -162 113 -336 343 -134 175 -200 243 -255 262 -61
            21 -132 21 -163 -1z"/>
        </g>
      </svg>
    </div>
    <div id='header-content-right'>
      <h2 class='toc-exclude'>Northeast Region</h2>
      <p>{date}</p>
    </div>
  </div>

  <div id='section-title'>
      <h2 class="toc-exclude">{sectionTitle}</h2>
  </div>
</header>

<style lang='scss'>
  $dark-blue: rgb(0,47,135);
  $light-blue: rgb(0,133,202);
  $text-color: white;
  $base-font-size: 22px;
  $header-height: 90px;
  $header-content-height: 50px;
  $section-title-height: $header-height - $header-content-height;

  header {
    top: -1px;
    width: 100vw;
    height: $header-height;
    background-color: $dark-blue;
    font-size: $base-font-size;
    color: $text-color;
    position: fixed;
    z-index: 3;
    flex-direction: column;
    
    #header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 90vw;
      max-width: 1500px;
      padding: 0px 15px;
      margin: 0 auto;
      box-sizing: border-box;
      height: $header-content-height;

      &::after {
        content: '';
        display: block;
        position: absolute;
        top: 5px;
        left: 30vw;
        height: 0;
        width: 0;
        border-left: 20vw solid transparent;
        border-right: 20vw solid transparent;
        border-bottom: calc($header-height - 5px) solid $light-blue;
      }

      div {
        z-index: 2;
      }
    
      div:nth-child(odd) {
        flex: 1;
      }

      h1,
      h2,
      p {
        margin: 0;
      }

      h1 {
        font-size: 1em;
      }

      h2 {
        font-size: 0.8em;
      }

      p {
        font-size: 0.6em;
        font-style: italic;
      }
    
      #noaa-bird {
        width: 104px;
        height: $header-content-height;
        overflow: hidden;
      }

      #header-content-right {
        text-align: right;
      }
    }

    #section-title {
      background-color: $light-blue;
      height: $section-title-height;
      display: flex;
      justify-content: center;
      align-items: center;
      padding-left: 12px;
      box-shadow: 0px 8px 8px rgba(0,47,135,0.4);
      width: 100vw;
      position: relative;
  
      h2 {
        margin: 0;
        font-size: 1.2em;
      }
    }
  }

  @media screen and (max-width: 1200px) {
    header > #header-content {
      width: 95vw;
    }
  }

  @media screen and (max-width: 900px) {
    header > #header-content {
      width: 100vw;
    }
  }

  @media screen and (max-width: 800px) {
    header {
      font-size: 18px;
    }
  }
  
  @media screen and (max-width: 420px) {
    header {
      font-size: 14px;

      #header-content {
        padding: 0px 5px;
      }
    }
  }
</style>