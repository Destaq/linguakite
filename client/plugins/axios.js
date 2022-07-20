export default function ({ $axios, app, store }) {
  $axios.onRequest(config => {
    if (store.state.auth.loggedIn) {
      config.headers.common['Authorization'] = app.$auth.$storage._state["_token.cookie"]
    }
  })
}
