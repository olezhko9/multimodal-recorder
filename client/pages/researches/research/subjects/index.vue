<template>
  <div>
    <b-breadcrumb size="is-medium">
      <b-breadcrumb-item tag='router-link' to="/">Исследования [{{ research && research.name }}]</b-breadcrumb-item>
      <b-breadcrumb-item
        tag='router-link'
        :to="{ path: '/subjects', query: { researchId } }"
        active>
        Испытуемые
      </b-breadcrumb-item>
    </b-breadcrumb>

    <div class="buttons">
      <b-button
        type="is-primary"
        icon-left="plus"
        @click="modalSubject = {}">
        Новый испытуемый
      </b-button>
    </div>

    <b-table
      v-if="research"
      :data="subjects"
      :total="subjects.length"
      :paginated="subjects.length > perPage"
      :per-page="perPage"
      scrollable>
      <b-table-column field="id" label="ID" v-slot="props">
        {{ props.row._id }}
      </b-table-column>

      <b-table-column
        v-for="field in research.subjectForm"
        :key="field.name"
        :field="'info.' + field.name"
        :label="field.name"
        v-slot="props">
        {{ props.row.info[field.name] }}
      </b-table-column>

      <b-table-column field="created_at" label="Дата создания" v-slot="props">
        {{ new Date(props.row.created_at).toLocaleString() }}
      </b-table-column>

      <b-table-column v-slot="props" field="">
        <div class="table-buttons">
          <b-tooltip label="Открыть в проводнике">
            <b-button
              type="is-primary"
              icon-left="folder"
              @click="openDirectory(props.row.directory)">
            </b-button>
          </b-tooltip>
          <b-button
            type="is-primary"
            icon-left="open-in-new"
            tag="nuxt-link"
            :to="{ path: '/researches/research/records', query: { researchId, subjectId: props.row._id } }">
          </b-button>
          <b-button
            type="is-danger"
            icon-left="delete"
            @click="onSubjectDeleteClick(props.row)">
          </b-button>
        </div>
      </b-table-column>

      <template #empty>
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            <p>
              <b-icon
                icon="emoticon-sad"
                size="is-large">
              </b-icon>
            </p>
            <p>Ничего не найдено</p>
          </div>
        </section>
      </template>
    </b-table>

    <b-modal
      :active="!!modalSubject"
      trap-focus
      has-modal-card
      :destroy-on-hide="true"
      aria-modal
      @close="onSubjectModalClose">
      <form v-if="modalSubject">
        <div class="modal-card" style="width: 640px">
          <header class="modal-card-head">
            <p class="modal-card-title">Новый испытуемый</p>
          </header>
          <section class="modal-card-body">
            <b-field v-for="field in research.subjectForm" :key="field.name" :label="field.name">
              <b-numberinput
                v-if="field.type === 'number'"
                v-model.number="modalSubject[field.name]"
                expanded>
              </b-numberinput>
              <b-input
                v-else
                v-model="modalSubject[field.name]"
                expanded>
              </b-input>
            </b-field>
          </section>
          <footer class="modal-card-foot">
            <b-button
              label="Закрыть"
              type="is-danger"
              @click="onSubjectModalClose"/>
            <b-button
              label="Сохранить"
              type="is-primary"
              @click="onSubjectModalSave"/>
          </footer>
        </div>
      </form>

    </b-modal>

    <div class="buttons">
      <b-button
        type="is-danger"
        outlined
        tag="router-link"
        to="/researches">
        Назад
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from "vuex"
import { notifyAfter } from "@/modules/notification-decorators"

export default {
  name: "subjects",

  data() {
    return {
      research: null,
      perPage: 10,
      modalSubject: null,
    }
  },

  computed: {
    ...mapState('research', {
      researches: state => state.researches,
    }),
    ...mapState('subject', {
      subjects: state => state.subjects,
    }),
    ...mapGetters('research', [
      'researchById'
    ]),

    researchId() {
      return this.$route.query.researchId
    }
  },

  async mounted() {
    !this.researches.length && await this.getResearches()
    await this.getSubjects({ researchId: this.researchId })

    this.research = this.researchById(this.researchId)
  },

  methods: {
    ...mapActions('research', [
      'getResearches',
    ]),
    ...mapActions('subject', [
      'getSubjects',
      'createSubject',
      'deleteSubject',
    ]),

    async openDirectory(directory) {
      return this.$axios.$post('/fs/directory/open', {
        directory
      })
    },

    @notifyAfter('Успешно')
    async onSubjectDeleteClick(subject) {
      return this.deleteSubject({ subjectId: subject._id })
    },

    onSubjectModalClose() {
      this.modalSubject = null
    },

    @notifyAfter('Успешно')
    async onSubjectModalSave() {
      const res = await this.createSubject({
        researchId: this.researchId,
        ...this.modalSubject
      })
      this.onSubjectModalClose()

      return res
    }
  }
}
</script>

<style scoped>

</style>
