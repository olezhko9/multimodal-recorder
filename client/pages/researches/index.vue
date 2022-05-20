<template>
  <div>
    <b-breadcrumb size="is-medium">
      <b-breadcrumb-item active>Мои исследования</b-breadcrumb-item>
    </b-breadcrumb>

    <div class="buttons">
      <b-button
        type="is-primary"
        icon-left="plus"
        tag="router-link"
        to="/researches/research">
        Новое исследование
      </b-button>
    </div>

    <div v-for="research in researches" :key="research.id" class="box">
      <div class="box-body">
        <div class="box-content">
          <b>{{ research.name }}</b>
          <p>{{ research.description }}</p>
          <p>
            Устройства:
            <b-tag
              v-for="device in research.devices"
              :key="device.device_id"
              type="is-primary"
              class="mr-2">
              {{ device.device_id }}
            </b-tag>
          </p>
        </div>
        <div class="box-buttons">
          <b-button
            type="is-primary"
            icon-left="account-group"
            tag="router-link"
            :to="{ path: '/researches/research/subjects', query: { researchId: research._id } }">
            Испытуемые
          </b-button>
          <b-button type="is-danger" icon-left="delete" @click="onDeleteResearchClick(research._id)"></b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { notifyAfter } from "@/modules/notification-decorators"

export default {
  name: "researches",

  data() {
    return {}
  },

  computed: {
    ...mapState('research', {
      researches: state => state.researches,
    }),
  },

  async mounted() {
    await this.getResearches()
  },

  methods: {
    ...mapActions('research', [
      'getResearches',
      'deleteResearch'
    ]),

    @notifyAfter('Удалено')
    onDeleteResearchClick(researchId) {
      return this.deleteResearch({ id: researchId })
    },
  }
}
</script>

<style scoped>

</style>
