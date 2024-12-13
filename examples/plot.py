import os
import sys
import matplotlib.pyplot as plt
import json

# Import custom toolbox
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange"))
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange\\RFEMToolbox"))
from RFEMToolbox import StartupSettings

# Load data
settings = StartupSettings.load_settings()
with open(settings.json_save_path, 'r') as file:
    data = json.load(file)

# Extract data for plotting
fe_mesh_size = [entry["elements"] for entry in data]
displacements = [entry["max_displacement"] for entry in data]
total_computation_time = [entry["total_calculation_time"] for entry in data]

# Plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot displacement vs FE mesh size
ax1.plot(fe_mesh_size, displacements, marker='o', linestyle='-', color='b', label='Displacement')
ax1.set_xlabel('FE Mesh Size (Elements)')
ax1.set_ylabel('Displacement', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True)

# Invert x-axis
ax1.invert_yaxis()

# Add a second y-axis for total computation time
ax2 = ax1.twinx()
ax2.plot(fe_mesh_size, total_computation_time, marker='s', linestyle='--', color='r', label='Computation Time')
ax2.set_ylabel('Total Computation Time (s)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Add legends for both lines
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

# Title and layout
plt.title('FE Mesh Size vs Displacement and Computation Time (Inverted X-Axis)')
plt.tight_layout()

# Show plot
plt.show()
