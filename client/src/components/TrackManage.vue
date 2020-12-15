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
              <a class="nav-link active">{{ this.clientData.name }}</a>
            </li>
            <li class="nav-item">
              <a>
                <button class="btn btn-warning btn-sm" @click="$router.push({name: 'ClientLogout'})">Logout</button>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container">
      <b-form @submit="onTrackSubmit" class="w-100">
        <b-form-group label-for="stateSelect">
          <b-select
            id="stateSelect"
            :options="track_states"
            :state="validateState($v.track_form.state)"
            v-model="$v.track_form.state.$model">
          </b-select>
        </b-form-group>

        <b-form-group label-for="durationInput" invalid-feedback="Duration must be greater than 0" label="Minutes">
          <b-input
            id="durationInput"
            type="number"
            :state="validateState($v.track_form.duration)"
            v-model="$v.track_form.duration.$model">
          </b-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Add</b-button>
      </b-form>

      <br>
      <b-form @submit="endRent">
        <b-form-group label-for="mileageInput" invalid-feedback="Mileage must be greater than 0" label="Mileage">
          <b-input
            id="mileageInput"
            type="number"
            :state="validateState($v.end_rent_form.mileage)"
            v-model="$v.end_rent_form.mileage.$model">
          </b-input>
        </b-form-group>

        <b-form-group
          label-for="pointLocation"
          invalid-feedback="Choose a point">
          <v-selectize id="pointLocation"
                       :options="this.points"
                       v-model="end_rent_form.point"
                       placeholder="Type a point location..."
                       aria-required="true">
          </v-selectize>
        </b-form-group>


        <b-button type="variant" variant="danger">End rent</b-button>
      </b-form>
    </div>

    <br>
    <div class="container">
      <table class="table table-hover">
        <thead>
        <tr>
          <th scope="col">State</th>
          <th scope="col">Duration</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(track, index) in history" :key="index">
          <td>{{ track.state_name }}</td>
          <td>{{ track.duration }}</td>
        </tr>
        </tbody>
      </table>
    </div>


  </div>

</template>

<script>
import axios from "axios";
import {minValue, required} from 'vuelidate/lib/validators'
import Vue from "vue";

export default {
  name: "TrackManage",
  data() {
    return {
      clientData: {
        name: '',
        phone: '',
      },
      points: [],
      track_states: [],
      history: [],
      rent_data: {
        contract_id: null,
        registration_number: null,
        model_name: null,
        brand_name: null,
      },
      track_form: {
        state: null,
        duration: 1,
      },
      end_rent_form: {
        mileage: 1,
        point: null,
      },

    }
  },
  validations: {
    track_form: {
      state: {
        required,
      },
      duration: {
        required,
        minValue: minValue(1),
      },
    },
    end_rent_form: {
      mileage: {
        required,
        minValue: minValue(1),
      }
    }
  },
  methods: {
    validateState(item) {
      const {$dirty, $error} = item
      return $dirty ? !$error : null
    },
    onTrackSubmit() {
      const path = 'http://localhost:5000/main/rent/track';

      const payload = {
        contract_id: this.rent_data.contract_id,
        status_name: this.track_form.state,
        duration: this.track_form.duration
      }
      axios.post(path, payload, {
        headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
      })
        .then((resp) => {
          this.load_rent_history();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    endRent() {
      const path = 'http://localhost:5000/main/rent/end';

      const payload = {
        contract_id: this.rent_data.contract_id,
        mileage: this.end_rent_form.mileage,
        address: this.end_rent_form.point.label
      }


      axios.post(path, payload, {
        headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
      })
        .then((resp) => {
          this.$router.push({name: "ClientMain"})
        })
        .catch((error) => {
          console.error(error);
        });
    },
    load_client_data() {
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
            if (resp.data.isActiveContract) {
              this.rent_data = resp.data.rent_data;
            }
            Vue.$cookies.set('userphone', this.clientData.phone)
            this.points = resp.data.points;
            this.load_rent_history();
          }
        })
        .catch((error) => {
          console.error(error);
          this.$router.push({name: 'LogAndRegister'})
        });
    },
    load_rent_data() {
      const path = 'http://localhost:5000/main/rent/track';
      axios.get(path, {
        headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
      })
        .then((resp) => {
          let states = []
          resp.data.states.forEach(state => {
            states.push({value: state.state_name, text: state.state_name})
          })
          this.track_states = states
        })
        .catch((error) => {
          console.error(error);
        });
    },
    load_rent_history() {
      const path = 'http://localhost:5000/main/rent/track/history';

      const payload = {
        contract_id: this.rent_data.contract_id
      }

      axios.post(path, payload, {
        headers: {Authorization: "Bearer " + Vue.$cookies.get('token')}
      })
        .then((resp) => {
          this.history = resp.data.history;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.load_client_data();
    this.load_rent_data();
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
