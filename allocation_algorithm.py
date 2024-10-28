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

    def allocate(self, app):
      score = {} # Dictionary to store the score of each hospital

      blood_bank_dict = {} # Dictionary to store the blood banks with the same blood type
      for bank in blood_banks:
          if bank.bloodType not in blood_bank_dict:
              blood_bank_dict[bank.bloodType] = []
          blood_bank_dict[bank.bloodType].append(bank)
      print(blood_bank_dict)
      
      for hospital in hospitals: 
          beds = hospital.beds
          requestTime = hospital.requestTime
          remaningBags = hospital.remaningBags
          score[hospital.id] = int(10 * requestTime + 7 * (1 / remaningBags) + 3 * beds)
          print(f"Hospital ID: {hospital.id}, Score: {score[hospital.id]}")
      
      sorted_hospitals = sorted(hospitals, key=lambda h: score[h.id], reverse=True) # O(nlogn) complexity
      
      # Step 5: Allocate blood bags to hospitals using the blood bank dictiona and update the stock of blood bags in the blood banks
    
      for hospital in sorted_hospitals: # O(n) complexity
          bloodType = hospital.bloodType 
          numberofBags = hospital.numberofBags 
          if bloodType in blood_bank_dict:                          # Check if blood type is available in blood bank dictionary / O(1) complexity as in operator has O(1) complexity in dictionaries.
              for bank in blood_bank_dict[bloodType]:               # Iterate through blood banks with the same blood type / O(n * k) complexity, however k is always 1, so O(n).
                  if numberofBags <= bank.stock:                    # Check if the blood bank has enough stock
                      print(f"Blood Bank ID: {bank.id}, Blood Type: {bank.bloodType}, Stock: {bank.stock}")
                      bank.stock -= numberofBags
                      print(f"Hospital ID: {hospital.id}, Blood Type: {hospital.bloodType}, Number of Bags: {hospital.numberofBags}, NumberofBagsinStock: {bank.stock}")
                      break
                  else: # If the blood bank does not have enough stock, allocate all available stock
                      print(f"Blood Bank ID: {bank.id}, Blood Type: {bank.bloodType}, Stock: {bank.stock}")
                      numberofBags -= bank.stock 
                      bank.stock = 0 
                      print(f"Hospital ID: {hospital.id}, Blood Type: {hospital.bloodType}, Number of Bags: {hospital.numberofBags}, NumberofBagsinStock: {bank.stock}")