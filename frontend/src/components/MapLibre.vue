<template>
  <div id="map" style="width: 100%; height: 400px;"></div>
</template>

<script>
import maplibregl from 'maplibre-gl'

export default {
  name: 'MapComponent',
  data () {
    return {
      map: null
    }
  },
  mounted () {
    this.initializeMap()
  },
  methods: {
    initializeMap () {
      this.map = new maplibregl.Map({
        container: 'map',
        center: [38, 127], // initial map center [lng, lat]
        zoom: 1
      })
    }
  },
  beforeUnmount () {
    if (this.map) {
      this.map.remove()
    }
  }
}
</script>

<style>
/* Add styles here if needed */
</style>
