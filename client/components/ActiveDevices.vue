<template>
  <div class="is-flex is-flex-direction-row">
    <div v-if="devices.length" v-for="device_id in startedDevices" class="box is-marginless">
      <div class="box-body">
        <div class="device-card__header">
          <b>{{ deviceById(device_id).name }}</b>
        </div>
        <div class="device-card__buttons ml-2">
          <b-button
            type="is-primary"
            icon-left="eye"
            size="is-small"
            @click="openDeviceWindow(device_id)">
          </b-button>
          <b-button
            type="is-danger"
            icon-left="stop"
            size="is-small"
            @click="onStopDeviceClick(device_id)">
          </b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex"
import { notifyAfter } from "@/modules/notification-decorators"

export default {
  name: "ActiveDevices",

  computed: {
    ...mapState('device', {
      devices: state => state.devices,
      startedDevices: state => state.startedDevices,
    }),
    ...mapGetters('device', [
      'deviceById'
    ])
  },

  methods: {
    ...mapActions('device', [
      'stopDevice'
    ]),

    @notifyAfter('Успешно')
    async onStopDeviceClick(device_id) {
      return this.stopDevice({ device_id })
    },

    openDeviceWindow(device_id) {
      window.open('/devices/monitor?deviceId=' + device_id, '_blank')
    },
  }
}
</script>

<style scoped lang="scss">
.box {
  min-width: 200px;
  padding: 10px 15px;
  margin-left: 10px !important;
  border: 2px solid $primary;
}
</style>
