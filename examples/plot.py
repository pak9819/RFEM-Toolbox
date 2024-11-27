import os
import sys

sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange"))
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange\\RFEMToolbox"))

import matplotlib.pyplot as plt
import json

from RFEMToolbox import StartupSettings


settings = StartupSettings.load_settings()
with open(settings.json_save_path, 'r') as file:
    data = json.load(file)

fe_mesh_size = [entry["fe_mesh_size"] for entry in data]
displacements = [entry["displacement"] for entry in data]

plt.figure(figsize=(10, 6)) 
plt.plot(fe_mesh_size, displacements, marker='o', linestyle='-', color='b', label='Displacement vs FE Mesh Size')
plt.title('FE Mesh Size vs Displacement')
plt.xlabel('FE Mesh Size')
plt.ylabel('Displacement')
plt.grid(True)
plt.legend()
plt.gca().invert_xaxis()
plt.tight_layout()

plt.show()
