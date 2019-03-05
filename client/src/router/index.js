import Vue from 'vue'
import Router from 'vue-router'
// const Speech = () => import('@/components/Speech')
import Speech from '@/components/Speech';
import Test from '@/components/Test';

Vue.use(Router)

export default new Router({
   mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Speech',
      component: Speech
    },
		{
			path: '/test',
			name: 'Test',
			component: Test
		}
  ]
})
