from RFEM.initModel import Model
from RFEM.Results.meshTables import MeshTables
from RFEM.Tools.GetObjectNumbersByType import GetAllObjects
from Utils import DataUtils


class RFEMDataHandler:

    def __init__(self, model_name) -> None:
        self.model = Model(True, model_name)
        self._raw_elements, self._nodes = self._get_rfem_data()
        self._raw_data = GetAllObjects(model=self.model)
        self._materials = DataUtils.get_materials(self._raw_data)
        self._elements = None

    @property
    def nodes(self):
        return self._nodes

    @property
    def elements(self):
        if self._elements is None:
            self._elements = self._extract_elements()
        return self._elements

    @property
    def materials(self):
        return self._materials

    def _get_rfem_data(self) -> tuple:
        fe1d_elements = MeshTables.GetAllFE1DElements(model=self.model)
        fe_nodes = MeshTables.GetAllFENodes(model=self.model)
        return fe1d_elements, fe_nodes

    def _extract_elements(self) -> list[dict]:
        nodes = set()
        for item in self._raw_elements:
            nodes.update([item["FE_node1_no"], item["FE_node2_no"]])

        elements = []
        for node in nodes:
            node_dict = {node: []}
            for item in self._raw_elements:
                if node in (item["FE_node1_no"], item["FE_node2_no"]):
                    value = item[
                        "FE_node2_no" if item["FE_node1_no"] == node else "FE_node1_no"
                    ]
                    node_dict[node].append(value)
            elements.append(node_dict)
        return elements


if __name__ == "__main__":
    data_handler = RFEMDataHandler(model_name="Stütze.rf6")