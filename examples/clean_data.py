import os
import sys

sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange"))
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange\\RFEMToolbox"))

from RFEMToolbox import StartupSettings

import json

def convert_time_to_seconds(time_str):
    h, m, s = map(float, time_str.split(":"))
    return round(h * 3600 + m * 60 + s, 3)

def calculate_displacement_delta(disp, disp_ref):
    return ((disp-disp_ref)/disp_ref)*100

def process_data(file_path, displacement_reference):
    # Read and parse the JSON file
    with open(file_path, "r", encoding="ascii") as file:
        data = json.load(file)
    for item in data:
        if not type(item["mesh_calculation_time"]) == float:
            item["mesh_calculation_time"] = convert_time_to_seconds(item["mesh_calculation_time"])
        if not type(item["total_calculation_time"]) == float:
            item["total_calculation_time"] = convert_time_to_seconds(item["total_calculation_time"])
        item["mesh_size"] = round(item["mesh_size"], 2)
        item["displacement_delta"] = calculate_displacement_delta(item["max_displacement"], displacement_reference)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


settings = StartupSettings.load_settings()
file_path = settings.json_save_path
displacement_ref = settings.displacement_reference
process_data(file_path, displacement_ref)



