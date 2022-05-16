<template>
  <div>
    <h1 class="title is-4">Начать новое исследование</h1>

    <b-field label="Название">
      <b-input v-model="research.name"></b-input>
    </b-field>

    <b-field label="Описание">
      <b-input v-model="research.description" type="textarea"></b-input>
    </b-field>

    <b-field label="Устройства">
      <device-selector :devices="devices" @update="onDevicesUpdate"/>
    </b-field>

    <div class="buttons buttons--space-btw">
      <b-button
        type="is-danger"
        outlined
        tag="router-link"
        :to="{ path: '/researches' }">
        Назад
      </b-button>
      <b-button type="is-primary" @click="onSaveResearchClick">Начать исследование</b-button>
    </div>
  </div>
</template>

<script>
import DeviceSelector from "@/components/DeviceSelector"
import { mapActions, mapState } from "vuex"

export default {
  name: "research",
  components: {
    DeviceSelector
  },

  data() {
    return {
      research: {
        name: '',
        description: '',
        devices: []
      }
    }
  },

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
    ]),
    ...mapActions('research', [
      'createResearch'
    ]),

    onDevicesUpdate(devices) {
      this.research.devices = devices
    },

    async onSaveResearchClick() {
      await this.createResearch(this.research)
      await this.$router.push('/researches')
    }
  },
}
</script>

<style scoped>

</style>
