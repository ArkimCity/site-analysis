import json

index_file_path = "C:/Users/jaeun/OneDrive/문서/GitHub/site-analysis/frontend/src/assets/json/building_files_info.json"
loader_file_path = "C:/Users/jaeun/OneDrive/문서/GitHub/site-analysis/frontend/src/assets/json/loader.js"


with open(index_file_path) as f:
    index_file_json = json.load(f)

    with open(loader_file_path, "w") as f2:
        f2.writelines([
            f"import mapData{i} from './building_data_divided/" + key + "'\n"
            for i, key in enumerate(index_file_json)
        ])

        f2.write("\n")
