<template>
  <div class="bg-white h-screen" id="holder">
    <div class="w-full flex flex-wrap">
      <!-- Register Section -->
      <div class="w-full md:w-1/2 flex flex-col">
        <div class="flex justify-center md:justify-start pt-12 md:pl-12 md:-mb-12">
          <NuxtLink to="/" class="bg-white text-black font-bold text-xl p-4">
            <img src="/logo_transparent.svg" class="w-6 mr-2 inline" />
            <span class="align-text-top"> LinguaKite </span>
          </NuxtLink>
        </div>

        <div class="
            flex flex-col
            justify-center
            md:justify-start
            my-auto
            pt-8
            md:pt-0
            px-8
            md:px-24
            lg:px-32
          ">
          <p class="text-center text-3xl text-black">Join Us.</p>

          <form class="flex flex-col pt-3 md:pt-8" @submit.prevent="registerUser">
            <div class="alert alert-error" v-if="shouldDisplayError">
              <div class="flex-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                  class="w-6 h-6 mx-2 stroke-current">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636">
                  </path>
                </svg>
                <label>{{ error }}</label>
              </div>
            </div>
            <div class="flex flex-col pt-4">
              <label for="name" class="text-lg text-neutral">name</label>
              <input type="text" id="name" v-model="name" placeholder="johndoe" class="
                  shadow
                  appearance-none
                  border
                  rounded
                  w-full
                  py-2
                  px-3
                  text-gray-700
                  mt-1
                  leading-tight
                  focus:outline-none
                  focus:shadow-outline
                " />
            </div>

            <div class="flex flex-col pt-4">
              <label for="email" class="text-lg text-neutral">Email</label>
              <input type="email" id="email" v-model="email" placeholder="your@email.com" class="
                  shadow
                  appearance-none
                  border
                  rounded
                  w-full
                  py-2
                  px-3
                  text-gray-700
                  mt-1
                  leading-tight
                  focus:outline-none
                  focus:shadow-outline
                " />
            </div>

            <div class="flex flex-col pt-4">
              <label for="password" class="text-lg text-neutral">Password</label>
              <input type="password" id="password" placeholder="Password" v-model="password" class="
                  shadow
                  appearance-none
                  border
                  rounded
                  w-full
                  py-2
                  px-3
                  text-gray-700
                  mt-1
                  leading-tight
                  focus:outline-none
                  focus:shadow-outline
                " />
            </div>

            <div class="flex flex-col pt-4">
              <label for="confirm-password text" class="text-lg text-neutral">Confirm Password</label>
              <input type="password" id="confirm-password" placeholder="Password" v-model="confirmpassword" class="
                  shadow
                  appearance-none
                  border
                  rounded
                  w-full
                  py-2
                  px-3
                  text-gray-700
                  mt-1
                  leading-tight
                  focus:outline-none
                  focus:shadow-outline
                " />
            </div>

            <input type="submit" value="Register" class="
                bg-black
                text-white
                font-bold
                text-lg
                hover:bg-gray-700
                p-2
                mt-8
                cursor-pointer
              " />
          </form>
          <div class="text-center pt-12 pb-12 text-black">
            <p>
              Already have an account?
              <NuxtLink to="/login" class="underline font-semibold">Log in here.</NuxtLink>
            </p>
          </div>
        </div>
      </div>

      <!-- Image Section -->
      <div class="w-1/2 shadow-2xl">
        <img class="object-cover w-full h-screen hidden md:block"
          src="https://images.unsplash.com/photo-1563723788237-3a0ad15dcdbe" alt="Background" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: "solitary",
  head() {
    return {
      title: "Register",
    };
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",
      confirmpassword: "",
      error: "",
      shouldDisplayError: false,
    };
  },
  methods: {
    async registerUser() {
      // send off request to backend with axios
      if (this.password !== this.confirmpassword) {
        this.showError("Passwords do not match.");
      } else if (this.name.length < 3) {
        this.showError("name must be at least 3 characters.");
      } else if (this.name.indexOf(" ") >= 0 || /\d/.test(this.name)) {
        this.showError(
          "name can only contain letters, hyphens, and underscores."
        );
      } else {
        try {
          await this.$axios.post("/api/auth/register", {
            name: this.name,
            email: this.email,
            password: this.password,
          });
          await this.$auth.loginWith("cookie", {
            data: {
              email: this.email,
              password: this.password,
            },
          });
          this.$router.push("/");
        } catch (error) {
          console.log(error);
          // this.showError(error.response.data.message);
        }
      }
    },
    showError(error) {
      this.error = error;
      this.shouldDisplayError = true;
    },
  },
};
</script>
