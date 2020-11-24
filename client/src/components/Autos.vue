<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Autos</h1>
        <hr>
        <br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.auto-modal>Add Auto</button>

        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Brand</th>
            <th scope="col">Model</th>
            <th scope="col">Registration number</th>
            <th scope="col">Mileage</th>
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
      addAutoForm: {
        model_id: 0,
        registration_number: '',
        mileage: 0,
        quality: 0,
      },
      editForm: {
        brand_name_select: null,
        old_model_id: 0,
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
            this.model_options.push({label: model.model_name, code: model.model_id})
          })
          this.editForm.new_model_id = this.model_options[0]
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getAutos() {
      const path = 'http://localhost:5000/services/auto/autos';
      axios.get(path)
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
      this.editForm.brand_name_select = auto.brand_name
      this.editForm.new_model_id = {label: auto.model_name, code: auto.model_id};
      this.editForm.old_model_id = auto.model_name;
      this.editForm.old_number = auto.number;
      this.editForm.new_number = auto.number;
      this.editForm.mileage = auto.mileage;
      this.editForm.quality = auto.quality;
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
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAutoModal.hide();
      const payload = {
        old_model_id: this.editForm.old_model_id,
        new_model_id: this.editForm.new_model_id.code,
        old_number: this.editForm.old_number,
        new_number: this.editForm.new_number,
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
  },
  created() {
    this.getBrands();
    this.getAutos();
  },
};
</script>

<style scoped>

</style>
