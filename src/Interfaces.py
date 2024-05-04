"""
This module provides interfaces for interacting with RFEM (structural analysis software) and exporting data to MATLAB format.

RFEMInterface:
- Provides methods to retrieve data (1D, 2D, and 3D finite elements, finite element nodes, and all objects) from an RFEM model.

ScipyInterface:
- Offers a method to save node and element matrices to a MATLAB file.

Dependencies:
- RFEM.initModel.Model: Main class representing the RFEM model.
- RFEM.Results.meshTables.MeshTables: Fetches mesh-related data from the RFEM model.
- RFEM.Tools.GetObjectNumbersByType.GetAllObjects: Retrieves all objects from the RFEM model.
- scipy.io.savemat: Function to save MATLAB files.
"""

from RFEM.initModel import Model
from RFEM.Results.meshTables import MeshTables
from RFEM.Tools.GetObjectNumbersByType import GetAllObjects
from scipy.io import savemat


class RFEMInterface:

    def __init__(self, model: Model) -> None:
        self.model = model

    def get_fe1d_elements(self):
        """Retrieve 1D finite elements from the RFEM model."""
        return MeshTables.GetAllFE1DElements(model=self.model)

    def get_fe2d_elements(self):
        """Retrieve 2D finite elements from the RFEM model."""
        return MeshTables.GetAllFE2DElements(model=self.model)
    
    def get_fe3d_elements(self):
        """Retrieve 2D finite elements from the RFEM model."""
        return MeshTables.GetAllFE3DElements(model=self.model)

    def get_fe_nodes(self):
        """Retrieve finite element nodes from the RFEM model."""
        return MeshTables.GetAllFENodes(model=self.model)

    def get_all_objects(self):
        """Retrieve all objects from the RFEM model."""
        return GetAllObjects(model=self.model)
    

class ScipyInterface:

    @staticmethod
    def save_matlab(filepath: str, node_matrix: list[list[int]], element_matrix: list[list]):
        savemat(
        filepath, 
        {
            "node_matrix": node_matrix, 
            "element_matrix": element_matrix
        }
    )