<template>
  <div>
    <b-breadcrumb size="is-medium">
      <b-breadcrumb-item tag='router-link' to="/">Исследования [{{ research && research.name }}]</b-breadcrumb-item>
      <b-breadcrumb-item
        tag='router-link'
        :to="{ path: '/researches/research/subjects', query: {researchId: this.researchId} }">
        Испытуемые [{{ subjectName(subjectId) }}]
      </b-breadcrumb-item>
      <b-breadcrumb-item active>Записи</b-breadcrumb-item>
    </b-breadcrumb>

    <div class="buttons">
      <b-button
        type="is-primary"
        icon-left="plus"
        tag="router-link"
        :to="{ path: '/researches/research/records/record', query: { researchId, subjectId } }">
        Новая запись
      </b-button>
    </div>

    <b-table
      :data="records"
      :total="records.length"
      :paginated="records.length > perPage"
      :per-page="perPage"
      :pagination-simple="true">
      <b-table-column field="id" label="ID" v-slot="props">
        {{ props.row._id }}
      </b-table-column>

      <b-table-column field="created_at" label="Дата создания" v-slot="props">
        {{ new Date(props.row.created_at).toLocaleString() }}
      </b-table-column>

      <b-table-column v-slot="props" field="">
        <b-tooltip label="Открыть в проводнике">
          <b-button
            type="is-primary"
            icon-left="folder"
            @click="openDirectory(props.row.directory)">
          </b-button>
        </b-tooltip>
        <b-button
          type="is-danger"
          icon-left="delete"
          @click="onRecordDeleteClick(props.row)">
        </b-button>
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

    <div class="buttons">
      <b-button
        type="is-danger"
        outlined
        tag="router-link"
        :to="{ path: '/researches/research/subjects', query: {researchId: this.researchId} }">
        Назад
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from "vuex"
import { notifyAfter } from "@/modules/notification-decorators"

export default {
  name: "records",

  data() {
    return {
      research: null,
      subject: null,
      perPage: 10,
    }
  },

  computed: {
    ...mapState('research', {
      researches: state => state.researches,
    }),
    ...mapState('subject', {
      subjects: state => state.subjects,
    }),
    ...mapState('record', {
      records: state => state.researchRecords,
    }),
    ...mapGetters('research', [
      'researchById'
    ]),
    ...mapGetters('subject', [
      'subjectById',
      'subjectName',
    ]),

    researchId() {
      return this.$route.query.researchId
    },

    subjectId() {
      return this.$route.query.subjectId
    },
  },

  async mounted() {
    !this.researches.length && await this.getResearches()
    !this.subjects.length && await this.getSubjects({ researchId: this.researchId })
    await this.getResearchRecords({ researchId: this.researchId, subjectId: this.subjectId })

    this.research = this.researchById(this.researchId)
    this.subject = this.subjectById(this.subjectId)
  },

  methods: {
    ...mapActions('research', [
      'getResearches',
    ]),
    ...mapActions('record', [
      'getResearchRecords',
      'deleteRecord',
    ]),
    ...mapActions('subject', [
      'getSubjects',
    ]),

    async openDirectory(directory) {
      return this.$axios.$post('/fs/directory/open', {
        directory
      })
    },

    @notifyAfter('Успешно')
    async onRecordDeleteClick(record) {
      return this.deleteRecord({ recordId: record._id })
    }
  }
}
</script>

<style scoped>

</style>
