<template>
  <div>
    <h1>EEG data</h1>
    <div id="graph" style="width: 100%; height: 800px;"></div>
  </div>
</template>

<script>
export default {
  name: "eeg",

  data() {
    return {
      plotlyLoaded: false,
      sse: null
    }
  },

  watch: {
    plotlyLoaded(isLoaded) {
      console.log(20, isLoaded)
      if (isLoaded) {
        const graph = document.getElementById('graph');

        const eegChannelsCount = 15
        let traces = []

        for (let i = 0; i < eegChannelsCount; i++) {
          traces[i] = {
            x: [],
            y: [],
            xaxis: `x${i + 1}`,
            yaxis: `y${i + 1}`,
            type: 'scatter',
            name: 'Канал ' + (i + 1)
          }
        }

        const layout = {
          grid: {
            rows: eegChannelsCount,
            columns: 1,
            pattern: 'independent',
            roworder: 'top to bottom'
          },
          xaxis: {
            dtick: 0.5,
            tick0: -3
          }
        };

        Plotly.newPlot(graph, traces, layout);

        let sseOpenedOnce = false
        this.sse = new EventSource("http://localhost:5000/stream?device=openbci_cython")

        this.sse.onopen = function () {
          console.log('sse open')
          if (sseOpenedOnce) {
            this.sse && this.sse.close()
          }
          sseOpenedOnce = true
        }

        this.sse.onerror = function(err) {
          console.log('sse error', err)
          this.sse && this.sse.close()
          this.sse = null
        }

        let timestamps = []

        this.sse.addEventListener("upd", function (event) {
          let eegData = JSON.parse(event.data);

          const n = 250 * 3
          eegData[30] = eegData[30].map(time => Math.trunc(time * 1000))
          timestamps = timestamps.concat(eegData[30]).slice(-n)

          const now = +new Date()
          const last = (timestamps[timestamps.length - 1] - now) / 1000
          const timeDiffs = timestamps.map(time => (time - now) / 1000 - last)

          for (let i = 0; i < eegChannelsCount; i++) {
            traces[i].x = timeDiffs
            traces[i].y = traces[i].y.concat(eegData[i + 1]).slice(-n) // i's channel data
          }
          Plotly.react(graph, traces, layout);
        });
      }
    }
  },

  mounted() {
    console.log('mounted')
  },

  head() {
    return {
      script: [
        {
          src: "https://cdn.plot.ly/plotly-2.8.3.min.js",
          defer: true,
          callback: () => {
            console.log('loaded')
            this.plotlyLoaded = true
          }
        }
      ]
    }
  },

  beforeRouteLeave(to, from, next) {
    if (this.sse) {
      this.sse.close()
      this.sse = null
    }
    next()
  }
}
</script>

<style scoped>

</style>
