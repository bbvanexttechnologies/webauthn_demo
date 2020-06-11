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
                <v-toolbar-title>Login</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form v-model="valid">
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
                <router-link to="/register">
                Register
                </router-link>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="submit">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>

  const axios = require('axios')
  export default {
    name: 'LoginForm',
    data: () => ({
      valid: false,
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+/.test(v) || 'E-mail must be valid',
      ],
    }),
    methods: {
      submit(){
        if (this.valid){
          axios.post('http://localhost:5000/login/init', {
            username: this.email
          })
          .then( async function (response) {
            console.log('challenge',response)
            const transformedCredentialRequestOptions = webauthn_tools.transformCredentialRequestOptions(
                response.data);

            let credential;
            try {
                credential = await navigator.credentials.get({
                publicKey: transformedCredentialRequestOptions,
              });
            } catch (err) {
                return console.error("Error when creating credential:", err);
            }
            console.log('credential',credential)
            let transformAssertionForServer;
            transformAssertionForServer = webauthn_tools.transformAssertionForServer(credential)
            console.log("transformAssertionForServer",transformAssertionForServer)
            axios.post('http://localhost:5000/login/end', {
              AuthenticatorAttestationResponse: transformAssertionForServer
            })
            .then( async function (response) {
              console.log('end',response)
              localStorage.setItem('token',response.data.jwt)
              localStorage.setItem('isAuth',"true")
              localStorage.setItem('username',response.data.username)

            })
            .catch(err => {
                console.log(err)
                localStorage.setItem('isAuth',"false")
                localStorage.setItem('token','')
                localStorage.setItem('username','')
            })

          })


        }
      }
    }
  }
  var webauthn_tools = require('../utils/webauthn.js');
</script>
