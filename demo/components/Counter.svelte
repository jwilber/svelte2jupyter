<script>
  export let count = 0;
  const increment = () => {
    count += 1;
  };
</script>

<button on:click={increment}>
  jared count is {count}
</button>

<style>
  button {
    border: 2px solie black;
    color: red;
    font-family: Arial;
  }
</style>
