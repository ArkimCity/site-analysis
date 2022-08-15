<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <SideBar/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import SideBar from '../components/SideBar.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    SideBar
  }
}
</script>
