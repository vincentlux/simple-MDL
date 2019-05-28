import Vue from 'vue'
import Router from 'vue-router'
// const Speech = () => import('@/components/Speech')
import Speech from '@/components/Speech';
import Test from '@/components/Test';
import Upload from '@/components/Upload';
import Welcome from '@/components/Welcome';
import Sidebar from '@/components/Sidebar';

Vue.use(Router)

export default new Router({
   mode: 'history',
  routes: [
		{
      path: '/',
      name: 'Test',
      component: Test
		},
		{
      path: '/sidebar',
      name: 'Sidebar',
      component: Sidebar
    },
    // {
    //   path: '/',
    //   name: 'Speech',
    //   component: Speech
    // },
		// {
		// 	path: '/test',
		// 	name: 'Test',
		// 	component: Test
		// },
		// {
		// 	path: '/upload',
		// 	name: 'Upload',
		// 	component: Upload
		// }
  ]
})
