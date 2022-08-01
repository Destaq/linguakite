<template>
  <main class="flex flex-col font-serif" id="specialHeightViewport">
    <div class="flex flex-1 overflow-hidden">
      <div class="border rounded-lg px-4 flex bg-gray-50 w-4/5 mr-2">
        <div class="flex flex-1 flex-col">
          <div class="grid grid-cols-5 gap-x-2 border-b">
            <select class="select select-ghost w-full mx-auto italic font-medium p-0 focus:outline-none my-auto"
              v-model="simplificationType" @change="fetchContentAgain">
              <option>Original Text</option>
              <option>Summarized Text</option>
              <option>Synonymized Text</option>
            </select>
            <h2 class="text-xl font-bold col-span-3 text-center my-auto underline cursor-pointer">{{ title }}</h2>
            <svg v-if="ttsOn === false" xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 cursor-pointer my-auto place-self-end" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" stroke-width="2" @click="playPageTTS">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer my-auto place-self-end" fill="none"
              viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" v-else @click="stopPageTTS">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"
                clip-rule="evenodd" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
          </div>
          <div class="whitespace-pre-line fle flex-1 overflow-y-auto my-2" v-if="chunks.length !== 0">
            <span v-for="(word, index) in chunks[currentPage - 1]" :key="index">
              <span :class="wordStyling(word)" class="cursor-pointer" @click="wordClicked(word)"
                :data-end="word.word[0]" v-if="index === 0 && currentPage > 1">{{ word.word.slice(2, word.word.length)
                }}</span>
              <span :class="wordStyling(word)" class="cursor-pointer" @click="wordClicked(word)"
                :data-end="word.word[0]" v-else>{{ word.word.slice(1, word.word.length) }}</span>
            </span>
          </div>

          <button type="button" class="flex-1" v-else disabled>
            <svg class="inline mr-2 w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
              viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor" />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill" />
            </svg>
          </button>

          <div class="flex border-t rounded-none w-full">
            <div class="btn-group w-full mx-auto grid grid-cols-12 mt-1 gap-x-0.5">
              <button class="btn btn-sm col-span-1" :class="currentPage <= 1 ? 'btn-disabled' : ''"
                @click="updateProgress(-1)" v-if="chunks.length > 1 && currentPage <= chunks.length">«</button>
              <button
                v-if="(chunks.length === 1 && currentPage <= chunks.length) || (currentPage === chunks.length && currentPage <= chunks.length)"
                class="btn btn-sm w-full" :class="chunks.length === 1 ? 'col-span-12' : 'col-span-10'"
                @click="updateProgress(1)">Mark
                Complete</button>
              <button v-if="currentPage > chunks.length && fetchFinished === true" class="btn btn-sm w-full col-span-12"
                @click="updateProgress(-1)">
                Relearn Article
              </button>
              <button class="btn col-span-10 btn-sm text-center" v-if="chunks.length > currentPage">Page {{ currentPage
              }}</button>
              <button class="btn btn-sm col-span-1" :class="currentPage === chunks.length ? 'btn-disabled' : ''"
                @click="updateProgress(1)" v-if="chunks.length > 1 && currentPage <= chunks.length">»</button>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-col bg-gray-50 w-1/5 p-4 rounded-lg border">
        <div class="w-full border-b mt-1 h-min">
          <h3 class="text-lg font-semibold mx-auto text-center -mt-1.5">Help</h3>
          <div class="h-1.5"></div>
        </div>
        <div class="grid grid-rows-3 h-full">
          <div class="row-span-2 mt-2">
            <p>{{ clickedWord }}<span v-if="clickedWordTranslation !== ''"> — {{ clickedWordTranslation }}</span><span
                v-if="clickedWordRank !== ''"> — #{{ clickedWordRank }}</span></p>
            <p class="italic font-light mt-2">{{ clickedWordDefinition }}</p>
            <button class="btn btn-secondary btn-xs rounded-sm w-full mt-4" @click="getPronunciation"
              v-if="clickedWord !== ''">Pronunciation</button>
            <button class="btn btn-accent btn-xs rounded-sm w-full mt-2" @click="toggleWord"
              v-if="clickedWord !== ''">Mark as&nbsp;<span v-if="known === false">known</span><span
                v-else>unknown</span></button>
          </div>
          <blockquote class="relative p-4 border-t items-center text-md italic text-neutral-600 border-neutral-500">
            <p class="mb-4">{{ quoteData.q }}</p>
            <cite class="flex items-center">
              <div class="flex flex-col items-start">
                <span class="mb-1 text-sm italic font-bold">{{ quoteData.a }}</span>
              </div>
            </cite>
            <p class="text-2xs absolute bottom-0">Quote provided by <a href="https://zenquotes.io/" target="_blank"
                class="link">ZenQuotes API</a></p>
          </blockquote>
        </div>
      </div>
    </div>
  </main>
