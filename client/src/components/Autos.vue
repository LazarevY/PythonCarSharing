<template>
  <div class="container">
    <div class="row">
      <div>
        <h1>Autos</h1>
        <hr>
        <br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.auto-modal>Add Auto</button>
        <button type="button" class="btn btn-success btn-sm" @click="updateAutos">Reload Autos</button>

        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">
              <div>Brand</div>
              <br>
              <v-selectize :options="filter_auto.brands"
                           v-model="filter_auto.brand">
              </v-selectize>
            </th>
            <th scope="col">
              Model
              <v-selectize :options="filter_auto.models"
                           v-model="filter_auto.model">
              </v-selectize>

            </th>
            <th scope="col">
              Registration number
              <v-selectize :options="filter_auto.numbers"
                           v-model="filter_auto.number">
              </v-selectize>
            </th>
            <th scope="col">Mileage</th>
            <th scope="col">Available</th>
            <th scope="col">Office</th>
            <th scope="col">Quality</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(auto, index) in autos" :key="index">
            <td>{{ auto.brand_name }}</td>
            <td>{{ auto.model_name }}</td>
            <td>{{ auto.number }}</td>
            <td>{{ auto.mileage }}</td>
            <td>{{ auto.available }}</td>
            <td @click="updateLocation(auto)">{{ auto.current_office }}</td>
            <td>{{ auto.quality }}</td>
            <td>
              <button
                type="button"
                class="btn btn-warning btn-sm"
                v-b-modal.auto-update-modal
                @click="editAuto(auto)">
                Update
              </button>
              <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="deleteAuto(auto)">
                Delete
              </button>
              <button
                type="button"
                class="btn btn-warning btn-sm"
                v-b-modal.historyViewModal
                @click="viewHistory(auto)">
                History
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addAutoModal"
             id="auto-modal"
             title="Add a auto"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-brand-group"
                      label="Brand: "
                      label-for="form-brand-select">
          <b-select id="form-brand-select"
                    :options="getBrandOptions()"
                    @change="updateModelsOptions(brand)"
                    v-model="brand"
                    placeholder="Select brand"
                    required>
          </b-select>
        </b-form-group>
        <b-form-group id="form-model-group"
                      label="Model: "
                      label-for="form-model-select">
          <v-selectize id="form-model-select"
                       :options="model_options"
                       v-model="addAutoForm.model_id"
                       placeholder="Select model"
                       aria-required="true">
          </v-selectize>
        </b-form-group>
        <b-form-group id="form-number-group"
                      label="Number:"
                      label-for="form-number-input">
          <b-form-input id="form-model-input"
                        type="text"
                        v-model="addAutoForm.registration_number"
                        required
                        placeholder="Enter auto number">
          </b-form-input>
        </b-form-group>

        <b-form-group label-for="form-mileage-input"
                      label="Mileage: ">
          <b-form-input id="form-mileage-input"
                        type="number"
                        v-model.number="addAutoForm.mileage"
                        required
                        placeholder="Mileage">

          </b-form-input>
        </b-form-group>
        <b-form-group label-for="form-quality-input"
                      label="Quality: ">
          <b-form-input id="form-quality-input"
                        type="number"
                        v-model.number="addAutoForm.quality"
                        required
                        placeholder="Quality">

          </b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editAutoModal"
             id="auto-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-edit-brand-group"
                      label="Brand: "
                      label-for="form-edit-brand-select">
          <b-select id="form-edit-brand-select"
                    :options="getBrandOptions()"
                    @change="updateModelsOptions(editForm.brand_name_select)"
                    v-model="editForm.brand_name_select"
                    placeholder="Select brand"
                    required>
          </b-select>
        </b-form-group>
        <b-form-group id="form-edit-model-group"
                      label="Model: "
                      label-for="form-edit-model-select">
          <v-selectize id="form-edit-model-select"
                       :options="model_options"
                       v-model="editForm.new_model_id"
                       placeholder="Select model"
                       aria-required="true">
          </v-selectize>
        </b-form-group>

        <b-form-group label="Location: "
                      label-for="form-edit-location-select"
                      v-show="!editForm.disable_location_edit">
          <v-selectize id="form-edit-location-select"
                       :options="change_location_points"
                       v-model="editForm.new_office"
                       placeholder="Select location"
                       aria-required="true">
          </v-selectize>
        </b-form-group>

        <b-form-group id="form-edit-number-group"
                      label="Number:"
                      label-for="form-edit-number-input">
          <b-form-input id="form-edit-number-input"
                        type="text"
                        v-model="editForm.new_number"
                        required
                        placeholder="Enter auto number">
          </b-form-input>
        </b-form-group>

        <b-form-group label-for="form-edit-mileage-input"
                      label="Mileage: ">
          <b-form-input id="form-edit-mileage-input"
                        type="number"
                        v-model.number="editForm.mileage"
                        required
                        placeholder="Mileage">

          </b-form-input>
        </b-form-group>
        <b-form-group label-for="form-edit-quality-input"
                      label="Quality: ">
          <b-form-input id="form-edit-quality-input"
                        type="number"
                        v-model.number="editForm.quality"
                        required
                        placeholder="Quality">

          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="historyView"
             id="historyViewModal"
             title="History"
             hide-footer>
      <div class="container">

        <table v-for="note in auto_history" class="table table-bordered">
          <tr>
            <th>Client</th>
            <td>{{ note.client }}</td>
          </tr>
          <tr>
            <th>Begin date</th>
            <td>{{ note.begin_date }}</td>
          </tr>
          <tr>
            <th>End date</th>
            <td>{{ note.end_date }}</td>
          </tr>
          <tr>
            <th>Mileage</th>
            <td>{{ note.mileage }}</td>
          </tr>
        </table>
      </div>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';
