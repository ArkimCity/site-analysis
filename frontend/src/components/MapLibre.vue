<template>
  <div>
    <MglMap
      mapStyle="https://api.maptiler.com/maps/streets/style.json?key=ZeIDe0UYO8FtUdnVvqI0"
      :center="center"
      :zoom="zoom"
    >
      <MglNavigationControl position="top-right"></MglNavigationControl>
      <MglMarker :coordinates="center"></MglMarker>
    </MglMap>
  </div>
</template>

<script>
import { MglMap, MglNavigationControl, MglMarker } from 'vue-maplibre-gl'

export default {
  name: 'MapComponent',
  components: {
    MglMap,
    MglNavigationControl,
    MglMarker
  },
  data () {
    return {
      center: [126.9780, 37.5665], // Coordinates for Seoul
      zoom: 1
    }
  }
}
</script>

<style>
.maplibregl-canvas {
  width: 100px;
}
</style>
