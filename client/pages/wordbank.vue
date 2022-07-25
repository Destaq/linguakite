<template>
  <div>
    <div class="flex w-full">
      <!-- (frequency estimate) -->
      <form class="grid form-control w-full" @submit.prevent="uploadVocabEstimate">
        <div class="flex items-end">
          <input type="number" placeholder="3000" class="input input-bordered flex-1 mr-2" v-model="vocabEstimate" />
          <input class="btn" type="submit" value="Go" />
        </div>
        <div class="mt-1 text-sm text-gray-500">
          Upload an estimate of your English vocab size (via a tool such as
          <a href="https://mikeinnes.io/2022/02/26/vocab" class="link link-primary" target="_blank">this</a>).
          <span class="label-text">
            <span class="tooltip tooltip-right cursor-pointer"
              data-tip="We'll use this to populate your wordbank automatically.">
              <span class="italic text-gray-500">(Why?)</span>
            </span>
          </span>
        </div>
      </form>

      <div class="divider divider-horizontal">OR</div>

      <!-- (upload wordlist) -->
      <form class="grid form-control w-full my-8" @submit.prevent="uploadWordList">
        <div class="flex">
          <input
            class="block w-full cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 focus:outline-none focus:border-transparent text-sm rounded-lg flex-1 mr-2"
            aria-describedby="user_help" id="user_avatar" type="file">
          <input type="submit" class="btn" />
        </div>
        <div class="mt-1 text-sm text-gray-500" id="user_help">You can also upload a newline separated <span
            class="text-xs font-mono">.txt</span> file of your known words.</div>
      </form>
    </div>

    <!-- (wordbank table) -->
    <WordbankTable ref="wordbankTable" class="mt-4" />
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: "Wordbank",
    };
  },
  data() {
    return {
      vocabEstimate: null,
      singleWord: null,
    }
  },
  methods: {
    async uploadVocabEstimate() {
      await this.$axios.post("/api/update-vocab-estimate", {
        vocab_size: this.vocabEstimate,
      });
      this.vocabEstimate = null;

      this.$refs.wordbankTable.renderWordbank(1);
    },
    async uploadWordList() {
      await this.$axios.post("/api/upload-vocab-file", {
        vocab_size: this.vocabEstimate,
      });
      this.vocabEstimate = null;

      this.$refs.wordbankTable.renderWordbank(1);
    }
  }
}
</script>

<style>
input[type=file]::-webkit-file-upload-button,
input[type=file]::file-selector-button {
  @apply text-white bg-gray-700 font-medium text-sm cursor-pointer border-0 py-3.5 pl-8 pr-4;
  margin-inline-start: -1rem;
  margin-inline-end: 1rem;
}
</style>
