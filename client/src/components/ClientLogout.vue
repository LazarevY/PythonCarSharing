<template>

</template>

<script>
import Vue from "vue";

export default {
  name: "ClientLogout",
  created() {
    Vue.$cookies.remove('token');
    Vue.$cookies.remove('phone');
    this.$router.push({name: 'LogAndRegister'});
  }
}
</script>

<style scoped>

</style>
