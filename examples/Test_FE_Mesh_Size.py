import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange"))
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange\\RFEMToolbox"))

import RFEM
import RFEM.Calculate
import RFEM.Calculate.meshSettings
import RFEM.Results
import RFEM.Results.resultTables
import RFEM.enums
import RFEM.initModel
import RFEM.Calculate.optimizationSettings
import RFEM.Reports
import RFEM.Reports.printoutReport
import RFEM.Results.designOverview
import RFEM.Results.meshTables

from RFEMToolbox import StartupSettings
from RFEMToolbox.Utils import JSONDataWriter
from RFEMToolbox.Interfaces import RFEMInterface 
from RFEMToolbox.DataProcessor import RFEMDataHandler 

import re


class MaterialPropertyRepository:

    def __init__(self, settings_repo) -> None:
        self._e_module = None
        self._poisson = None
        self._density = None

        model = self._open_model(settings_repo.model_path)
        print("Downloading material properties")
        self.handler = RFEMDataHandler(model=model)
        self._load_properties()
        self._close_model(settings_repo.model_name)

    @property
    def e_module(self):
        return self._e_module

    @property
    def poisson(self):
        return self._poisson
    
    @property
    def density(self):
        return self._density
    
    def _open_model(self, model_path):
        return RFEM.initModel.openFile(model_path)

    def _close_model(self, model_name):
        RFEM.initModel.closeModel(model_name)

    def _load_properties(self):
            try:
                self._e_module = self.handler.materials[0]["temperature"]["material_temperature"][0]["row"]["elasticity_modulus_global"]
            except: self._e_module = 0
            try:
                self._poisson = self.handler.materials[0]["temperature"]["material_temperature"][0]["row"]["poisson_ratio_global"]
            except: self._poisson = 0
            try:
                self._density = self.handler.materials[0]["temperature"]["material_temperature"][0]["row"]["mass_density"]
            except: self._density = 0


class FEMMeshTest:

    def __init__(self, settings_repo, writer, material_properties):
        self.model_path = settings_repo.model_path
        self.model_name = settings_repo.model_name
        self.fe_mesh_size = settings_repo.fe_mesh_size
        self.steps = settings_repo.steps
        self.direction = settings_repo.displacement_direction
        self.node_number = settings_repo.node_number - 1 # create list index
        self.length = settings_repo.length
        self.height = settings_repo.height
        self.width = settings_repo.width
        self.boundary_left = settings_repo.boundary_left
        self.support_mid = settings_repo.boundary_mid
        self.boundary_right = settings_repo.boundary_right
        self.load_type = settings_repo.load_type
        self.force = settings_repo.force
        self.displacement_ref = settings_repo.displacement_reference
        self.file_path = self._get_path(settings_repo.log_file_path, settings_repo.log_file_project_name)
        self.material = settings_repo.material
        self.e_module = material_properties.e_module
        self.poisson = material_properties.poisson
        self.density = material_properties.density
        self.structure_type = settings_repo.structure_type
        self.structure_id = settings_repo.structure_id

        self.writer: JSONDataWriter = writer

    def _get_path(self, base_directory, project_name):

        base_dir = Path(base_directory)
        relative_path = f"{project_name}\\content\\!solver\\Data.sm_log"

        if not base_dir.exists() or not base_dir.is_dir():
            print(f"Directory not found: {base_directory}")
            return None

        instance_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('instance')]

        latest_instance = max(instance_dirs, key=lambda d: d.stat().st_mtime)
        target_path = latest_instance / relative_path
        return target_path
 
    def _open_model(self):
        self.model = RFEM.initModel.openFile(self.model_path)

    def _close_model(self):
        RFEM.initModel.closeModel(self.model_name)

    def _update_settings(self, settings, size):
        new_sett = {}
        for i in settings:
            if i[0] == 'windSimulationMeshConfig':
                if RFEM.initModel.GetAddonStatus(self.model.clientModel, RFEM.enums.AddOn.wind_simulation_active):
                    new_sett['wind_simulation_active'] = settings['wind_simulation_active']
            elif i[0] == 'general_target_length_of_fe':
                new_sett['general_target_length_of_fe'] = size
            else:
                new_sett[i[0]] = settings[i[0]]

        self.model.clientModel.service.set_mesh_settings(new_sett)

    def _generate_mesh(self):
        RFEM.Calculate.meshSettings.GenerateMesh(self.model)
    
    def get_max(self, data):
        max_displacement_z = max(
            (item.get('displacement_z', float('-inf')) for item in data if isinstance(item, dict)),
            default=float('-inf')  # Default in case the list is empty or no valid 'displacement_z' values
        )
        return max_displacement_z if max_displacement_z != float('-inf') else None

    def _calculate_displacement(self):
        RFEM.initModel.Calculate_all(False, self.model)
        results = RFEM.Results.resultTables.ResultTables.SurfacesGlobalDeformations()
        # results = RFEM.Results.resultTables.ResultTables.NodesDeformations(model=self.model)
        return self.get_max(results)
    
    def _get_total_time(self):
        # Regular expression pattern to match 'Total time: ...'
        pattern = r'Total time:\s*([\d\.:]+)'
        total_times = []
        with open(self.file_path, 'r', encoding='utf-16') as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    # Extract the time value from the first capturing group
                    time_value = match.group(1)
                    total_times.append(time_value)

        if len(total_times) >= 2:
            # Return the two Total Time values
            mesh_total_time = total_times[0]
            calc_total_time = total_times[1]
            return (mesh_total_time, calc_total_time)
        elif len(total_times) == 1:
            print("Only one 'Total time' value found in the log file.")
            mesh_total_time = total_times[0]
            calc_total_time = None
            return (mesh_total_time, calc_total_time)
        else:
            print("No 'Total time' value found in the log file.")
            return (None, None)

    def run(self):
        for i, step in enumerate(self.steps):
            print(f"Epoch {i + 1} / {len(self.steps)} | Meshsize={self.fe_mesh_size}")

            self._open_model()
            model_settings = RFEM.Calculate.meshSettings.GetMeshSettings()
            self._update_settings(model_settings, self.fe_mesh_size)
            self._generate_mesh()

            displacement = self._calculate_displacement()
            print(displacement)

            interface = RFEMInterface(self.model)
            elements = interface.get_fe2d_elements()
            nodes = interface.get_fe_nodes()

            time = self._get_total_time()

            self.writer.write(
                struct_type=self.structure_type,
                struct_id=f"{self.structure_id}_{i}",
                length=self.length,
                height=self.height,
                width=self.width,
                material=self.material,
                e_module=self.e_module,
                poisson=self.poisson,
                density=self.density,
                support_left=self.boundary_left,
                support_mid=self.support_mid,
                support_right=self.boundary_right,
                load_type=self.load_type,
                force=self.force,
                elements=len(elements),
                nodes=len(nodes),
                mesh_size=self.fe_mesh_size, 
                max_displacement=displacement, 
                displacement_delta=displacement,
                calculation_time_mesh=time[0],
                calculation_time_total=time[1]
            )

            self._close_model()

            self.fe_mesh_size -= step

if __name__ == "__main__":

    settings = StartupSettings.load_settings()
    writer = JSONDataWriter(settings.json_save_path)

    dummy_model = RFEM.initModel.Model()

    material_properties = MaterialPropertyRepository(settings_repo=settings)

    fem_mesh_test = FEMMeshTest(
        settings_repo=settings,
        writer=writer,
        material_properties=material_properties
    )
    
    fem_mesh_test.run()