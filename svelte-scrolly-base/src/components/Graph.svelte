<script context='module'>
  const EL_NINO_END_YEARS = [1952, 1954, 1958, 1959, 1964, 1966, 1969, 1970, 1973, 1977, 1978, 1980, 1983, 1987, 1988, 1992, 1995, 1998, 2003, 2005, 2007, 2010, 2015, 2016, 2019, 2024];
    const COLORS = [
    [0,0,255],
    [255,0,0],
    [255,165,0],
    [76,187,23]
  ];
  const AVG_COLOR = chroma.average(COLORS);
  const COLOR_SCALES = {
    xNeg: chroma.scale([AVG_COLOR, COLORS[0]]),
    xPos: chroma.scale([AVG_COLOR, COLORS[1]]),
    yNeg: chroma.scale([AVG_COLOR, COLORS[2]]),
    yPos: chroma.scale([AVG_COLOR, COLORS[3]])
  };

  const DATA_PROCESSING_OPTIONS = {
    'default': noProcessing,
    'basic': basicProcessing,
    'comparedToNormal': comparedToNormalProcessing
  };


  function noProcessing(rawData) {
    return rawData;
  }
  
  function basicProcessing(rawData) {
    const stationName = rawData.meta.name;
    const data = { data: [], season: [], isElNino: [] };
    for (let i = 0; i < rawData.data.length; i++) {
      const [dateStr, p1, p2] = rawData.data[i];
      data.data.push({
        x: parseFloat(p1),
        y: parseFloat(p2)
      });

      const seasonEndYear = parseInt(dateStr.slice(0,4));
      data.season.push(`${seasonEndYear - 1}-${dateStr.slice(2,4)}`);
      data.isElNino.push(EL_NINO_END_YEARS.includes(seasonEndYear));
    }
    return {
      stationName,
      ...data
    }
  }

  function comparedToNormalProcessing(rawData, elNinoOnly=true) {
    const stationName = rawData.meta.name;
    const data = {
      data: [],
      season: [],
      isElNino: [],
      pointBackgroundColor: [],
      ranges: {
        x: { min: 999, max: -999},
        y: { min: 999, max: -999}
      }
    };
    for (let i = 0; i < rawData.data.length; i++) {
      const [dateStr, p1, p2] = rawData.data[i];
      const seasonEndYear = parseInt(dateStr.slice(0,4));
      
      if (elNinoOnly && !EL_NINO_END_YEARS.includes(seasonEndYear)) continue;
      const x = parseFloat(p1);
      if (x > data.ranges.x.max) data.ranges.x.max = x;
      if (x < data.ranges.x.min) data.ranges.x.min = x;
      
      const y = parseFloat(p2);
      if (y > data.ranges.y.max) data.ranges.y.max = y;
      if (y < data.ranges.y.min) data.ranges.y.min = y;
      
      data.data.push({
        x,
        y,
        season: `'${String(seasonEndYear - 1).slice(2,4)}-'${dateStr.slice(2,4)}`
      });

      data.isElNino.push(EL_NINO_END_YEARS.includes(seasonEndYear));
    }

    const xMaxDiff = Math.max(
      Math.abs(data.ranges.x.min),
      Math.abs(data.ranges.x.max),
    );
    const yMaxDiff = Math.max(
      Math.abs(data.ranges.y.min),
      Math.abs(data.ranges.y.max),
    );
    data.pointBackgroundColor = data.data.map(({x,y}) => {
      const xColor = x <= 0 ? COLOR_SCALES.xNeg(calcWeight(Math.abs(x), xMaxDiff)) : COLOR_SCALES.xPos(calcWeight(x, xMaxDiff));
      const yColor = y <= 0 ? COLOR_SCALES.yNeg(calcWeight(Math.abs(y), yMaxDiff)) : COLOR_SCALES.yPos(calcWeight(y, yMaxDiff));
      return `rgb(${chroma.average([xColor, yColor], 'lrgb').rgb()})`;
    });

    return {
      stationName,
      ...data
    }
  }


  function calcDate(numDays, beforeOrAfter, refDateStr) {
		const refTimeStamp = Date.parse(refDateStr + ' 00:00');
		const daysInMS = numDays * 86400000 * (beforeOrAfter === 'before' ? -1 : 1);
		let newDateTimeStamp = refTimeStamp + daysInMS;
		if (newDateTimeStamp > new Date().getTime()) newDateTimeStamp = new Date().getTime();
		return new Date(newDateTimeStamp).toISOString().slice(0, 10);
	}

  function constructAcisBody(stationId, paramsObj) {
    let { elems, sdate, edate, numberOfDays } = paramsObj;
    
    const today = new Date().toISOString().slice(0,10);
    if (!(sdate && edate)) {
      if (edate) {
        sdate = numberOfDays ? calcDate(numberOfDays, 'before', edate) : edate;
      } else if (sdate) {
        edate = numberOfDays ? calcDate(numberOfDays, 'after', sdate) : today;
      } else {
        edate = today;
        sdate = numberOfDays ? calcDate(numberOfDays, 'before', edate) : today;
      }
    }
    
    return {
      sid: stationId,
      elems,
      sdate,
      edate
    };
  }

  function callAcis(paramsObj) {
    return fetch('https://data.rcc-acis.org/StnData', {
      method: 'POST',
      body: JSON.stringify(paramsObj),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => res.json())
      .catch(e => {
        console.error(e);
        return null;
      })
  }

  function averageOfPeriod(rawData) {
    const numYears = rawData.length;
    const numVars = rawData[0].length - 1;
    
    const sums = Array(numVars).fill(0);
    for (let i = 0; i < numYears; i++) {
      rawData[i].slice(1).forEach((val,j) => sums[j] += parseFloat(val));
    }
    return sums.map(v => v / numYears);
  }

  function calcWeight(value, max) {
    return value / max;
  }

  function lineGenerator(lineOptions) {
    return {
      type: 'line',
      yMin: undefined,
      yMax: undefined,
      xMin: undefined,
      xMax: undefined,
      borderColor: 'black',
      drawTime: 'beforeDraw',
      ...lineOptions
    };
  }

  function constructGradient(chartInst, position) {
    let c1 = 'rgb(0, 0, 0)';
    let c2 = 'rgb(127, 127, 127)';
    let c3 = 'rgb(255, 255, 255)';
    let direction = 'to right';
    const axis = position.split('-')[0];
    if (position === 'x') {
      c1 = `rgba(${COLORS[0]})`;
      c2 = AVG_COLOR;
      c3 = `rgba(${COLORS[1]})`;
    } else if (position === 'y') {
      c1 = `rgba(${COLORS[2]})`;
      c2 = AVG_COLOR;
      c3 = `rgba(${COLORS[3]})`;
      direction = 'to top';
    }

    const min = chartInst.scales[axis].min;
    const max = chartInst.scales[axis].max;
    const range = max - min;
    const stop = Math.abs(min) / range * 100;
    return `linear-gradient(${direction}, ${c1} 0%, ${c2} ${stop}%, ${c3} 100%)`
  }
</script>

<script>
  import chroma from 'chroma-js';
  import { Scatter } from 'svelte-chartjs';
  import annotationPlugin from 'chartjs-plugin-annotation';
  import ChartDataLabels from 'chartjs-plugin-datalabels';
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
  } from 'chart.js';
  ChartJS.register(
    annotationPlugin,
    Title,
    Tooltip,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    ChartDataLabels
  );

  export let station = null;
  export let acisParams;
  export let acisDataProcessor = 'default';
  
  let chartRef = null;
  let processedData = null;
  let xGradient = 'rgb(255,255,255)';
  let yGradient = 'rgb(255,255,255)';

  function updateGradients(chartInst) {
    if (chartInst) {
      xGradient = constructGradient(chartInst, 'x');
      yGradient = constructGradient(chartInst, 'y');
    }
  }

  async function fetchData(stationObj, queryParams, dataProcessingSelection) {
    if (
      typeof stationObj === 'object' && 'value' in stationObj &&
      typeof queryParams === 'object' &&
      typeof dataProcessingSelection === 'string'
    ) {
      try {
        const paramsObj = constructAcisBody(stationObj.value, queryParams);
        const rawData = await callAcis(paramsObj);
        processedData = DATA_PROCESSING_OPTIONS[dataProcessingSelection](rawData);
      } catch (e) {
        console.error(e);
        processedData = null;
      }
    } else {
      processedData = null;
    }
  }

  $: station, acisParams, acisDataProcessor, fetchData(station, acisParams, acisDataProcessor);
  $: processedData, updateGradients(chartRef);
