import ast
import re
from typing import List, Dict


class DataUtils:

    def _string_to_dict(string: str) -> dict:
        formatted_str = re.sub(r"^[A-Za-z]+\(params=(.*)\)$", r"\1", string)
        return ast.literal_eval(formatted_str)

    @staticmethod
    def _transform_element_data(elements: list[dict]) -> list[list[int]]:
        # apply logic for mesh that consists of rectangles and triangles
        transformed_elements = []
        for dictionary in elements:
            surface = [int(dictionary[key]) for key in dictionary if key.startswith("FE_node")]
            transformed_elements.append(surface)
        return transformed_elements

    @staticmethod
    def _transform_node_data(nodes: list[dict]) -> list[list[float]]:
        out = []
        for item in nodes:
            out.append([float(item["x"]), float(item["y"]), float(item["z"])])
        return out

    @classmethod
    def _get_items(cls, data: List[str], prefix: str) -> List[Dict]:
        items = []
        for item in data[0]:
            if item.startswith(prefix):
                items.append(cls._string_to_dict(item))
        return items

    @classmethod
    def get_materials(cls, data: List[str], verbose=False) -> List[Dict]:
        if verbose == True:
            return cls._get_items(data, "Material")
        else:
            pass # Filter
            # 1d
            # Querschnittsfläche
            # 2d
            # e-module, querdehnzahl, dicke, dichte, eigengewicht
            # 3d
            # NaN

    @classmethod
    def get_members(cls, data: List[str]) -> List[Dict]:
        return cls._get_items(data, "Member")