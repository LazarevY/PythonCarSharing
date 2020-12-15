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
          <li class="nav-item active">
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
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Brands</h1>
          <hr>
          <br><br>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.brand-modal>Add Brand</button>

          <br><br>
          <table class="table table-hover">
            <thead>
            <tr>
              <th scope="col">Brand</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(brand, index) in brands" :key="index">
              <td>{{ brand.name }}</td>
              <td>
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.brand-update-modal
                  @click="editBrand(brand)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="deleteBrand(brand)">
                  Delete
                </button>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>

      <b-modal ref="addBrandModal"
               id="brand-modal"
               title="Add a new brand of auto"
               hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-title-group"
                        label="Brand name:"
                        label-for="form-brand-input">
            <b-form-input id="form-brand-input"
                          type="text"
                          v-model="addBrandForm.brand_name"
                          required
                          placeholder="Enter brand name">
            </b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>

      <b-modal ref="editBrandModal"
               id="brand-update-modal"
               title="Update"
               hide-footer>
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group id="form-title-edit-group"
                        label="New brand name:"
                        label-for="form-brand-edit-input">
            <b-form-input id="form-title-edit-input"
                          type="text"
                          v-model="editForm.new_name"
                          required
                          placeholder="Enter title">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-author-edit-group"
                        label="Old name:"
                        label-for="form-author-edit-input"
                        hidden>
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.old_name"
                          required
                          readonly>
            </b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-form>
      </b-modal>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Brands",
  data() {
    return {
      brands: [],
      addBrandForm: {
        brand_name: '',
      },
      editForm: {
        old_name: '',
        new_name: '',
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
    addBrand(payload) {
      const path = 'http://localhost:5000/services/auto/brands';
      axios.post(path, payload)
        .then(() => {
          this.getBrands();
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.log(error);
          this.getBrands();
        });
    },
    updateBrand(payload) {
      const path = 'http://localhost:5000/services/auto/brands';
      axios.put(path, payload)
        .then(() => {
          this.getBrands();
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
          this.getBrands();
        });
    },
    editBrand(brand) {
      this.editForm.new_name = brand.name;
      this.editForm.old_name = brand.name;
    },
    deleteBrand(brand) {
      const path = 'http://localhost:5000/services/auto/brands/remove';
      if (confirm("Delete brand " + brand.name + "?")) {
        const payload = {
          brand_name: brand.name,
        };
        axios.post(path, payload)
          .then((resp) => {
            this.getBrands();
          })
          .catch((error) => {
            console.error(error);
            this.getBrands();
          });
      }
    },
    initForm() {
      this.addBrandForm.brand_name = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBrandModal.hide();
      const payload = {
        brand_name: this.addBrandForm.brand_name,
      };
      this.addBrand(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBrandModal.hide();
      const payload = {
        new_name: this.editForm.new_name,
        old_name: this.editForm.old_name,
      };
      this.updateBrand(payload);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBrandModal.hide();
      this.initForm();
      this.getBrands();
    },
  },
  created() {
    this.getBrands();
  },
};
</script>

