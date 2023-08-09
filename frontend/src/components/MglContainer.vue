<template>
  <mgl-map
    mapStyle="https://api.maptiler.com/maps/streets/style.json?key=ZeIDe0UYO8FtUdnVvqI0"
    :zoom="11"
    :center="[126.9780, 37.5665]"
  >
    <mgl-navigation-control position="top-left"/>
    <mgl-marker
      v-for="(marker, index) in markers"
      :key="index"
      :coordinates="marker.lngLat"
    />
  </mgl-map>
</template>

<script>
import { MglMap, MglNavigationControl, MglMarker } from 'vue-maplibre-gl'
import seoul_hosptial from '../assets/json/seoul_hospital.json'

export default {
  name: 'MglContainer',
  components: {
    MglMap,
    MglNavigationControl,
    MglMarker
  },
  data() {
    return {
      markers: [] // Array to hold marker data
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      const markers = []

      seoul_hosptial.DATA.forEach(element => {
        let radius = 500
        if (['의원', '한의원', '치과의원'].includes(element.dutydivnam)) {
          return // Skip these types for now
        } else if (['병원', '한방병원', '치과병원'].includes(element.dutydivnam)) {
          radius = 1000
        } else if (['종합병원'].includes(element.dutydivnam)) {
          radius = 3000
        } else {
          return
        }

        // Add marker data to the markers array
        markers.push({
          lngLat: [element.wgs84lon, element.wgs84lat],
          radius: radius
        })
      })

      this.markers = markers
    }
  }
}
</script>

<style>
/* Your styles here */
</style>
