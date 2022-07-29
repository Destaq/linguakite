<template>
  <main class="flex flex-col font-serif" id="specialHeightViewport">
    <div class="flex flex-1 overflow-hidden">
      <div class="border rounded-lg px-4 flex bg-gray-50 w-4/5 mr-2">
        <div class="flex flex-1 flex-col">
          <div class="grid grid-cols-5 gap-x-2 border-b">
            <select class="select select-ghost w-full mx-auto italic font-medium p-0 focus:outline-none my-auto"
              v-model="simplification" @change="simplifyContent">
              <option>No Simplification</option>
              <option>Little Simplification</option>
              <option>Medium Simplification</option>
              <option>More Simplification</option>
              <option>Most Simplification</option>
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
          <p class="whitespace-pre-line fle flex-1 overflow-y-auto my-2">
            <span v-for="(word, index) in chunks[currentPage - 1]" :key="index">
              <span :class="wordStyling(word)" class="cursor-pointer" @click="wordClicked(word)"
                :data-end="word.word[0]" v-if="index === 0 && currentPage > 1">{{ word.word.slice(2, word.word.length)
                }}</span>
              <span :class="wordStyling(word)" class="cursor-pointer" @click="wordClicked(word)"
                :data-end="word.word[0]" v-else>{{ word.word.slice(1, word.word.length) }}</span>
            </span>
          </p>
          <div class="flex border-t rounded-none w-full">
            <div class="btn-group w-full mx-auto grid grid-cols-12 mt-1 gap-x-0.5">
              <button class="btn btn-sm col-span-1" :class="currentPage <= 1 ? 'btn-disabled' : ''"
                @click="updateProgress(-1)" v-if="chunks.length > 1">«</button>
              <button v-if="chunks.length === 1 || currentPage === chunks.length" class="btn btn-sm w-full"
                :class="chunks.length === 1 ? 'col-span-12' : 'col-span-10'">Mark Complete</button>
              <button class="btn col-span-10 btn-sm text-center" v-if="chunks.length > currentPage">Page {{ currentPage
              }}</button>
              <button class="btn btn-sm col-span-1" :class="currentPage === chunks.length ? 'btn-disabled' : ''"
                @click="updateProgress(1)" v-if="chunks.length > 1">»</button>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-col bg-gray-50 w-1/5 p-4 rounded-lg border">
        <div class="w-full border-b mt-1 h-min">
          <h3 class="text-lg font-semibold mx-auto text-center -mt-1.5">Help</h3>
          <div class="h-1.5"></div>
        </div>
        <div class="grid grid-rows-4 h-full">
          <div class="row-span-3 mt-2">
            <p>{{ clickedWord }}<span v-if="clickedWordTranslation !== ''"> — {{ clickedWordTranslation }}</span><span
                v-if="clickedWordRank !== ''"> — #{{ clickedWordRank }}</span></p>
            <p class="italic font-light mt-2">{{ clickedWordDefinition }}</p>
            <button class="btn btn-secondary btn-xs rounded-sm w-full mt-4" @click="getPronunciation"
              v-if="clickedWord !== ''">Pronunciation</button>
            <button class="btn btn-accent btn-xs rounded-sm w-full mt-2" @click="toggleWord"
              v-if="clickedWord !== ''">Mark as&nbsp;<span v-if="known === false">known</span><span
                v-else>unknown</span></button>
          </div>
          <div class="border-t items-center flex">
            <p class="text-xl font-semibold text-center mx-auto">{{ timerTime }}</p>
          </div>
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
      simplification: "No Simplification",
      timerTime: "02:25:53",
      clickedWord: "",
      clickedWordLemma: "",
      clickedWordTranslation: "",
      clickedWordDefinition: "",
      clickedWordRank: "",
      known: false,
      chunks: [],
      currentPage: 1,
      synth: null
    }
  },
  head() {
    return {
      title: this.title,
    }
  },
  async fetch() {
    const authToken = this.$auth.strategies.cookie.token.$storage._state["_token.cookie"];
    const response = await this.$axios.get("/api/read-text", {
      params: {
        id: this.$route.params.id,
      },
      headers: {
        Authorization: authToken,
      },
    });

    this.title = response.data.title;
    this.content = response.data.content;
    this.splitContentToChunks();
  },
  methods: {
    // TODO: timer (+ API call)
    simplifyContent() {
      // TODO
    },
    getPronunciation() {
      let sound = new SpeechSynthesisUtterance(this.clickedWord);
      sound.lang = 'en-US';
      window.speechSynthesis.speak(sound);
    },
    async wordClicked(word) {
      const wordNoPunc = word.word.replace(/[.,\/#!$%\^&\*;:{}=\_`~()]/g, "")

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
    }, // don't forget to toggle at end
    stopPageTTS() {
      window.speechSynthesis.cancel(this.synth);
      this.ttsOn = false;
    },
    updateProgress(value) {
      this.currentPage += value;

      // TODO: api call to update progress and times seen
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
