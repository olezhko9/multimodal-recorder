<template>
  <div>
    <b-breadcrumb size="is-medium">
      <b-breadcrumb-item active>Устройства</b-breadcrumb-item>
    </b-breadcrumb>

    <div class="buttons">
      <b-button type="is-primary" icon-left="plus">Новое устройство</b-button>
    </div>

    <div class="columns is-multiline">
      <div v-for="device in devices" :key="device.device_id" class="column is-6">
        <div class="box">
          <div class="box-body">
            <div class="device-card__header">
              <b>{{ device.name }}</b>
            </div>
            <div class="device-card__buttons">
              <b-button type="is-danger" icon-left="delete" @click="deleteDevice(device.device_id)"></b-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex"

export default {
  name: "Devices",

  computed: {
    ...mapState('device', {
      devices: state => state.devices,
    }),
  },

  async mounted() {
    !this.devices.length && await this.getDevices()
  },

  methods: {
    ...mapActions('device', [
      'getDevices',
      'deleteDevice',
    ])
  }
}
</script>

<style scoped>

</style>
