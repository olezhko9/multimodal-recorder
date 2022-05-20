<template xmlns="http://www.w3.org/1999/html">
  <div>
    <b-breadcrumb size="is-medium">
      <b-breadcrumb-item tag='router-link' to="/">Исследования [{{ research && research.name }}]</b-breadcrumb-item>
      <b-breadcrumb-item
        tag='router-link'
        :to="{ path: '/researches/research/subjects', query: {researchId} }">
        Испытуемые [{{ subjectName(subjectId) }}]
      </b-breadcrumb-item>
      <b-breadcrumb-item
        tag='router-link'
        :to="{ path: '/researches/research/records', query: {researchId, subjectId} }">
        Записи
      </b-breadcrumb-item>
      <b-breadcrumb-item active>Новая запись</b-breadcrumb-item>
    </b-breadcrumb>

    <section v-if="recordState !== 'ACTIVE'" id="record-prepare">
      <div v-if="research" class="mb-4">
        <div v-if="researchDevices && researchDevices.length">
          <span class="label mb-3">Устройства</span>
          <div class="columns is-multiline">
            <div
              v-for="(device, index) in researchDevices"
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
                        :disabled="recordState === 'ACTIVE'"
                        @click="onStopDeviceClick(device)">
                      </b-button>
                    </b-tooltip>
                  </div>
                </div>
              </div>
            </div>

            <device-settings-modal
              :device="modalDevice"
              @close="modalDevice = null"
              @save="onSaveSettingsClick"
            />
          </div>

          <div class="buttons">
            <b-button
              v-if="startedDevices.length === 0"
              type="is-primary"
              icon-left="play"
              @click="onStartDeviceClick(null)">
              Запустить все устройства
            </b-button>
            <b-button
              v-else-if="startedDevices.length === researchDevices.length"
              :disabled="recordState === 'ACTIVE'"
              type="is-danger"
              icon-left="stop"
              @click="onStopDeviceClick(null)">
              Остановить все устройства
            </b-button>
          </div>
        </div>
      </div>

      <b-message v-if="!canRecord" type="is-danger">
        Запустите все устройства, чтобы иметь возможность начать запись
      </b-message>
    </section>
    <section v-else>
      <iframe
        ref="frame"
        v-if="frameSrc"
        :src="frameSrc"
        frameborder="0"
        class="box"
        @load="onFrameLoaded">
      </iframe>
    </section>

    <div class="buttons buttons--space-btw mt-4">
      <b-button
        type="is-danger"
        outlined
        tag="router-link"
        :to="{ path: '/researches/research/records', query: { researchId, subjectId } }">
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
        type="is-danger"
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
import lodash from "lodash"
import DeviceSettingsModal from "@/components/DeviceSettingsModal"

export default {
  name: "index",
  components: {
    DeviceSettingsModal,
  },

  data() {
    return {
      research: null,
      modalDevice: null,
      researchDevices: [],

      frameSrc: '',
      frameLoaded: false,
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
    ...mapState('subject', {
      subjects: state => state.subjects,
    }),
    ...mapGetters('research', [
      'researchById'
    ]),
    ...mapGetters('device', [
      'isDeviceStarted'
    ]),
    ...mapGetters('subject', [
      'subjectName'
    ]),

    researchId() {
      return this.$route.query.researchId
    },

    subjectId() {
      return this.$route.query.subjectId
    },

    canRecord() {
      return this.research && this.research.devices.length === this.startedDevices.length
    }
  },

  async mounted() {
    !this.devices.length && await this.getDevices()
    !this.researches.length && await this.getResearches()
    !this.subjects.length && await this.getSubjects({ researchId: this.researchId })

    this.research = this.researchById(this.researchId)
    this.researchDevices = lodash.cloneDeep(this.research.devices)
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
    ...mapActions('subject', [
      'getSubjects',
    ]),

    @notifyAfter('Успешно')
    async onStartDeviceClick(device) {
      if (!device) {
        // запускаем все устройства
        return this.startDevice(this.researchDevices)
      } else {
        return this.startDevice(device)
      }
    },

    @notifyAfter('Успешно')
    async onStopDeviceClick(device) {
      if (!device) {
        return this.stopDevice(this.researchDevices.map(device => ({ device_id: device.device_id })))
      }
      return this.stopDevice({ device_id: device.device_id })
    },

    onFrameLoaded() {
      const frame = this.$refs.frame
      const msg = JSON.stringify({
        research: this.research
      })
      frame.contentWindow.postMessage(msg, '*')
      this.frameLoaded = true
      console.log('frame loaded')
    },

    loadFrame() {
      this.frameSrc = this.$axios.defaults.baseURL
        + '/test/index.html/'
        + '?rand=' + Math.round(Math.random() * 10000000) // to prevent caching
    },

    @notifyAfter('Запись начата')
    async onStartRecordClick() {
      this.loadFrame()
      return this.startRecord({ researchId: this.researchId, subjectId: this.subjectId })
    },

    @notifyAfter('Запись остановлена')
    async onStopRecordClick() {
      return this.stopRecord()
    },

    onSaveSettingsClick(deviceSettings) {
      this.researchDevices = this.researchDevices.map(device => {
        if (device._id === this.modalDevice._id) {
          return {
            ...device,
            settings: deviceSettings
          }
        }
        return device
      })
      this.modalDevice = null
    },

    openDeviceWindow(device) {
      window.open('/devices' + (device.device_id === 'camera' ? '/camera' : '/eeg'), '_blank')
    }
  }
}
</script>

<style lang="css" scoped>
  iframe {
    width: 100%;
    min-height: 500px;
    padding: 0;
  }
</style>
