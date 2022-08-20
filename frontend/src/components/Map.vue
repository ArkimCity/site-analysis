<template>
  <div ref='map'></div>
</template>

<script>
// 필요 데이터 불러오기
import mapData from '../assets/json/filtered_buildings_geojson.json'

// import { Clock, PerspectiveCamera, Scene, WebGLRenderer } from 'three'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

let smapleStartPoint = mapData.features[0].geometry.coordinates[0][0]
smapleStartPoint = [parseFloat(smapleStartPoint[0]), parseFloat(smapleStartPoint[1])]
// const smapleStartPoint = [100, 100]

// 각 기본 렌더링 사항 정의
const scene = new THREE.Scene()
// 카메라 설정
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
geometry.translate(smapleStartPoint[0] + 1, smapleStartPoint[1] + 1, 0)
const material = new THREE.MeshStandardMaterial({
  side: THREE.FrontSide,
  color: 'hsl(0, 100%, 50%)',
  wireframe: false
})
const cube = new THREE.Mesh(geometry, material)
const axes = new THREE.AxesHelper(5)
const controls = new OrbitControls(camera, renderer.domElement)

export default {
  name: 'Map',
  data: function () {
    return {
      mapData: mapData
    }
  },
  created: function () {
    scene.add(camera)
    scene.add(light)
    scene.add(cube)

    mapData.features.forEach((element) => {
      this.makeBuilding(scene, element)
      return false
    })

    scene.add(axes)
    renderer.setSize(window.innerWidth, window.innerHeight)
    light.position.set(smapleStartPoint[0], smapleStartPoint[1], 10)

    // 카메라 위치/방향 업데이트
    camera.position.set(smapleStartPoint[0], smapleStartPoint[1], 10)
    controls.target = new THREE.Vector3(smapleStartPoint[0], smapleStartPoint[1], 0)
    scene.background = new THREE.Color('hsl(0, 100%, 100%)')
    // controls.rotateSpeed = 1.0
    // controls.zoomSpeed = 5
    // controls.panSpeed = 0.8
    // controls.staticMoving = true
    // controls.dynamicDampingFactor = 0.3
  },
  mounted: function () {
    this.$refs.map.appendChild(renderer.domElement)
    this.animate()
  },
  methods: {
    animate: function () {
      requestAnimationFrame(this.animate)
      renderer.render(scene, camera)
      controls.update()
    },
    makeBuilding: function (scene, data) {
      if (data.geometry.type === 'Polygon' && data.properties.A10 && data.geometry.coordinates.length > 0) {
        const coords = data.geometry.coordinates
        const height = data.properties.A10

        const shape = new THREE.Shape()
        const firstCoord = coords.shift()
        shape.moveTo(parseFloat(firstCoord[0]), parseFloat(firstCoord[1]))
        coords.forEach(element => {
          shape.lineTo(parseFloat(element[0]), parseFloat(element[1]))
        })

        const extrudeSettings = {
          steps: 1,
          depth: parseFloat(height),
          bevelEnabled: false
        }

        const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings)
        const material = new THREE.MeshStandardMaterial({
          side: THREE.FrontSide,
          color: 'hsl(0, 100%, 50%)',
          wireframe: false
        })
        const mesh = new THREE.Mesh(geometry, material)
        scene.add(mesh)
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
    }
  }
}
</script>
