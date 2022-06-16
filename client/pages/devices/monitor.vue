<template>
  <div>
    <h1 class="title is-4">
      Монитор данных устройства {{ deviceById(deviceId) ? deviceById(deviceId).name : '' }}
    </h1>
    <div
      v-if="modality.startsWith('serial') || modality === 'positional/2d'"
      id="graph"
      style="width: 100%;"
      :style="{height: Math.max(channelsCount * 60, 500) + 'px'}">
    </div>
    <img
      v-else-if="modality.startsWith('visual')"
      :src="sseUrl"
      width="640"
      height="480"
    />
    <b-message v-else type="is-danger">
      Стриминг данных для данного устройства или модальности данных не поддерживается
    </b-message>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist'
import { mapActions, mapGetters, mapState } from "vuex"

export default {
  name: "DeviceMonitoring",

  data() {
    return {
      sseUrl: '',
      sse: null,

      channelsCount: 1,
      samplingRate: 200,
      modality: '',
      lastSecondsToShow: 3,

      traces: [],
      fps: 30,
    }
  },

  computed: {
    ...mapState('device', {
      devices: state => state.devices,
    }),
    ...mapGetters('device', [
      'deviceById',
      'startedDeviceParams',
    ]),

    deviceId() {
      return this.$route.query.deviceId
    }
  },

  async mounted() {
    const channelsDict = {
      'arduino_uno': 1,
      'openbci_cython': 16
    }
    this.samplingRate = this.startedDeviceParams(this.deviceId).sampling_rate
    this.modality = this.startedDeviceParams(this.deviceId).modality
    this.channelsCount = channelsDict[this.deviceId]

    !this.devices.length && await this.getDevices()

    this.sseUrl = "http://localhost:5000/device/stream?device=" + this.deviceId

    if (this.modality.startsWith('visual') || this.modality.startsWith('audio')) return

    this.graph = document.getElementById('graph');

    if (this.modality === 'positional/2d') {
      this.layout = {
        xaxis: {
          range: [0, 1]
        },
        yaxis: {
          range: [1, 0]
        },
        title: 'Gaze data'
      };

      this.traces = []

      var trace1 = {
        x: [],
        y: [],
        mode: 'markers',
        type: 'scatter',
        name: 'Right Eye',
        marker: { size: 6 }
      };

      var trace2 = {
        x: [],
        y: [],
        mode: 'markers',
        type: 'scatter',
        name: 'Left Eye',
        marker: { size: 6 }
      };

      this.traces = [trace1, trace2]
    } else if (this.modality.startsWith('serial')) {
      this.layout = {
        grid: {
          rows: this.channelsCount,
          columns: 1,
          pattern: 'independent',
          roworder: 'top to bottom'
        },
        xaxis: {
          dtick: 0.5,
          tick0: -3
        },
        yaxis: {
          nticks: 3
        }
      }

      for (let i = 0; i < this.channelsCount; i++) {
        this.traces[i] = {
          x: [],
          y: [],
          xaxis: `x${i + 1}`,
          yaxis: `y${i + 1}`,
          type: 'scatter',
          name: 'Канал ' + (i + 1)
        }
      }
    } else return

    Plotly.newPlot(this.graph, this.traces, this.layout);

    let sseOpenedOnce = false
    this.sse = new EventSource(this.sseUrl)

    this.sse.onopen = function () {
      console.log('sse open')
      if (sseOpenedOnce) {
        this.sse && this.sse.close()
      }
      sseOpenedOnce = true
    }

    this.sse.onerror = function (err) {
      console.log('sse error', err)
      this.sse && this.sse.close()
      this.sse = null
    }

    let timestamps = []

    this.sse.addEventListener("upd", (event) => {
      let deviceData = JSON.parse(event.data);
      const columnsCount = deviceData.length
      const timestampChannel = columnsCount - 1

      const n = this.samplingRate * this.lastSecondsToShow
      deviceData[timestampChannel] = deviceData[timestampChannel].map(time => Math.trunc(time * 1000))
      timestamps = timestamps.concat(deviceData[timestampChannel]).slice(-n)

      const now = +new Date()
      const last = (timestamps[timestamps.length - 1] - now) / 1000
      const timeDiffs = timestamps.map(time => (time - now) / 1000 - last)

      if (this.modality === 'positional/2d') {
        this.traces[0].x = this.traces[0].x.concat(deviceData[0]).slice(-n)
        this.traces[0].y = this.traces[0].y.concat(deviceData[1]).slice(-n)
        this.traces[1].x = this.traces[1].x.concat(deviceData[2]).slice(-n)
        this.traces[1].y = this.traces[1].y.concat(deviceData[3]).slice(-n)
      } else if (this.modality.startsWith('serial')) {
        for (let i = 0; i < this.channelsCount; i++) {
          this.traces[i].x = timeDiffs
          this.traces[i].y = this.traces[i].y.concat(deviceData[i]).slice(-n) // i's channel data
        }
      }
    });

    this.updatePlotLoop()
  },

  methods: {
    ...mapActions('device', [
      'getDevices',
    ]),

    updatePlotLoop() {
      setTimeout(function () {
        Plotly.react(this.graph, this.traces, this.layout);
        this.updatePlotLoop()
      }.bind(this), 1000 / this.fps)
    }
  },

  beforeRouteLeave(to, from, next) {
    if (this.sse && this.sse.close) {
      this.sse.close()
    }
    this.sse = null
    next()
  }
}
</script>

<style scoped>

</style>
