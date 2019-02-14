// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
// import Vuetify from 'vuetify'
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
// const App = () => import('./App')
import App from './App'
import router from './router'

// Vue.use(Vuetify)
Vue.use(BootstrapVue);

// require('../node_modules/vuetify/dist/vuetify.min.css')
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
})