</script>

<figure>
  {#if processedData}
    <div class='scatter-y-axis-gradient left' style='--yGradient: {yGradient}'>
      <p>Wetter</p>
      <p>Drier</p>
    </div>
    <div class='scatter-y-axis-gradient right' style='--yGradient: {yGradient}'>
      <p>Wetter</p>
      <p>Drier</p>
    </div>
    <div class='scatter-x-axis-gradient top' style='--xGradient: {xGradient}'>
      <p>Cooler</p>
      <p>Warmer</p>
    </div>
    <div class='scatter-x-axis-gradient bottom' style='--xGradient: {xGradient}'>
      <p>Cooler</p>
      <p>Warmer</p>
    </div>
    <Scatter
      bind:chart={chartRef}
      class='scatter-graph-canvas'
      data={{
        datasets: [{
          borderColor: 'black',
          borderWidth: 1,
          hoverBorderWidth: 2,
          pointBackgroundColor: processedData.pointBackgroundColor,
          radius: 8,
          hoverRadius: 10,
          data: processedData.data
        }]
      }}
      options={{
        responsive: true,
        layout: {
          padding: {
            right: 25
          }
        },
        scales: {
          x: {
            title: {
              text: 'Temperature Difference From Normal (°F)',
              display: true
            },
            grid: {
              tickLength: 28,
              tickBorderDash: [0, 23, 5]
            }
          },
          y: {
            title: {
              text: 'Precipitation Difference From Normal (inches)',
              display: true
            },
            grid: {
              tickLength: 28,
              tickBorderDash: [5, 23]
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: `${(typeof station === 'object' && 'name' in station) ? station.name : ''} Temp/Precip in La Niña Winters`,
            color: 'orange',
            align: 'start',
            fullSize: false,
            padding: {
              bottom: 30
            }
          },
          annotation: {
            clip: false,
            common: {
              drawTime: 'beforeDatasetsDraw'
            },
            annotations: {
              horizontalLine: lineGenerator({ yMin: 0, yMax: 0 }),
              verticalLine: lineGenerator({ xMin: 0, xMax: 0 })
            }
          },
          datalabels: {
            formatter: function(value) {
              return 'season' in value ? value.season : '';
            },
            align: 'bottom',
            color: 'black',
            backgroundColor: 'rgba(255,255,255,0.5)',
            borderRadius: 5,
            padding: 2,
            offset: 7
          },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                console.log(ctx);
                return [ctx.raw.season, `Temp: ${Math.round(ctx.raw.x * 10) / 10} °F`,`Precip: ${Math.round(ctx.raw.y * 100) / 100} in.`];
              }
            },
            displayColors: false
          }
        },
      }}
    />
  {/if}
</figure>

<style lang='scss'>
  figure {
    position: relative;

    :global(.scatter-graph-canvas) {
      z-index: 1;
      position: relative;
    }

    .scatter-y-axis-gradient,
    .scatter-x-axis-gradient {
      position: absolute;
      color: white;
      font-size: 14px;
      font-weight: bold;
      display: flex;
      justify-content: space-between;
      box-sizing: border-box;
      
      p {
        margin: 0;
        font-size: 12px;
      }
    }
    
    .scatter-x-axis-gradient {
      right: 24px;
      left: 67px;
      height: 23px;
      padding: 3px 12px;
      background: var(--xGradient);
      
      &.bottom {
        bottom: 47px;
      }

      &.top {
        top: 21px;
      }
    }


    .scatter-y-axis-gradient {
      bottom: 70px;
      top: 44px;
      width: 23px;
      padding: 12px 3px;
      flex-direction: column;
      background: var(--yGradient);
      
      &.left {
        left: 44px;
      }

      &.right {
        right: 1px;
      }

      p {
        writing-mode: vertical-lr;
        transform: scale(-1);
      }
    }
  }
</style>