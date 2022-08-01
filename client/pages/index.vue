<template>
  <div v-if="$auth.loggedIn">

  </div>
  <div v-else>
    <!-- Landing Page -->
    <div>
      <main>
        <div class="
            relative
            pt-16
            pb-32
            flex
            content-center
            items-center
            justify-center
          " style="min-height: 75vh">
          <div class="absolute top-0 w-full h-full bg-center bg-cover"
            style="background-image: url('https://images.unsplash.com/photo-1519682577862-22b62b24e493?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1267&amp;q=80');">
            <span id="blackOverlay" class="w-full h-full absolute opacity-75 bg-black"></span>
          </div>
          <div class="container relative mx-auto">
            <div class="items-center flex flex-wrap">
              <div class="w-full lg:w-6/12 px-4 ml-auto mr-auto text-center">
                <div class="pr-12">
                  <h1 class="text-white font-semibold text-5xl">
                    Fly like a kite in your language learning
                  </h1>
                  <p class="mt-4 text-lg text-gray-300">
                    With LinguaKite, learn English <span class="italic">through</span> English, with thousands of texts
                    (including your own), a personalized wordbank, vocabulary building exercises, and more!
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="
              top-auto
              bottom-0
              left-0
              right-0
              w-full
              absolute
              pointer-events-none
              overflow-hidden
            " style="height: 70px">
            <svg class="absolute bottom-0 overflow-hidden" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"
              version="1.1" viewBox="0 0 2560 100" x="0" y="0">
              <polygon class="text-gray-300 fill-current" points="2560 0 2560 100 0 100"></polygon>
            </svg>
          </div>
        </div>
        <section class="pb-20 bg-gray-300 -mt-24">
          <div class="container mx-auto px-4">
            <div class="flex flex-wrap">
              <div class="lg:pt-12 pt-6 w-full md:w-4/12 px-4 text-center">
                <div class="
                    relative
                    flex flex-col
                    min-w-0
                    break-words
                    bg-white
                    w-full
                    mb-8
                    shadow-lg
                    rounded-lg
                  ">
                  <div class="px-4 py-5 flex-auto">
                    <div class="
                        text-white
                        p-3
                        text-center
                        inline-flex
                        items-center
                        justify-center
                        w-12
                        h-12
                        mb-5
                        shadow-lg
                        rounded-full
                        bg-red-400
                      ">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4 6h16M4 12h16M4 18h7" />
                      </svg>
                    </div>
                    <h6 class="text-xl font-semibold">1000s of Articles</h6>
                    <p class="mt-2 mb-4 text-gray-600">
                      Our built-in database will mean you never run out of interesting content to read, even if you
                      don't upload your own.
                    </p>
                  </div>
                </div>
              </div>
              <div class="w-full md:w-4/12 px-4 text-center">
                <div class="
                    relative
                    flex flex-col
                    min-w-0
                    break-words
                    bg-white
                    w-full
                    mb-8
                    shadow-lg
                    rounded-lg
                  ">
                  <div class="px-4 py-5 flex-auto">
                    <div class="
                        text-white
                        p-3
                        text-center
                        inline-flex
                        items-center
                        justify-center
                        w-12
                        h-12
                        mb-5
                        shadow-lg
                        rounded-full
                        bg-primary
                      ">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                      </svg>
                    </div>
                    <h6 class="text-xl font-semibold">
                      Personalized Interface
                    </h6>
                    <p class="mt-2 mb-4 text-gray-600">
                      Every single word gets analyzed and color-coded based on your familiarity with it. You can also
                      set goals and view detailed usage statistics.
                    </p>
                  </div>
                </div>
              </div>
              <div class="pt-6 w-full md:w-4/12 px-4 text-center">
                <div class="
                    relative
                    flex flex-col
                    min-w-0
                    break-words
                    bg-white
                    w-full
                    mb-8
                    shadow-lg
                    rounded-lg
                  ">
                  <div class="px-4 py-5 flex-auto">
                    <div class="
                        text-white
                        p-3
                        text-center
                        inline-flex
                        items-center
                        justify-center
                        w-12
                        h-12
                        mb-5
                        shadow-lg
                        rounded-full
                        bg-accent
                      ">
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z">
                        </path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                      </svg>
                    </div>
                    <h6 class="text-xl font-semibold">Motivational Goals</h6>
                    <p class="mt-2 mb-4 text-gray-600">
                      Set yourself a daily goal to get more learning done — your reading time is tracked with our
                      accurate-to-the-millisecond stopwatch.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex flex-wrap items-center mt-28">
              <div class="w-1/3 px-4 mr-auto ml-auto">
                <div class="
                    text-gray-600
                    p-3
                    text-center
                    inline-flex
                    items-center
                    justify-center
                    w-16
                    h-16
                    mb-6
                    shadow-lg
                    rounded-full
                    bg-gray-100
                  ">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 class="text-3xl mb-2 font-semibold leading-normal">
                  Learn Anywhere, Anytime
                </h3>
                <p class="
                    text-lg
                    font-light
                    leading-relaxed
                    mt-4
                    mb-4
                    text-gray-700
                  ">
                  People lead busy lives, so we've made it easy for you to learn
                  even if you just have a few minutes free.
                </p>
                <p class="
                    text-lg
                    font-light
                    leading-relaxed
                    mt-0
                    mb-4
                    text-gray-700
                  ">
                  LinguaKite saves your progress, so you can continue where
                  you left off. What's more, most texts are only a few pages
                  or less, and can be easily read through in a matter of minutes.
                </p>
                <NuxtLink to="/register" class="font-bold text-gray-800 mt-8">Sign me up!</NuxtLink>
              </div>
              <div class="w-2/3 mr-auto ml-auto px-4">
                <PracticePuzzle :puzzle="samplePuzzle2" puzzleNumber="2" checkIt="true" class="rounded-lg -rotate-3" />
                <PracticePuzzle :puzzle="samplePuzzle3" puzzleNumber="11" class="rounded-lg rotate-3 bg-green-300" />
                <PracticePuzzle :puzzle="samplePuzzle1" puzzleNumber="7" class="rounded-lg -rotate-3" />
              </div>
            </div>
          </div>
        </section>
        <section class="relative py-20">
          <div class="
              bottom-auto
              top-0
              left-0
              right-0
              w-full
              absolute
              pointer-events-none
              overflow-hidden
              -mt-20
            " style="height: 80px">
            <svg class="absolute bottom-0 overflow-hidden" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"
              version="1.1" viewBox="0 0 2560 100" x="0" y="0">
              <polygon class="text-white fill-current" points="2560 0 2560 100 0 100"></polygon>
            </svg>
          </div>
          <div class="container mx-auto px-4">
            <div class="items-center flex flex-wrap">
              <div class="w-full md:w-4/12 ml-auto mr-auto px-4">
                <img alt="..." class="max-w-full rounded-lg shadow-lg"
                  src="https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=634&amp;q=80" />
              </div>
              <div class="w-full md:w-5/12 ml-auto mr-auto px-4">
                <div class="md:pr-12">
                  <div class="
                      text-pink-600
                      p-3
                      text-center
                      inline-flex
                      items-center
                      justify-center
                      w-16
                      h-16
                      mb-6
                      shadow-lg
                      rounded-full
                      bg-pink-300
                    ">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z">
                      </path>
                    </svg>
                  </div>
                  <h3 class="text-3xl font-semibold">Community Built</h3>
                  <p class="mt-4 text-lg leading-relaxed text-gray-600">
                    Articles are drawn from an open-source <a class="link" href="https://www.medium.com">Medium</a>
                    database
                    and are also drawn from contributions by other users.
                  </p>
                  <ul class="list-none mt-6">
                    <li class="py-2">
                      <div class="flex items-center">
                        <div>
                          <span class="
                              text-xs
                              font-semibold
                              inline-block
                              py-1
                              px-2
                              uppercase
                              rounded-full
                              text-pink-600
                              bg-pink-200
                              mr-3
                            "></span>
                        </div>
                        <div>
                          <h4 class="text-gray-600">
                            Native, natural articles
                          </h4>
                        </div>
                      </div>
                    </li>
                    <li class="py-2">
                      <div class="flex items-center">
                        <div>
                          <span class="
                              text-xs
                              font-semibold
                              inline-block
                              py-1
                              px-2
                              uppercase
                              rounded-full
                              text-pink-600
                              bg-pink-200
                              mr-3
                            "></span>
                        </div>
                        <div>
                          <h4 class="text-gray-600">
                            Perspectives from across the globe
                          </h4>
                        </div>
                      </div>
                    </li>
                    <li class="py-2">
                      <div class="flex items-center">
                        <div>
                          <span class="
                              text-xs
                              font-semibold
                              inline-block
                              py-1
                              px-2
                              uppercase
                              rounded-full
                              text-pink-600
                              bg-pink-200
                              mr-3
                            "></span>
                        </div>
                        <div>
                          <h4 class="text-gray-600">Hundreds of tags</h4>
                        </div>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="text-gray-600 body-font">
          <div class="container px-5 py-24 mx-auto">
            <div class="flex flex-col text-center w-full mb-20">
              <h1 class="
                  sm:text-3xl
                  text-2xl
                  font-medium
                  title-font
                  mb-4
                  text-gray-900
                ">
                A Fresh Alternative
              </h1>
              <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
                LinguaKite is in its humble beginnings. Made with love in Prague,
                Czechia, its developers hope you'll love the smoothness of the site,
                intelligence of the database algorithm,
                and progress you'll make learning!
              </p>
            </div>
            <div class="flex flex-wrap -m-4 text-center">
              <div class="p-4 md:w-1/4 sm:w-1/2 w-full">
                <div class="border-2 border-gray-200 px-4 py-6 rounded-lg">
                  <svg class="w-12 text-primary mb-3 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253">
                    </path>
                  </svg>
                  <h2 class="title-font font-medium text-3xl text-gray-900">
                    2.1K
                  </h2>
                  <p class="leading-relaxed">Articles</p>
                </div>
              </div>
              <div class="p-4 md:w-1/4 sm:w-1/2 w-full">
                <div class="border-2 border-gray-200 px-4 py-6 rounded-lg">
                  <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    class="text-primary w-12 h-12 mb-3 inline-block" viewBox="0 0 24 24">
                    <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"></path>
                  </svg>
                  <h2 class="title-font font-medium text-3xl text-gray-900">
                    3+
                  </h2>
                  <p class="leading-relaxed">Leaners</p>
                </div>
              </div>
              <div class="p-4 md:w-1/4 sm:w-1/2 w-full">
                <div class="border-2 border-gray-200 px-4 py-6 rounded-lg">
                  <svg class="w-12 text-primary mb-3 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z">
                    </path>
                  </svg>
                  <h2 class="title-font font-medium text-3xl text-gray-900">
                    24
                  </h2>
                  <p class="leading-relaxed">Languages</p>
                </div>
              </div>
              <div class="p-4 md:w-1/4 sm:w-1/2 w-full">
                <div class="border-2 border-gray-200 px-4 py-6 rounded-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-12 text-primary mb-3 inline-block" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <h2 class="title-font font-medium text-3xl text-gray-900">
                    7h
                  </h2>
                  <p class="leading-relaxed">Last Update</p>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="pb-10 relative block bg-gray-900">
          <div class="
              bottom-auto
              top-0
              left-0
              right-0
              w-full
              absolute
              pointer-events-none
              overflow-hidden
              -mt-20
            " style="height: 80px">
            <svg class="absolute bottom-0 overflow-hidden" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"
              version="1.1" viewBox="0 0 2560 100" x="0" y="0">
              <polygon class="text-gray-900 fill-current" points="2560 0 2560 100 0 100"></polygon>
            </svg>
          </div>
          <div class="container mx-auto px-4 lg:pt-24 lg:pb-12">
            <div class="flex flex-wrap text-center justify-center">
              <div class="w-full lg:w-6/12 px-4">
                <h2 class="text-4xl font-semibold text-white">
                  Backed by Science
                </h2>
                <p class="text-lg leading-relaxed mt-4 mb-4 text-gray-500">
                  Users who spent at least
                  <span class="text-gray-200">5 mins/day</span> on SurgeLingo
                  performed an average of
                  <span class="text-gray-200">23% better</span> on
                  language proficiency tests than their traditional-method counterparts -
                  <span class="text-gray-200">after just one month</span>.
                </p>
              </div>
            </div>
            <hr class="w-1/2 my-10 mx-auto" />
            <div class="flex flex-wrap justify-center">
              <div class="w-full lg:w-3/12 px-4 text-center">
                <p class="text-2xl leading-relaxed text-gray-100">
                  What are you waiting for?
                  <NuxtLink to="/register" class="underline hover:text-white">Start flying!</NuxtLink>
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import PracticePuzzle from '~/components/PracticePuzzle.vue';
export default {
  head() {
    return {
      title: "Home",
    };
  },
  components: { PracticePuzzle },
  data() {
    return {
      samplePuzzle1: {
        "answer": "125364", "context": " ... without us.", "question": ["Life", "will", "with", "or", "continue", "us"], "type": "Order Words"
      },
      samplePuzzle2: {
        "answer": "done", "options": ["practice", "cause", "act", "done"], "question": "We’ve _____ a poor job at marketing the climate crisis to selfish human beings .", "type": "Multiple Choice"
      },
      samplePuzzle3: { "answer": "conforming with or constituting a norm or standard or level or type or social norm; not abnormal", "question": "Define 'normal' in the context: \"The problem was never just warming — it was about a disruption in the normal, habitable range of our planet’s climate.\"", "type": "Define" }
    }
  }
}
</script>
