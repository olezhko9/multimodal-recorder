<template>
  <div class="page">
    <b-navbar type="is-primary">
      <template #brand>
        <b-navbar-item tag="router-link" :to="{ path: '/' }">
          <img src="/logo.png">
        </b-navbar-item>
      </template>
      <template #start>
        <b-navbar-item href="#">
          Исследования
        </b-navbar-item>
        <b-navbar-dropdown label="Устройства">
          <b-navbar-item tag="router-link" :to="{ path: '/camera' }">
            Камера
          </b-navbar-item>
          <b-navbar-item tag="router-link" :to="{ path: '/eeg' }">
            EEG
          </b-navbar-item>
        </b-navbar-dropdown>
      </template>
    </b-navbar>

    <div class="container is-max-desktop">
      <Nuxt />
    </div>

    <div class="statusbar">
      <span>{{ recorderState }}</span>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'DefaultLayout',
  data () {
    return {
      items: []
    }
  },

  computed: {
    ...mapState('recorder', {
      recorderState: state => state.status,
    })
  }
}
</script>

<style lang="scss">
.page {
  min-height: 100vh;
}

.container {
  padding: 2.5rem 0;
}

.statusbar {
  position: fixed;
  bottom: 0;
  width: 100%;
  padding: 3px 15px;
  min-height: 30px;
  background-color: $primary;
  color: white;
}
</style>
