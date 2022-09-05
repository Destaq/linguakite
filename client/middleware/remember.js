// create a new file middleware/remember.js and register it as a global middleware in your nuxt.config.js
// (more info on middlewares - https://nuxtjs.org/docs/directory-structure/middleware/)
export default function ({ $auth, app }) {
  $auth.options.cookie.options.expires = 14;

  let authTokenValue = app.$cookiz.get("auth._token.cookie");
  let authExpirationValue = app.$cookiz.get("auth._token_expiration.cookie");

  // set the expiration date for the auth._token.cookie cookie
  app.$cookiz.set("auth._token.cookie", authTokenValue, {
    maxAge: 60 * 60 * 24 * 14,
    expires: new Date(Date.now() + 60 * 60 * 24 * 14),
  });
  app.$cookiz.set("auth._token_expiration.cookie", authExpirationValue, {
    maxAge: 60 * 60 * 24 * 14,
    expires: new Date(Date.now() + 60 * 60 * 24 * 14),
  });
}