</template>


<script>
export default {
  data() {
    return {
      title: "",
      content: "",
      ttsOn: false,
      simplificationType: "Original Text",
      clickedWord: "",
      clickedWordLemma: "",
      clickedWordTranslation: "",
      clickedWordDefinition: "",
      clickedWordRank: "",
      known: false,
      chunks: [],
      currentPage: 1,
      synth: null,
      startDate: null,
      elapsedTime: 0,
      fetchFinished: false,
      quoteData: {
        q: "Show me a family of readers, and I will show you the people who move the world.",
        a: "Napoleon Bonaparte"
      } // inspirational quote on bottom right
    }
  },
  head() {
    return {
      title: this.title,
    }
  },
  mounted() {
    // https://stackoverflow.com/a/41480142/12876940
    // https://stackoverflow.com/questions/56550164/how-can-i-mimic-onbeforeunload-in-a-vue-js-2-application

    this.startDate = new Date();

    window.addEventListener('beforeunload', this.logReadingTime);
    window.addEventListener('focus', this.focusFunc);
    window.addEventListener('blur', this.blurFunc);
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.logReadingTime);
    window.removeEventListener('focus', this.focusFunc);
    window.removeEventListener('blur', this.blurFunc);
  },
  beforeRouteLeave(_to, _from, next) {
    this.logReadingTime();
    next();
  },
  async fetch() {
    const authToken = this.$auth.strategies.cookie.token.$storage._state["_token.cookie"];
    const response = await this.$axios.get("/api/read-text", {
      params: {
        id: this.$route.params.id,
        type: this.simplificationType
      },
      headers: {
        Authorization: authToken,
      },
    });

    this.title = response.data.title;
    this.content = response.data.content;
    this.currentPage = parseInt(response.data.start_page);

    // NOTE: quite heavy free rate limiting
    // also fetch from Zen Quotes API
    try {
      const quoteResponse = await this.$axios.get("https://zenquotes.io/api/random");
      this.quoteData = quoteResponse.data[0];
    } catch {
      // still being rate limited
    }

    this.splitContentToChunks();
  },
  methods: {
    async logReadingTime() {
      const endDate = new Date();
      const spentTime = endDate.getTime() - this.startDate.getTime();
      this.elapsedTime += spentTime;

      // send api call to log reading time
      await this.$axios.post("/api/log-time", {
        elapsed_time: this.elapsedTime,
      });
    },
    focusFunc() {
      this.startDate = new Date();
    },
    blurFunc() {
      const endDate = new Date();
      const spentTime = endDate.getTime() - this.startDate.getTime();
      this.elapsedTime += spentTime;
    },
    async fetchContentAgain() {
      this.fetchFinished = false;
      this.chunks = [];  // to show loading button again

      const response = await this.$axios.get("/api/read-text", {
        params: {
          id: this.$route.params.id,
          type: this.simplificationType
        },
      });

      this.title = response.data.title;
      this.content = response.data.content;
      this.currentPage = parseInt(response.data.start_page);

      this.splitContentToChunks();
    },
    getPronunciation() {
      let sound = new SpeechSynthesisUtterance(this.clickedWord);
      sound.lang = 'en-US';
      window.speechSynthesis.speak(sound);
    },
    async wordClicked(word) {
      var wordNoPunc = word.word.replace(/[.,\/#!$%\^&\*;:{}=\_`~()\"\'\“]/g, "")

      // also if ’ in wordNoPunc, remove it and anything after it
      if (wordNoPunc.includes("’")) {
        wordNoPunc = wordNoPunc.split("’")[0];
      }

      this.clickedWord = wordNoPunc.toLowerCase();
      this.clickedWordLemma = word.lemma;
      this.clickedWordRank = word.rank >= 60000 ? "60 000+" : word.rank;
      this.known = word.known;

      try {
        const response = await this.$axios.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + wordNoPunc);

        // get the first definition
        this.clickedWordDefinition = response.data[0].meanings[0].definitions[0].definition;
      } catch {
        this.clickedWordDefinition = "No definition found.";
      }

      // now do translation via deepl key (this.$config.deeplSecret)
      const response2 = await this.$axios.get(`/api/get-translation?word=${wordNoPunc}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        });

      this.clickedWordTranslation = response2.data.translation;

    },
    async toggleWord() {
      await this.$axios.post("/api/update-word-status", {
        word: this.clickedWord.trim(),
        word_lemma: this.clickedWordLemma.trim(),
        known: this.known,
      });
      this.known = !this.known;

      // go through all chunks and update those words with the same lemma
      this.chunks.forEach(chunk => {
        chunk.forEach(word => {
          if (word.lemma === this.clickedWordLemma) {
            word.known = this.known;
          }
        });
      });
    },
    playPageTTS() {
      // play tts for current page (chunk map)
      this.ttsOn = true;
      let tts = "";
      for (let i = 0; i < this.chunks[this.currentPage - 1].length; i++) {
        tts += this.chunks[this.currentPage - 1][i].word + " ";
      }
      this.synth = new SpeechSynthesisUtterance(tts);
      this.synth.lang = 'en-US';
      window.speechSynthesis.speak(this.synth);
      this.synth.addEventListener('end', () => {
        this.ttsOn = false;
      });
    },
    stopPageTTS() {
      window.speechSynthesis.cancel(this.synth);
      this.ttsOn = false;
    },
    async updateProgress(value) {
      this.currentPage += value;

      var pageToUpdateSend;

      if (this.currentPage > this.chunks.length) {
        // we've reached the end
        pageToUpdateSend = this.currentPage - 1;
      } else {
        // all clear, can parse chunks
        pageToUpdateSend = this.currentPage;
      }

      await this.$axios.post("/api/update-text-progress", {
        id: this.$route.params.id,
        page: this.currentPage,
        totalPages: this.chunks.length,
        chunkLemmas: this.chunks[pageToUpdateSend - 1].map(word => word.lemma),
      });
    },
    splitContentToChunks() {
      var words = this.content.map(e => e.word)


      var chunk = {}
      var chunk_group = [];
      var chunk_length = 0
      // iterate through word in words
      for (var i = 0; i < words.length; i++) {
        // update chunk length
        chunk_length += words[i].length + 1; // just forget serversid

        if (i > 1) {
          if (words[i - 1].charAt(words[i - 1].length - 1) === "." || words[i - 1].charAt(words[i - 1].length - 1) === "?" || words[i - 1].charAt(words[i - 1].length - 1) === "!") {
            // words[i] = words[i].replace(/[.,\/#!$%\^&\*;:{}=\_`~()\"\'\“]/g, "")
            // also capitalize

            if (words[i].charAt(0) === "\n" && this.simplificationType === "Synonymized Text") {
              words[i] = words[i].charAt(0) + words[i].charAt(1).toUpperCase() + words[i].slice(2);
            } else{
              words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
            }
          }
        }

        if (chunk_length > 2500 &&
          words[i].indexOf("\n") > -1
        ) {
          // if newline is at the back
          if (words[i].indexOf("\n") == words[i].length - 1) {
            chunk = {
              "word": " " + words[i].substring(0, words[i].length - 1) + "\n\n",
              "lemma": this.content[i].lemma,
              "known": this.content[i].known,
              "rank": this.content[i].rank
            }
            chunk_group.push(chunk);
            this.chunks.push(chunk_group);
            chunk_group = [];
            chunk_length = 0;
          } else {
            chunk = {
              "word": " " + words[i].substring(words[i].indexOf("\n"), words[i].length),
              "lemma": this.content[i].lemma,
              "known": this.content[i].known,
              "rank": this.content[i].rank
            }
            this.chunks.push(chunk_group);
            chunk_group = [];
            chunk_group.push(chunk);
            chunk_length = words[i].length + 1;
          }
          chunk = {};
        } else {
          // if chunk length is less than 1000, add word to chunk
          chunk = {
            "word": " " + words[i].replace("\n", "\n\n"),
            "lemma": this.content[i].lemma,
            "known": this.content[i].known,
            "rank": this.content[i].rank
          };
          chunk_group.push(chunk);
        }
      }


      // potentially append final
      if (chunk_length > 0) {
        this.chunks.push(chunk_group);
      }

      this.fetchFinished = true;
    },
    wordStyling(word) {
      let output = word.known ? 'bg-normal underline decoration-2' : 'bg-red-400 underline decoration-2';
      if (word.rank < 100) {
        output += " decoration-violet-900";
      } else if (word.rank < 250) {
        output += " decoration-sky-900";
      } else if (word.rank < 500) {
        output += " decoration-green-900";
      } else if (word.rank < 1000) {
        output += " decoration-lime-400"
      } else if (word.rank < 2500) {
        output += " decoration-yellow-700"
      } else if (word.rank < 5000) {
        output += " decoration-amber-800"
      } else if (word.rank < 10000) {
        output += " decoration-orange-800"
      } else if (word.rank < 25000) {
        output += " decoration-red-400"
      } else if (word.rank < 60000) {
        output += " decoration-pink-500"
      } else {
        output += " decoration-stone-800"
      }
      return output;
    }
  }
}
</script>

<style scoped>
#specialHeightViewport {
  height: 85vh;
}

.bg-red-400::after {
  @apply bg-gray-50;
  content: attr(data-end);
}

.bg-normal::after {
  content: attr(data-end);
}
</style>
