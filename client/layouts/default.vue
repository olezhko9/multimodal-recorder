<template>
  <div class="page">
    <b-navbar type="is-primary">
      <template #brand>
        <b-navbar-item tag="a" href="/">
          <img src="/brain_logo.webp" class="logo">
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
      <Nuxt/>
    </div>

    <div class="statusbar">
      <div>
        <div v-if="recordState === 'ACTIVE'" class="ring-container mr-1">
          <div class="ringring"></div>
          <div class="circle"></div>
        </div>
        <b-icon v-else-if="recordState === 'PAUSED'" icon="pause" type="is-white" size="is-small"></b-icon>
        <span>Запись {{ recordStateTexts }}</span>
      </div>
      <active-devices class="devices-panel"/>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ActiveDevices from "@/components/ActiveDevices"

export default {
  name: 'DefaultLayout',
  components: {
    ActiveDevices,
  },

  data() {
    return {
      items: []
    }
  },

  computed: {
    ...mapState('record', {
      recordState: state => state.recordState,
    }),
    ...mapState('device', {
      startedDevices: state => state.startedDevices,
    }),

    recordStateTexts() {
      switch (this.recordState) {
        case 'INACTIVE':
        case 'STOPPED':
          return 'неактивна'
        case 'ACTIVE':
          return 'активна'
        case 'PAUSED':
          return 'приостановлена'
      }
    }
  }
}
</script>

<style lang="scss">
.page {
  min-height: 100vh;
}

.container {
  padding: 2.5rem 2rem 5rem;
}

.logo {
  -webkit-filter: invert(100%);
  filter: invert(100%);
}

.statusbar {
  position: fixed;
  bottom: 0;
  width: 100%;
  padding: 3px 15px;
  min-height: 30px;
  background-color: $primary;
  color: white;
  display: flex;
  justify-content: space-between;
}

.ring-container {
  position: relative;
  display: inline-block;
}

.circle {
  width: 12px;
  height: 12px;
  background-color: $success;
  border-radius: 50%;
}

.ringring {
  border: 3px solid #62bd19;
  -webkit-border-radius: 30px;
  height: 22px;
  width: 22px;
  -webkit-animation: pulsate 1s ease-out;
  -webkit-animation-iteration-count: infinite;
  opacity: 0.0;
  position: absolute;
  top: -5px;
  left: -5px;
}

@-webkit-keyframes pulsate {
  0% {
    -webkit-transform: scale(0.1, 0.1);
    opacity: 0.0;
  }
  50% {
    opacity: 1.0;
  }
  100% {
    -webkit-transform: scale(1.2, 1.2);
    opacity: 0.0;
  }
}

.devices-panel {
  position: absolute;
  bottom: 5px;
  right: 1rem;
}
</style>
