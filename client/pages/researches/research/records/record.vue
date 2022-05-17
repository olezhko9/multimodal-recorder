<template>
  <div>
    <h1 class="title is-4">Новая запись</h1>

    <div v-if="research" class="mb-4">
      <div v-if="research.devices && research.devices.length">
        <span class="label mb-3">Устройства</span>
        <div class="columns is-multiline">
          <div
            v-for="(device, index) in research.devices"
            :key="device.id"
            class="column is-6">
            <div class="box">
              <div class="box-body">
                <div class="device-card__header">
                  <b>{{ device.name }}</b>
                </div>
                <div class="device-card__buttons">
                  <b-button
                    :disabled="isDeviceStarted(device.device_id)"
                    type="is-primary"
                    icon-left="cog"
                    @click="modalDevice = device">
                  </b-button>
                  <b-button
                    v-if="isDeviceStarted(device.device_id)"
                    type="is-primary"
                    icon-left="eye"
                    @click="openDeviceWindow(device)">
                  </b-button>
                  <b-tooltip
                    v-if="!isDeviceStarted(device.device_id)"
                    label="Запустить устройство">
                    <b-button
                      type="is-primary"
                      icon-left="play"
                      @click="onStartDeviceClick(device)">
                    </b-button>
                  </b-tooltip>
                  <b-tooltip v-else label="Остановить устройство">
                    <b-button
                      type="is-danger"
                      icon-left="stop"
                      @click="onStopDeviceClick(device)">
                    </b-button>
                  </b-tooltip>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <b-message v-if="!canRecord" type="is-danger">
      Запустите все устройства, чтобы иметь возможность начать запись
    </b-message>

    <div class="buttons buttons--space-btw">
      <b-button
        type="is-danger"
        outlined
        tag="router-link"
        :to="{ path: '/researches/research/records', query: { researchId } }">
        Назад
      </b-button>
      <b-button
        v-if="recordState !== 'ACTIVE'"
        :disabled="!canRecord"
        type="is-primary"
        icon-left="play"
        @click="onStartRecordClick">
        Начать запись
      </b-button>
      <b-button
        v-if="recordState === 'ACTIVE'"
        type="is-primary"
        icon-left="stop"
        @click="onStopRecordClick">
        Остановить запись
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import { notifyAfter } from "@/modules/notification-decorators"

export default {
  name: "index",

  data() {
    return {
      research: null,
      modalDevice: null,
    }
  },

  computed: {
    ...mapState('research', {
      researches: state => state.researches,
    }),
    ...mapState('device', {
      devices: state => state.devices,
      startedDevices: state => state.startedDevices,
    }),
    ...mapState('record', {
      recordState: state => state.recordState,
    }),
    ...mapGetters('research', [
      'researchById'
    ]),
    ...mapGetters('device', [
      'isDeviceStarted'
    ]),

    researchId() {
      return this.$route.query.researchId
    },

    canRecord() {
      return this.research && this.research.devices.length === this.startedDevices.length
    }
  },

  async mounted() {
    !this.devices.length && await this.getDevices()
    !this.researches.length && await this.getResearches()

    this.research = this.researchById(this.researchId)
  },

  methods: {
    ...mapActions('research', [
      'getResearches',
    ]),
    ...mapActions('device', [
      'getDevices',
      'startDevice',
      'stopDevice',
    ]),
    ...mapActions('record', [
      'startRecord',
      'stopRecord',
    ]),

    @notifyAfter('Успешно')
    async onStartDeviceClick(device) {
      return this.startDevice(device)
    },

    @notifyAfter('Успешно')
    async onStopDeviceClick(device) {
      return this.stopDevice({ deviceId: device.device_id })
    },

    @notifyAfter('Запись начата')
    async onStartRecordClick() {
      return this.startRecord({ researchId: this.researchId })
    },

    @notifyAfter('Запись остановлена')
    async onStopRecordClick() {
      return this.stopRecord()
    },

    openDeviceWindow(device) {
      window.open('/devices' + (device.device_id === 'camera' ? '/camera' : '/eeg'), '_blank')
    }
  }
}
</script>

<style lang="css" scoped>

</style>
