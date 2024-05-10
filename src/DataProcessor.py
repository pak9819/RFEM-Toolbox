"""
This module handles RFEM data processing and provides convenient access to mesh elements, nodes, and materials.

MeshType:
- Enumerates types of mesh in RFEM: FE1D, FE2D, and FE3D.

RFEMDataHandler:
- Manages RFEM data handling based on provided mesh type.
- Initializes with RFEM model and mesh type.
- Retrieves element and node data from RFEM via RFEMInterface.
- Utilizes DataUtils for data transformation.

Dependencies:
- enum.Enum: Base class for creating enumerated constants.
- Interfaces.RFEMInterface: Provides interfaces to interact with RFEM models.
- Utils.DataUtils: Utility functions for data transformation.
"""

from RFEM.initModel import Model

from enum import Enum
from Interfaces import RFEMInterface
from Utils import DataUtils


class MeshType(Enum):
    FE1D = 1
    FE2D = 2
    FE3D = 3


class RFEMDataHandler:

    def __init__(self, model: Model, mesh_type: MeshType):
        self._rfem_interface = RFEMInterface(model=model)
        self._mesh_type = mesh_type
        self._raw_element_data = self._get_rfem_elements()
        self._raw_node_data = self._get_rfem_nodes()
        self._raw_data = self._rfem_interface.get_all_objects()
        self._materials = DataUtils.get_materials(self._raw_data)
        self._elements = None
        self._nodes = None

    @property
    def nodes(self) -> list[list[float]]:
        if self._nodes is None:
            self._nodes = DataUtils._transform_node_data(self._raw_node_data)
        return self._nodes

    @property
    def elements(self) -> list[list[int]]:
        if self._elements is None:
            self._elements = DataUtils._transform_element_data(self._raw_element_data)
        return self._elements

    @property
    def materials(self):
        return self._materials

    def _get_rfem_elements(self) -> list[dict]:
        if self._mesh_type == MeshType.FE1D:
            fe_elements = self._rfem_interface.get_fe1d_elements()
        elif self._mesh_type == MeshType.FE2D: 
            fe_elements = self._rfem_interface.get_fe2d_elements()
        elif self._mesh_type == MeshType.FE3D: 
            fe_elements = self._rfem_interface.get_fe3d_elements()
        return fe_elements
    
    def _get_rfem_nodes(self) -> list[dict]:
        return self._rfem_interface.get_fe_nodes()

if __name__ == "__main__":
    
    model = Model(True, "Stütze.rf6")
    data_handler = RFEMDataHandler(model=model, mesh_type=MeshType.FE2D)
    print(data_handler.elements)
    print(data_handler.nodes)