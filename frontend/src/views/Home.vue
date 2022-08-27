<template>
  <div class="home">
    <Map id='map'></Map>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Map from '../components/Map.vue'

export default {
  name: 'Home',
  components: {
    Map
  }
}
</script>
