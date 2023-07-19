<template>
<div id='sidebar'>
  <br><br><br>
  <div v-if="this.$store.state.selectedBuilding.propertiesData">
    <Canvas id="canvas"></Canvas><br>

    <!-- 아래는 properties -->
    pnu: {{ this.$store.state.selectedBuilding.propertiesData.A2 }}
    <br><br>
    주소: {{ this.$store.state.selectedBuilding.propertiesData.A4 }}
    {{ this.$store.state.selectedBuilding.propertiesData.A5 }}
    <br><br>
    용도: {{ this.$store.state.selectedBuilding.propertiesData.A9 }}
    <br><br>
    구조: {{ this.$store.state.selectedBuilding.propertiesData.A11 }}
    <br>
  </div>
  <div v-else>
    건물 위에 마우스를 올려주세요
  </div>
</div>
</template>

<script>
import Canvas from './Canvas.vue'

export default {
  name: 'SideBar',
  components: {
    Canvas
  }
}
</script>

<style scoped>
#canvas {
  width: 250px;
    top: 25px;
    left: 25px;
}
#sidebar {
  font-family: "Malgun Gothic", sans-serif;
  font-weight: bold;
}
</style>
