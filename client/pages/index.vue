<template>
  <div>
    <div v-if="$auth.loggedIn">
      <p>Welcome logged in user!</p>
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
      title: "Home"
    };
  },
};
</script>
