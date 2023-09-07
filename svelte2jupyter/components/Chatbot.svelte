<script>
  // import { onMount } from "svelte";
  import { select } from "d3-selection";
  import { writable } from "svelte/store";

  export let feedback = false;
  export let port = "https://0.0.0.0:8000";

  const chatLog = writable([]);

  let mymessage = "";
  let messageplaceholder = "";
  let chatLoading = false;

  // onMount(() => {
  //   getDataFromDB();
  // });

  // async function getDataFromDB() {
  //   const response = await fetch(`${port}/chat/qa_table/retrieve`);
  //   const data = await response.json();
  //   const dbRows = data["rows"];
  //   const formattedRows = dbRows.map((row) => ({
  //     id: row[0],
  //     question: row[1],
  //     answer: row[2],
  //     vote_status: row[3],
  //   }));
  //   $chatLog = [...formattedRows];
  // }

  const askModel = async (event) => {
    event.preventDefault(); // Prevents page refresh
    mymessage = messageplaceholder;
    messageplaceholder = "";
    chatLoading = true;
    let currentEntry = {
      id: $chatLog.length + 1,
      question: mymessage,
      answer: "Loading...",
      vote_status: "na",
    };
    $chatLog = [...$chatLog, currentEntry];

    const response = await fetch(`${port}/chatJupyter/${mymessage}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: mymessage,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      currentEntry["answer"] = data["answer"];
      chatLog.update((state) => {
        state[state.length - 1] = currentEntry;
        return state;
      });
    } else {
      const err = await response.text();
      alert(err);
    }
    chatLoading = false;
  };

  function scrollToView(node) {
    setTimeout(() => {
      node.scrollIntoView({ behavior: "smooth" });
    }, 0);
  }

  let dotState = 0;

  setInterval(() => {
    dotState = (dotState + 1) % 4;
  }, 200);

  $: dots = ".".repeat(dotState).padEnd(3);

  async function insertVote(feedbackUpdate) {
    const response = await fetch("/chat/qa_table/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(feedbackUpdate),
    });

    if (response.ok) {
      console.log("response", response);
    } else {
      const err = await response.text();
      alert(err);
    }
  }

  function logVote(event, vote, index) {
    const messageLog = $chatLog[index];
    messageLog.vote = vote;
    const feedbackUpdate = {
      id: index + 1, // increment bc sqlite 1-indexed
      vote_status: vote,
    };

    insertVote(feedbackUpdate);

    select(event.currentTarget.parentNode)
      .selectAll("button")
      .style("border", "3px solid transparent")
      .style("opacity", 0.65);
    select(event.currentTarget)
      .style("border", "3px solid var(--black)")
      .style("opacity", 1);
  }
</script>

<div class="ranked-feedback-container">
  <div class="ranked-chat">
    <section class="chatbox">
      <div class="chat-log">
        {#each $chatLog as message, index (index)}
          <div
            class="chat-message"
            use:scrollToView={index === $chatLog.length - 1}
          >
            <div class="chat-message-center">
              <div class="avatar">
                <!-- <img src={logo} alt="SvelteKit" /> -->
              </div>
              <div class="message-content">
                <div class="question">
                  <h5 class="bold">Question:</h5>
                  <p>{message.question}</p>
                </div>
                <div class="answers">
                  <div class="answer">
                    <h5 class="bold">Response:</h5>
                    <p>{message.answer}</p>
                    <!-- {#if feedback}
                      <div class="feedback-buttons">
                        <button
                          on:click={(event) => logVote(event, "up", index)}
                          class="small-button thumbs-up">up</button
                        >
                        <button
                          on:click={(event) => logVote(event, "down", index)}
                          class="small-button thumbs-down">down</button
                        >
                      </div>
                    {/if} -->
                  </div>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </section>
    <div class="chat-input-holder">
      <form on:submit={askModel} class="chat-input-form">
        <input
          bind:value={messageplaceholder}
          class="chat-input-textarea"
          placeholder="Type Question Here"
        />
        <button
          class="btnyousend {messageplaceholder === '' ? '' : 'active'}"
          type="submit">{chatLoading ? dots : "Send"}</button
        >
      </form>
      <p class="message">Note - may produce inaccurate information.</p>
    </div>
  </div>
</div>

<style>
      :root {
  /* colors */
  --green: #00ebc7;
  --red: #FF5470;
  --yellow: #fde24f;
  --black: #1b2d45;
  --darkBlue: #00214d;
  --darkGrey: #222;
  --grey: #bfbfbf;
  --lightGrey: #f2f4f6;
  --white: white;
  
  /* color intentions */
  --primary: var(--yellow);
  --danger: var(--red);
  --background: var(--white);
  --textColor: var(--black);
  --lineColor: var(--grey);
  --cardBg: var(--white);
  --headerBackground: var(--white);
  --footerBackground: var(--green);
  --footerTextColor: var(--black);
  --headerTextColor: var(--black);
  --buttonColor: var(--primary);
  --buttonTextColor: var(--textColor);
  --borderBottom: solid 2px var(--primary);
  
  
  
  /* Styles */
  --line: solid 1px var(--lineColor);
  
  /* Typography */
  --headingFont: 'Lato', monospace;
  --bodyFont: 'Work Sans', sans-serif;
  --baseFontSize: 100%;
  /* font sizes */
  --h1: 3.052em;
  --h2: 2.441em;
  --h3: 1.953em;
  --h4: 1.563em;
  --h5: 1.25em;
  --smallText: 0.8em;
  
  /* Elevation 1: base, 4: xl*/
  --shadow-s: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  
  /* Positioning */
  --containerPadding: 2.5%;
  --headerHeight: 3rem;
  /* --borderRadius: 10px; */
  --borderRadius: 0px;
  --height: height: calc(100vh - var(--headerHeight));
  
  /* Media Queries (not supported yet) */
  /* --xsmall: 340;
  --small: 500px;
  --med: 800;
  --large: 960;
  --wide: 1200; */
  
  }
    .small-button {
      margin-left: 10px;
      background: none;
      border: 3px solid transparent;
      color: inherit;
      padding: 6px 10px;
      cursor: pointer;
      box-shadow: none;
      font-size: var(--smallText);
    }
  
    .feedback-buttons {
      text-align: center;
      margin: auto;
      width: 20%;
    }
  
    .small-button:hover {
      box-shadow: var(--shadow-md);
    }
  
    .thumbs-up,
    .thumbs-up:hover,
    .thumbs-up::selection {
      background: var(--green);
    }
    .thumbs-down,
    .thumbs-down:hover,
    .thumbs-down::selection {
      background: var(--red);
    }
    .ranked-chat {
      height: 100vh;
      display: grid;
      grid-template-columns: 100%;
      grid-template-rows: 80% 20%;
    }
  
    .message {
      font-size: var(--smallText);
      padding-left: 40px;
      padding-right: 40px;
      margin: 0 auto;
    }
  
    .chat-input-holder {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 24px;
      width: 100%;
      max-width: 640px;
      margin: auto;
    }
  
    .chat-input-textarea {
      background-color: var(--lightgrey);
      cursor: pointer;
      width: 100%;
      border-radius: 5px;
      border: var(--line);
      border-color: none;
      margin: 12px;
      outline: none;
      padding: 12px;
      color: var(--black);
      font-size: var(--baseFontSize);
      box-shadow: var(--shadow-md);
      flex: 3;
      border-radius: 0px;
      border-right: 0px;
    }
  
    .chat-input-form {
      display: flex;
      width: 100%;
    }
  
    .btnyousend {
      border-radius: 0px;
      margin-top: 12px;
      margin-bottom: 12px;
      margin-left: -15px;
      background: var(--primary);
      color: var(--black);
      opacity: 0.5;
      transition: all 0.3s;
    }
  
    .active {
      opacity: 1;
    }
  
  
    .bold {
      font-weight: bold;
      font-size: var(--smallText);
      margin: 0;
      padding: 0;
    }
  
    .chatbox {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: calc(100vh - var(--headerHeight));
      background-color: var(--white);
      box-sizing: border-box;
      width: 95%;
      margin: auto;
      height: 100%;
    }
  
    .chat-log {
      flex: 1;
      overflow-y: auto;
      padding: 0 10px;
      box-sizing: border-box;
    }
  
    .chat-message {
      background-color: var(--white);
      border-bottom: var(--line);
      box-sizing: border-box;
    }
  
    .chat-message-center {
      display: flex;
      flex-direction: column;
      margin-left: auto;
      margin-right: auto;
      padding: 12px;
      box-sizing: border-box;
    }
  
    .message-content {
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
    }
  
    .message-content .question {
      text-align: left;
      border: 1px solid var(--grey);
      padding: 5px;
      /* margin-bottom: 10px; */
      background-color: var(--lightGrey);
    }
  
    .message-content .answer {
      display: inline-block;
      text-align: left;
      padding: 10px;
      border: 1px solid var(--black);
    }
  
    .message-content .answers {
      display: grid;
      grid-template-columns: 100%;
      gap: 0%;
      width: 100%;
      margin: auto;
    }
</style>
