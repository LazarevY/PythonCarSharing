<template>
  <div class="container">

    <b-form @submit="signupSubmit" @reset="signupReset" class="w-100">

      <b-form-group label-for="signupPhone" invalid-feedback="Phone is 11 digits" label="Phone">
        <div class="error" v-if="!check_unique.phone">
          Phone number already exist in database
        </div>
        <b-form-input id="signupPhone"
                      type="number"
                      v-model="$v.signupForm.phone.$model"
                      :state="validateState($v.signupForm.phone)"
                      required
                      placeholder="Your phone">

        </b-form-input>
      </b-form-group>


      <b-form-group label="Name">
        <b-form-input id="signupName"
                      type="text"
                      v-model="signupForm.name"
                      required
                      placeholder="Your name">

        </b-form-input>
      </b-form-group>

      <b-form-group label="Last name">
        <b-form-input id="signupLastName"
                      type="text"
                      v-model="signupForm.lastName"
                      required
                      placeholder="Your last name">

        </b-form-input>
      </b-form-group>

      <div class="error" v-if="!check_unique.passport">
        Passport already exist in database
      </div>
      <b-form-group label-for="signupPassport" invalid-feedback="Passport is 10 digits" label="Passport">
        <b-form-input id="signupPassport"
                      type="number"
                      v-model="$v.signupForm.passport.$model"
                      :state="validateState($v.signupForm.passport)"
                      required
                      placeholder="Your passport">

        </b-form-input>
      </b-form-group>

      <div class="error" v-if="!check_unique.drive_license">
        License already exist in database
      </div>
      <b-form-group label-for="signupLicense" invalid-feedback="License is 10 digits" label="Drive license">
        <b-form-input id="signupLicense"
                      type="number"
                      v-model="$v.signupForm.drive_license.$model"
                      :state="validateState($v.signupForm.drive_license)"
                      required
                      placeholder="Your drive license">

        </b-form-input>
      </b-form-group>

      <b-form-group label-for="signupPassword"
                    invalid-feedback="Password more 5 sym!" label="Password">
        <b-form-input id="signupPassword"
                      type="password"
                      v-model="$v.signupForm.password.$model"
                      :state="validateState($v.signupForm.password)"
                      required
                      placeholder="Password (6 sym or more)">

        </b-form-input>
      </b-form-group>

      <b-form-group
        label-for="signupPasswordRepeat"
        invalid-feedback="Passwords must be same" label="Repeat password">
        <b-form-input id="signupPasswordRepeat"
                      type="password"
                      v-model="$v.signupForm.password_repeat.$model"
                      :state="validateState($v.signupForm.password_repeat)"
                      required
                      placeholder="Repeat password">

        </b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary" :disabled="$v.signupForm.$invalid">Register</b-button>

    </b-form>


    <br>
    <br>

    <div class="error" v-if="!check_login.status">
      {{ this.check_login.message }}
    </div>

    <b-form class="w-100" @submit="singinSubmit">
      <b-form-group invalid-feedback="Incorrect phone">
        <b-form-input id="signinPhone"
                      type="number"
                      v-model="$v.signinForm.phone.$model"
                      required
                      :state="validateState($v.signinForm.phone)"
                      placeholder="Your phone">

        </b-form-input>
      </b-form-group>

      <b-form-group invalid-feedback="Too few symbols">
        <b-form-input id="signinPassword"
                      type="password"
                      v-model="$v.signinForm.password.$model"
                      required
                      :state="validateState($v.signinForm.password)"
                      placeholder="Your password">

        </b-form-input>
      </b-form-group>
      <b-button variant="primary" type="submit" :disabled="$v.signinForm.$invalid">Log in</b-button>
    </b-form>
  </div>
</template>


<script>
import {maxLength, minLength, required, sameAs} from 'vuelidate/lib/validators'
import axios from "axios";
import Vue from "vue";

export default {

  name: "LogAndRegister",
  data() {
    return {
      signupForm: {
        phone: null,
        name: '',
        lastName: '',
        passport: null,
        drive_license: null,
        password: '',
        password_repeat: '',
      },
      signinForm: {
        phone: null,
        password: '',
      },
      check_unique: {
        phone: true,
        passport: true,
        drive_license: true,
        checked: 0
      },
      check_login: {
        status: true,
        message: ''
      }
    }
  },
  validations: {
    signupForm: {
      phone: {
        required,
        minLength: minLength(11),
        maxLength: maxLength(11)
      },
      passport: {
        required,
        minLength: minLength(10),
        maxLength: maxLength(10),
      },
      drive_license: {
        required,
        minLength: minLength(10),
        maxLength: maxLength(10),
      },
      password: {
        required,
        minLength: minLength(6)
      },
      password_repeat: {
        required,
        sameAsPassword: sameAs('password')
      }
    },
    signinForm: {
      phone: {
        required,
        minLength: minLength(11),
        maxLength: maxLength(11)
      },
      password: {
        required,
        minLength: minLength(6)
      },
    }
  },
  methods: {
    validateState(item) {
      const {$dirty, $error} = item
      return $dirty ? !$error : null
    },
    checkClientUniqueProperty(name, value) {
      const path = 'http://localhost:5000/register/check_unique';
      let res = false;
      axios.post(path, {name: name, value: value})
        .then((r) => {
          console.log()
          res = r.data.result;
          this.check_unique[name] = r.data.result;
        })
        .catch((error) => {
          console.error(error);
        });

      this.check_unique[name] = res;
      console.log(this.check_unique[name]);
      return this.check_unique[name];
    },
    signupSubmit() {

      this.check_unique.phone = true;
      this.check_unique.drive_license = true;
      this.check_unique.passport = true;

      let payload = {
        name: this.signupForm.name,
        lastName: this.signupForm.lastName,
        phone: this.signupForm.phone,
        passport: this.signupForm.passport,
        drive_license: this.signupForm.drive_license,
        password: this.signupForm.password
      };

      const path = 'http://localhost:5000/register';
      axios.post(path, payload)
        .then((resp) => {
          this.check_unique.phone = resp.data.unique.phone;
          this.check_unique.drive_license = resp.data.unique.drive_license;
          this.check_unique.passport = resp.data.unique.passport;
        })
        .catch((error) => {
          console.error(error);
        });

    },
    signupReset() {

    },
    singinSubmit() {
      this.check_login.status = true

      let payload = {
        phone: this.signinForm.phone,
        password: this.signinForm.password,
      };
      const path = 'http://localhost:5000/login';
      axios.post(path, payload)
        .then((resp) => {
          if (resp.data.logined === false) {
            this.check_login.message = resp.data.message;
            this.check_login.status = false;
            this.$router.push({name: 'LogAndRegister'})
          } else {
            this.check_login.status = true;
            Vue.$cookies.set('token', resp.data.token)
            this.$router.push({name: 'ClientMain'})
          }
        })
        .catch((error) => {
          console.error(error);
        });
    }
  },
  created() {
    if (Vue.$cookies.isKey('token'))
      this.$router.push({name: 'ClientMain'});
  }
}
</script>

<style scoped>

.error {
  color: red;
  margin-bottom: 4px;
}

</style>
