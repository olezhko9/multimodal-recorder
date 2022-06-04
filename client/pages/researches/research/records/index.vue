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
      :loading="isLoading"
      detailed
      detail-key="_id"
      how-detail-icon
      @details-open="onRecordDetailsClick">
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
        <b-tooltip label="Открыть связанные Notebooks">
          <b-button
            type="is-primary"
            icon-left="folder-pound"
            @click="openDirectory(props.row.notebooks_directory)">
          </b-button>
        </b-tooltip>
        <b-button
          type="is-danger"
          icon-left="delete"
          @click="onRecordDeleteClick(props.row)">
        </b-button>
      </b-table-column>

      <template #detail="props">
        <file-explorer
          :tree="props.row.tree"
          :modalities="props.row.device_modality_dict"
          @click:notebook="onNotebookRunClick($event, props.row._id)"/>
      </template>

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

    <b-modal
      :active.sync="notebookModalActive"
      has-modal-card
      trap-focus>
      <template #default="props">
        <div class="modal-card">
          <section class="modal-card-body" style="border-top-left-radius: 10px; border-top-right-radius: 10px;">
            <h2 class="title is-5">Notebook запущен</h2>
            <p>Это может занять некоторые время, чтобы выполнить его. Результат будет доступен в
              <a @click="openDirectory(notebookDir)">этой папке</a>
            </p>
          </section>
          <footer class="modal-card-foot">
            <b-button type="is-primary" @click="props.close()">Закрыть</b-button>
          </footer>
        </div>
      </template>
    </b-modal>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters, mapMutations } from "vuex"
import { notifyAfter } from "@/modules/notification-decorators"
import FileExplorer from "@/components/FileExplorer"

export default {
  name: "records",
  components: {
    FileExplorer,
  },

  data() {
    return {
      research: null,
      subject: null,
      perPage: 10,
      notebookModalActive: false,
      notebookDir: '',
      isLoading: false,
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
    ...mapState('notebook', {
      notebooks: state => state.notebooks,
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
    try {
      this.isLoading = true
      !this.researches.length && await this.getResearches()
      !this.subjects.length && await this.getSubjects({ researchId: this.researchId })
      await this.getResearchRecords({ researchId: this.researchId, subjectId: this.subjectId })

      this.research = this.researchById(this.researchId)
      this.subject = this.subjectById(this.subjectId)

      !this.notebooks.length && await this.getNotebooks()
    } finally {
      this.isLoading = false
    }
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
    ...mapActions('notebook', [
      'getNotebooks',
      'runNotebook',
    ]),
    ...mapMutations('record', {
      setDirectoryTree: 'SET_DIRECTORY_TREE'
    }),

    @notifyAfter('Открыто')
    async openDirectory(directory) {
      return this.$axios.$post('/fs/directory/open', {
        directory
      })
    },

    async onRecordDetailsClick(record) {
      if (!record.tree) {
        const tree = await this.$axios.$post('/fs/directory/tree', {
          directory: record.directory
        })
        this.setDirectoryTree({
          recordId: record._id,
          tree,
        })
      }
    },

    @notifyAfter('Успешно')
    async onRecordDeleteClick(record) {
      return this.deleteRecord({ recordId: record._id })
    },

    async onNotebookRunClick(notebookParams, recordId) {
      try {
        if (notebookParams.notebook) {
          this.notebookDir = await this.runNotebook({ recordId, ...notebookParams })
          this.notebookModalActive = true
        }
      } finally {
      }
    }
  }
}
</script>

<style scoped>

</style>
