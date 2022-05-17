<template>
  <div>
    <section class="container has-text-centered">
      <h1 class="title is-size-2">
        {{ error.statusCode === 404 ? 'Страница не найдена' : 'Внутренняя ошибка сервера' }}
      </h1>
      <h2 v-if="error.statusCode !== 404" class="is-size-6">
        {{ getErrorMessage() }}
      </h2>
      <br/>
      <img src="/brain_error.png" style="max-width: 300px">
    </section>
  </div>
</template>
<script>

export default {
  props: ['error'],

  methods: {
    getErrorMessage() {
      const errorMessage = this.error.message.toLowerCase()
      switch (errorMessage) {
        case 'network error': return 'Сервер выключен или временно недоступен'
        default: return this.error.message
      }
    }
  }
}
</script>
