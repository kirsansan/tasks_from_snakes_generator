""" clapp People for a test"""

from dataclasses import dataclass


@dataclass
class People:
    name: str
    phone: str
    pk: int

    # def __init__(self, name="", phone="", pk=None):
    #     self.name = name
    #     self.phone = phone
    #     self.pk = pk

    def get_name(self) -> str:
        return self.name

    def get_phone(self) -> str:
        return self.phone

