<template>
  <div class="card w-4/5 p-4 mx-auto font-serif my-2 border rounded-none" :class="computedBackground">
    <p class="font-semibold">#{{ puzzleNumber }}:&nbsp; {{ puzzle["type"] }}</p>
    <div v-if="puzzle['type'] === 'Order Words'" class="ml-12 italic">
      <p>{{ puzzle['context'] }}</p>
    </div>
    <div v-if="puzzle['type'] === 'Order Words' || puzzle['type'] === 'Order Sentences'">
      <ol class="list-decimal">
        <li v-for="(element, index) in puzzle['question']" :key="index" class="ml-12">
          {{ element }}
        </li>
      </ol>
    </div>
    <div v-else>{{ puzzle["question"] }}</div>
    <div v-if="puzzle['type'] === 'Multiple Choice'">
      <div class="grid grid-cols-4 gap-x-2 form-control">
        <div v-for="(option, index) in puzzle['options']" :key="index">
          <label class="label w-2/3 mx-auto cursor-pointer border-secondary mt-2" :class="userAnswer === option ? 'font-bold underline' : ''">
            <input type="radio" :value="option" class="invisible w-0" v-model="userAnswer" />
            <span class="label-text mx-auto">{{ option }}</span>
          </label>
        </div>
      </div>
    </div>
    <div v-else-if="puzzle['type'] === 'Define'">
      <input type="text" class="input w-full input-sm mt-2 input-bordered rounded-none"
        :placeholder="'This can be defined as...'">
    </div>
    <div v-else>
      <input type="text" class="input w-full input-sm mt-2 input-bordered rounded-none" v-model="userAnswer"
        placeholder="1234...">
    </div>

    <div v-if="checkIt">
      <p class="font-medium mt-3 ml-0.5 text-sm">
        Answer <span v-if="puzzle['type'] === 'Define'">(check manually)</span>: {{ puzzle['answer'] }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userAnswer: "",
      answerCorrect: false,
    }
  },
  props: ["puzzle", "puzzleNumber", "checkIt"],
  computed: {
    computedBackground() {
      if (this.checkIt) {
        if (this.puzzle['type'] === 'Multiple Choice') {
          if (this.puzzle['answer'] === this.userAnswer) {
            return "bg-green-200"
          } else {
            this.answerCorrect = false;
            return "bg-red-200"
          }
        } else if (this.puzzle['type'] === 'Order Words' || this.puzzle['type'] === 'Order Sentences') {
          if (this.puzzle['answer'] === this.userAnswer) {
            return "bg-green-200"
          } else {
            this.answerCorrect = false;
            return "bg-red-200"
          }
        } else {
          return "bg-yellow-100"
        }
      } else {
        return "bg-yellow-100"
      }
    }
  }
}
</script>
