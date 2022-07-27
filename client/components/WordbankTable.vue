<template>
  <div class="overflow-x-auto">
    <table class="table table-fixed table-compact w-full">
      <thead>
        <tr>
          <th></th>
          <th>Word Lemma</th>
          <th class="w-1/3 whitespace-normal">Definition</th>
          <th>Translation</th>
          <th># of Times Seen</th>
          <th>Rank</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody class="text-center">
        <tr v-for="(word, index) in words" :key="word.lemma">
          <th>{{ word.index + 1 }}</th>
          <td>{{ word.lemma }}</td>
          <!-- Todo: figure out wrapping -->
          <td class="w-1/3 whitespace-normal">
            <div tabindex="0" class="collapse collapse-arrow" @click="fetchDefinition(word)">
              <div class="collapse-title font-bold">
                Reveal
              </div>
              <div class="collapse-content">
                <p>{{ word.definition }}</p>
              </div>
            </div>
          </td>
          <td>{{ word.translation }}</td>
          <td>{{ word.number_of_times_seen }}</td>
          <td>{{ word.lemma_rank }}</td>
          <td>
            <button class="btn btn-circle btn-outline btn-xs btn-accent" @click="deleteWord(word.lemma)">
              <!-- delete the userword association for this lemma and this user (includes times seen) -->
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="btn-group justify-center gap-x-0.5 mt-4">
      <button class="btn btn-sm" :class="currentPage <= 1 ? 'btn-disabled' : ''"
        @click="renderWordbank(currentPage - 1)">«</button>
      <button class="btn w-1/3 btn-sm">Page {{ currentPage }}</button>
      <button class="btn btn-sm" :class="currentPage === Math.ceil(totalElements / 20) ? 'btn-disabled' : ''"
        @click="renderWordbank(currentPage + 1)">»</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      words: [],
      currentPage: 1,
      totalElements: 20, // set from backend
    }
  },
  async fetch() {
    // NOTE: have to use fetch() when not in a page
    // and also have to use `this.` when using fetch
    if (this.$auth.loggedIn) {
      const authToken = this.$auth.strategies.cookie.token.$storage._state["_token.cookie"];
      const response = await this.$axios.get("/api/fetch-wordbank", {
        params: {
          page: this.currentPage,
        },
        headers: {
          Authorization: authToken,
        },
      })
      this.words = response.data.words;
      this.totalElements = response.data.total_elements;
    }
  },
  methods: {
    async deleteWord(lemma) {
      await this.$axios.delete("/api/delete-word", {
        data: { lemma: lemma }
      });

      // if we deleted the last word, go back to the previous page
      if ((this.totalElements - 1) % 20 === 0) {
        this.renderWordbank(this.currentPage - 1);
      } else {
        this.renderWordbank(this.currentPage);
      }

      this.renderWordbank(this.currentPage);
    },
    async renderWordbank(page = 1) {
      // rerender wordbank whenever this runs (as only 20 words are received from server)
      const authToken = this.$auth.strategies.cookie.token.$storage._state["_token.cookie"];
      const response = await this.$axios.get("/api/fetch-wordbank",
        {
          params: {
            page: page,
          },
          headers: {
            Authorization: authToken,  // usually not required, just because called from fetch()
          },
        }
      );

      this.words = response.data.words;
      this.totalElements = response.data.total_elements;
      this.currentPage = page;
    },
    async fetchDefinition(word) {
      // fetch from https://dictionaryapi.dev/
      var definition;
      try {
        const response = await this.$axios.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word.lemma);

        // get the first definition
        definition = response.data[0].meanings[0].definitions[0].definition;
      } catch {
        definition = "No definition found.";
      }

      // update the word with the definition
      this.words = this.words.map(w => {
        if (w.lemma === word.lemma) {
          w.definition = definition;
        }
        return w;
      });
    }
  }
}
</script>

<style>
.table-fixed td,
.table-fixed th {
  padding: 1rem
    /* 16px */
  ;
  vertical-align: middle;
  white-space: normal;
  text-align: center;
}
</style>
