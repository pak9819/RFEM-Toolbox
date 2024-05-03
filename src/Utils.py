import ast
import re
from typing import List, Dict


class DataUtils:

    def _string_to_dict(string: str) -> dict:
        formatted_str = re.sub(r"^[A-Za-z]+\(params=(.*)\)$", r"\1", string)
        return ast.literal_eval(formatted_str)

    @classmethod
    def _get_items(cls, data: List[str], prefix: str) -> List[Dict]:
        items = []
        for item in data[0]:
            if item.startswith(prefix):
                items.append(cls._string_to_dict(item))
        return items

    @classmethod
    def get_materials(cls, data: List[str]) -> List[Dict]:
        return cls._get_items(data, "Material")

    @classmethod
    def get_members(cls, data: List[str]) -> List[Dict]:
        return cls._get_items(data, "Member")