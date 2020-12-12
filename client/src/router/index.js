import Vue from 'vue';
import Router from 'vue-router';
import 'selectize/dist/css/selectize.default.css' // This is required, we use the same css as selectize.js
import VSelectize from '@isneezy/vue-selectize'

import {extend, localize, ValidationObserver, ValidationProvider} from "vee-validate";
import en from "vee-validate/dist/locale/en.json";
import * as rules from "vee-validate/dist/rules";


import Brands from "@/components/Brands";
import Models from "@/components/Models";
import Autos from "../components/Autos";
import LogAndRegister from "../components/LogAndRegister";
import Vuelidate from 'vuelidate'
import ClientMain from "../components/ClientMain";


import VueCookies from 'vue-cookies'
Vue.use(VueCookies)
Vue.$cookies.config('7d')


Object.keys(rules).forEach(rule => {
  extend(rule, rules[rule]);
});

localize("en", en);
Vue.component("ValidationObserver", ValidationObserver);
Vue.component("ValidationProvider", ValidationProvider);

Vue.component('v-selectize', VSelectize)
Vue.use(Router);
Vue.use(Vuelidate)

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
    },
    {
      path: '/services/auto/autos',
      name: 'Autos',
      component: Autos
    },
    {
      path: '/login',
      name: 'LogAndRegister',
      component: LogAndRegister
    },
    {
      path: '/main',
      name: 'ClientMain',
      component: ClientMain
    },
    {
      path: '/',
      redirect: {name: 'LogAndRegister'}
    }
  ],
});
