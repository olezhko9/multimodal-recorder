<template>
  <div>
    <h1 class="title is-4">Записи исследования "{{ research && research.name }}"</h1>

    <div class="buttons">
      <b-button
        type="is-primary"
        icon-left="plus"
        tag="router-link"
        :to="{ path: '/researches/research/records/record', query: { researchId } }">
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

      <b-table-column v-slot="props" field="" label="Открыть папку" centered>
        <b-button
          type="is-primary"
          icon-left="folder"
          @click="openDirectory(props.row.directory)">
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
        to="/researches">
        Назад
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from "vuex"

export default {
  name: "records",

  data() {
    return {
      research: null,
      records: [],
      perPage: 10,
    }
  },

  computed: {
    ...mapState('research', {
      researches: state => state.researches,
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
    this.records = await this.getResearchRecords({ researchId: this.researchId })

    this.research = this.researchById(this.researchId)
  },

  methods: {
    ...mapActions('research', [
      'getResearches',
      'getResearchRecords',
    ]),

    async openDirectory(directory) {
      return this.$axios.$post('/fs/directory/open', {
        directory
      })
    }
  }
}
</script>

<style scoped>

</style>
