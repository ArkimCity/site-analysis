<template>
  <mgl-map
    mapStyle="https://api.maptiler.com/maps/streets/style.json?key=ZeIDe0UYO8FtUdnVvqI0"
    :zoom=11
    :center="[126.9780, 37.5665]"
  >
    <mgl-navigation-control position="top-left"/>
  </mgl-map>
</template>

<script>
import { MglMap, MglNavigationControl } from 'vue-maplibre-gl'

export default {
  name: 'MglContainer',
  components: {
    MglMap,
    MglNavigationControl
  }
}
</script>

<style>

</style>