import 'selectize/dist/css/selectize.default.css' // This is required, we use the same css as selectize.js

export default {
  name: "Autos",
  data() {
    return {
      brand: '',
      brands: [],
      autos: [],
      brand_options: [],
      model_options: [],
      change_location_points: [],
      addAutoForm: {
        model_id: 0,
        registration_number: '',
        mileage: 0,
        quality: 0,
      },
      filter_auto: {
        brand: {
          label: '<Any>',
          code: null,
        },
        model: {
          label: '<Any>',
          code: null
        },
        number: {
          label: '<Any>',
          code: null
        },
        brands: [],
        models: [],
        numbers: [],
      },
      auto_history: [],
      editForm: {
        disable_location_edit: true,
        brand_name_select: null,
        old_model_id: 0,
        new_office: null,
        new_model_id: 0,
        old_number: '',
        new_number: '',
        mileage: 0,
        quality: 0,
      },
    };
  },
  methods: {
    getBrands() {
      const path = 'http://localhost:5000/services/auto/brands';
      axios.get(path)
        .then((res) => {
          this.brands = res.data.brands;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getBrandOptions() {
      const options = []
      this.brands.forEach(brand => {
        options.push({value: brand.name, text: brand.name})
      });
      return options;
    },
    updateModelsOptions(brand_name) {
      console.log(brand_name)
      this.getModelOptions(brand_name);
    },
    getModelOptions(brand_name, event = '') {
      const path = 'http://localhost:5000/services/auto/models/for_brand';
      const payload = {
        brand_name: brand_name,
      };
      axios.post(path, payload)
        .then((res) => {
          this.model_options = []
          res.data.models.forEach(model => {
            let mod = {label: model.model_name, code: model.model_id}
            this.model_options.push(mod)
            if (mod.code === this.editForm.old_model_id) {
              this.editForm.new_model_id.val(mod);
            }
          })
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getAutos() {
      const path = 'http://localhost:5000/services/auto/autos/get';
      let payload = {
        brand: this.filter_auto.brand.code,
        model: this.filter_auto.model.code,
        number: this.filter_auto.number.code,
      }
      axios.post(path, payload)
        .then((res) => {
          this.autos = res.data.autos;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addAuto(payload) {
      const path = 'http://localhost:5000/services/auto/autos';
      axios.post(path, payload)
        .then(() => {
          this.created();
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.log(error);
          this.getAutos();
        });
    },
    updateAuto(payload) {
      const path = 'http://localhost:5000/services/auto/autos';
      axios.put(path, payload)
        .then(() => {
          this.created()
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
          this.getAutos();
        });
    },
    editAuto(auto) {
      this.editForm.brand_name_select = auto.brand_name;
      this.editForm.disable_location_edit = !auto.available;
      this.editForm.old_model_id = auto.model_id;
      this.editForm.old_number = auto.number;
      this.editForm.new_model_id = {label: auto.model_name, code: auto.model_id};
      this.editForm.new_number = auto.number;
      this.editForm.mileage = auto.mileage;
      this.editForm.quality = auto.quality;

      let path = 'http://localhost:5000/services/auto/autos/location';

      let payload = {
        number: auto.number,
        current_office_id: auto.current_office_id,
      }

      this.getModelOptions(auto.brand_name)

      axios.post(path, payload)
        .then((resp) => {
          let locations = [];
          resp.data.locations.forEach((location) => {
            let loc = {
              label: location.office_label,
              code: location.office_id,
            }
            locations.push(loc);
            if (loc.code === auto.current_office_id) {
              this.editForm.new_office = loc;
            }
          });
          this.change_location_points = locations;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
        });

      this.getModelOptions(auto.brand_name);

    },
    viewHistory(auto) {
      let path = 'http://localhost:5000/services/auto/autos/history';

      let payload = {
        number: auto.number,
      }

      axios.post(path, payload)
        .then((resp) => {
          this.auto_history = resp.data.history
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
        });
    },
    deleteAuto(auto) {
      const path = 'http://localhost:5000/services/auto/autos/remove';
      if (confirm("Delete auto " + auto.number + "?")) {
        const payload = {
          number: auto.number,
        };
        axios.post(path, payload)
          .then((resp) => {
            this.created();
          })
          .catch((error) => {
            console.error(error);
            this.getAutos();
          });
      }
    },
    initForm() {
      this.addAutoForm.brand_name_select = null;
      this.addAutoForm.model_name_select = null;
      this.addAutoForm.registration_number = null;
      this.addAutoForm.mileage = 1000;
      this.addAutoForm.quality = 50;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addAutoModal.hide();
      const payload = {
        model_id: this.addAutoForm.model_id.code,
        registration_number: this.addAutoForm.registration_number,
        mileage: this.addAutoForm.mileage,
        quality: this.addAutoForm.quality,
      };
      this.addAuto(payload);
      this.initForm();
    },
    updateLocation(auto) {

    },
    updateAutos() {
      this.load_filter_data();
      this.getAutos();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAutoModal.hide();
      const payload = {
        old_model_id: this.editForm.old_model_id,
        new_model_id: this.editForm.new_model_id.code,
        old_number: this.editForm.old_number,
        new_number: this.editForm.new_number,
        new_office_id: this.editForm.new_office.code,
        mileage: this.editForm.mileage,
        quality: this.editForm.quality,
      };
      this.updateAuto(payload);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addAutoModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAutoModal.hide();
      this.initForm();
      this.created()
    },
    load_filter_data() {
      const path = 'http://localhost:5000/services/auto/autos/filter';
      let payload = {
        brand_id: this.filter_auto.brand.code,
        model_id: this.filter_auto.model.code,
        number: this.filter_auto.number.code,
      }
      axios.post(path, payload)
        .then((resp) => {
          let brands = []
          let old = this.filter_auto.brand;
          brands.push({label: '<Any>', code: null})
          this.filter_auto.brand = {label: '', code: null};
          resp.data.brands.forEach((brand) => {
            let t = {label: brand.brand_name, code: brand.brand_id};
            brands.push(t);
            if (t.code === old.code) {
              this.filter_auto.brand = old;
            }
          })
          this.filter_auto.brands = brands;

          let models = []
          old = this.filter_auto.model;
          models.push({label: '<Any>', code: null})
          this.filter_auto.model = {label: '', code: null};
          resp.data.models.forEach((model) => {
            let t = {label: model.model_name, code: model.model_id};
            models.push(t);
            if (t.code === old.code) {
              this.filter_auto.model = old;
            }
          })
          this.filter_auto.models = models;

          let numbers = []
          old = this.filter_auto.number;
          this.filter_auto.number = {label: '', code: null};
          numbers.push({label: '<Any>', code: null})
          resp.data.numbers.forEach((number) => {
            let t = {label: number.number, code: number.number};
            numbers.push(t);
            if (t.code === old.code) {
              this.filter_auto.number = old;
            }
          })
          this.filter_auto.numbers = numbers;
        })
        .catch((error) => {
          console.error(error);
          this.getAutos();
        });
    }
  },
  watch: {
    'filter_auto.brand': () => {
      this.getAutos();
    },
  },
  created() {
    this.getBrands();
    this.getAutos();
    this.load_filter_data();
  },
};
</script>

<style scoped>

</style>
