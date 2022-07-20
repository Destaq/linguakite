<template>
  <div>
    <div v-if="$auth.loggedIn">
      <p>Welcome logged in user!</p>
      <button @click="sendReq" class="btn">Click Me!</button>
    </div>
    <div v-else>
      <p>Please sign up or log in...</p>
    </div>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: "Home",
    };
  },
  methods: {
    async sendReq() {
      await this.$axios.get("/api/auth/test");
    },
  },
};
</script>
