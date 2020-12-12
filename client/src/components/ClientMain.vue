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
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Link</a>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
          </li>
        </ul>
        <div class="form-inline mt-2 mt-md-0">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link active">{{ this.clientData.name }}</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main role="main" class="container" v-show="!have_active_contract">
      <b-form>
        <b-form-group
          label-for="pointLocation"
          invalid-feedback="Choose a point">
          <v-selectize id="pointLocation"
                       :options="this.points"
                       v-model="auto_rent.office_choice"
                       placeholder="Type a point location..."
                       aria-required="true">
          </v-selectize>
        </b-form-group>
      </b-form>

      <br>
      <table class="table table-hover">
        <thead>
        <tr>
          <th scope="col">Brand</th>
          <th scope="col">Model</th>
          <th scope="col">Registration number</th>
          <th scope="col">Mileage</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(auto, index) in autos" :key="index">
          <td>{{ auto.brand_name }}</td>
          <td>{{ auto.model_name }}</td>
          <td>{{ auto.number }}</td>
          <td>{{ auto.mileage }}</td>
          <td>
            <button
              v-b-modal.rent-modal
              type="button"
              class="btn btn-danger btn-sm"
              @click="prepareRent(auto)">
              Rent
            </button>
          </td>
        </tr>
        </tbody>
      </table>
    </main>

    <main role="main" class="container" v-show="have_active_contract">
      <h2>You have a rent</h2>

    </main>

    <b-modal ref="rentModal"
             id="rent-modal"
             title="Take rent"
             hide-footer>
      <b-form @submit="onRentSubmit" @reset="onRentReset" class="w-100">
        <b-form-group>
          <b-form-input id="form-brand-input"
                        type="text"
                        readonly
                        v-model="rent_form.auto_brand">
          </b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-input id="form-model-input"
                        type="text"
                        readonly
                        v-model="rent_form.auto_model">
          </b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-input id="form-number-input"
                        type="text"
                        readonly
                        v-model="rent_form.auto_number">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Rent</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>


  </div>

</template>

<script>
import axios from "axios";
import Vue from "vue";

export default {
  name: "ClientMain",
  data() {
    return {
      clientData: {
        name: '',
        phone: '',
      },
      points: [],
      autos: [],
      have_active_contract: null,
      auto_rent: {
        office_choice: null,
      },
      rent_form: {
        auto_brand: '',
        auto_model: '',
        auto_number: '',
        client_phone: null,
      }

    }
  },
  validations: {},
  methods: {
    validateState(item) {
      const {$dirty, $error} = item
      return $dirty ? !$error : null
    },
    getAutosForPoint(pointData) {
      const path = 'http://localhost:5000/main/autos_for_point';

      let payload = {
        point_id: pointData.id
      }

      axios.post(path, payload, {
        headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
      })
        .then((resp) => {
          this.autos = resp.data.autos;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    prepareRent(auto) {
      this.rent_form.auto_brand = auto.brand_name
      this.rent_form.auto_model = auto.model_name
      this.rent_form.auto_number = auto.number
      this.rent_form.client_phone = this.clientData.phone
    },
    onRentSubmit() {
      this.$refs.rentModal.hide();
      const path = 'http://localhost:5000/main/rent/create';

      const payload = {
        phone: this.clientData.phone,
        auto_number: this.rent_form.auto_number
      }

      axios.post(path, payload,{
        headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
      })
        .then((resp) => {

        })
        .catch((error) => {
        });
    },
    onRentReset() {

    },
  },
  watch: {
    'auto_rent.office_choice': function (value) {
      if (this.auto_rent.office_choice !== null) {
        this.getAutosForPoint({id: this.auto_rent.office_choice.code, addr: this.auto_rent.office_choice.label})
      }
    }
  },
  created() {
    const path = 'http://localhost:5000/main';
    axios.get(path, {
      headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
    })
      .then((resp) => {
        if (resp.data.logined === false || !resp.data.logined) {
          this.$router.push({name: 'LogAndRegister'})
        } else {
          this.clientData.name = resp.data.userdata.name;
          this.clientData.phone = resp.data.userdata.phone;
          this.have_active_contract = resp.data.isActiveContract;
          Vue.$cookies.set('userphone', this.clientData.phone)
          this.points = resp.data.points;
        }
      })
      .catch((error) => {
        console.error(error);
        this.$router.push({name: 'LogAndRegister'})
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
