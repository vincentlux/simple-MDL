import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Books from '@/components/Books';
import Simple from '@/components/Simple';
import Speech from '@/components/Speech';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Simple',
      component: Simple,
    },
    {
      path: '/book',
      name: 'Books',
      component: Books,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/s',
      name: 'Speech',
      component: Speech,
    },
  ],
  mode: 'history',
});
