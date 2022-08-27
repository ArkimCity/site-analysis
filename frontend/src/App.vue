<template>
  <div>
    <SideBar id="sidebar"/>
    <div id="nav"></div>
    <router-view/>
  </div>
</template>

<script>
import SideBar from './components/SideBar.vue'

export default {
  components: {
    SideBar
  }
}
</script>

<style>
body {
  margin: 0;
  overflow: hidden;

}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  position: absolute;
  width: 100%;
  order: 2;
  background-color: #5a748f;
  height: 60px;
  top: 0;
  opacity: 0.7;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#sidebar {
  position: absolute;
  background-color: aliceblue;
  height: 100vh;
  width: 300px;
  left: 0;
  top: 70px;
}

#map {
  /* position: absolute; */
  left: 300px;
}
</style>
