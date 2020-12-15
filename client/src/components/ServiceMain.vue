<template>
  <div>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <a class="navbar-brand" href="#">Fixed navbar</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
              aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" @click="$router.push({name: 'ServiceMain'})">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="$router.push({name: 'Brands'})">Brands</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="$router.push({name: 'Models'})">Models</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="$router.push({name: 'Autos'})">Autos</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="$router.push({name: 'ServiceClient'})">Clients</a>
          </li>
        </ul>
        <div class="form-inline mt-2 mt-md-0">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link active"></a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>

</template>

<script>
import axios from "axios";
import 'selectize/dist/css/selectize.default.css' // This is required, we use the same css as selectize.js
import VSelectize from '@isneezy/vue-selectize'

export default {
  name: "ServiceClient",
  data() {
    return {}
  },
  validations: {},
  created() {

  },

}
</script>

<style scoped>
.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}


</style>
