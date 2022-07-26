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
        <button class="btn btn-square">+</button>
        <button class="btn btn-sm btn-error w-28" @click="logOut">
          Log Out
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    logOut() {
      this.$auth.logout();
    }
  }
};
</script>
