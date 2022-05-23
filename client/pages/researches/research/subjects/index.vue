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
        width="150"
        centered
        v-slot="props">
        <template v-if="field.name === 'Пол'">
          <b-icon v-if="props.row.info[field.name] === 'Мужчина'" icon="gender-male" size="is-small"></b-icon>
          <b-icon v-else-if="props.row.info[field.name] === 'Женщина'" icon="gender-female" size="is-small"></b-icon>
        </template>
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
          <b-tooltip label="Открыть записи">
            <b-button
              type="is-primary"
              icon-left="database"
              tag="nuxt-link"
              :to="{ path: '/researches/research/records', query: { researchId, subjectId: props.row._id } }">
            </b-button>
          </b-tooltip>
          <b-button
            type="is-danger"
            icon-left="delete"
            @click="onSubjectDeleteClick(props.row)">
          </b-button>
        </div>
      </b-table-column>

      <template #footer>
        <th class="is-hidden-mobile">
          <div class="th-wrap is-numeric"></div>
        </th>
        <th class="is-hidden-mobile">
          <div class="th-wrap"></div>
        </th>
        <th class="is-hidden-mobile">
          <div class="th-wrap is-centered">Средний возраст: {{ meanAge }}</div>
        </th>
        <th class="is-hidden-mobile">
          <div class="th-wrap is-centered">{{ genderArray[0] }} муж., {{ genderArray[1] }} жен.</div>
        </th>
        <th class="is-hidden-mobile">
          <div class="th-wrap"></div>
        </th>
        <th class="is-hidden-mobile">
          <div class="th-wrap"></div>
        </th>
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
              <b-select
                v-else-if="field.type === 'select'"
                v-model="modalSubject[field.name]"
                expanded>
                <option v-for="option in (field.options || [])" :key="option" :value="option">{{ option }}</option>
              </b-select>
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
    },

    meanAge() {
      let sum = 0, count = 0
      for (let subject of this.subjects) {
        if (subject && subject.info && subject.info['Возраст']) {
          sum += subject.info['Возраст']
          count++
        }
      }
      if (count) return (sum / count).toFixed(2)

      return 0
    },

    genderArray() {
      const gendersCount = [0, 0] // 0 - муж, 1 - жен
      for (let subject of this.subjects) {
        if (subject && subject.info && subject.info['Пол']) {
          if (subject.info['Пол'] === 'Мужчина') gendersCount[0]++
          else if (subject.info['Пол'] === 'Женщина') gendersCount[1]++
        }
      }

      return gendersCount
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

    @notifyAfter('Открыто')
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
