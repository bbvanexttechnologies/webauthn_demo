<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>
<script>
// @ is an alias to /src

export default {
  name: 'Home',
  data: () => ({
    //
  }),
  mounted() {
    console.log(localStorage.getItem('isAuth'));
    console.log(localStorage.getItem('token'));

  },
};

</script>
