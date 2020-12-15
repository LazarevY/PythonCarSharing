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
            <a class="nav-link" @click="$router.push({name: 'ClientMain'})">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="$router.push({name: 'ClientStatistic'})">Statistic</a>
          </li>
        </ul>
        <div class="form-inline mt-2 mt-md-0">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link active">{{}}</a>
            </li>
            <li class="nav-item">
              <a><button class="btn btn-warning btn-sm" @click="$router.push({name: 'ClientLogout'})">Logout</button></a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container">
      <table class="table table-bordered">
        <tr>
          <th>Model</th>
          <th>Rents</th>
        </tr>
        <tr v-for="(model, index) in top_models" :key="index">
          <td>{{ model.brand_name }} {{ model.model_name }}</td>
          <td>{{ model.rents }}</td>
        </tr>
      </table>
    </div>

    <br>
    <div class="container">
      <table class="table table-bordered">
        <tr>
          <th>Global rents</th>
          <th>Primary model</th>
        </tr>
        <tr>
          <td>{{ this.rents.count }}</td>
          <td>{{ this.rents.primary_brand }} {{ this.rents.primary_model }}</td>
        </tr>
      </table>
    </div>
    <div class="container">
      <table class="table table-bordered">
        <tr>
          <th>Violates</th>
        </tr>
        <tr>
          <td>{{ this.violates.count }}</td>
        </tr>
      </table>
    </div>

    <div class="container">
      <table class="table table-bordered" v-for="rent_data in this.rents_data">
        <tr>
          <th>Contract id</th>
          <td>{{ rent_data.contract_id }}</td>
        </tr>
        <tr>
          <th>Model</th>
          <td>{{ rent_data.brand_name }} {{ rent_data.model_name }}</td>
        </tr>
        <tr>
          <th>Number</th>
          <td>{{ rent_data.number }}</td>
        </tr>
        <tr>
          <th>Rent begin</th>
          <td>{{ rent_data.rent_begin_date }}</td>
        </tr>
        <tr>
          <th>Rent end</th>
          <td>{{ rent_data.rent_end_date }}</td>
        </tr>
      </table>
    </div>


  </div>

</template>

<script>
import axios from "axios";
import Vue from "vue";

export default {
  name: "ClientStatistic",
  data() {
    return {
      top_models: [],
      rents: {
        count: null,
        primary_brand: null,
        primary_model: null,
      },
      rents_data: [],
      violates: {
        count: null,
      }
    }
  },
  validations: {},
  methods: {
    validateState(item) {
      const {$dirty, $error} = item
      return $dirty ? !$error : null
    },
  },
  created() {
    const path = 'http://localhost:5000/main/client/statistic';
    axios.get(path, {
      headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
    })
      .then((resp) => {
        this.top_models = resp.data.top_models;
        this.rents = resp.data.rents;
        this.rents_data = resp.data.rents_data;
        this.violates = resp.data.violates;
      })
      .catch((error) => {
        console.error(error);
      });
  }

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
