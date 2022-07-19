<template>
  <div class="flex min-h-screen flex-col">
    <NavBar class="top-0 z-50 sticky" />
    <Nuxt
      class="flex-grow px-4 sm:max-w-xl md:max-w-full lg:max-w-screen-xl mb-4 mt-2"
    />
  </div>
</template>

<script>
export default {
  head() {
    return {
      htmlAttrs: {
        "data-theme": "bumblebee"
      }
    };
  }
};
</script>
