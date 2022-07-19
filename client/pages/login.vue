<template>
  <div class="bg-white font-family-karla h-screen text-black">
    <div class="w-full flex flex-wrap">
      <!-- Login Section -->
      <div class="w-full md:w-1/2 flex flex-col">
        <div
          class="flex justify-center md:justify-start pt-12 md:pl-12 md:-mb-24"
        >
          <NuxtLink to="/" class="bg-white text-black font-bold text-xl p-4">
            <img src="/logo_transparent.svg" class="w-6 mr-2 inline" />
            <span class="align-text-top"> SurgeLingo </span>
          </NuxtLink>
        </div>

        <div
          class="
            flex flex-col
            justify-center
            md:justify-start
            my-auto
            pt-8
            md:pt-0
            px-8
            md:px-24
            lg:px-32
          "
        >
          <p class="text-center text-3xl">Welcome.</p>
          <form class="flex flex-col pt-3 md:pt-8" @submit.prevent="logIn">
            <div class="alert alert-error" v-if="showLoginError">
              <div class="flex-1">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  class="w-6 h-6 mx-2 stroke-current"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"
                  ></path>
                </svg>
                <label>Email or password incorrect.</label>
              </div>
            </div>
            <div class="flex flex-col pt-4">
              <label for="email" class="text-lg">Email</label>
              <input
                type="text"
                id="email"
                placeholder="johndoe"
                v-model="email"
                class="
                  shadow
                  appearance-none
                  border
                  rounded
                  w-full
                  py-2
                  px-3
                  mt-1
                  leading-tight
                  focus:outline-none
                  focus:shadow-outline
                "
              />
            </div>

            <div class="flex flex-col pt-4">
              <label for="password" class="text-lg">Password</label>
              <input
                type="password"
                id="password"
                placeholder="Password"
                v-model="password"
                class="
                  shadow
                  appearance-none
                  border
                  rounded
                  w-full
                  py-2
                  px-3
                  mt-1
                  leading-tight
                  focus:outline-none
                  focus:shadow-outline
                "
              />
            </div>

            <input
              type="submit"
              value="Log In"
              class="
                bg-black
                text-white
                font-bold
                text-lg
                p-2
                mt-8
                cursor-pointer
              "
            />
          </form>
          <div class="text-center pt-12 pb-12">
            <p>
              Don't have an account?
              <NuxtLink to="/register" class="underline font-semibold"
                >Register here.</NuxtLink
              >
            </p>
          </div>
        </div>
      </div>

      <!-- Image Section -->
      <div class="w-1/2 shadow-2xl">
        <img
          class="object-cover w-full h-screen hidden md:block"
          src="https://images.unsplash.com/photo-1563723788237-3a0ad15dcdbe"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      showLoginError: false,
    };
  },
  head() {
    return {
      title: "Log In",
    };
  },
  methods: {
    async logIn() {
      try {
        await this.$auth.loginWith("cookie", {
          data: {
            email: this.email,
            password: this.password,
          },
        });
        this.$router.push("/");
      } catch (error) {
        console.log(error);
        this.showLoginError = true;
      }
    },
  },
};
</script>
