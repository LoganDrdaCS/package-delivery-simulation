from enum import Enum
import csv
from datetime import datetime

"""
This file involves all the classes and functions related to the actual packages that need to be delivered.
Includes the reading of the Package File, the instantiation of packages, and a way to keep track of the status of each.
"""

# Overall time complexity is O(n)

class Package:
    def __init__(self, id: int, address: str, city: str, state: str, zip: int, deadline, weight: int, note: str = None): # O(1)
        self.status = PackageStatus.WAITING # Initial package status: waiting to be shipped
        self.id = id
        self.address = address
        self.address_id = None
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight # kgs
        self.note = note
        self.departure_time = None
        self.delivery_time = None
        self.truck_number = None

    # Defining a function that prints basic information for the UI, such as package ID, address, delivery status, truck number, and delivery time (if applicable)
    def print_summary(self): # O(1)
        if self.status == PackageStatus.DELIVERED:
            if self.deadline == "EOD":
                return f"Package {self.id} was delivered to {self.address} at {(self.delivery_time).strftime('%I:%M%p').lower()} by truck {self.truck_number}."
            else:
                return f"Package {self.id} with a deadline of {self.deadline} was delivered to {self.address} at {(self.delivery_time).strftime('%I:%M%p').lower()} by truck {self.truck_number}."
        elif self.delivery_time is None:
            if self.deadline == "EOD":
                return f"Package {self.id} status is {self.status.value} and the delivery time to {self.address} is not set."
            else:
                return f"Package {self.id} status is {self.status.value} with a deadline of {self.deadline} and the delivery time to {self.address} is not set."
        else:
            if self.deadline == "EOD":
                return f"Package {self.id} is {self.status.value} on truck {self.truck_number}. It is scheduled for delivery to {self.address} at {(self.delivery_time).strftime('%I:%M%p').lower()}."
            else:
                return f"Package {self.id} is {self.status.value} on truck {self.truck_number}. Its deadline is {self.deadline} and it is scheduled for delivery to {self.address} at {(self.delivery_time).strftime('%I:%M%p').lower()}."
    
    # Defining a function that will print all of the attributes of a specified package
    def print_all_details(self): # O(1)
        if self.status.value == "delivered":
            return f"\nPackage {self.id} Details\nStatus: {self.status.value}\nTruck Number: {self.truck_number}\nAddress: {self.address}, {self.city}, {self.state} {self.zip}\nDeadline: {self.deadline}\nWeight: {self.weight} kgs\nNotes: {self.note}\nDeparture Time: {(self.departure_time).strftime('%I:%M%p').lower()}\nDelivery Time: {(self.delivery_time).strftime('%I:%M%p').lower()}"
        elif self.status.value == "in transit":
            return f"\nPackage {self.id} Details\nStatus: {self.status.value}\nTruck Number: {self.truck_number}\nAddress: {self.address}, {self.city}, {self.state} {self.zip}\nDeadline: {self.deadline}\nWeight: {self.weight} kgs\nNotes: {self.note}\nDeparture Time: {(self.departure_time).strftime('%I:%M%p').lower()}\nPlanned Delivery Time: {(self.delivery_time).strftime('%I:%M%p').lower()}"
        elif self.status.value == "waiting to be shipped":
            return f"\nPackage {self.id} Details\nStatus: {self.status.value}\nTruck Number: {self.truck_number}\nAddress: {self.address}, {self.city}, {self.state} {self.zip}\nDeadline: {self.deadline}\nWeight: {self.weight} kgs\nNotes: {self.note}\nPlanned Departure Time: {(self.departure_time).strftime('%I:%M%p').lower()}\nPlanned Delivery Time: {(self.delivery_time).strftime('%I:%M%p').lower()}"

    # Defining a function to update the hash table with the status of the package based on the user's requested time input
    def update(self, hash_table, user_time): # O(1)
        time_to_update_at = datetime.strptime("10:20am", "%I:%M%p") # check to see if Package 9 address needs updating
        if user_time < self.departure_time:
            self.status = PackageStatus.WAITING
        elif user_time > self.delivery_time:
            self.status = PackageStatus.DELIVERED
        else:
            self.status = PackageStatus.TRANSIT
        if self.id == 9 and user_time >= time_to_update_at:
            correct_package9(self, hash_table) # Special update for package 9's address at 10:20am
        elif self.id == 9 and user_time < time_to_update_at:
            decorrect_package9(self, hash_table)
        else:
            hash_table.add(self.id, self)

# Defining a function to correct the wrong address listed for Package 9 at 10:20am:
def correct_package9(package9: Package, hash_table): #O(1)
    package9.address = "410 S State St"
    package9.address_id = 19
    package9.zip = 84111
    hash_table.add(package9.id, package9)

# Defining a function to de-correct the address listed for Package 9 if before 10:20am:
def decorrect_package9(package9: Package, hash_table): #O(1)
    package9.address = "300 State St"
    package9.address_id = 12
    package9.zip = 84103
    hash_table.add(package9.id, package9)
    
# For scalability, defining an enumeration for the status of the packages
class PackageStatus(Enum): # O(1)
    WAITING = "waiting to be shipped"
    TRANSIT = "in transit"
    DELIVERED = "delivered"

# This one-time function will read through the CSV WGUPS Package File and
# instantiate a Package object for each row, and will add the objects to a returned list
def load_csv_packages() -> list: # O(n)
    package_list = [] # create an empty list to hold the instantiated packages

    with open(r"project_package/data/Packages.csv", mode='r', newline='') as file:  # open and read the CSV file
        reader = csv.reader(file)

        for row in reader:  # iterate through each row in the CSV
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = int(row[4])
            deadline = row[5]
            weight = int(row[6])
            note = row[7] if len(row) > 7 else None

            package = Package(id, address, city, state, zip_code, deadline, weight, note) # create a Package instance
            package_list.append(package)

    return package_list # for main.py to work with
