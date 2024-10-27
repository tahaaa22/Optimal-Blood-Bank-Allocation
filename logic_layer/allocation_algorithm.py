class AllocationEngine:
    def allocate(self, hospitals, blood_banks):
          score={}
          for i in range (len(hospitals)):
            beds= hospitals[i].beds
            requestTime= hospitals[i].requestTime
            remaningBags= hospitals[i].remaningBags
            score[hospitals[i].id] = int(10*requestTime + 7*(1/remaningBags) + 3*beds)
          
          sorted_hospitals = sorted(hospitals, key=lambda h: score[h.id], reverse=True)
          for hospital in sorted_hospitals:
            print(f"Hospital ID: {hospital.id}, Score: {score[hospital.id]}")

          for i in range (len(sorted_hospitals)):
            bloodType = sorted_hospitals[i].bloodType
            numberofBags = sorted_hospitals[i].numberofBags
            for j in range (len(blood_banks)):
              if blood_banks[j].bloodType == bloodType:
                if numberofBags <= blood_banks[j].stock:
                  print(f"Blood Bank ID: {blood_banks[j].id}, Blood Type: {blood_banks[j].bloodType}, Stock: {blood_banks[j].stock}")
                  blood_banks[j].stock -= numberofBags
                  print(f"Hospital ID: {sorted_hospitals[i].id}, Blood Type: {sorted_hospitals[i].bloodType}, Number of Bags: {sorted_hospitals[i].numberofBags}, NumberofBagsinStock: {blood_banks[j].stock}" )
                  break
                else:
                  print(f"Blood Bank ID: {blood_banks[j].id}, Blood Type: {blood_banks[j].bloodType}, Stock: {blood_banks[j].stock}")
                  numberofBags -= blood_banks[j].stock 
                  blood_banks[j].stock = 0
                  print(f"Hospital ID: {sorted_hospitals[i].id}, Blood Type: {sorted_hospitals[i].bloodType}, Number of Bags: {sorted_hospitals[i].numberofBags}, NumberofBagsinStock: {blood_banks[j].stock}" )
            
          
        


          
        


        

        

      
     

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
    Hospital(4, 250, 10, 10, "O+", 20),
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


   