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


def get_only_polygons(data_all):
    data_filtered = {"type": parcels_data_all["type"], "features": []}

    for each_building in data_all["features"]:
        if each_building["geometry"]["type"] != "Polygon":
            print("폴리곤 아님")
            continue
        data_filtered["features"].append(each_building)

    return data_filtered


def get_x_y_lists(parcels_data_filtered):
    # 필지 데이터에서 최대 및 최소값 지정
    y_min, x_min, y_max, x_max = math.inf, math.inf, -math.inf, -math.inf
    for each_parcel in parcels_data_filtered["features"]:
        coordinates = each_parcel["geometry"]["coordinates"]
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

    x_interval = (x_max - x_min) / DIVISION_NUMBER
    y_interval = (y_max - y_min) / DIVISION_NUMBER

    x_list = [x_min + x_interval * i for i in range(DIVISION_NUMBER + 1)]
    y_list = [y_min + y_interval * i for i in range(DIVISION_NUMBER + 1)]

    return x_list, y_list

def save_divided_data_by_location_key(map_data_filtered, x_list, y_list):
    divided_map_data = {}

    for each_building in map_data_filtered["features"]:
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
                            divided_map_data[(x_list[j], y_list[i], x_list[j + 1], y_list[i + 1])] = {"type": map_data_filtered["type"], "features": [each_building]}
                            breaker = True
                            break

            if breaker:
                break

    return divided_map_data

def prepare_save_path(folder_name):
    data_divided_folder_path = os.path.join(
        os.path.abspath(__file__), "..", "..", f"frontend/src/assets/json/{folder_name}"
    )
    if not os.path.exists(data_divided_folder_path):
        # 없을 경우 새로 생성
        os.mkdir(data_divided_folder_path)
    else:
        # 파일 교체
        shutil.rmtree(data_divided_folder_path)
        os.mkdir(data_divided_folder_path)

    return data_divided_folder_path


def save_divided_results(divided_map_data, data_divided_folder_path, mode):
    assert mode in ("parcels", "buildings")

    file_name_json = {}
    for loc_key in divided_map_data:
        file_name = f"{loc_key[0]}_{loc_key[1]}_{loc_key[2]}_{loc_key[3]}.json"

        file_name_json[file_name] = {"x_min": loc_key[0], "y_min": loc_key[1], "x_max": loc_key[2], "y_max": loc_key[3]}

        with open(os.path.join(data_divided_folder_path, file_name), "w", encoding="utf-8") as f:
            json.dump(divided_map_data[loc_key], f)

    with open(
        os.path.join(data_divided_folder_path, "..", f"{mode}_files_info.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(file_name_json, f)


if __name__ == "__main__":
    # 002 - 필지, 010 - 건물
    parcels_json_file = "AL_11_D002_20230506.json"
    buildings_json_file = "AL_11_D010_20230506.json"

    with open(os.path.join(os.path.abspath(__file__), "..", parcels_json_file), encoding="utf-8") as f:
        parcels_data_all = json.load(f)
    with open(os.path.join(os.path.abspath(__file__), "..", buildings_json_file), encoding="utf-8") as f:
        buildings_data_all = json.load(f)

    # 조건을 가지고 추린 것만 사용 - 여기서는 min  Polygon 만 사용
    parcels_data_filtered = get_only_polygons(parcels_data_all)
    buildings_data_filtered = get_only_polygons(buildings_data_all)

    # 필지 데이터에서 최대 및 최소값 지정
    x_list, y_list = get_x_y_lists(parcels_data_filtered)

    # 추린 데이터 가지고 파일 분할
    divided_parcels_map_data = save_divided_data_by_location_key(parcels_data_filtered, x_list, y_list)
    divided_buildings_map_data = save_divided_data_by_location_key(buildings_data_filtered, x_list, y_list)

    # 분할된 필지 데이터 폴더 생성
    parcels_data_divided_folder_path = prepare_save_path("parcels_data_divided")
    buildings_data_divided_folder_path = prepare_save_path("buildings_data_divided")

    save_divided_results(divided_parcels_map_data, parcels_data_divided_folder_path, "parcels")
    save_divided_results(divided_buildings_map_data, buildings_data_divided_folder_path, "buildings")
