<template>
  <div class="fs-explorer">
    <b-button
      v-if="fsHistory.length"
      icon-left="chevron-left"
      type="is-ghost"
      class="mb-1"
      @click="onBackButtonClick">
      Назад
    </b-button>
    <div
      v-if="fsTree && fsTree.tree && fsTree.tree.length"
      class="columns is-multiline is-paddingless">
      <div v-for="file in fsTree.tree" class="column is-4">
        <div
          class="box fs-file"
          @dblclick="obDoubleClick(file)">
          <div class="fs-file__header" :title="file.name">
            <b-icon v-if="file.type === 'directory'" icon="folder" class="mr-2"></b-icon>
            <b-tooltip v-if="modalities[file.name]" :label="modalities[file.name]" type="is-primary" position="is-bottom">
              <span class="fs-file__name">{{ file.name }}</span>
            </b-tooltip>
            <span v-else class="fs-file__name">{{ file.name }}</span>
          </div>
          <div class="fs-file__control">
            <b-dropdown position="is-bottom-left">
              <template #trigger="{ active }">
                <b-icon icon="dots-vertical"></b-icon>
              </template>
              <b-dropdown-item
                class="context-menu__item"
                @click="openDirectory(file.path)">
                <b-icon icon="folder"></b-icon>
                Открыть в проводнике
              </b-dropdown-item>
              <b-dropdown-item
                v-if="file.type === 'directory'"
                class="context-menu__item"
                @click="runPipeline(file.path, file.name)">
                <b-icon icon="folder-cog"></b-icon>
                Первичная обработка
              </b-dropdown-item>
              <b-dropdown-item
                class="context-menu__item"
                @click="openNotebooksModal(file.path, file.name)">
                <b-icon icon="file-code"></b-icon>
                Запустить Notebook
              </b-dropdown-item>
              <b-dropdown-item
                class="context-menu__item"
                @click="removeDirectory(file.path)">
                <b-icon icon="delete" type="is-danger"></b-icon>
                Удалить
              </b-dropdown-item>
            </b-dropdown>
          </div>
        </div>
      </div>
    </div>
    <section v-else class="section">
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
  </div>
</template>

<script>
import { notifyAfter } from "@/modules/notification-decorators"
import NotebooksModal from "@/components/NotebooksModal"
import PipelineModal from "@/components/PipelineModal"
import { mapState } from "vuex"

export default {
  name: "FileExplorer",

  props: {
    tree: {
      type: Object
    },
    modalities: {
      type: Object,
      default: () => {
      }
    }
  },

  data() {
    return {
      fsTree: this.tree || null,
      fsHistory: []
    }
  },

  computed: {
    ...mapState('notebook', {
      notebooks: state => state.notebooks,
    }),
  },

  watch: {
    tree(newTree) {
      this.fsTree = newTree
    }
  },

  mounted() {
  },

  methods: {
    obDoubleClick(file) {
      if (file.type === 'directory') {
        this.fsHistory.push(this.fsTree)
        this.fsTree = file
      } else {
        return this.openDirectory(file.path)
      }
    },

    onBackButtonClick() {
      this.fsTree = this.fsHistory.pop()
    },

    @notifyAfter('Открыто')
    async openDirectory(directory) {
      return this.$axios.$post('/fs/directory/open', {
        directory
      })
    },

    @notifyAfter('Удалено')
    async removeDirectory(directory) {
      return this.$axios.$post('/fs/directory/remove', {
        directory
      })
    },

    openNotebooksModal(dataPath, filename) {
      this.$buefy.modal.open({
        component: NotebooksModal,
        parent: this,
        hasModalCard: true,
        props: {
          notebooks: this.notebooks,
          onSave: (notebook) => {
            this.$emit('click:notebook', {
              notebook,
              dataPath,
            })
          }
        }
      })
    },

    runPipeline(dataPath, filename) {
      this.$buefy.modal.open({
        component: PipelineModal,
        parent: this,
        hasModalCard: true,
        props: {
          onSave: (pipeline) => {
            this.$emit('click:pipeline', {
              pipeline,
              dataPath,
              filename
            })
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.fs-explorer {
  margin: -10px;
}
</style>
