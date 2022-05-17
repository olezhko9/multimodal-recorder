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

    <device-settings-modal
      :device="modalDevice"
      @close="closeSettingsModal"
      @save="onSaveSettingsClick"
    />
  </div>
</template>

<script>
import DeviceSettingsModal from "@/components/DeviceSettingsModal"
import lodash from 'lodash'

export default {
  name: "DeviceSelector",
  components: {
    DeviceSettingsModal,
  },

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
        this.selectedDevices.push(lodash.cloneDeep(device))
        this.onDevicesUpdate()
      }
    },

    closeSettingsModal() {
      this.modalDevice = null
    },

    onSaveSettingsClick(deviceSettings) {
      this.selectedDevices = this.selectedDevices.map(device => {
        if (device._id === this.modalDevice._id) {
          return {
            ...device,
            settings: deviceSettings
          }
        }
        return device
      })
      this.closeSettingsModal()
      this.onDevicesUpdate()
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
