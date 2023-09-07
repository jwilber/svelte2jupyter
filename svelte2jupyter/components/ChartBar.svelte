<script>
  import { writable } from "svelte/store";

  import { scaleBand, scaleLinear } from "d3-scale";
  import { slide } from "svelte/transition";
  import { max } from "d3-array";
  import { onMount } from "svelte";

  export let width = 250;
  export let height = 250;
  export let paddingInner = 0.5;
  export let fill = "coral";
  export let showXAxis = true;
  export let showYAxis = true;
  export let showLabels = true;
  export let weight = 1;

  export let margin = {
    top: 15,
    bottom: 25,
    left: 25,
    right: 15,
  };

  $: data = [
    { label: "a", value: 12 * weight },
    { label: "b", value: 20 * weight },
    { label: "c", value: 15 },
  ];

  // define scales
  $: xScale = scaleBand()
    .domain(data.map((d) => d.label))
    .range([margin.left, width - margin.right])
    .paddingInner(paddingInner);
  $: yScale = scaleLinear()
    .domain([0, max(data, (d) => d.value) * 1.15])
    .range([height - margin.bottom, margin.top]);
  $: barWidth = xScale.bandwidth();

  onMount(() => {
    console.log("xscale", xScale.domain());
  });
  console.log("BAR CHART~~~!");
  const increment = () => {
    count += 1;
  };

  const components = writable([]);
  const selectedPage = writable(null);

  const componentMap = {
    Chatbot: "Chat",
    Dropdown: "Dropdown",
    Feedback: "Feedback",
    Compare: "ComparisonChat",
  };

  const setSelectedPage = (component) => {
    selectedPage.set(component);
  };

  fetch("/components")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log("yyy", data);
      components.set(data);
      selectedPage.set(data[0]);
    })
    .catch((error) => {
      console.log("Fetch request failed", error);
    });
</script>

tpuchj
<div class="container">
  <div class="chart-container" {width} {height}>
    <svg {width} {height}>
      {#if showLabels}
        <!-- x-axis -->
        <g class="axis x-axis">
          {#each xScale.domain() as tick}
            <g
              class="x-axis-tick"
              transform={`translate(${xScale(tick)} ${height - margin.top})`}
            >
              <text
                text-anchor="middle"
                x={barWidth / 2}
                y="5"
                class="axis-text">{tick}</text
              >
            </g>
          {/each}
        </g>
        <!-- y-axis -->
        <g class="axis y-axis">
          {#each yScale.ticks() as tick}
            {#if tick % 10 === 0}
              <g
                class="y-axis-tick"
                transform={`translate(${0} ${yScale(tick)})`}
                in:slide={{ y: 200, duration: 200 }}
              >
                <line x2={tick === 0 ? "0%" : "100%"} />
                <text text-anchor="left" x={0} y="-1" class="axis-text"
                  >{tick}</text
                >
              </g>
            {/if}
          {/each}
        </g>
      {/if}
      <!-- rects -->
      {#each data as d, i}
        <rect
          x={xScale(d.label)}
          y={yScale(d.value)}
          width={barWidth}
          height={yScale(0) - yScale(d.value)}
          {fill}
        />
      {/each}
      {#if showYAxis}
        <!-- y-axis line -->
        <line
          id="y-axis-line"
          x1={margin.left}
          x2={margin.left}
          y1={margin.top}
          y2={height - margin.bottom}
          stroke="black"
        />
      {/if}
      {#if showXAxis}
        <!-- x-axis-line -->
        <line
          id="x-axis-line"
          x1={margin.left}
          x2={width - margin.right}
          y1={height - margin.bottom}
          y2={height - margin.bottom}
          stroke="black"
        />
      {/if}
    </svg>
  </div>
  <div id="input-container" style:width>
    <p>Weight: {weight}</p>
    <input
      type="range"
      min="0"
      max="10"
      step="1"
      bind:value={weight}
      class="slider"
      id="myRange"
    />
  </div>
</div>

<style>
  #input-container {
    display: flex;
    flex-direction: row;
    text-align: left;
    max-width: 100%;
  }
  #input-container input {
    align-self: center;
    width: 100px;
  }
  .chart-container,
  .chart-container :global(*) {
    box-sizing: border-box;
  }
  .chart-container {
    width: 100%;
    height: 100%;
  }

  .y-axis line {
    stroke: #333;
    stroke-dasharray: 2;
    opacity: 0.5;
  }
  rect:hover {
    stroke-width: 4;
    stroke: black;
    fill: blue;
  }
  #x-axis-line {
    /* stroke-dasharray: 0; */
  }
</style>
