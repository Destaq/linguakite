<template>
  <div>
    <form @submit.prevent="getQuiz"
      class="w-4/5 mx-auto border shadow-md rounded-none p-4 bg-gray-100 grid gap-y-2 items-center mb-4"
      v-if="loaded === true">
      <h2 class="font-semibold text-lg mx-auto -mb-1">Quiz Generator</h2>
      <div class="grid grid-cols-2 gap-x-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text text-gray-700">Number of Questions</span>
          </label>
          <input type="number" v-model="numberOfQuestions" placeholder="10" class="input input-bordered rounded-none" />
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">Chosen Article</span>
          </label>
          <select class="select select-bordered rounded-none" v-model="chosenArticle">
            <option v-for="article in userLibrary" :key="article.id" :value="article.id">{{ article.title }}</option>
          </select>
        </div>
      </div>

      <!-- question types -->
      <div class="form-control grid grid-cols-4 w-full gap-x-6 mt-2">
        <label class="label cursor-pointer bg-white px-4 border">
          <span class="label-text">Multiple Choice</span>
          <input type="checkbox" v-model="desiredQuestionTypes['Multiple Choice']" class="checkbox checkbox-primary" />
        </label>
        <label class="label cursor-pointer bg-white px-4 border">
          <span class="label-text">Order Words</span>
          <input type="checkbox" v-model="desiredQuestionTypes['Order Words']" class="checkbox checkbox-primary" />
        </label>
        <label class="label cursor-pointer bg-white px-4 border">
          <span class="label-text">Order Sentences</span>
          <input type="checkbox" v-model="desiredQuestionTypes['Order Sentences']" class="checkbox checkbox-primary" />
        </label>
        <label class="label cursor-pointer bg-white px-4 border">
          <span class="label-text">Define</span>
          <input type="checkbox" v-model="desiredQuestionTypes['Define']" class="checkbox checkbox-primary" />
        </label>
      </div>

      <!-- submit -->
      <button class="btn btn-secondary btn-sm w-full mt-4 rounded-none" type="submit">Generate</button>
    </form>
    <PracticePuzzle v-for="(puzzle, index) in puzzles" :puzzle="puzzle" :puzzleNumber="index + 1" :key="index" :checkIt="checkIt" :puzzleIndex="index" />

    <div class="w-full items-center flex mt-4">
      <button class="btn btn-accent btn-sm w-4/5 rounded-none mx-auto items-center" @click="checkAnswers">Check
        Answers</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      numberOfQuestions: 10,
      userLibrary: [],
      chosenArticle: -1,
      desiredQuestionTypes: {
        "Multiple Choice": true,
        "Order Words": true,
        "Order Sentences": true,
        "Define": true
      },
      puzzles: [],
      loaded: false,
      checkIt: false,
    }
  },
  head() {
    return {
      title: 'Practice'
    }
  },
  async fetch() {
    const authToken = this.$auth.strategies.cookie.token.$storage._state["_token.cookie"];
    const response = await this.$axios.get("/api/get-user-library", {
      headers: {
        Authorization: authToken !== undefined ? authToken : "",
      },
    });

    this.userLibrary = response.data.user_library;

    this.userLibrary.push({
      id: -1,
      title: "Random Article"
    })

    this.chosenArticle = this.userLibrary[0].id;
    this.loaded = true;
  },
  methods: {
    async getQuiz() {
      this.checkIt = false;
      var input_types = [];
      for (var key in this.desiredQuestionTypes) {
        if (this.desiredQuestionTypes[key]) {
          input_types.push(key);
        }
      }

      const response = await this.$axios.post("/api/fetch-quiz", {
        n: this.numberOfQuestions,
        input_types: input_types,
        text_id: this.chosenArticle,
      })

      this.puzzles = response.data.puzzles;
    },
    async checkAnswers() {
      await this.$axios.post("/api/update-quizzes-done");
      
      this.checkIt = true;
    }
  }
}
</script>

<style scoped>
.select:focus {
  /* make same outline as input */
  outline: 1px solid hsla(var(--bc) / 0.2);
  outline-offset: 0px;
}
</style>
