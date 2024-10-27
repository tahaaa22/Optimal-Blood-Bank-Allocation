class AllocationEngine:
    def allocate(self, hospitals, blood_banks):
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
      
      # Print the allocation details
      # Print the updated stock of blood bags in the blood banks
      # Print the remaining number of bags in the hospitals

class Hospital:
    def __init__(self, id, beds, requestTime, remaningBags, bloodType, numberofBags):
        self.id = id
        self.beds = beds
        self.requestTime = requestTime 
        self.remaningBags = remaningBags
        self.bloodType = bloodType
        self.numberofBags = numberofBags

hospitals = [
    Hospital(1, 100, 4, 50, "A+", 10),
    Hospital(2, 150, 5, 30, "A-", 8),
    Hospital(3, 200, 8, 20, "B+", 15),
    Hospital(4, 250, 10, 10, "O+", 200),
    Hospital(5, 300, 9, 5, "AB+", 25)
]

class BloodBank:
    def __init__(self, id, bloodType, stock):
        self.id = id
        self.bloodType = bloodType
        self.stock = stock
blood_banks = [
    BloodBank(1, "A+", 100),
    BloodBank(2, "A-", 80),
    BloodBank(3, "B+", 120),
    BloodBank(4, "B-", 60),
    BloodBank(5, "O+", 150),
    BloodBank(6, "O-", 90),
    BloodBank(7, "AB+", 70),
    BloodBank(8, "AB-", 50)
]
main = AllocationEngine()
main.allocate(hospitals, blood_banks)