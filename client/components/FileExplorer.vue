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
          class="box file"
          @dblclick="obDoubleClick(file)">
          <div class="file_header">
            <b-icon v-if="file.type === 'directory'" icon="folder" class="mr-2"></b-icon>
            <span class="folder__name">{{ file.name }}</span>
          </div>
          <div class="file_control">
            <b-dropdown position="is-bottom-left">
              <template #trigger="{ active }">
                <b-icon icon="dots-vertical"></b-icon>
              </template>

              <b-dropdown-item>Открыть</b-dropdown-item>
              <b-dropdown-item>Another action</b-dropdown-item>
              <b-dropdown-item>Something else</b-dropdown-item>
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

export default {
  name: "FileExplorer",

  props: {
    tree: {
      type: Object
    }
  },

  data() {
    return {
      fsTree: this.tree || null,
      fsHistory: []
    }
  },

  mounted() {},

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
  }
}
</script>

<style scoped>
.fs-explorer {
  margin: -10px;
}

.file {
  display: flex;
  flex-direction: row;
  justify-tree: space-between;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}

.file_header {
  display: flex;
  align-items: center;
  width: 90%;
}

.folder__name {
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
