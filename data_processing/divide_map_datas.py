"""
- 데이터 원본 사이트
http://openapi.nsdi.go.kr/nsdi/eios/OpenapiList.do?provOrg=NIA&gubun=F
    - gis 건물통합정보
    - 연속지적도형정보

http://www.gisdeveloper.co.kr/?p=2332
    - 행정구역 도형
    - EPSG:5179

<hr>

- 데이터 원본 geojson 으로 변환
https://mapshaper.org/

- import 시
    - encoding=euc-kr
- import 이후 console 에서 lat long 으로 변환하고 싶을 시
    - -proj wgs84
"""

import json
import os
import math
import shutil


DIVISION_NUMBER = 50

def flatten_list(nested_list):
    flattened_list = []
    for item in nested_list:
        if isinstance(item, list):
            flattened_list.extend(flatten_list(item))
        else:
            flattened_list.append(item)
    return flattened_list

if __name__ == "__main__":
    # 002 - 필지, 010 - 건물
    buildings_json_file = "AL_11_D002_20230506.json"

    with open(os.path.join(os.path.abspath(__file__), "..", buildings_json_file), encoding="utf-8") as f:
        map_data_all = json.load(f)

    # 최대 최소 좌표
    y_min, x_min, y_max, x_max = math.inf, math.inf, -math.inf, -math.inf

    # 조건을 가지고 추린 것만 사용 - 여기서는 Polygon 만 사용
    map_data_filtered = {"type": map_data_all["type"], "features": []}

    for each_building in map_data_all["features"]:
        if each_building["geometry"]["type"] != "Polygon":
            # MultiPolygon 4개 존재. 편의상 극소수임으로 무시
            print("폴리곤 아님")
            continue

        # 모든 건물을 통틀어 좌표 최대값 및 최소값 체크
        coordinates = each_building["geometry"]["coordinates"]
        flattened_coordinates = flatten_list(coordinates)

        flattened_coordinates_even = flattened_coordinates[::2]
        flattened_coordinates_odd = flattened_coordinates[1::2]

        building_x_min = min(flattened_coordinates_even)
        building_y_min = min(flattened_coordinates_odd)
        building_x_max = max(flattened_coordinates_even)
        building_y_max = max(flattened_coordinates_odd)

        y_min = min(y_min, building_y_min)
        x_min = min(x_min, building_x_min)
        y_max = max(y_max, building_y_max)
        x_max = max(x_max, building_x_max)

        map_data_filtered["features"].append(each_building)


    x_interval = (x_max - x_min) / DIVISION_NUMBER
    y_interval = (y_max - y_min) / DIVISION_NUMBER

    x_list = [x_min + x_interval * i for i in range(DIVISION_NUMBER + 1)]
    y_list = [y_min + y_interval * i for i in range(DIVISION_NUMBER + 1)]

    # 추린 데이터 가지고 파일 분할
    divided_map_data = {}
    for building_index, each_building in enumerate(map_data_filtered["features"]):
        coordinates = each_building["geometry"]["coordinates"]
        flattened_coordinates = flatten_list(coordinates)
        x_s, y_s = flattened_coordinates[0], flattened_coordinates[1]

        breaker = False

        for i in range(DIVISION_NUMBER):
            if y_list[i] <= y_s < y_list[i + 1]:
                for j in range(DIVISION_NUMBER):
                    if x_list[j] <= x_s < x_list[j + 1]:

                        if (x_list[j], y_list[i], x_list[j + 1], y_list[i + 1]) in divided_map_data:
                            divided_map_data[(x_list[j], y_list[i], x_list[j + 1], y_list[i + 1])]["features"].append(each_building)
                            breaker = True
                            break
                        else:
                            divided_map_data[(x_list[j], y_list[i], x_list[j + 1], y_list[i + 1])] = {"type": map_data_all["type"], "features": [each_building]}
                            breaker = True
                            break

            if breaker:
                break

    # 분할된 건물 데이터 폴더 생성
    building_data_divided_folder_path = os.path.join(os.path.abspath(__file__), "..", "..", "frontend/src/assets/json/building_data_divided")
    if not os.path.exists(building_data_divided_folder_path):
        # 없을 경우 새로 생성
        os.mkdir(building_data_divided_folder_path)
    else:
        # 파일 교체
        shutil.rmtree(building_data_divided_folder_path)
        os.mkdir(building_data_divided_folder_path)

    file_name_json = {}
    for loc_key in divided_map_data:
        file_name = f"{loc_key[0]}_{loc_key[1]}_{loc_key[2]}_{loc_key[3]}.json"

        file_name_json[file_name] = {"x_min": loc_key[0], "y_min": loc_key[1], "x_max": loc_key[2], "y_max": loc_key[3]}

        with open(os.path.join(building_data_divided_folder_path, file_name), "w", encoding="utf-8") as f:
            json.dump(divided_map_data[loc_key], f)

    with open(os.path.join(building_data_divided_folder_path, "..", "building_files_info.json"), "w", encoding="utf-8") as f:
        json.dump(file_name_json, f)
