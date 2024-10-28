class BloodBag:
    def __init__(self, id, blood_type, capacity, stock, location):
        pass

class Hospital:
    def __init__(self, id, needs, location, priority_level):
        pass

class Request:
    def __init__(self, hospital_id, blood_type, number_of_blood_bags, remaining_blood_bags):
        self.hospital_id = str(hospital_id)
        self.blood_type = str(blood_type)
        self.number_of_blood_bags = str(number_of_blood_bags)
        self.remaining_blood_bags = str(remaining_blood_bags)

    def __str__(self) -> str:
        return f"Request from hospital {self.hospital_id} for {self.number_of_blood_bags} bags of {self.blood_type} blood. {self.remaining_blood_bags} bags remaining."
