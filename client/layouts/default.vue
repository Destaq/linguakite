<template>
  <div class="flex min-h-screen flex-col">
    <NavBar class="top-0 z-50 sticky" />
    <Nuxt
      class="flex-grow px-4 sm:w-xl md:w-full lg:w-screen-xl my-4"
    />
  </div>
</template>

<script>
export default {
  head() {
    return {
      htmlAttrs: {
        "data-theme": "emerald"
      }
    };
  }
};
</script>

<style>
.input:focus {
  outline: 2px solid transparent;
  box-shadow: 0 0 0 0px hsl(var(--b1)),0 0 0 1px hsla(var(--bc)/.2);
}
</style>
