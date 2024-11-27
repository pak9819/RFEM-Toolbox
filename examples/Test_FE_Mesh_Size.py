import os
import sys

sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange"))
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange\\RFEMToolbox"))

import RFEM
import RFEM.Calculate
import RFEM.Calculate.meshSettings
import RFEM.Results
import RFEM.Results.resultTables
import RFEM.enums
import RFEM.initModel

from RFEMToolbox import StartupSettings
from RFEMToolbox.Utils import JSONDataWriter


class FEMMeshTest:
    def __init__(self, settings_repo, writer):
        self.model_path = settings_repo.model_path
        self.model_name = settings_repo.model_name
        self.fe_mesh_size = settings_repo.fe_mesh_size
        self.steps = settings_repo.steps
        self.direction = settings_repo.displacement_direction
        self.node_number = settings_repo.node_number - 1 # create list index
        self.writer = writer
        self.displacements = []

    def _open_model(self):
        self.model = RFEM.initModel.openFile(self.model_path)

    def _close_model(self):
        RFEM.initModel.closeModel(self.model_name)

    def _update_settings(self, settings):
        new_sett = {}
        for i in settings:
            if i[0] == 'windSimulationMeshConfig':
                if RFEM.initModel.GetAddonStatus(self.model.clientModel, RFEM.enums.AddOn.wind_simulation_active):
                    new_sett['wind_simulation_active'] = settings['wind_simulation_active']
            elif i[0] == 'general_target_length_of_fe':
                new_sett['general_target_length_of_fe'] = self.fe_mesh_size
            else:
                new_sett[i[0]] = settings[i[0]]

        self.model.clientModel.service.set_mesh_settings(new_sett)

    def _generate_mesh(self):
        RFEM.Calculate.meshSettings.GenerateMesh(self.model)

    def _calculate_displacement(self):
        RFEM.initModel.Calculate_all(False, self.model)
        results = RFEM.Results.resultTables.ResultTables.NodesDeformations(model=self.model)
        return results[self.node_number][self.direction]

    def run(self):
        for i, step in enumerate(self.steps):
            print(f"Epoch {i + 1} / {len(self.steps)} | Meshsize={self.fe_mesh_size}")

            self._open_model()
            model_settings = RFEM.Calculate.meshSettings.GetMeshSettings()
            self._update_settings(model_settings)
            self._generate_mesh()

            displacement = self._calculate_displacement()
            self.displacements.append(displacement)
            print(displacement)

            self.writer.write(fe_mesh_size=self.fe_mesh_size, displacement=displacement, index=i)

            self._close_model()

            self.fe_mesh_size -= step


if __name__ == "__main__":

    settings = StartupSettings.load_settings()
    writer = JSONDataWriter(settings.json_save_path)

    dummy_model = RFEM.initModel.Model()

    fem_mesh_test = FEMMeshTest(
        settings_repo=settings,
        writer=writer
    )
    
    fem_mesh_test.run()