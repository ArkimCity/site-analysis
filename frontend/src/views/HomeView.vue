<template>
  <div class="home">
    <MglContainer id="mgl-container"></MglContainer>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
// import Map from '../components/Map.vue'
import MglContainer from '../components/MglContainer.vue'

export default {
  name: 'HomeView',
  components: {
    MglContainer
  }
}
</script>

<style>
.home {
  height: 100vh;
}
</style>
