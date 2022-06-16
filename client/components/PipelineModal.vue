<template>
  <form action="">
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Настройка pipeline</p>
      </header>
      <section class="modal-card-body">
        <b-field label="Выберите метод" class="mb-5">
          <b-autocomplete
            :data="allowedMethods"
            :open-on-focus="true"
            :max-height="180"
            placeholder="Выберите метод обработки"
            field="name"
            @select="onMethodSelect">

            <template slot-scope="props">
              <div class="media">
                <div class="media-content">
                  <b>{{ props.option.name }}</b>
                  <b-tag type="is-primary" size="is-small">{{ props.option.modalities[0] }}</b-tag>
                  <br>
                  <small>{{ props.option.doc }}</small>
                </div>
              </div>
            </template>
          </b-autocomplete>
        </b-field>
        <div v-if="pipeline.length" class="pipeline">
          <div
            v-for="(method, index) in pipeline"
            :key="method.name"
            class="pipeline-item">
            <div class="pipeline-control">
              <div class="pipeline-marker">
                <span>{{ index + 1 }}</span>
              </div>
              <div class="pipeline-connector"></div>
            </div>
            <div class="pipeline-content box">
              <b-collapse>
                <template #trigger="props">
                  <div class="pipeline-content__header">
                    <div>
                      <p>
                        <b>{{ method.name }}</b>
                        <b-tag type="is-primary">{{ method.modalities[0] }}</b-tag>
                      </p>
                      <p v-html="method.doc"></p>
                    </div>
                    <div>
                      <button class="delete" @click="removeMethod(index)"></button>
                    </div>
                  </div>
                </template>
                <br>
                <div>
                  <p v-if="!Object.keys(method.arguments).length" class="has-text-danger">Нет аргументов</p>
                  <b-field
                    v-else
                    v-for="(argConfig, argName) in method.arguments" :key="argName"
                    :message="argConfig.doc ? argConfig.doc : ''"
                    label-position="inside"
                    type="is-primary"
                    class="mb-4">
                    <template #label>
                      {{ argName }}
                    </template>
                    <b-select
                      v-model="method.options[argName]"
                      v-if="argConfig === 'select' || argConfig.type === 'select'"
                      :value="argConfig.default"
                      placeholder="Выберите значение из списка"
                      expanded>
                      <option v-for="option in (argConfig.options || [])" :value="option">{{ option }}</option>
                    </b-select>
                    <b-input
                      v-else-if="argConfig === 'number' || argConfig.type === 'number'"
                      v-model.number="method.options[argName]"
                      :value="argConfig.default || null"
                      placeholder="Введите значение"
                      expanded>
                    </b-input>
                    <b-input
                      v-else
                      v-model="method.options[argName]"
                      :value="argConfig.default || null"
                      placeholder="Введите значение"
                      expanded>
                    </b-input>
                  </b-field>
                </div>
              </b-collapse>
            </div>
          </div>
        </div>
        <b-message v-else type="is-warning" has-icon>
          Pipeline позволяет последовательно применить к выбранным данным указанные методы обработки.
          Самостоятельно проверяйте модальность данных и методов.
        </b-message>
      </section>
      <footer class="modal-card-foot">
        <b-button
          label="Закрыть"
          type="is-danger"
          @click="onCloseClick"/>
        <b-button
          :disabled="pipeline.length === 0"
          label="Запустить"
          type="is-primary"
          @click="onSaveClick"/>
      </footer>
    </div>
  </form>
</template>

<script>
import lodash from "lodash"
import { mapState } from "vuex"

export default {
  name: "PipelineModal",

  props: {
    onSave: {
      type: Function,
    }
  },

  data() {
    return {
      pipeline: []
    }
  },

  computed: {
    ...mapState('pipeline', {
      allMethods: state => state.allMethods,
    }),

    allowedMethods() {
      return this.allMethods.filter(method => !this.pipeline.find(m => m.name === method.name))
    }
  },

  methods: {
    onMethodSelect(method) {
      this.pipeline.push({ ...lodash.cloneDeep(method), options: {} })
    },

    removeMethod(methodIndex) {
      this.pipeline.splice(methodIndex, 1)
    },

    onSaveClick() {
      const pipeline = this.pipeline.map(method => {
        return {
          name: method.name,
          options: method.options,
        }
      })
      this.onSave && this.onSave(pipeline)
      this.$parent.close()
    },

    onCloseClick() {
      this.$parent.close()
    }
  }
}
</script>

<style lang="scss" scoped>
.pipeline-item {
  display: flex;
  flex-direction: row;
  width: 100%;
}

.pipeline-control {
  width: 50px;
  display: flex;
  flex-direction: column;

  .pipeline-connector {
    width: calc(50% + 2px);
    height: 100%;
    border-right: 2px solid $primary;
  }

  .pipeline-marker {
    width: 1.7rem;
    height: 1.7rem;
    display: flex;
    align-items: center;
    justify-content: center;
    align-self: center;
    color: $primary;
    background-color: #fff;
    border-radius: 50%;
    border: 2px solid $primary;
  }
}

.modal-card-body {
  min-height: 300px;
}

.pipeline-content {
  flex: 1;

  .pipeline-content__header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
}

.pipeline-item:not(:last-child) {
  .pipeline-content {
    margin-bottom: 2rem;
  }
}
</style>
