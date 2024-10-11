from enum import Enum
from project_package.package import Package
from datetime import datetime, timedelta

# Using constants for easy changes to values in the future
SPEED = 18 # miles per hour
CAPACITY = 16 # packages total per truck

"""
This file involves all the classes and functions related to the delivery trucks.
Includes enumerations for truck status, and also a way to add packages to a truck.
"""

# This class will have 3 instantiations. Each will start off at the hub.
class Truck:
    def __init__(self, id: int):
        self.status = TruckStatus.HUB
        # self.driver = TruckDriver.NONE
        self.location = "4001 South 700 East"
        self.mileage = 0
        self.departure_time = None
        self.time = None
        self.speed = SPEED
        self.capacity = CAPACITY
        self.id = id
        self.onboard_package_list = [] # a list to contain the packages onboard the truck

    # Defining a simple way to add packages to a truck
    def add_package(self, package: Package):
        if len(self.onboard_package_list) < self.capacity:
            self.onboard_package_list.append(package)
        else:
            print(f"Truck {self.id} has already reached maximum capacity. This package cannot be added.")

    # Defining an easy way to determine the truck's ID and its status with a simple call
    def __str__(self):
        return f"Truck {self.id} is {self.status.value}."

# For simplicity, defining an enumeration for the status of the trucks
class TruckStatus(Enum):
    HUB = "at the hub"
    TRANSIT = "en route"
