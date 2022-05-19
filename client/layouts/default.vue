<template>
  <div class="page">
    <b-navbar type="is-primary">
      <template #brand>
        <b-navbar-item tag="a" href="/">
          <img src="/logo.png">
        </b-navbar-item>
      </template>
      <template #start>
        <b-navbar-item tag="router-link" :to="{ path: '/researches' }">
          Исследования
        </b-navbar-item>
        <b-navbar-dropdown label="Устройства">
          <b-navbar-item tag="router-link" :to="{ path: '/devices/camera' }">
            Камера
          </b-navbar-item>
          <b-navbar-item tag="router-link" :to="{ path: '/devices/eeg' }">
            EEG
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-item href="#">
          Настройки
        </b-navbar-item>
        <b-navbar-item tag="router-link" :to="{ path: '/about' }">
          О приложении
        </b-navbar-item>
      </template>
    </b-navbar>

    <div class="container is-max-desktop">
      <Nuxt />
    </div>

    <div class="statusbar">
      <span>{{ recordState }}</span>
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
    ...mapState('record', {
      recordState: state => state.recordState,
    })
  }
}
</script>

<style lang="scss">
.page {
  min-height: 100vh;
}

.container {
  padding: 2.5rem 2rem;
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
