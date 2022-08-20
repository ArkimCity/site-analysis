<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <Map id='Map'/>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Map from '../components/Map.vue'

export default {
  name: 'Home',
  components: {
    // HelloWorld,
    Map
  }
}
</script>
