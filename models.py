class Hospital:
    def __init__(self, id, name, beds, blood_inventory):
        self.id = id
        self.name = name
        self.number_of_beds = beds
        self.blood_inventory : list[int] = blood_inventory


class Request:
    def __init__(self, hospital, blood_type, number_of_blood_bags, remaining_blood_bags):
        self.hospital = hospital
        self.blood_type = str(blood_type)
        self.number_of_blood_bags = str(number_of_blood_bags)
        self.remaining_blood_bags = str(remaining_blood_bags)

    def __str__(self) -> str:
        return f"Request from hospital {self.hospital_id} for {self.number_of_blood_bags} bags of {self.blood_type} blood. {self.remaining_blood_bags} bags remaining."
