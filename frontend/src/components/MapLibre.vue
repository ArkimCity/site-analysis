<template>
  <div id="map" style="width: 100%; height: 400px;"></div>
</template>

<script>
import maplibregl from 'maplibre-gl'

export default {
  name: 'MapComponent',
  data() {
    return {
      map: null
    }
  },
  mounted() {
    this.initializeMap()
  },
  methods: {
    initializeMap() {
      this.map = new maplibregl.Map({
        container: 'map',
        style: 'https://maplibre.org/maplibre-gl-js-docs/style-spec/json/examples/osm-liberty.json',
        center: [0, 0], // initial map center [lng, lat]
        zoom: 1
      })
    }
  },
  beforeDestroy() {
    if (this.map) {
      this.map.remove()
    }
  }
}
</script>

<style>
/* Add styles here if needed */
</style>
