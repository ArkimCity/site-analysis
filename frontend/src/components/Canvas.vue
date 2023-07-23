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

      if (newValue.propertiesData) {
        const box = newValue.clone() // 같은 three js mesh 가 두개의 scene 에 동시에 존재할 수 없기 때문에 clone 합니다.
        scene.add(box)

        const boundingBox = new THREE.Box3().setFromObject(box)
        const center = boundingBox.getCenter(new THREE.Vector3())
        const size = boundingBox.getSize(new THREE.Vector3())

        const multiples = 1.1
        const cameraX = center.x
        const cameraY = center.y
        const cameraZ = center.z + Math.max(size.x, size.y, size.z) * multiples

        camera.position.set(cameraX, cameraY, cameraZ)
        camera.lookAt(center)

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
