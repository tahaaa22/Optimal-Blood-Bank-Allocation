from PyQt5 import QtCore, QtWidgets
from models import Request, Hospital
from PyQt5.QtWidgets import QMessageBox
from allocation_algorithm import AllocationEngine
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
        dialog = QMessageBox()
        dialog.setText("Simulation started")
        dialog.setWindowTitle("Simulation")
        dialog.setIcon(QMessageBox.Information)
        dialog.exec()
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
        dialog = QMessageBox()
        dialog.setText("Simulation stopped")
        dialog.setWindowTitle("Simulation")
        dialog.setIcon(QMessageBox.Information)
        dialog.exec()
        self.stop_thread = True  
        
    def create_request(self):
        hospital_ind = random.randint(0, 7)
        hospital = self.HOSPITALS[hospital_ind]
        blood_type = random.choice(self.BLOOD_TYPES)
        number_of_blood_bags = random.randint(500, 1000)
        remaining_blood_bags = random.randint(100, 200)
        return Request(hospital, blood_type, number_of_blood_bags, remaining_blood_bags)

    def print_request(self):
        request = self.create_request()

        self.ui.orders_table.insertRow(self.ui.orders_table.rowCount())
        for i in range(5):
            item = QtWidgets.QTableWidgetItem()
            self.ui.orders_table.setItem(self.number_of_requests, i, item)

        self.ui.orders_table.item(self.number_of_requests, 0).setText(self._translate("MainWindow", request.hospital.name))
        self.ui.orders_table.item(self.number_of_requests, 1).setText(self._translate("MainWindow", request.blood_type))
        self.ui.orders_table.item(self.number_of_requests, 2).setText(self._translate("MainWindow", request.number_of_blood_bags))
        self.ui.orders_table.item(self.number_of_requests, 3).setText(self._translate("MainWindow", request.remaining_blood_bags))
        self.ui.orders_table.item(self.number_of_requests, 4).setText(self._translate("MainWindow", f"{self.hours}:{self.minutes}"))
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
        # TODO update inventory table
        pass

    def update_output(self):
        # TODO update output table
        pass

    def distribute_blood(self):
        AllocationEngine.allocate(self)
        
