from enum import Enum
from datetime import datetime, timedelta
import csv

"""
This file involves all the classes and functions related to the actual packages that need to be delivered.
Includes the reading of the WGUPS Package File, the instantiation of packages, and a way to keep track of the status of each.
"""

# This class will have 40 instantiations, called from the load_csv_packages() function
class Package:
    def __init__(self, id: int, address: str, city: str, state: str, zip: int, deadline, weight: int, note: str = None):
        self.status = PackageStatus.WAITING
        self.id = id
        self.address = address
        self.address_id = None
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.departure_time = None
        self.delivery_time = None

    # Defining an easy way to determine the package's ID and its status with a simple call
    def __str__(self):
        if self.status == PackageStatus.DELIVERED:
            return f"Package {self.id} was delivered at {(self.delivery_time).strftime('%I:%M%p').lower()}."
        elif self.delivery_time is None:
            return f"Package {self.id} status is {self.status.value} and delivery time is not set."
        else:
            return f"Package {self.id} is {self.status.value}. It is scheduled for delivery at {(self.delivery_time).strftime('%I:%M%p').lower()}."

    def update(self, hash_table, user_time):
        if user_time < self.departure_time:
            self.status = PackageStatus.WAITING
        elif user_time > self.delivery_time:
            self.status = PackageStatus.DELIVERED
        else:
            self.status = PackageStatus.TRANSIT
        hash_table.add(self.id, self)
        
# For simplicity, defining an enumeration for the status of the packages
class PackageStatus(Enum):
    WAITING = "waiting to be shipped"
    TRANSIT = "in transit"
    DELIVERED = "delivered"

# This one-time function will read through the CSV WGUPS Package File
# It will then instantiate a Package object for each row and add the objects to a returned list
def load_csv_packages() -> list:
    package_list = [] # creating an empty list to hold the instantiated packages

    with open(r"project_package/data/Packages.csv", mode='r', newline='') as file:  # Open and read the CSV file
        reader = csv.reader(file)

        for row in reader:  # Iterate through each row in the CSV
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = int(row[4])
            deadline = row[5]
            weight = int(row[6])
            note = row[7] if len(row) > 7 else None

            package = Package(id, address, city, state, zip_code, deadline, weight, note) # creating a Package instance
            package_list.append(package)

    return package_list # for main.py to work with

