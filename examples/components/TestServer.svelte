<script>
  import { max } from "d3-array";
  import { scaleLinear, scaleBand, scaleOrdinal } from "d3-scale";
  import { writable } from "svelte/store";

  export let data;
  export let height = 400;
  export let width = 700;

  const textVal = writable("panda");
  let question = "What is monday?";

  const averageLatency = data.reduce((acc, curr) => {
    if (!acc[curr.model]) {
      acc[curr.model] = { sum: curr.latency, count: 1 };
    } else {
      acc[curr.model].sum += curr.latency;
      acc[curr.model].count++;
    }
    return acc;
  }, {});

  const avgRankData = Object.keys(averageLatency).map((key) => ({
    model: key,
    avgRank: averageLatency[key].sum / averageLatency[key].count,
  }));

  let margin = {
    top: 20,
    bottom: 20,
    left: 175,
    right: 20,
  };

  $: innerWidth = width - margin.left - margin.right;
  $: innerHeight = height - margin.top - margin.bottom;

  $: yScale = scaleBand()
    .rangeRound([margin.top, innerHeight - margin.bottom])
    .padding(0.05)
    .domain(avgRankData.map((d) => d.model));

  $: xScale = scaleLinear()
    .rangeRound([margin.left, innerWidth - margin.right])
    .domain([0, max(avgRankData, (d) => d.avgRank)]);

  $: colorScale = scaleOrdinal()
    .domain(avgRankData.map((d) => d.model))
    .range(["#FF5470", "#1B2D45", "#00EBC7", "#FDE24F"]);

  async function clicked() {
    console.log("rrrrrr");
    const response = await fetch(`http://127.0.0.1:50315/chat/${question}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: "hello",
      }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log("data", data);
      $textVal = data["answer"];
    } else {
      const err = await response.text();
      alert(err);
    }
  }
</script>

<div id="bar-chart-holder" {width} {height}>
  <svg {width} {height}>
    <text x="10" y="20" fill="black">{$textVal}</text>
    <!-- y-ticks -->
    {#each avgRankData.map((d) => d.model) as tick}
      <g
        transform={`translate(${margin.left} ${
          yScale(tick) + yScale.bandwidth() / 2
        })`}
      >
        <text class="axis-text" x="-5" y="0" text-anchor="end">{tick}</text>
      </g>
    {/each}

    <!-- x-ticks -->
    {#each xScale.ticks() as tick}
      <g
        transform={`translate(${xScale(tick)}, ${innerHeight - margin.bottom})`}
      >
        <text class="axis-text" y="15" text-anchor="middle">{tick}</text>
      </g>
    {/each}

    <!-- bars -->
    {#each avgRankData as d}
      <rect
        on:click={clicked}
        y={yScale(d.model)}
        x={margin.left}
        width={xScale(d.avgRank) - margin.left}
        height={yScale.bandwidth()}
        fill={colorScale(d.model)}
      />
      <text
        class="label-text"
        y={yScale(d.model) + yScale.bandwidth() / 2}
        x={xScale(d.avgRank) + 5}
        text-anchor="start"
        dominant-baseline="middle"
      >
        {d.avgRank.toFixed(2)}
      </text>
    {/each}
    <line
      class="axis-line"
      x1={margin.left}
      x2={innerWidth - margin.right}
      y1={innerHeight - margin.bottom}
      y2={innerHeight - margin.bottom}
    />
  </svg>
</div>

<style>
  @import url("https://fonts.googleapis.com/css?family=Work+Sans:400|Lato:400|Inconsolata:400");

  * {
    font-family: Lato;
  }
  #bar-chart-holder {
    height: 100%;
    width: 100%;
  }

  rect:hover {
    stroke: red;
    stroke-width: 5;
  }
  .axis-text {
    font-size: 12px;
  }
  .axis-line {
    stroke-width: 3;
    stroke: black;
    fill: none;
  }
</style>
