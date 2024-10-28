class Hospital:
    def __init__(self, id, name, beds, blood_inventory):
        self.id = id
        self.name = name
        self.number_of_beds = beds
        self.blood_inventory : list[int] = blood_inventory


class Request:
    def __init__(self,id, hospital, blood_type, number_of_blood_bags, remaining_blood_bags, hours, minutes):
        self.id = id
        self.hospital = hospital
        self.blood_type = blood_type
        self.number_of_blood_bags = number_of_blood_bags
        self.remaining_blood_bags = remaining_blood_bags
        self.hours = hours
        self.minutes = minutes

    def __str__(self) -> str:
        return f"Request from hospital {self.hospital.id} for {self.number_of_blood_bags} bags of {self.blood_type} blood. {self.remaining_blood_bags} bags remaining."
