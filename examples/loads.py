import os
import sys
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange"))
sys.path.append(os.path.join(os.path.abspath('../'), "RFEM-Matlab-Exchange\\RFEMToolbox"))

import RFEM

from RFEMToolbox import StartupSettings

def getLoads():
    loads = []
    print(loads)

if __name__ == "__main__":

    model_name = StartupSettings.get_model_name()

    model = RFEM.initModel.Model(new_model=False, model_name=model_name)
    getLoads()

