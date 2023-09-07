<script>
  let bridgeTraffic = [
    { name: "Henry Hudson Bridge", traffic: 58809 },
    { name: "Hugh L. Carey Tunnel", traffic: 54007 },
    { name: "Queens-Midtown Tunnel", traffic: 86081 },
    { name: "R.F.K. Memorial Bridge Manhattan Plaza", traffic: 91509 },
    { name: "George Washington Bridge", traffic: 280784 },
    { name: "Holland Tunnel", traffic: 87232 },
    { name: "Lincoln Tunnel", traffic: 109796 },
  ];

  bridgeTraffic.sort((a, b) => b.traffic - a.traffic);
</script>

<svg>
  {#each bridgeTraffic as bridge, i}
    <!-- <p>{bridge.name}</p> -->
    <g transform={`translate(500, ${i * 20 + 10})`}>
      <rect width={bridge.traffic / 1000} height="10" fill="red" />
      <text text-anchor="end" dominant-baseline="middle" y="5" x="-5"
        >{bridge.name}</text
      >
      <text
        fill="#aaa"
        font-size="12"
        dominant-baseline="middle"
        y="5"
        x={bridge.traffic / 1000 + 5}>{bridge.traffic.toLocaleString()}</text
      >
    </g>
  {/each}
</svg>

<style>
  svg {
    border: 1px solid black;
    width: 100%;
    height: 200px;
  }
</style>
