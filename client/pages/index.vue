<template>
  <div>
    <div v-if="$auth.loggedIn">
      <p>Welcome logged in user!</p>
      <button @click="sendReq" class="btn btn-sm">Test Server + Auth</button>
    </div>
    <div v-else>
      <p>Please sign up or log in...</p>
    </div>
    <p>Server: {{ output.message }}</p>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: "Home",
    };
  },
  data() {
    return {
      output: {
        message: "",
      },
    };
  },
  // async asyncData({ _route, _params, $axios, $auth }) {
  //   // NOTE: attempting to access a protected resource when unauthorized will not do anything
  //   let output = {
  //     message: "unauthorized",
  //   };
  //   // below is an example of how to make a request to the server on page load
  //   // if ($auth.loggedIn) {
  //   //   const authToken =
  //   //     $auth.strategies.cookie.token.$storage._state["_token.cookie"];
  //   //   output = await $axios.$get("/api/auth/test", {
  //   //     headers: {
  //   //       Authorization: authToken,
  //   //     },
  //   //   });
  //   // }
  //   // return { output }; // must be dict
  // },
  methods: {
    async sendReq() {
      // making an action like this will fire off the JWT cookie token update
      // just loading the page is not enough
      await this.$axios.get("/api/auth/test").then((res) => {
        this.output.message = res.data.message;
      });
    },
  },
};
</script>
