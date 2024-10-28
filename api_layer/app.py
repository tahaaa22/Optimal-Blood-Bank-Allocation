from PyQt5 import QtCore, QtWidgets
from models import Request
import random
import time
import threading

blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

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
        
    def start(self):
        print("Simulation started")
        self.stop_thread = False
        self.simulation_thread = threading.Thread(target=self.simulate_requests)
        self.simulation_thread.start()

    def simulate_requests(self):
        while not self.stop_thread:
            self.update_time()
            if (self.minutes % 10 == 0):
                self.print_request()
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
        hospital_id = random.randint(1, 8)
        blood_type = random.choice(blood_types)
        number_of_blood_bags = random.randint(500, 1000)
        remaining_blood_bags = random.randint(100, 200)
        return Request(hospital_id, blood_type, number_of_blood_bags, remaining_blood_bags)

    def print_request(self):
        request = self.create_request()

        self.ui.orders_table.insertRow(self.ui.orders_table.rowCount())
        for i in range(5):
            item = QtWidgets.QTableWidgetItem()
            self.ui.orders_table.setItem(self.number_of_requests, i, item)

        self.ui.orders_table.item(self.number_of_requests, 0).setText(self._translate("MainWindow", request.hospital_id))
        self.ui.orders_table.item(self.number_of_requests, 1).setText(self._translate("MainWindow", request.blood_type))
        self.ui.orders_table.item(self.number_of_requests, 2).setText(self._translate("MainWindow", request.number_of_blood_bags))
        self.ui.orders_table.item(self.number_of_requests, 3).setText(self._translate("MainWindow", request.remaining_blood_bags))
        self.ui.orders_table.item(self.number_of_requests, 4).setText(self._translate("MainWindow", f"{self.hours}:{self.minutes}"))
        self.number_of_requests += 1