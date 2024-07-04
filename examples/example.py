import RFEM
import RFEM.Calculate
import RFEM.Calculate.meshSettings
import RFEM.Results
import RFEM.Results.resultTables
import RFEM.enums
import RFEM.initModel

class FEMMeshTest:

    def __init__(self, model_path, initial_fe_mesh_size=0.5, steps=None):
        self.model_path = model_path
        self.fe_mesh_size = initial_fe_mesh_size
        self.steps = steps if steps is not None else [0.02] * 20
        self.displacements = []

    def _open_model(self):
        self.model = RFEM.initModel.openFile(self.model_path)

    def _close_model(self):
        RFEM.initModel.closeModel('Kragarm.rf6')

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
        return results[2]['displacement_z']

    def run(self):
        for step in self.steps:
            self._open_model()

            settings = RFEM.Calculate.meshSettings.GetMeshSettings()
            self._update_settings(settings)

            self._generate_mesh()

            self.fe_mesh_size -= step

            displacement_z = self._calculate_displacement()
            self.displacements.append(displacement_z)

            self._close_model()

        print(self.displacements)


if __name__ == "__main__":

    test_model = RFEM.initModel.Model("FE_Mesh_test")

    fem_mesh_test = FEMMeshTest('C:\\Users\\User\\Desktop\\Kragarm.rf6')
    fem_mesh_test.run()