from dataclasses import dataclass
from typing import Any


@dataclass
class PatientGet:
    id: int
    box_code: str
    first_name: str
    last_name: str
    phone_contact: str
    phone_auth: str
    gov_id: str
    hospital_id: str
    date_of_birth: str
    gender: str
    address: str
    nationality: str
    locale: str

    def full_name(self):
        return self.first_name + " " + self.last_name

    @staticmethod
    def from_dict(obj: Any):
        ##print("from_dict called")
        _id = int(obj.get("id"))
        _box_code = str(obj.get("box_code"))
        _first_name = str(obj.get("first_name"))
        _last_name = str(obj.get("last_name"))
        _phone_contact = str(obj.get("phone_contact"))
        _phone_auth = str(obj.get("phone_auth"))
        _gov_id = str(obj.get("gov_id"))
        _hospital_id = str(obj.get("hospital_id"))
        _date_of_birth = str(obj.get("date_of_birth"))
        _gender = str(obj.get("gender"))
        _address = str(obj.get("address"))
        _nationality = str(obj.get("nationality"))
        _locale = str(obj.get("locale"))
        return PatientGet(
            _id,
            _box_code,
            _first_name,
            _last_name,
            _phone_contact,
            _phone_auth,
            _gov_id,
            _hospital_id,
            _date_of_birth,
            _gender,
            _address,
            _nationality,
            _locale,
        )
