from enum import Enum
import csv

"""
This file involves all the classes and functions related to the actual packages that need to be delivered.
Includes the reading of the WGUPS Package File, the instantiation of packages, and a way to keep track of the status of each.
"""

# Overall time complexity is O(n)

class Package:
    def __init__(self, id: int, address: str, city: str, state: str, zip: int, deadline, weight: int, note: str = None): # O(1)
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
        self.truck_number = None

    # Defining an easy way to determine the package's ID, truck number, and status
    def __str__(self): # O(1)
        if self.status == PackageStatus.DELIVERED:
            if self.deadline == "EOD":
                return f"Package {self.id} was delivered at {(self.delivery_time).strftime('%I:%M%p').lower()} by truck {self.truck_number}."
            else:
                return f"Package {self.id} with a deadline of {self.deadline} was delivered at {(self.delivery_time).strftime('%I:%M%p').lower()} by truck {self.truck_number}."
        elif self.delivery_time is None:
            if self.deadline == "EOD":
                return f"Package {self.id} status is {self.status.value} and the delivery time is not set."
            else:
                return f"Package {self.id} status is {self.status.value} with a deadline of {self.deadline} and the delivery time is not set."
        else:
            if self.deadline == "EOD":
                return f"Package {self.id} is {self.status.value} on truck {self.truck_number}. It is scheduled for delivery at {(self.delivery_time).strftime('%I:%M%p').lower()}."
            else:
                return f"Package {self.id} is {self.status.value} on truck {self.truck_number}. Its deadline is {self.deadline} and it is scheduled for delivery at {(self.delivery_time).strftime('%I:%M%p').lower()}."

    # Defining a function to update the hash table with the status of the package based on the user's requested time input
    def update(self, hash_table, user_time): # O(1)
        if user_time < self.departure_time:
            self.status = PackageStatus.WAITING
        elif user_time > self.delivery_time:
            self.status = PackageStatus.DELIVERED
        else:
            self.status = PackageStatus.TRANSIT
        hash_table.add(self.id, self)
        
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
