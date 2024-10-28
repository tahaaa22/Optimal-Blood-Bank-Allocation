import unittest
from allocation_algorithm import AllocationEngine, Hospital, BloodBank


class TestAllocationAlgorithm(unittest.TestCase):
    def setUp(self):
        self.hospitals = [
            Hospital(1, 100, 4, 50, "A+", 10),
            Hospital(2, 150, 5, 30, "A-", 8),
            Hospital(3, 200, 8, 20, "B+", 15),
            Hospital(4, 250, 10, 10, "O+", 20),
            Hospital(5, 300, 9, 5, "AB+", 25)
        ]
        self.blood_banks = [
            BloodBank(1, "A+", 100),
            BloodBank(2, "A-", 80),
            BloodBank(3, "B+", 120),
            BloodBank(4, "B-", 60),
            BloodBank(5, "O+", 150),
            BloodBank(6, "O-", 90),
            BloodBank(7, "AB+", 70),
            BloodBank(8, "AB-", 50)
        ]
        self.engine = AllocationEngine()

    def test_allocation(self):
        self.engine.allocate(self.hospitals, self.blood_banks)
        
        # Check if the blood bank stock is updated correctly
        self.assertEqual(self.blood_banks[2].stock, 105)  # BloodBank(3, "B+", 120) - 15 bags allocated to Hospital(3)
        
        # Check if the hospital's blood bag request is fulfilled
        self.assertEqual(self.hospitals[2].numberofBags, 15)  # Hospital(3) requested 15 bags of "B+"

    def test_no_allocation_if_insufficient_stock(self):
        # Modify hospital to request more bags than available in any single blood bank
        self.hospitals[2].numberofBags = 200  # Hospital(3) requests 200 bags of "B+"
        self.engine.allocate(self.hospitals, self.blood_banks)
        
        # Check if the blood bank stock is updated correctly
        self.assertEqual(self.blood_banks[2].stock, 0)  # BloodBank(3, "B+", 120) - all 120 bags allocated to Hospital(3)
        
        # Check if the hospital's blood bag request is partially fulfilled
        self.assertEqual(self.hospitals[2].numberofBags, 200)  # Hospital(3) requested 200 bags of "B+"

    def test_allocation_with_multiple_blood_banks(self):
        # Modify hospital to request more bags than available in a single blood bank but less than total available
        self.hospitals[3].numberofBags = 160  # Hospital(4) requests 160 bags of "O+"
        self.engine.allocate(self.hospitals, self.blood_banks)
        
        # Check if the blood bank stock is updated correctly
        self.assertEqual(self.blood_banks[4].stock, 0)  # BloodBank(5, "O+", 150) - all 150 bags allocated to Hospital(4)
        self.assertEqual(self.blood_banks[5].stock, 90)  # BloodBank(6, "O-", 90) - 10 bags allocated to Hospital(4)
        
        # Check if the hospital's blood bag request is partially fulfilled
        self.assertEqual(self.hospitals[3].numberofBags, 160)  # Hospital(4) requested 160 bags of "O+"

    def test_allocation_with_no_matching_blood_type(self):
        # Modify hospital to request a blood type not available in any blood bank
        self.hospitals[0].bloodType = "C+"  # Hospital(1) requests "C+" which is not available
        self.engine.allocate(self.hospitals, self.blood_banks)
        
        # Check if the blood bank stock remains unchanged
        self.assertEqual(self.blood_banks[0].stock, 100)  # BloodBank(1, "A+", 100) - no allocation
        
        # Check if the hospital's blood bag request is not fulfilled
        self.assertEqual(self.hospitals[0].numberofBags, 10)  # Hospital(1) requested 10 bags of "C+"

if __name__ == '__main__':
    unittest.main()