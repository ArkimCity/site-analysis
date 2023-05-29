<template>
  <div ref='map' id='map'></div>
</template>

<script>
// 필요 데이터 불러오기
import mapData from '../assets/json/filtered_buildings_geojson.json'
import { toJSON } from 'dom-to-json'
// import { VRButton } from 'three/examples/jsm/webxr/VRButton.js'

// 상수
import consts from '../store/constants.js'

// import { Clock, PerspectiveCamera, Scene, WebGLRenderer } from 'three'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

let smapleStartPoint = mapData.features[0].geometry.coordinates[0][0]
smapleStartPoint = [parseFloat(smapleStartPoint[0]), parseFloat(smapleStartPoint[1])]

const landDataUrl = 'https://apis.data.go.kr/1611000/nsdi/LandCharacteristicsService/wfs/getLandCharacteristicsWFS'
const params = {
  serviceKey: 'LhVMAvf7G82KFeNYzgE28ylo5LVFxX6K%2F2XBtOGTyFbcIzWgF3UKcafqjFyKtZIOIsZDrK9ItETvlAlHait3sg%3D%3D',
  typeName: 'F251',
  bbox: '217970,447107,218515,447524',
  pnu: '414501170010186',
  maxFeatures: '10',
  srsName: 'EPSG:5174',
  resultType: 'results'
}

let landDataRequestUrl = landDataUrl + '?'
Object.keys(params).forEach((key) => {
  landDataRequestUrl += key + '=' + params[key] + '&'
})

fetch(landDataRequestUrl).then(response => {
  return response.text()
}).then((data) => {
  const parser = new DOMParser()
  const xml = parser.parseFromString(data, 'text/xml')
  const parsed = toJSON(xml)

  const parcels = parsed.childNodes[0].childNodes.map((parcel) => {
    const coordsString = parcel.childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].nodeValue
    const coordsAll = coordsString.split(' ').map(coordString => {
      return parseFloat(coordString)
    })

    const coords = []
    for (let i = 0; i < coordsAll.length; i += 2) {
      coords.push([coordsAll[i], coordsAll[i + 1]])
    }
    console.log(coords)
    const pnuString = parcel.childNodes[0].childNodes[1].childNodes[0].nodeValue
    return { coords, pnuString }
  })
  console.log(parcels)
}).catch(err => {
  console.log(err)
})
// 각 기본 렌더링 사항 정의
const scene = new THREE.Scene()
// 카메라 설정 - OrthographicCamera
// const camera = new THREE.OrthographicCamera(
//   window.innerWidth / -2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / -2, 1, 1000000
// )
const camera = new THREE.PerspectiveCamera(
  75, window.innerWidth / window.innerHeight, 0.1, 10000
)
const renderer = new THREE.WebGLRenderer({
  antialias: true
})
renderer.xr.enabled = true
// document.body.appendChild(VRButton.createButton(renderer))
const light = new THREE.AmbientLight('hsl(0, 100%, 100%)')
const axes = new THREE.AxesHelper(5)
const controls = new OrbitControls(camera, renderer.domElement)

// 레이캐스터 추가
const raycaster = new THREE.Raycaster()
// THREE 마우스 포인터 정보
const pointer = new THREE.Vector2()
function onPointerMove (event) {
  // calculate pointer position in normalized device coordinates
  // (-1 to +1) for both components
  pointer.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1
  pointer.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1
}
window.addEventListener('mousemove', onPointerMove)

export default {
  name: 'Map',
  data: function () {
    return {
      mapData: mapData,
      buildingMeshes: [],
      buildingLines: [],
      selectedBuildingMesh: {},
      defaultMeshColor: 'hsl(0, 100%, 50%)',
      selectedMeshColor: 'hsl(50, 100%, 50%)'
    }
  },
  created: function () {
    scene.add(camera)
    scene.add(light)

    // const mapDataFeaturesTest = [mapData.features[0], mapData.features[1]]
    const group = new THREE.Group()
    mapData.features.forEach((element) => {
      this.makeBuilding(element, group)
    })
    scene.add(group)
    scene.add(axes)
    renderer.setSize(window.innerWidth, window.innerHeight)
    window.addEventListener('resize', this.onResize, false)
    // 카메라 위치/방향 업데이트
    // light.position.set(smapleStartPoint[0], smapleStartPoint[1], 1000)
    // camera.position.set(smapleStartPoint[0], smapleStartPoint[1], 1000)
    light.position.set(0, 0, 1000)
    camera.position.set(0, 0, 1000)
    group.position.set(-smapleStartPoint[0], -smapleStartPoint[1], -100)
    console.log(group.position)
    controls.target = new THREE.Vector3(0, 0, 0)
    // controls.enableRotate = false
    scene.background = new THREE.Color('rgb(100, 100, 100)')
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
          if (intersects[i].object.type === 'Mesh') {
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
    makeBuilding: function (data, group) {
      const coords = data.geometry.coordinates
      let height = 1
      if (data.properties[consts.columns['높이']] !== 0) {
        height = data.properties[consts.columns['높이']]
      }
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
          color: this.defaultMeshColor,
          wireframe: false
        })
        const mesh = new THREE.Mesh(geometry, material)
        mesh.propertiesData = data.properties
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
