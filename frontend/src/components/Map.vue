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
// const width = window.innerWidth
// const height = window.innerHeight
// const camera = new THREE.OrthographicCamera(
//   width / -2, width / 2, height / 2, height / -2, 1, 1000
// )

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  10000
)
const renderer = new THREE.WebGLRenderer({
  antialias: true
})
const light = new THREE.DirectionalLight('hsl(0, 100%, 100%)')
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

    // const mapDataFeaturesTest = [mapData.features[0], mapData.features[1]]

    mapData.features.forEach((element) => {
      this.makeBuilding(scene, element)
    })

    scene.add(axes)
    renderer.setSize(window.innerWidth, window.innerHeight)
    light.position.set(smapleStartPoint[0], smapleStartPoint[1], 100)

    // 카메라 위치/방향 업데이트
    camera.position.set(smapleStartPoint[0], smapleStartPoint[1], 100)
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
      const coords = data.geometry.coordinates
      const height = data.properties.A10

      if (data.geometry.type === 'Polygon' && data.properties.A10 && data.geometry.coordinates.length > 0) {
        const shape = new THREE.Shape()
        const coordsArray = coords[0]

        shape.moveTo(coordsArray[0][0], coordsArray[0][1], 0)
        coordsArray.slice(1).forEach(element => {
          shape.lineTo(element[0], element[1], 0)
        })

        const extrudeSettings = {
          depth: height,
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
