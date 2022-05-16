<template>
  <div>
    <b-select
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

    <div v-if="selectedDevices.length" class="mt-4">
      <div class="columns is-multiline">
        <div
          v-for="(device, index) in selectedDevices"
          :key="device.id"
          class="column is-6">
          <div class="box">
            <div class="box-body">
              <div class="device-card__header">
                <b>{{ device.name }}</b>
              </div>
              <div class="device-card__buttons">
                <b-button
                  type="is-primary"
                  icon-left="cog"
                  @click="modalDevice = device">
                </b-button>
                <b-button
                  type="is-danger"
                  icon-left="delete"
                  @click="removeSelectedDevice(index)">
                </b-button>
              </div>
            </div>
          </div>
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
              <b-select
                v-if="setting.type === 'select'"
                v-model="setting.value"
                expanded>
                <option v-for="opt in setting.options" :value="opt">{{ opt }}</option>
              </b-select>
              <b-input
                v-else
                v-model="setting.value"
                expanded>
              </b-input>
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
  </div>
</template>

<script>
export default {
  name: "DeviceSelector",

  props: {
    devices: {
      type: Array,
      default: () => []
    }
  },

  data() {
    return {
      selectedDevices: [],
      modalDevice: null,
    }
  },

  computed: {
    notSelectedDevices() {
      return this.devices.filter(device => !this.selectedDevices.find(d => d.name === device.name))
    }
  },

  methods: {
    onDeviceSelect(device) {
      if (device) {
        for (let setting of device.settings) {
          setting.value = setting.default
        }
        this.selectedDevices.push(device)
        this.onDevicesUpdate()
      }
    },

    closeSettingsModal() {
      this.modalDevice = null
    },

    removeSelectedDevice(deviceIndex) {
      this.selectedDevices.splice(deviceIndex, 1)
      this.onDevicesUpdate()
    },

    onDevicesUpdate() {
      this.$emit('update', this.selectedDevices)
    }
  }
}
</script>

<style scoped>

</style>
