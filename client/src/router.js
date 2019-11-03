import Vue from 'vue';
import Router from 'vue-router';
import Fetch from './components/Fetch.vue';
import Home from './views/Home.vue';
import Todo from './components/Todos.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/fetch',
      name: 'fetch',
      component: Fetch,
    },
    {
      path: '/todos',
      name: 'Todo',
      component: Todo,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
    },
    {
      path: '/',
      name: 'home',
      component: Home,
    },
  ],
});
