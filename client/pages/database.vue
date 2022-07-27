<template>
  <div>
    <div>
      <!-- search bar and search tools -->
      <form @submit.prevent="search" class="w-4/5 mx-auto border shadow-lg rounded-none p-4 bg-gray-100 grid grid-rows-4 gap-y-2 items-center">
        <!-- title search -->
        <div class="grid grid-cols-12 gap-x-4">
          <input type="text" placeholder="Some title..." class="input w-full col-span-6" v-model="titleSearch" />

          <!-- tag search -->
          <input type="text" placeholder="Covid-19, Birthday Party, Dogs" class="input w-full col-span-4"
            v-model="tagSearch" />
          <div class="grid grid-cols-2 col-span-2">
            <div class="flex items-center px-2 cursor-pointer">
              <input id="bordered-radio-1" type="radio" name="bordered-radio" class="radio radio-xs" v-model="tagType"
                value="or">
              <label for="bordered-radio-1"
                class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer select-none">Any</label>
            </div>
            <div class="flex items-center px-2 cursor-pointer">
              <input id="bordered-radio-2" type="radio" name="bordered-radio" class="radio radio-xs" value="and"
                v-model="tagType">
              <label for="bordered-radio-2"
                class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer select-none">All</label>
            </div>
          </div>
        </div>

        <!-- length ranges -->
        <div class="grid grid-cols-2 gap-x-6">
          <div class="grid grid-cols-7">
            <span class="w-11/12 text-sm text-center justify-center bg-gray-300 rounded-lg justify-self-start self-start">{{ minWords }}</span>
            <input type="range" min="0" :max="maxWords - 50" value="0" class="range range-sm col-span-6" step="50" v-model="minWords" />
          </div>
          <div class="grid grid-cols-7">
            <span class="w-11/12 text-sm text-center -ml-1 justify-center bg-gray-300 rounded-lg">{{ maxWords }}</span>
            <input type="range" min="50" max="20000" value="20000" class="range range-sm col-span-6" step="50" v-model="maxWords" />
          </div>
        </div>

        <!-- difficulty -->
        <div class="grid grid-cols-6 gap-x-2">
          <div class="flex items-center rounded border border-gray-200 hover:border-gray-300 px-2 cursor-pointer">
            <input id="radio-3" type="radio" name="bordered-radio" class="radio radio-xs" value="No Filter"
              v-model="difficulty">
            <label for="radio-3"
              class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">No Filter</label>
          </div>
          <div class="flex items-center rounded border border-gray-200 hover:border-gray-300 px-2 cursor-pointer">
            <input id="radio-4" type="radio" name="bordered-radio" class="radio radio-xs" value="Very Easy"
              v-model="difficulty">
            <label for="radio-4"
              class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">Very Easy</label>
          </div>
          <div class="flex items-center rounded border border-gray-200 hover:border-gray-300 px-2 cursor-pointer">
            <input id="radio-5" type="radio" name="bordered-radio" class="radio radio-xs" value="Easy"
              v-model="difficulty">
            <label for="radio-5"
              class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">Easy</label>
          </div>
          <div class="flex items-center rounded border border-gray-200 hover:border-gray-300 px-2 cursor-pointer">
            <input id="radio-6" type="radio" name="bordered-radio" class="radio radio-xs" value="Medium"
              v-model="difficulty">
            <label for="radio-6"
              class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">Medium</label>
          </div>
          <div class="flex items-center rounded border border-gray-200 hover:border-gray-300 px-2 cursor-pointer">
            <input id="radio-7" type="radio" name="bordered-radio" class="radio radio-xs" value="Hard"
              v-model="difficulty">
            <label for="radio-7"
              class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">Hard</label>
          </div>
          <div class="flex items-center rounded border border-gray-200 hover:border-gray-300 px-2 cursor-pointer">
            <input id="radio-8" type="radio" name="bordered-radio" class="radio radio-xs" value="Very Hard"
              v-model="difficulty">
            <label for="radio-8"
              class="py-4 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">Very Hard</label>
          </div>
        </div>

        <!-- submit -->
        <button class="btn btn-secondary btn-sm w-full" type="submit">Search</button>
      </form>
    </div>
    <!-- ############# -->
    <DatabaseTable ref="dbTable" class="pt-4" />
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: "Database",
    }
  },
  data() {
    return {
      titleSearch: "",
      tagSearch: "",
      minWords: 0,
      maxWords: 20000,
      tagType: "or",
      difficulty: "No Filter"
    };
  },
  methods: {
    search() {
      this.$refs.dbTable.loadTextbank(
        this.titleSearch,
        this.difficulty,
        this.tagSearch.split(",").map(tag => tag.trim()),
        this.tagType,
        this.minWords,
        this.maxWords,
        []
      );
    }
  },
  watch: {
    maxWords() {
      if (this.maxWords < this.minWords + 50) {
        this.minWords = this.maxWords - 50;
      }
    }
  }
}
</script>
