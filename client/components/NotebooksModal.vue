<template>
  <form action="">
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Запустить Jupyter Notebook для выбранных данных</p>
      </header>
      <section class="modal-card-body">
        <div class="columns is-multiline">
          <div
            v-for="notebook in notebooks"
            :key="notebook"
            class="column is-6">
            <div
              class="box fs-file">
              <div :title="notebook" class="fs-file__header" @click="selectNotebook(notebook)">
                <b-icon icon="file-code" class="mr-2"></b-icon>
                <span class="fs-file__name">{{ notebook }}</span>
              </div>
              <b-checkbox
                :value="selectedNotebook"
                :native-value="notebook"
                class="is-marginless"
                @input="selectNotebook(notebook)">
              </b-checkbox>
            </div>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <b-button
          label="Закрыть"
          type="is-danger"
          @click="onCloseClick"/>
        <b-button
          label="Запустить"
          type="is-primary"
          @click="onSaveClick"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "NotebooksModal",

  props: {
    notebooks: {
      type: Array,
      default: []
    },

    onSave: {
      type: Function,
    }
  },

  data() {
    return {
      selectedNotebook: [],
    }
  },

  methods: {
    selectNotebook(notebook) {
      if (this.selectedNotebook[0] === notebook)
        this.selectedNotebook = []
      else
        this.selectedNotebook = [notebook]
    },

    onSaveClick() {
      this.onSave && this.onSave(this.selectedNotebook[0])
      this.$parent.close()
    },

    onCloseClick() {
      this.$parent.close()
    }
  }
}
</script>

<style scoped>
.fs-file__header {
  cursor: pointer;
}
</style>
