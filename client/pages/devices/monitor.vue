<template>
  <div>
    <h1 class="title is-4">
      Монитор данных устройства {{ deviceById(deviceId) ? deviceById(deviceId).name : '' }}
    </h1>
    <div
      v-if="['arduino_uno', 'openbci_cython'].includes(deviceId)"
      id="graph"
      style="width: 100%;"
      :style="{height: Math.max(channelsCount * 60, 500) + 'px'}">
    </div>
    <img
      v-else
      :src="sseUrl"
      width="640"
      height="480"
    />
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist'
import { mapActions, mapGetters, mapState } from "vuex"

export default {
  name: "SerialPlot",

  data() {
    return {
      sseUrl: '',
      sse: null,

      channelsCount: 1,
      samplingRate: 330,

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
    ]),

    deviceId() {
      return this.$route.query.deviceId
    }
  },

  async mounted() {
    !this.devices.length && await this.getDevices()

    this.sseUrl = "http://localhost:5000/device/stream?device=" + this.deviceId

    if (this.deviceId === 'camera') return

    this.graph = document.getElementById('graph');

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
      let eegData = JSON.parse(event.data);
      const columnsCount = eegData.length
      const timestampChannel = columnsCount - 1

      const n = this.samplingRate * 3
      eegData[timestampChannel] = eegData[timestampChannel].map(time => Math.trunc(time * 1000))
      timestamps = timestamps.concat(eegData[timestampChannel]).slice(-n)

      const now = +new Date()
      const last = (timestamps[timestamps.length - 1] - now) / 1000
      const timeDiffs = timestamps.map(time => (time - now) / 1000 - last)

      for (let i = 0; i < this.channelsCount; i++) {
        this.traces[i].x = timeDiffs
        this.traces[i].y = this.traces[i].y.concat(eegData[i]).slice(-n) // i's channel data
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
