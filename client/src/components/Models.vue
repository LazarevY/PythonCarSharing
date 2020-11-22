<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Models</h1>
        <hr>
        <br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.model-modal>Add Model</button>

        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Brand</th>
            <th scope="col">Model</th>
            <th scope="col">Category</th>
            <th scope="col">Price</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(model, index) in models" :key="index">
            <td>{{ model.brand_name }}</td>
            <td>{{ model.model_name }}</td>
            <td>{{ model.category_name }}</td>
            <td>{{ model.price }}</td>
            <td>
              <button
                type="button"
                class="btn btn-warning btn-sm"
                v-b-modal.model-update-modal
                @click="editModel(model)">
                Update
              </button>
              <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="deleteModel(model)">
                Delete
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addModelModal"
             id="model-modal"
             title="Add a new model of auto"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-brand-group"
                      label="Brand: "
                      label-for="form-brand-select">
          <v-selectize id="form-brand-select"
                       :options="getBrandOptions()"
                       v-model="addModelForm.brand_name_select"
                       placeholder="Select brand"
                       required>
          </v-selectize>
        </b-form-group>
        <b-form-group id="form-category-group"
                      label="Category: "
                      label-for="form-category-select">
          <v-selectize id="form-category-select"
                       :options="categories_options"
                       v-model="addModelForm.model_category_name_select"
                       placeholder="Select category"
                       aria-required="true">
          </v-selectize>
        </b-form-group>
        <b-form-group id="form-title-group"
                      label="Model name:"
                      label-for="form-model-input">
          <b-form-input id="form-model-input"
                        type="text"
                        v-model="addModelForm.model_name"
                        required
                        placeholder="Enter model name">
          </b-form-input>
        </b-form-group>

        <b-form-group label-for="form-price-input"
                      label="Price: ">
          <b-form-input id="form-price-input"
                        type="number"
                        v-model.number="addModelForm.price"
                        required
                        placeholder="Price of model">

          </b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editModelModal"
             id="model-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-edit-brand-group"
                      label="Brand: "
                      label-for="form-edit-brand-select">
          <v-selectize id="form-edit-brand-select"
                       :options="getBrandOptions()"
                       v-model="editForm.new_brand_name"
                       placeholder="Select brand if needed"
                       required>
          </v-selectize>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="New model name:"
                      label-for="form-model-edit-input">
          <b-form-input id="form-model-edit-input"
                        type="text"
                        v-model="editForm.new_model_name"
                        required>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-edit-category-group"
                      label="Category: "
                      label-for="form-edit-brand-select">
          <v-selectize id="form-edit-category-select"
                       :options="categories_options"
                       v-model="editForm.new_category_name"
                       placeholder="Select category"
                       required>
          </v-selectize>
        </b-form-group>
        <b-form-group label-for="form-edit-price-input"
                      label="Price: ">
          <b-form-input id="form-edit-price-input"
                        type="number"
                        v-model.number="editForm.price"
                        required
                        placeholder="Price of model">

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
import VSelectize from '@isneezy/vue-selectize'

export default {
  name: "Models",
  data() {
    return {
      models: [],
      brands: [],
      brand_options: [],
      categories_options: [],
      addModelForm: {
        brand_name_select: '',
        model_name: '',
        model_category_name_select: '',
        price: 0,
      },
      editForm: {
        old_brand_name: '',
        new_brand_name: '',
        old_model_name: '',
        new_model_name: '',
        old_category_name: '',
        new_category_name: '',
        price: 0,
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
        options.push({label: brand.name, code: brand.name})
      });
      return options;
    },
    getCategories() {
      const path = 'http://localhost:5000/services/auto/categories';
      axios.get(path)
        .then((res) => {
          res.data.categories.forEach(category => {
            this.categories_options.push({label: category.name, code: category.name})
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },

    getModels() {
      const path = 'http://localhost:5000/services/auto/models';
      axios.get(path)
        .then((res) => {
          this.models = res.data.models;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addModel(payload) {
      const path = 'http://localhost:5000/services/auto/models';
      axios.post(path, payload)
        .then(() => {
          this.getModels();
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.log(error);
          this.getModels();
        });
    },
    updateModel(payload) {
      const path = 'http://localhost:5000/services/auto/models';
      axios.put(path, payload)
        .then(() => {
          this.getModels();
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
          this.getModels();
        });
    },
    editModel(model) {
      this.editForm.new_brand_name = {label: model.brand_name, code: model.brand_name}
      this.editForm.old_brand_name = model.brand_name;
      this.editForm.new_model_name = model.model_name;
      this.editForm.old_model_name = model.model_name;
      this.editForm.new_category_name = {label: model.category_name, code: model.category_name};
      this.editForm.old_category_name = model.category_name;
      this.editForm.price = model.price;
    },
    deleteModel(model) {
      const path = 'http://localhost:5000/services/auto/models/remove';
      if (confirm("Delete model " + model.model_name + "?")) {
        const payload = {
          brand_name: model.brand_name,
          model_name: model.model_name,
        };
        axios.post(path, payload)
          .then((resp) => {
            this.getModels();
          })
          .catch((error) => {
            console.error(error);
            this.getModels();
          });
      }
    },
    initForm() {
      this.addModelForm.brand_name_select = null;
      this.addModelForm.model_name = '';
      this.addModelForm.model_category_name_select = null;
      this.addModelForm.price = 1000;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addModelModal.hide();
      const payload = {
        brand_name: this.addModelForm.brand_name_select.code,
        model_name: this.addModelForm.model_name,
        category_name: this.addModelForm.model_category_name_select.code,
        price: this.addModelForm.price,
      };
      this.addModel(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModelModal.hide();
      const payload = {
        new_brand_name: this.editForm.new_brand_name.code,
        old_brand_name: this.editForm.old_brand_name,
        new_model_name: this.editForm.new_model_name,
        old_model_name: this.editForm.old_model_name,
        new_category_name: this.editForm.new_category_name.code,
        price: this.editForm.price,
      };
      this.updateModel(payload);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addModelModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModelModal.hide();
      this.initForm();
      this.getModels();
    },
  },
  created() {
    this.getModels();
    this.getBrands();
    this.getCategories();
  },
};
</script>

<style scoped>

</style>
