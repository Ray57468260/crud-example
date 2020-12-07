import Vue from 'vue'
import Router from 'vue-router'
import layouts from '@/components/layouts'
import basic from '@/components/basic'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'layouts',
      component: layouts,
      children: [
        {
          path: 'basic',
          name: 'basic',
          component: basic
        }
      ]
    }
  ]
})
