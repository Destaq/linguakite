<template>
  <div>
    <div v-for="(text, index) in texts" :key="index">
      <div class="card w-4/5 mx-auto bg-base-100 shadow-xl">
        <div class="card-body grid grid-cols-8 px-6 py-4">
          <div class="col-span-7 mr-8">
            <h2 class="card-title underline mb-2">{{ text.title }}</h2>
            <p>{{ text.content_preview }}</p>
            <p class="mt-2">
              <span v-for="tag in text.tags.slice(0, 10)" :key="index" class="text-accent text-sm font-light">
                #{{ tag.toLowerCase() }}&nbsp;
              </span>
            </p>
          </div>
          <div class="card-actions justify-end col-span-1 my-auto">
            <label :for="'my-modal-' + index" class="btn modal-button btn-primary"
              @click="fetchSpecificDetails(text.id)">
              More Details
            </label>
            <input type="checkbox" :id="'my-modal-' + index" class="modal-toggle" />
            <label :for="'my-modal-' + index" class="modal cursor-pointer">
              <label class="modal-box relative max-w-none" for="">
                <h3 class="text-lg font-bold text-neutral"> {{ specificTextDetails.title }}</h3>
                <p class="font-semibold text-accent">{{ specificTextDetails.percentage_known }}% of words known</p>
                <div class="grid grid-cols-4 gap-x-2">
                  <p class="py-4 col-span-3 whitespace-pre-line">{{ specificTextDetails.bigContentPreview }}</p>
                  <div class="mx-auto py-4">
                    <span class="font-bold">{{ specificTextDetails.total_words }}</span><span class="font-normal">
                      total words</span><br>
                    <span class="font-bold">{{ specificTextDetails.unique_words }}</span><span class="font-normal">
                      unique words</span><br>
                    <span class="font-bold">{{ specificTextDetails.average_word_length }}</span><span
                      class="font-normal"> avg. chars/word</span><br>
                    <span class="font-bold">{{ specificTextDetails.average_sentence_length }}</span><span
                      class="font-normal"> avg. words/sentence</span><br>
                  </div>
                </div>
                <div class="grid grid-cols-4 gap-x-2">
                  <a :href="specificTextDetails.url" class="italic font-extralight text-secondary link col-span-3">An
                    article by {{ specificTextDetails.authors }}, published {{ specificTextDetails.date }}</a>
                  <NuxtLink class="btn btn-secondary btn-sm w-1/2 -mt-1.5 mx-auto"
                    :to="'/read/' + specificTextDetails.id">Read</NuxtLink>
                </div>
              </label>
            </label>
          </div>
        </div>
      </div>
      <div class="btn-group justify-center gap-x-0.5 mt-4">
        <button class="btn w-2/5 btn-sm" @click="loadTextbank('', 'No Limit', [], 'or', 0, 20000)">Load More</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      texts: [
        // {
        //   title: "", // max # of characters here too
        //   content_preview: "", // max # of characters here + ..., done serverside
        //   id: 1234,
        //   tags: []
        // }
      ],
      specificTextDetails: {
        id: -1, // used for the /read/:id route
        title: "",
        bigContentPreview: ``,
        url: "",
        authors: "",
        date: "",
        unique_words: 0,
        total_words: 0,
        average_sentence_length: 0.000,
        average_word_length: 0.000,
        percentage_known: 0.000  // calculated server-side, not based on unique words!
      }
    }
  },
  async fetch() {
    // NOTE: have to use fetch() when not in a page
    // and also have to use `this.` when using fetch
    if (this.$auth.loggedIn) {
      const authToken = this.$auth.strategies.cookie.token.$storage._state["_token.cookie"];
      const response = await this.$axios.get("/api/fetch-textbank", {
        params: {
          titleSearchString: "",
          difficultyType: "No Limit",
          tags: [],
          and_or_or: "or",
          minWordLength: 0,
          maxWordLength: 20000,
          usedIds: this.texts.map(text => text.id),
        },
        headers: {
          Authorization: authToken,
        },
      })
      this.texts = response.data.texts;
    }
  },
  methods: {
    clearTextbank() {
      this.texts = [];
    },
    async loadTextbank(titleSearchString, difficultyType, tags, and_or_or, minWordLength, maxWordLength) {
      // rerender textbank whenever this runs (as only 20 texts are received from server)
      const authToken = this.$auth.strategies.cookie.token.$storage._state["_token.cookie"];
      const response = await this.$axios.get("/api/fetch-textbank",
        {
          params: {
            titleSearchString: titleSearchString,
            difficultyType: difficultyType,
            tags: tags,
            and_or_or: and_or_or,
            minWordLength: minWordLength,
            maxWordLength: maxWordLength,
            usedIds: this.texts.map(text => text.id)
          },
          // headers: {
          //   Authorization: authToken,  // usually not required, just because called from fetch()
          // },
        }
      );

      this.texts = response.data.texts;
    },
    async fetchSpecificDetails(id) {
      const response = await this.$axios.get("/api/fetch-text-details",
        {
          params: {
            id: id,
          },
        }
      );

      // update specificTextDetails
      this.specificTextDetails = response.data.textDetails;
    }
  }
}
</script>
