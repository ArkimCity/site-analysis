<template>
  <div ref='canvas'></div>
</template>

<script>
// import { Clock, PerspectiveCamera, Scene, WebGLRenderer } from 'three'
import * as THREE from 'three'
import { mapState } from 'vuex'
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
const axes = new THREE.AxesHelper(5)
// let controls = null
// const controls = new TrackballControls(camera)

export default {
  name: 'TheCanvas',
  data: function () {
    return {
    }
  },
  created: function () {
    this.$watch('$store.state.selectedBuilding', this.handleSelectedBuildingChange, { deep: true });
    scene.add(camera)
    scene.add(light)
    scene.add(axes)
    // renderer.setSize(window.innerWidth, window.innerHeight)
    scene.background = new THREE.Color('hsl(0, 100%, 100%)')
    // controls.rotateSpeed = 1.0
    // controls.zoomSpeed = 5
    // controls.panSpeed = 0.8
    // controls.noZoom = false
    // controls.noPan = false
    // controls.staticMoving = true
    // controls.dynamicDampingFactor = 0.3
  },
  mounted: function () {
    this.$refs.canvas.appendChild(renderer.domElement)
    this.animate()
  },
  methods: {
    animate: function () {
      requestAnimationFrame(this.animate)
      renderer.render(scene, camera)
      // cube.rotation.y += speed
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
    },
    ...mapState(['selectedBuilding'])
  },
  watch: {
    selectedBuilding: function (newValue, oldValue) {
      // Remove all other meshes from the scene and dispose them
      scene.children.forEach((child) => {
        if (child !== newValue && child.type === "Mesh") {
          scene.remove(child);
          // Dispose of the geometry and material to free up memory
          child.geometry.dispose();
          child.material.dispose();
        }
      });

      console.log(newValue);

      if (newValue.propertiesData) {
        const box = newValue.clone();
        scene.add(box);

        console.log("box added");

        // Calculate the bounding box of the box object
        const boundingBox = new THREE.Box3().setFromObject(box);

        // Calculate the center of the bounding box
        const center = boundingBox.getCenter(new THREE.Vector3());

        // Get the size of the bounding box
        const size = boundingBox.getSize(new THREE.Vector3());

        // Calculate the position for the camera
        const cameraX = center.x;
        const cameraY = center.y + 10;
        const cameraZ = center.z + Math.max(size.x, size.y, size.z) + 10;

        // Set the camera position and look at the center of the bounding box
        camera.position.set(cameraX, cameraY, cameraZ);
        camera.lookAt(center);

        // Set the light position
        light.position.set(cameraX, cameraY, 100);
      }
    }
  }
}
</script>
