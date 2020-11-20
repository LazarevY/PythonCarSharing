import Vue from 'vue';
import Router from 'vue-router';
import Brands from "@/components/Brands";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/services/auto/brands',
      name: 'Brands',
      component: Brands
    }
  ],
});
