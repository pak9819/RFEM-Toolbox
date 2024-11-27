import os
import sys
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange"))
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange\\RFEMToolbox"))

import RFEM
import RFEM.initModel

from RFEMToolbox.DataProcessor import RFEMDataHandler, MeshType
from RFEMToolbox.Exporter import Exporter
from RFEMToolbox import StartupSettings

if __name__ == "__main__":

    settings = StartupSettings.load_settings()

    model = RFEM.initModel.Model(new_model=False, model_name=settings.model_name)
    handler = RFEMDataHandler(model, MeshType.FE2D)

    nodes = handler.nodes
    elements = handler.elements

    Exporter.write(settings.save_path, nodes, elements)