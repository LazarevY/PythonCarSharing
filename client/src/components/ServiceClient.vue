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
          <li class="nav-item">
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
          <li class="nav-item active">
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

    <div class="container">
      <b-form>
        <b-form-group>
          <v-selectize
            id="clientSelect"
            :options="clients"
            v-model="client_load_form.phone">
          </v-selectize>
        </b-form-group>
      </b-form>
    </div>

    <div class="container" v-show="client_loaded">
      <table class="table table-bordered">
        <tr>
          <th>Client</th>
          <td>{{ client_data.name }} {{ client_data.lastName }}</td>
        </tr>
        <tr>
          <th>Phone</th>
          <td>{{ client_data.phone }}</td>
        </tr>
        <tr>
          <th>Drive license</th>
          <td>{{ client_data.license }}</td>
        </tr>
        <tr>
          <th>Categories</th>
          <td>
            <div v-for="(key, value) in client_data.categories">
              <label>
                {{ value }}
                <input type="checkbox" v-model="client_data.categories[value]">
              </label>
            </div>
            <button @click="updateClientCategories" class="btn btn-danger btn-sm">Change categories</button>
          </td>
        </tr>

      </table>
    </div>


  </div>

</template>

<script>
import axios from "axios";
import 'selectize/dist/css/selectize.default.css' // This is required, we use the same css as selectize.js
import VSelectize from '@isneezy/vue-selectize'

export default {
  name: "ServiceClient",
  data() {
    return {
      clients: [],
      client_data: {},
      client_loaded: false,
      client_load_form: {
        phone: '',
      },
    }
  },
  validations: {},
  methods: {
    validateState(item) {
      const {$dirty, $error} = item
      return $dirty ? !$error : null
    },
    load_client_data(phone_number) {
      const path = 'http://localhost:5000/services/client';
      const payload = {
        phone: phone_number
      };

      axios.post(path, payload)
        .then((resp) => {
          this.client_data = resp.data.client_data;
          this.client_loaded = true;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    load_clients_list() {
      const path = 'http://localhost:5000/services/client'
      let clients = [];
      axios.get(path)
        .then((resp) => {
          resp.data.clients.forEach((client) => {
            clients.push({label: client.phone, code: client.phone})
          })
          this.clients = clients;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    updateClientCategories() {
      const path = 'http://localhost:5000/services/client/categories';
      const payload = {
        phone: this.client_data.phone,
        categories: this.client_data.categories,
      };

      axios.post(path, payload)
        .then((resp) => {
            this.load_client_data(this.client_load_form.phone.code)
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  watch: {
    'client_load_form.phone': function (val) {
      if (this.client_load_form.phone !== null) {
        this.load_client_data(this.client_load_form.phone.code)
      }
    },
  },
  created() {
    this.load_clients_list();
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
