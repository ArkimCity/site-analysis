<template>
  <div ref='canvas'></div>
</template>

<script>
// import { Clock, PerspectiveCamera, Scene, WebGLRenderer } from 'three'
import * as THREE from 'three'
// import TrackballControls from 'three-trackballcontrols'
// import {
//     BloomEffect,
//     EffectComposer,
//     GlitchPass,
//     EffectPass,
//     RenderPass
// } from 'postprocessing'
const scene = new THREE.Scene()
// const composer = new THREE.EffectComposer(new WebGLRenderer())
// const effectPass = new THREE.EffectPass(camera, new BloomEffect())
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
)
const renderer = new THREE.WebGLRenderer({
  antialias: true
})
const light = new THREE.DirectionalLight('hsl(0, 100%, 100%)')
const geometry = new THREE.BoxGeometry(1, 1, 1)
const material = new THREE.MeshStandardMaterial({
  side: THREE.FrontSide,
  color: 'hsl(0, 100%, 50%)',
  wireframe: false
})
const cube = new THREE.Mesh(geometry, material)
const axes = new THREE.AxesHelper(5)
const speed = 0.01
// let controls = null

export default {
  name: 'TheCanvas',
  data: function () {
    return {
    }
  },
  created: function () {
    scene.add(camera)
    scene.add(light)
    scene.add(cube)
    scene.add(axes)
    // renderer.setSize(window.innerWidth, window.innerHeight)
    light.position.set(0, 0, 10)
    camera.position.z = 5
    scene.background = new THREE.Color('hsl(0, 100%, 100%)')
    // controls = new TrackballControls(this.camera)
    // this.controls.rotateSpeed = 1.0
    // this.controls.zoomSpeed = 5
    // this.controls.panSpeed = 0.8
    // this.controls.noZoom = false
    // this.controls.noPan = false
    // this.controls.staticMoving = true
    // this.controls.dynamicDampingFactor = 0.3
  },
  mounted: function () {
    this.$refs.canvas.appendChild(renderer.domElement)
    this.animate()
  },
  methods: {
    animate: function () {
      requestAnimationFrame(this.animate)
      renderer.render(scene, camera)
      cube.rotation.y += speed
      // this.controls.update()
    }
  },
  computed: {
    rotate: function () {
      if (this.speed === '') {
        return 0
      } else {
        return this.speed
      }
    }
  }
}
</script>

<style src='../assets/css/canvas.css'></style>
