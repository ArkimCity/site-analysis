<template>
  <div ref='map' id='map'></div>
</template>

<script>
import { mapState } from 'vuex'
import consts from '../store/constants.js'
import proj4 from 'proj4'
import districts from '../assets/json/si_goon_goo.json'
import seoulHospital from '../assets/json/seoul_hospital.json'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

// ----------------------------------------------------------------------------
let smapleStartPoint = districts.features[0].geometry.coordinates[0][0]
smapleStartPoint = [parseFloat(smapleStartPoint[0]), parseFloat(smapleStartPoint[1])]

// 각 기본 렌더링 사항 정의
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000000)
const renderer = new THREE.WebGLRenderer({ antialias: true })
const light = new THREE.AmbientLight('hsl(0, 100%, 100%)')
const axes = new THREE.AxesHelper(5)
const controls = new OrbitControls(camera, renderer.domElement)

// 레이캐스터 추가
const raycaster = new THREE.Raycaster()
// THREE 마우스 포인터 정보
const pointer = new THREE.Vector2()
function onPointerMove (event) {
  // calculate pointer position in normalized device coordinates
  pointer.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1
  pointer.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1
}
window.addEventListener('mousemove', onPointerMove)
// ----------------------------------------------------------------------------

export default {
  name: 'Map',
  // data -> computed -> created -> mounted
  data: function () {
    return {
      buildingMeshes: [],
      buildingLines: [],
      selectedBuildingMesh: {},
      defaultMeshColor: 'hsl(0, 100%, 50%)',
      otherDistrictMeshColor: 'hsl(10, 90%, 90%)',
      selectedMeshColor: 'hsl(50, 100%, 50%)'
    }
  },
  computed: {
    ...mapState(['fetchedPnu']),
    rotate: function () {
      if (this.speed === '') {
        return 0
      } else {
        return this.speed
      }
    }
  },
  created: function () {
    scene.add(camera)
    scene.add(light)

    const group = new THREE.Group()
    // 서울에 해당하는 25개 구
    districts.features.slice(0, 25).forEach((element) => {
      this.makeDistrict(element, group, true)
    })
    // 이외에 해당하는 시군구
    districts.features.slice(25).forEach((element) => {
      this.makeDistrict(element, group)
    })
    // 서울에 있는 병원 데이터
    seoulHospital.DATA.forEach((eachHospital) => {
      let radius = 500
      if (['의원', '한의원', '치과의원'].includes(eachHospital.dutydivnam)) {
        return // 너무 많아서 일단 스킵
      } else if (['병원', '한방병원', '치과병원'].includes(eachHospital.dutydivnam)) {
        radius = 1000
      } else if (['종합병원'].includes(eachHospital.dutydivnam)) {
        radius = 3000
      } else {
        return
      }

      const { x, y } = this.convertLatLongToEPSG5179(eachHospital.wgs84lat, eachHospital.wgs84lon)
      const height = 2 // Replace with the desired height for the extrusion

      const circleExtrudeMesh = this.createCircleExtrudeGeometry(x, y, height, radius, 0x0000ff, 0.3)
      circleExtrudeMesh.propertiesData = { isSeoul: false } // FIXME

      group.add(circleExtrudeMesh)
    })

    scene.add(group)
    scene.add(axes)
    renderer.setSize(window.innerWidth, window.innerHeight)
    window.addEventListener('resize', this.onResize, false)
    // 카메라 위치/방향 업데이트
    light.position.set(0, 0, 10000)
    camera.position.set(0, 0, 10000)
    group.position.set(-smapleStartPoint[0], -smapleStartPoint[1], -100)
    controls.target = new THREE.Vector3(0, 0, 0)
    controls.enableRotate = false
    scene.background = new THREE.Color('rgb(230, 230, 230)')
  },
  mounted: function () {
    this.$refs.map.appendChild(renderer.domElement)
    this.animate()
  },
  unmounted: function () {
    this.buildingMeshes.forEach((element) => {
      element.geometry.dispose()
      element.material.dispose()
      scene.remove(element)
    })
    this.buildingLines.forEach((element) => {
      element.geometry.dispose()
      element.material.dispose()
      scene.remove(element)
    })
  },
  watch: {
    fetchedPnu: function (newFetchedPnu, oldFetchedPnu) {
      this.fetchDatasWithPnu(newFetchedPnu)
    }
  },
  methods: {
    animate: function () {
      renderer.setAnimationLoop(this.animate)

      // update the picking ray with the camera and pointer position
      raycaster.setFromCamera(pointer, camera)
      // calculate objects intersecting the picking ray
      const intersects = raycaster.intersectObjects(scene.children)
      if (this.$store.state.selectedBuilding.propertiesData) {
        this.$store.state.selectedBuilding.material.color.set(this.defaultMeshColor)
      }
      if (intersects.length > 0) {
        for (let i = 0; i < intersects.length; i++) {
          if (intersects[i].object.type === 'Mesh' && intersects[i].object.propertiesData.isSeoul) {
            this.$store.state.selectedBuilding = intersects[i].object
            this.$store.state.selectedBuilding.material.color.set(this.selectedMeshColor)
            break
          }
        }
      } else {
        this.$store.state.selectedBuilding = { propertiesData: null }
      }

      renderer.render(scene, camera)
      controls.update()
    },
    onResize: function () {
      camera.aspect = window.innerWidth / window.innerHeight
      camera.updateProjectionMatrix()
      renderer.setSize(window.innerWidth, window.innerHeight)
    },
    makeDistrict: function (data, group, isSeoul = false) {
      const coords = data.geometry.coordinates
      const height = consts.DISTRICT_HEIGHT
      if (data.geometry.type === 'Polygon' && height && data.geometry.coordinates.length > 0) {
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
          color: isSeoul ? this.defaultMeshColor : this.otherDistrictMeshColor,
          wireframe: false
        })
        const mesh = new THREE.Mesh(geometry, material)
        mesh.propertiesData = data.properties
        mesh.propertiesData.isSeoul = isSeoul
        group.add(mesh)
        this.buildingMeshes.push(mesh)

        const edges = new THREE.EdgesGeometry(geometry)
        const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0xffffff }))
        line.testData = 'line'
        group.add(line)
        this.buildingLines.push(line)
      }
    },
    resizeCanvasToDisplaySize: function () {
      const canvas = renderer.domElement
      // look up the size the canvas is being displayed
      const width = window.innerWidth
      const height = window.innerHeight

      // adjust displayBuffer size to match
      if (canvas.width !== width || canvas.height !== height) {
        // you must pass false here or three.js sadly fights the browser
        renderer.setSize(width, height, false)
        camera.aspect = width / height
        camera.updateProjectionMatrix()

        // update any render target sizes here
        this.resizeCanvasToDisplaySize()
      }
    },
    convertLatLongToEPSG5179: function (latitude, longitude) {
      const sourceEPSG = 'EPSG:4326' // WGS84 (latitude and longitude)
      const targetEPSG = 'EPSG:5179' // Korean Transverse Mercator (KTM)
      // proj4.defs(sourceEPSG, '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
      proj4.defs(targetEPSG, '+proj=tmerc +lat_0=38 +lon_0=127.5 +k=0.9996 +x_0=1000000 +y_0=2000000 +ellps=GRS80 +units=m +no_defs')

      const point = proj4(sourceEPSG, targetEPSG, [parseFloat(longitude), parseFloat(latitude)])
      return { x: point[0], y: point[1] }
    },
    createCircleExtrudeGeometry: function (x, y, height, radius, color, opacity) {
      const material = new THREE.MeshPhongMaterial({
        color: color,
        transparent: true,
        opacity: opacity
      })

      const circleExtrudeGeometry = new THREE.SphereBufferGeometry(radius, 8, 8)
      circleExtrudeGeometry.translate(x, y, 0)
      const circleExtrudeMesh = new THREE.Mesh(circleExtrudeGeometry, material)
      return circleExtrudeMesh
    }
  }
}
</script>
