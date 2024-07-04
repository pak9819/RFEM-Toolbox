import RFEM
import RFEM.initModel

from src.DataProcessor import RFEMDataHandler, MeshType
from src.Exporter import Exporter

if __name__ == "__main__":

    model = RFEM.initModel.Model("Testmodel.rf6")

    handler = RFEMDataHandler(model, MeshType.FE2D)

    nodes = handler.nodes
    elements = handler.elements

    Exporter.write("\\test.mlx", nodes, elements)


