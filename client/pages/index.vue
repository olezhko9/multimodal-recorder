<template>
  <div>
    <h1 class="title is-4">Метод и средства для сбора и первичной обработки мультимодальных данных, собранных с помощью
      различных нейроинтерфейсов</h1>

    <b-tabs type="is-boxed">
      <b-tab-item label="Устройства">
        <b-field label="Добавить устройство">
          <b-select
            :value="selectDevice"
            placeholder="Выбрать устройство"
            expanded
            @input="onDeviceSelect">
            <option
              v-for="device in notSelectedDevices"
              :value="device"
              :key="device.name">
              {{ device.name }}
            </option>
          </b-select>
        </b-field>

        <div v-if="selectedDevices.length" class="mb-4">
          <span class="label">Выбранные устройства</span>
          <div
            v-for="device in selectedDevices"
            :key="device.id"
            class="box device-card">
            <div class="device-card__header">
              {{ device.name }}
            </div>
            <div class="device-card__buttons">
              <b-button type="is-primary" icon-left="cog" @click="modalDevice = device"></b-button>
              <b-button type="is-danger" icon-left="delete"></b-button>
            </div>
          </div>
        </div>

        <b-modal
          :active="!!modalDevice"
          trap-focus
          has-modal-card
          :destroy-on-hide="true"
          aria-modal
          @close="modalDevice = null">
          <form v-if="modalDevice">
            <div class="modal-card" style="width: 640px">
              <header class="modal-card-head">
                <p class="modal-card-title">Настройки {{ modalDevice.name }}</p>
              </header>
              <section class="modal-card-body">
                <b-field v-for="setting in modalDevice.settings" :key="setting.name" :label="setting.label">
                  <b-input v-model="setting.value" expanded></b-input>
                </b-field>
              </section>
              <footer class="modal-card-foot">
                <b-button
                  label="Закрыть"
                  type="is-danger"
                  @click="closeSettingsModal"/>
                <b-button
                  label="Сохранить"
                  type="is-primary"
                  @click="closeSettingsModal"/>
              </footer>
            </div>
          </form>
        </b-modal>
      </b-tab-item>

      <b-tab-item label="Настройки"></b-tab-item>
    </b-tabs>

    <div v-if="selectedDevices.length" class="buttons">
      <b-button v-if="readyState !== 'ACTIVE'" type="is-primary" @click="startRecord">Начать запись</b-button>
      <b-button v-if="readyState === 'ACTIVE'" type="is-primary" @click="pauseRecord">Приостановить запись</b-button>
      <b-button v-if="readyState === 'PAUSED'" type="is-primary" @click="unpauseRecord">Возобновить запись</b-button>
      <b-button v-if="readyState === 'ACTIVE'" type="is-primary" @click="stopRecord">Остановить запись</b-button>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: "index",

  data() {
    return {
      devices: [],
      selectDevice: null,
      selectedDevices: [],
      readyState: 'INACTIVE', // INACTIVE, ACTIVE, PAUSED, STOPPED

      modalDevice: null,
    }
  },

  computed: {
    notSelectedDevices() {
      return this.devices.filter(device => !this.selectedDevices.find(d => d.name === device.name))
    }
  },

  watch: {
    readyState(newState) {
      this.setStatus(newState)
    }
  },

  async mounted() {
    this.devices = await this.$axios.$get("http://127.0.0.1:5000/devices")
  },

  methods: {
    ...mapMutations('recorder', {
      setStatus: 'SET_STATUS',
    }),

    onDeviceSelect(device) {
      if (device) {
        for (let setting of device.settings) {
          setting.value = setting.default
        }
        this.selectedDevices.push(device)
      }
    },

    async startRecord() {
      const result = await this.$axios.$post("http://127.0.0.1:5000/record/start", this.selectedDevices)
      if (result === true) {
        this.readyState = 'ACTIVE'
      }
    },

    async pauseRecord() {
      const result = await this.$axios.$post("http://127.0.0.1:5000/record/pause", {})
      if (result === true) {
        this.readyState = 'PAUSED'
      }
    },

    async unpauseRecord() {
      const result = await this.$axios.$post("http://127.0.0.1:5000/record/unpause", {})
      if (result === true) {
        this.readyState = 'ACTIVE'
      }
    },

    async stopRecord() {
      const result = await this.$axios.$post("http://127.0.0.1:5000/record/stop", {})
      if (result === true) {
        this.readyState = 'STOPPED'
      }
    },

    closeSettingsModal() {
      this.modalDevice = null
    }
  }
}
</script>

<style lang="css" scoped>
.device-card {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
</style>
