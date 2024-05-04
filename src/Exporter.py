from RFEM.initModel import Model

from DataProcessor import RFEMDataHandler, MeshType
from Interfaces import ScipyInterface

class Exporter:
    
    @staticmethod
    def write(filepath: str, node_matrix: list[list[int]], element_matrix: list[list]):
        ScipyInterface.save_matlab(filepath, node_matrix, element_matrix)


if __name__ == "__main__":

    model = Model(True, "Stütze.rf6")
    data = RFEMDataHandler(model, MeshType.FE2D)

    filepath = "src\\matlab\\data.mat"
    Exporter.write(filepath, data.nodes, data.elements)