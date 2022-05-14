import { NotificationProgrammatic as Notification } from 'buefy'
import { LoadingProgrammatic as Loading } from 'buefy'


function notifyAfter(successText, duration = 3000, loading = true) {
  let notificationConfig = {}
  if (typeof successText === 'string') {
    notificationConfig = {
      successText,
      duration,
      loading
    }
  } else if (typeof successText !== "undefined" && successText !== null) {
    notificationConfig = successText
  }

  notificationConfig.successText = notificationConfig.successText || 'success'
  notificationConfig.duration = notificationConfig.duration || 3000
  notificationConfig.loading = typeof notificationConfig.loading !== 'undefined' ?
    notificationConfig.loading : true

  return function decorator(target, name, descriptor) {
    const func = descriptor.value

    descriptor.value = async function (...args) {
      let response = null
      let loadingIndicator
      let isRequestError = false
      try {
        if (notificationConfig.loading)
          loadingIndicator = Loading.open()

        response = await func.apply(this, args)
        return response
      } catch (e) {
        if (e.isAxiosError) {
          isRequestError = true
          response = e.response
        } else {
          console.log(e);
          throw e
        }
      } finally {
        if (loadingIndicator)
          loadingIndicator.close()

        let message
        let type = 'is-danger'

        if (response) {
          if (isRequestError) {
            message = response.data || 'Internal Server Error'
            type = "is-danger"
          } else {
            message = notificationConfig.successText || "Успешно"
            type = "is-success"
          }
        }

        if (message) {
          Notification.open({
            duration: notificationConfig.duration,
            message: message,
            type: type,
            position: 'is-bottom-right',
            queue: false
          })
        }
      }
    }
    return descriptor
  }
}

export { notifyAfter }
