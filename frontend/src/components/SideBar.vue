<template>
  <div id='sidebar'>
    시군구

    공원
    병원
    학교
    녹지
    도로
  </div>
</template>

<script>
export default {
  name: 'SideBar',
  data: function () {
    return {
      pnuInput: null
    }
  },
  components: {
  },
  methods: {
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
