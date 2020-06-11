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
                dark
                flat
              >
                <v-toolbar-title>HI {{username}}! You logged In using FIDO</v-toolbar-title>

                <v-spacer></v-spacer>
              </v-toolbar>

              <v-card-text>
                <v-card-subtitle>
                  Your JWT Token:
                </v-card-subtitle>
                <v-card-subtitle>
                  Note: The way you keep the session is not under FIDO scope. You can use differents methods different from JWT Tokens.
                </v-card-subtitle>
                  {{token}}
                  <v-spacer></v-spacer>
                  <v-spacer></v-spacer>
                  <v-spacer></v-spacer>
                  {{decoded}}

              </v-card-text>
              <v-card-actions>
              <v-btn color="primary" @click="submit">Logout</v-btn>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  data: () => ({

      token: '',
      username: '',
      decoded: '',

  }),
  mounted() {
    this.token = localStorage.getItem('token');
    this.username = localStorage.getItem('username')

  //  this.decoded = jwtDecode(this.token);
  //  console.log(this.decoded)
  },
  methods: {
    submit(){
      localStorage.setItem('token','')
      localStorage.setItem('isAuth',"false")
      this.token = localStorage.getItem('token');
      this.username = localStorage.getItem('username')
      this.decoded = ''

    }
  }
};
//var jwtDecode = require('jwt-decode');

</script>
