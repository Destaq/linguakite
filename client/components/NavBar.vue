<template>
  <div class="navbar bg-base-100 border-b">
    <div class="navbar-start">
      <div class="dropdown">
        <label tabindex="0" class="btn btn-ghost lg:hidden" v-if="$auth.loggedIn">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
          </svg>
        </label>
        <ul tabindex="0" class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
          v-if="$auth.loggedIn">
          <li>
            <NuxtLink to="/database">Database</NuxtLink>
          </li>
          <li>
            <NuxtLink to="/wordbank">Wordbank</NuxtLink>
          </li>
          <li>
            <NuxtLink to="/practice">Practice</NuxtLink>
          </li>
        </ul>
      </div>
      <NuxtLink class="btn btn-ghost normal-case text-xl" to="/"><img src="/logo_transparent.svg" class="w-6"
          viewBox="0 0 24 24" /><span class="ml-3">LinguaKite</span></NuxtLink>
    </div>
    <div class="navbar-center hidden lg:flex" v-if="$auth.loggedIn">
      <ul class="grid grid-cols-3 menu menu-horizontal p-0">
        <li>
          <NuxtLink to="/database" class="mx-auto">Database</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/wordbank" class="mx-auto">Wordbank</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/practice" class="mx-auto">Practice</NuxtLink>
        </li>
      </ul>
    </div>
    <div class="navbar-end w-3/4 md:w-1/2">
      <!-- if not authenticated -->
      <div v-if="!$auth.loggedIn">
        <NuxtLink class="btn btn-sm mr-1 w-24" to="/register">Sign Up</NuxtLink>
        <NuxtLink class="btn btn-sm ml-1 w-24" to="/login">Log In</NuxtLink>
      </div>

      <!-- if authenticated -->
      <div v-else>
        <label for="custom-text-modal" class="btn modal-button btn-outline btn-sm mr-5">+</label>

        <!-- Put this part before </body> tag -->
        <input type="checkbox" id="custom-text-modal" class="modal-toggle" ref="modalToggle" />
        <label for="custom-text-modal" class="modal cursor-pointer font-serif">
          <label class="modal-box relative w-1/2 max-w-none" for="">
            <h3 class="text-lg font-bold text-center">Upload Private Text</h3>
            <form @submit.prevent="uploadPrivateText" class="form-control p-2 mt-2">
              <div class="grid grid-cols-2 gap-x-2"><input type="text"
                  placeholder="Breathing Oyxgen Linked to Staying Alive" v-model="title"
                  class="input input-bordered input-sm rounded-none">
                <input type="text" placeholder="Science, Chemistry, News" v-model="tags"
                  class="input input-bordered input-sm rounded-none">
              </div>
              <textarea class="textarea-sm textarea textarea-bordered mt-2 rounded-none" rows="10"
                placeholder="Revolutionary study suggests that the widespread element is highly beneficial towards human survival — a groundbreaking find that earned its discoverers a nomination for this year's Nobel Prize in Medicine. Published just this Monday, the journal sheds extraordinary light on..."
                v-model="content"></textarea>
              <button type="submit" class="btn btn-secondary btn-sm mt-2 rounded-none">
                Upload
              </button>
            </form>
          </label>
        </label>
        <button class="btn btn-sm btn-error w-28 mr-2" @click="logOut">
          Log Out
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: "",
      content: "",
      tags: "",
    }
  },
  methods: {
    logOut() {
      this.$auth.logout();
    },
    async uploadPrivateText() {
      if (this.title !== "" && this.content !== "") {
        await this.$axios.post("/api/add-private-text", {
          title: this.title,
          content: this.content,
          url: "",
          authors: this.$auth.user,
          tags: this.tags.split(",").map(tag => tag.trim()),
        });

        // clear data
        this.title = "";
        this.content = "";
        this.tags = "";

        // close page
        this.$refs.modalToggle.checked = false;
      }
    }
  }
};
</script>
