// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

// 引入 element-ui
import ElementUI from 'element-ui'

// 引入 axios
import axios from 'axios'

import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

Vue.prototype.$axios = axios
axios.defaults.timeout = 5000
axios.defaults.baseURL = 'http://' + location.hostname + ':8000' // 配置接口地址

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  render: h => h(App),
  store,
  router,
  components: { App }
}).$mount('#app')