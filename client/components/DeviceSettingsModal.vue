<template>
  <b-modal
    :active="!!device"
    trap-focus
    has-modal-card
    :destroy-on-hide="true"
    aria-modal
    @close="onCloseClick">
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
              v-else-if="setting.type === 'number'"
              v-model.number="setting.value"
              expanded>
            </b-input>
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
            @click="onCloseClick"/>
          <b-button
            label="Сохранить"
            type="is-primary"
            @click="onSaveClick"/>
        </footer>
      </div>
    </form>
  </b-modal>
</template>

<script>
export default {
  name: "DeviceSettingsModal",

  props: {
    device: {
      type: Object,
    }
  },

  data() {
    return {
      modalDevice: JSON.parse(JSON.stringify(this.device))
    }
  },

  watch: {
    device(newDevice) {
      this.modalDevice = JSON.parse(JSON.stringify(newDevice))
    }
  },

  methods: {
    onCloseClick() {
      this.$emit('close')
    },

    onSaveClick() {
      this.$emit('save', this.modalDevice.settings)
    }
  }
}
</script>

<style scoped>

</style>
