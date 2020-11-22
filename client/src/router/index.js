import Vue from 'vue';
import Router from 'vue-router';
import Brands from "@/components/Brands";
import 'selectize/dist/css/selectize.default.css' // This is required, we use the same css as selectize.js
import VSelectize from '@isneezy/vue-selectize'
import Models from "@/components/Models";

Vue.component('v-selectize', VSelectize)
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/services/auto/brands',
      name: 'Brands',
      component: Brands
    },
    {
      path: '/services/auto/models',
      name: 'Models',
      component: Models
    }
  ],
});
