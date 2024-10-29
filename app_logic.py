from PyQt5 import QtCore, QtWidgets
from models import Request, Hospital
from PyQt5.QtWidgets import QMessageBox
from allocation_algorithm import allocate
import random
import time
import threading

class AppManager():
    def __init__(self, ui):
        self.ui = ui
        self.simulation_thread = None
        self.stop_thread = False
        self.hours = 12
        self.minutes = 0

        self.requests = []
        self.number_of_requests = 0

        self._translate = QtCore.QCoreApplication.translate
        self.HOSPITALS : list[Hospital] = []    
        self.BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        self.INVENTORY = {"A+": 1000, "A-": 1000, "B+": 1000, "B-": 1000, "AB+": 1000, "AB-": 1000, "O+": 1000, "O-": 1000}
        self.initiate_paramters()
        
    def start(self):
        self.stop_thread = False
        self.simulation_thread = threading.Thread(target=self.simulate_requests)
        self.simulation_thread.start()

    def simulate_requests(self):
        # We receive requests every 10 minutes
        # We receive donations every 20 minutes
        # We distribute blood every 30 minutes
        while not self.stop_thread:
            self.update_time()
            if self.minutes % 10 == 0:
                self.print_request()
            if self.minutes % 20 == 0:
                self.receive_donation()
            if self.minutes % 30 == 0:
                self.distribute_blood()
            time.sleep(0.2)

    def update_time(self):
        self.minutes += 1
        
        if self.minutes == 60:
            self.minutes = 0
            self.hours += 1
            
        if self.hours == 13:
            self.hours = 1

        self.ui.Seconds_LCD.display(self.minutes)
        self.ui.Minutes_LCD.display(self.hours)

    def stop_simulation(self):
        self.stop_thread = True  
        
    def create_request(self):
        hospital_ind = random.randint(0, 7)
        hospital = self.HOSPITALS[hospital_ind]
        blood_type = random.choice(self.BLOOD_TYPES)
        number_of_blood_bags = random.randint(500, 1000)
        remaining_blood_bags = random.randint(100, 200)
        return Request(self.number_of_requests, hospital, blood_type, number_of_blood_bags, remaining_blood_bags, self.hours, self.minutes)

    def print_request(self):
        request = self.create_request()

        self.ui.orders_table.insertRow(self.ui.orders_table.rowCount())
        for i in range(5):
            item = QtWidgets.QTableWidgetItem()
            self.ui.orders_table.setItem(self.number_of_requests, i, item)

        self.ui.orders_table.item(self.number_of_requests, 0).setText(self._translate("MainWindow", str(request.hospital.name)))
        self.ui.orders_table.item(self.number_of_requests, 1).setText(self._translate("MainWindow", str(request.blood_type)))
        self.ui.orders_table.item(self.number_of_requests, 2).setText(self._translate("MainWindow", str(request.number_of_blood_bags)))
        self.ui.orders_table.item(self.number_of_requests, 3).setText(self._translate("MainWindow", str(request.remaining_blood_bags)))
        self.ui.orders_table.item(self.number_of_requests, 4).setText(self._translate("MainWindow", f"{str(self.hours)}:{str(self.minutes)}"))
        self.number_of_requests += 1
        self.requests.append(request)

    def initiate_paramters(self):
        self.HOSPITALS = [Hospital(1, "Ain Shams", 200, [100, 100, 100, 100, 100, 100, 100, 100]),
                          Hospital(2, "Saudi German", 190, [100, 100, 100, 100, 100, 100, 100, 100]),
                          Hospital(3, "Cleopatra", 182, [100, 100, 100, 100, 100, 100, 100, 100]),
                          Hospital(4, "El Nozha", 120, [100, 100, 100, 100, 100, 100, 100, 100]),
                          Hospital(5, "El Safa", 100, [100, 100, 100, 100, 100, 100, 100, 100]),
                          Hospital(6, "Wadi El Neel", 90, [100, 100, 100, 100, 100, 100, 100, 100]),
                          Hospital(7, "Cardiac Center", 82, [100, 100, 100, 100, 100, 100, 100, 100]),
                          Hospital(8, "Ibn Sina", 75, [100, 100, 100, 100, 100, 100, 100, 100])]
        
    def receive_donation(self):
        blood_type_1 = random.choice(self.BLOOD_TYPES)
        blood_type_2 = random.choice(self.BLOOD_TYPES)
        blood_type_3 = random.choice(self.BLOOD_TYPES)
        number_of_blood_bags_1 = random.randint(10, 50)
        number_of_blood_bags_2 = random.randint(10, 50)
        number_of_blood_bags_3 = random.randint(10, 50)
        self.INVENTORY[blood_type_1] += number_of_blood_bags_1
        self.INVENTORY[blood_type_2] += number_of_blood_bags_2
        self.INVENTORY[blood_type_3] += number_of_blood_bags_3
        self.update_inventory()

    def update_inventory(self):
        # Clear existing table data
        self.ui.inventory_table.setRowCount(0)
        
        # Iterate over blood types in the INVENTORY dictionary
        for row_index, (blood_type, remaining_bags) in enumerate(self.INVENTORY.items()):
            self.ui.inventory_table.insertRow(row_index)
            
            # Create table items for each column
            blood_type_item = QtWidgets.QTableWidgetItem(blood_type)
            remaining_bags_item = QtWidgets.QTableWidgetItem(str(remaining_bags))
            component_item = QtWidgets.QTableWidgetItem("Whole blood")  # Assuming "Whole blood" for each type
            
            # Set items in the corresponding columns
            self.ui.inventory_table.setItem(row_index, 0, blood_type_item)
            self.ui.inventory_table.setItem(row_index, 1, remaining_bags_item)
            self.ui.inventory_table.setItem(row_index, 2, component_item)

    def update_output(self, requests):
        self.ui.output_table.setRowCount(0)

        # Iterate through the requests list to populate the table
        for row_index, request in enumerate(requests):
            self.ui.output_table.insertRow(row_index)
            
            # Assuming `request` has attributes: blood_type, needed_bags, hospital, status
            blood_type_item = QtWidgets.QTableWidgetItem(request.blood_type)
            needed_bags_item = QtWidgets.QTableWidgetItem(str(request.number_of_blood_bags))
            hospital_item = QtWidgets.QTableWidgetItem(request.hospital.name)
            status_item = QtWidgets.QTableWidgetItem("Fulfilled")

            # Insert data into the corresponding columns
            self.ui.output_table.setItem(row_index, 0, blood_type_item)
            self.ui.output_table.setItem(row_index, 1, needed_bags_item)
            self.ui.output_table.setItem(row_index, 2, hospital_item)
            self.ui.output_table.setItem(row_index, 3, status_item)

    def distribute_blood(self):
        sorted_requests = allocate(self)
        requests_to_be_fulfilled = [] # first we need to check that we are capable of fulfilling the request
        for request in sorted_requests:
            if self.INVENTORY[request.blood_type] >= request.number_of_blood_bags:
                requests_to_be_fulfilled.append(request)
                sorted_requests.remove(request)
                self.INVENTORY[request.blood_type] -= request.number_of_blood_bags
        self.requests = sorted_requests
        self.update_output(requests_to_be_fulfilled)
