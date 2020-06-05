<template>
  <v-app id="inspire">
    <v-content>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>Register</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form v-model="valid">
                  <v-text-field
                    label="Name"
                    v-model="name"
                    prepend-icon="mdi-account"
                    :rules="nameRules"
                    type="text"
                    :counter="10"
                  ></v-text-field>
                  <v-text-field
                    label="Surname"
                    v-model="surname"
                    prepend-icon="mdi-account"
                    :rules="nameRules"
                    type="text"
                    required
                    :counter="10"
                  ></v-text-field>
                  <v-text-field
                    label="Email"
                    v-model="email"
                    :rules="emailRules"
                    prepend-icon="mdi-email"
                    type="text"
                    required
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <router-link to="/login">
                Back
                </router-link>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="submit">Register</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  const axios = require('axios');

  export default {
    name: 'RegisterForm',
    data: () => ({
      valid: false,
      name: '',
      surname: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 10 || 'Name must be less than 10 characters',
      ],
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+/.test(v) || 'E-mail must be valid',
      ],
    }),
    methods: {
      submit(){

        if (this.valid){
          //STEP 0 -> Initial request, sents user data to FIDO server
          axios.post('http://localhost:5000/registration/init', {
            name: this.name,
            surname: this.surname,
            email: this.email
        })
        .then( async function (response) {
            console.log("STEP 2",response.data)
            //STEP 2 -> authenticatorMakeCredential
            /*
            The parameters received are passed to a function create() that returns a promise that resolves in a object called
            PublicKeyCredential which its returned by the authenticator. It contains an object called AuthenticatorAttestationResponse
            which contains information including the public key.
            When the browser calls to authenticatorMakeCredential() it validates the parameters and it fills some values.
            One of the most important parameters is the origin. Those parameters are send to the Authenticator with a SHA-256 hash of the
            clientDataJSON Object to test deception

            */

            const credential = await create({
              publicKey: response.data
            });

            //STEP 3 -> Creation of keys
            /*
            The Authenticator creates a new pair of keys.
            It first ask the user to verify himself using for instance his fingerprint. After that it creates a new pair
            of asymetric keys and stores the private key in a secure way.
            The public key is signed with the private key of the authenticator which is trusted and can be validated.
            */

            //STEP 4 -> The Authenticator returns the data to the Browser
            console.log("STEP 4",credential)

            //STEP 5 -> The browser creates the final data and sends them to the server: AuthenticatorAttestationResponse o
            axios.post('http://localhost:5000/registration/end', {
              AuthenticatorAttestationResponse: credential
            })
            .then( async function (response) {
              console.log(response)
            })
            .catch(function (error) {
                console.log(error)
            });
        })
        .catch(function (error) {
            console.log(error)
        });


        }
      }
    }
  }
  import {create} from '@github/webauthn-json';
</script>
