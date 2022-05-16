<template>
  <img :src="sseUrl" width="640" height="480">
</template>

<script>
export default {
  name: "camera",

  data() {
    return {
      sseUrl: 'http://127.0.0.1:5000/stream?device=camera'
    }
  },

  beforeRouteLeave(to, from, next) {
    this.sseUrl = null
    next()
  }
}
</script>

<style scoped>

</style>
