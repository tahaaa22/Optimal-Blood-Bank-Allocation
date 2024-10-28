from models import Request, Hospital  
    
class AllocationEngine:
    """
    TODO Rework the allocation algorithm to be compatible with the received requests
    1. Allocate function receives an instance of the App Manager which in turn contains:
        - A list of hospitals (self.HOSPITALS)
        - A list of blood banks (self.BLOOD_BANKS)
        - Invenotry (self.INVENTORY)
        - A list of requests

    2. The algorithm should prioritize the requests which consist of the following:
        - Hospital (request.hospital)
        - Requested blood type (request.blood_type)
        - Requested number of bags (request.number_of_blood_bags)
        - Remaining number of bags for that hospital (request.remaining_blood_bags)

    3. The algorithm is expected to sort the requests list
    """
    def allocate(self,app):
        score = {} # Dictionary to store the score of each hospital

    #   blood_bank_dict = {} # Dictionary to store the blood banks with the same blood type
    #   for bag in app.inventory: # O(n) complexity:
    #       if bag.bloodType not in blood_bank_dict:
    #           blood_bank_dict[bag.bloodType] = []
    #       blood_bank_dict[bag.bloodType].append(bag)
    #   print(blood_bank_dict)
        
        for request in app.requests: # O(n) complexity
            beds = request.hospital.number_of_beds
            requestTime =request.hours*60 + request.minutes 
            remaningBags = request.remaining_blood_bags
            score[request.hospital.id] = int(10 * requestTime + 7 * (1 / remaningBags) + 3 * beds)
            #FIXME: add this y taha
            #print(f"Hospital ID: {app.hospital.id}, Score: {score[app.hospital.id]}")
        
        sorted_requests = sorted(app.requests, key=lambda h: score[h.hospital.id], reverse=True) # O(nlogn) complexity
        
        # Step 5: Allocate blood bags to hospitals using the blood bank dictiona and update the stock of blood bags in the blood banks
        for request in sorted_requests: # O(n) complexity
            bloodType = request.blood_type 
            numberofBags = request.number_of_blood_bags                          # Check if blood type is available in blood bank dictionary / O(1) complexity as in operator has O(1) complexity in dictionaries.               # Iterate through blood banks with the same blood type / O(n * k) complexity, however k is always 1, so O(n).
            if numberofBags <= app.INVENTORY[bloodType]:                    # Check if the blood bank has enough stock
                
                app.INVENTORY[bloodType] -= numberofBags
                request.remaining_blood_bags=app.INVENTORY[bloodType]
                print(f"Hospital ID: {request.hospital.id}, Blood Type: {request.blood_type}, Number of Bags: {request.number_of_blood_bags}, NumberofBagsinStock: {request.remaining_blood_bags}")
                break
            else: # If the blood bank does not have enough stock, allocate all available stock
                
                numberofBags -= app.INVENTORY[bloodType]
                app.INVENTORY[bloodType] = 0
                request.remaining_blood_bags=numberofBags
                print(f"Hospital ID: {request.hospital.id}, Blood Type: {request.blood_type}, Number of Bags: {request.number_of_blood_bags}, NumberofBagsinStock: {request.remaining_blood_bags}")