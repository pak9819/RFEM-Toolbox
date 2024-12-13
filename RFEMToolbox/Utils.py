import ast
import re
import json


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
    def _get_items(cls, data: list[str], prefix: str) -> list[dict]:
        items = []
        for item in data[0]:
            if item.startswith(prefix):
                items.append(cls._string_to_dict(item))
        return items

    @classmethod
    def get_materials(cls, data: list[str], verbose=False) -> list[dict]:
            return cls._get_items(data, "Material")
            # Filter
            # 1d
            # Querschnittsfläche
            # 2d
            # e-module, querdehnzahl, dicke, dichte, eigengewicht
            # 3d
            # NaN

    @classmethod
    def get_members(cls, data: list[str]) -> list[dict]:
        return cls._get_items(data, "Member")
    

class JSONDataWriter:
    def __init__(self, file_path: str):
        """
        Initializes the JSONDataWriter with the path to the JSON file.
        
        :param file_path: Path to the JSON file where data will be written.
        """
        self.file_path = file_path

    def write(
            self, 
            struct_type: str, 
            struct_id: str, 
            length: float,
            height: float,
            width:float,
            support_left: str,
            support_mid: str,
            support_right: str, 
            load_type: str,
            force:float,
            material: str,
            e_module: float,
            poisson: float,
            density: float, 
            mesh_size: float, 
            elements: int, 
            nodes: int,
            max_displacement: float, 
            displacement_delta: float, 
            calculation_time_mesh: str,
            calculation_time_total: str
    ):
        """
        Writes a single entry of data to the JSON file.
        """
        data_entry = {
            "structure_type": struct_type,
            "structure_id": struct_id,
            "length": length,
            "height": height,
            "width": width,
            "support_left": support_left,
            "support_mid": support_mid,
            "support_right": support_right,
            "load_type": load_type,
            "force": force,
            "material": material,
            "e_module": e_module,
            "poisson": poisson,
            "density": density,
            "mesh_size": mesh_size,
            "elements": elements,
            "nodes": nodes,
            "max_displacement": max_displacement,
            "displacement_delta": displacement_delta,
            "mesh_calculation_time": calculation_time_mesh,
            "total_calculation_time": calculation_time_total
        }
        
        # Read the existing data if the file exists
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        # Append the new entry
        data.append(data_entry)
        
        # Write the updated data back to the file
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
