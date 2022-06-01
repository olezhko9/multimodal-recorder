<template>
  <div>
    <h1 class="title is-4">Начать новое исследование</h1>

    <b-tabs>
      <b-tab-item label="Основное">
        <b-field label="Название">
          <b-input v-model="research.name" placeholder="Мое исследование"></b-input>
        </b-field>

        <b-field label="Описание">
          <b-input v-model="research.description" type="textarea"></b-input>
        </b-field>

        <b-field label="Фрейм эксперимента">
          <b-select v-model="research.frame" placeholder="Выберите виртуальный стенд" expanded>
            <option v-for="frame in frames" :key="frame" :value="frame">{{ frame }}</option>
          </b-select>
        </b-field>
      </b-tab-item>

      <b-tab-item label="Устройства">
        <b-field label="Устройства">
          <device-selector :devices="devices" @update="onDevicesUpdate"/>
        </b-field>
      </b-tab-item>

      <b-tab-item label="Форма создания испытуемого">
        <template v-for="(field, index) in research.subjectForm">
          <b-field grouped>
            <b-field label="Имя параметра" expanded>
              <b-input v-model="field.name" expanded></b-input>
            </b-field>
            <b-field label="Тип параметра" expanded>
              <b-select v-model="field.type" expanded>
                <option value="string">Строка</option>
                <option value="number">Число</option>
                <option value="boolean">Да / Нет</option>
                <option value="select">Выбор из списка</option>
              </b-select>
            </b-field>
            <b-button
              type="is-danger"
              icon-left="delete"
              class="is-flex is-align-self-flex-end"
              @click="removeSubjectField(index)">
            </b-button>
          </b-field>
          <b-field v-if="field.type === 'select'" label="Варианты">
            <b-taginput v-model="field.options" type="is-primary"></b-taginput>
          </b-field>
          <hr>
        </template>
        <b-button
          type="is-primary"
          icon-left="plus"
          @click="addSubjectField">
          Добавить поле
        </b-button>
      </b-tab-item>
    </b-tabs>

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
        devices: [],
        subjectForm: [
          { name: 'Имя', type: 'string' },
          { name: 'Возраст', type: 'number' },
          { name: 'Пол', type: 'select', options: ["Мужчина", "Женщина"] },
        ],
        frame: null,

        pipelines: [
          {
            deivce_id: 'camera',
            pipeline: [
              {
                method: 'DataFilter.perform_bandstop',
                args: {
                  'center_freq': 15,
                  'band_width': 6.0,
                  'order': 4,
                  'filter_type': 'BESSEL',
                  'ripple': 0
                }
              }
            ]
          }
        ]
      },

      frames: [],
    }
  },

  computed: {
    ...mapState('device', {
      devices: state => state.devices,
    }),
  },

  async mounted() {
    !this.devices.length && await this.getDevices()
    this.frames = await this.$axios.$get('/frame')
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
      this.research.subjectForm = this.research.subjectForm.filter(field => !!field.name)
      await this.createResearch(this.research)
      await this.$router.push('/researches')
    },

    removeSubjectField(fieldIndex) {
      this.research.subjectForm.splice(fieldIndex, 1)
    },

    addSubjectField() {
      this.research.subjectForm.push({
        name: '',
        type: 'string'
      })
    }
  },
}
</script>

<style scoped>

</style>
