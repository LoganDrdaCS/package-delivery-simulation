from enum import Enum
from project_package.package import Package

# Overall time complexity is O(n) when multiple packages are involved

# Using constants for quick changes in the future (scalability)
SPEED = 18 # miles per hour
CAPACITY = 16 # packages total per truck

"""
This file involves all the classes and functions related to the delivery trucks.
Includes enumerations for truck status, and also a way to add packages to a truck.
"""

# Creating the Truck class. Each will start at the hub.
class Truck: # O(1)
    def __init__(self, id: int):
        self.status = TruckStatus.HUB # Initial status, at the hub
        self.location = "4001 South 700 East" # Default hub location
        self.mileage = 0
        self.departure_time = None
        self.time = None
        self.speed = SPEED
        self.capacity = CAPACITY
        self.id = id
        self.onboard_package_list = [] # list to contain the packages onboard the truck

    # Defining a method to add packages to the truck without exceeding capacity
    def add_package(self, package: Package): # O(1)
        if len(self.onboard_package_list) < self.capacity:
            self.onboard_package_list.append(package)
        else:
            print(f"Truck {self.id} has already reached maximum capacity. This package cannot be added.")

    # Defining an easy way to determine the truck's ID, status, and packages onboard
    def __str__(self): # O(n) where n = number of packages onboard
        return f"Truck {self.id} is {self.status.value}. Packages onboard: {self.onboard_package_list}."

# For scalability, defining an enumeration for the status of the trucks
class TruckStatus(Enum): # O(1)
    HUB = "at the hub"
    TRANSIT = "en route"
