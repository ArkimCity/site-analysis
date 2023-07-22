<template>
  <div ref='canvas'></div>
</template>

<script>
import * as THREE from 'three'
import { mapState } from 'vuex'
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
const renderer = new THREE.WebGLRenderer({ antialias: true })
const light = new THREE.DirectionalLight('hsl(0, 100%, 100%)')
const axes = new THREE.AxesHelper(5)

export default {
  name: 'TheCanvas',
  data: function () {
    return {
    }
  },
  created: function () {
    scene.add(camera)
    scene.add(light)
    scene.add(axes)
    scene.background = new THREE.Color('hsl(0, 100%, 100%)')
  },
  mounted: function () {
    this.$refs.canvas.appendChild(renderer.domElement)
    this.animate()
  },
  methods: {
    animate: function () {
      requestAnimationFrame(this.animate)
      renderer.render(scene, camera)
    },
    setBuilding: function (newValue) {
      // Remove all other meshes from the scene and dispose them
      scene.children.forEach((child) => {
        if (child !== newValue && child.type === 'Mesh') {
          scene.remove(child)
          // Dispose of the geometry and material to free up memory
          child.geometry.dispose()
          child.material.dispose()
        }
      })

      console.log(newValue)

      if (newValue.propertiesData) {
        const box = newValue.clone()
        scene.add(box)

        // Calculate the bounding box of the box object
        const boundingBox = new THREE.Box3().setFromObject(box)

        // Calculate the center of the bounding box
        const center = boundingBox.getCenter(new THREE.Vector3())

        // Get the size of the bounding box
        const size = boundingBox.getSize(new THREE.Vector3())

        // Calculate the position for the camera
        const multiples = 1.1
        const cameraX = center.x
        const cameraY = center.y
        const cameraZ = center.z + Math.max(size.x, size.y, size.z) * multiples

        // Set the camera position and look at the center of the bounding box
        camera.position.set(cameraX, cameraY, cameraZ)
        camera.lookAt(center)

        // Set the light position
        light.position.set(cameraX, cameraY, cameraZ)
      }
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
    selectedBuilding: function (newVal, oldVal) {
      this.setBuilding(newVal)
    }
  }
}
</script>
