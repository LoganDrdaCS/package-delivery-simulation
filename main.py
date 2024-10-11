# Student ID: 011010779

from project_package.package import load_csv_packages, PackageStatus
from project_package.truck import Truck
from project_package.hash_table import HashTable
import csv
from datetime import datetime, timedelta

# Using constants for easy changes to values in the future (scaling)
NUMBER_OF_TRUCKS = 3

"""
This file instantiates the trucks and packages. It _______________
"""

# ------------------------------------------------------------------------ #

if __name__ == "__main__":
    hash_table = HashTable() # creates a hash table
    package_list = load_csv_packages() # instantiating all of the packages
    for package in package_list:
        hash_table.add(package.id, package) # adding each package object to the hash table
    truck_list = [] # empty list to hold truck objects
    for i in range(NUMBER_OF_TRUCKS): # this loop is easily scalable if the number of trucks increases
        truck_list.append(Truck(i+1))

    # Setting departure times for the first 2 trucks
    truck_list[0].departure_time = datetime.strptime("8:00am", "%I:%M%p")
    truck_list[1].departure_time = datetime.strptime("9:05am", "%I:%M%p")
    truck_list[0].time = truck_list[0].departure_time
    truck_list[1].time = truck_list[1].departure_time


    # Creating lists of package IDs which will go on each truck
    truck1_manual_package_ids = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    truck2_manual_package_ids = [3, 4, 5, 6, 8, 18, 19, 21, 24, 25, 26, 28, 32, 33, 36, 38]
    truck3_manual_package_ids = [2, 7, 9, 10, 11, 12, 17, 22, 23, 27, 35, 39]

    # Creates lists of package objects that were manually chosen for each truck
    truck1_manual_packages = []
    truck2_manual_packages = []
    truck3_manual_packages = []
    for package_id in truck1_manual_package_ids:
        truck1_manual_packages.append(package_list[package_id - 1])
    for package_id in truck2_manual_package_ids:
        truck2_manual_packages.append(package_list[package_id - 1])
    for package_id in truck3_manual_package_ids:
        truck3_manual_packages.append(package_list[package_id - 1])

    # Setting departure time for each package on the first 2 trucks
    for package in truck1_manual_packages:
        package.departure_time = truck_list[0].departure_time
    for package in truck2_manual_packages:
        package.departure_time = truck_list[1].departure_time

    # Reading the remaining 2 data files
    with open(r"project_package\data\Addresses.csv") as file:
        address_list = list(csv.reader(file))
    with open(r"project_package\data\Distances.csv") as file:
        distance_list = list(csv.reader(file))
    
    # Defining a function to calculate distance between addresses
    def distance_calculator(x, y):
        distance = distance_list[x][y]
        if distance == '':
            distance = distance_list[y][x]
        return float(distance)
    
    # Defining a function to return the address ID (0 through 26) from an address specified
    def address_id_converter(address: str):
        for row in address_list:
            if address in row[2]:
                return int(row[0])
    
    # Assigning the address ID (0 through 26) to all of the packages
    for package in package_list:
        package.address_id = address_id_converter(package.address)
    
    # Uses closest neighbor algorithm to build the queue and make the deliveries
    def make_deliveries(truck_manual_package_list, truck):
        current_address_id = 0
        while truck_manual_package_list:
            least_distance = 100
            closest_index = None
            index = -1
            # if len(truck_manual_package_list) == 6:
            #     print('time for a break')
            for package in truck_manual_package_list:
                index += 1
                if distance_calculator(current_address_id, package.address_id) <= least_distance:
                    least_distance = distance_calculator(current_address_id, package.address_id)
                    closest_index = index
            current_address_id = truck_manual_package_list[closest_index].address_id
            # truck.onboard_package_list.append(truck_manual_package_list.pop(closest_index))
            truck.mileage += least_distance
            truck.time += timedelta(hours = (least_distance / truck.speed))
            truck_manual_package_list[closest_index].delivery_time = truck.time
            truck.location = truck_manual_package_list[closest_index].address
            truck_manual_package_list[closest_index].status = PackageStatus.DELIVERED
            # updating each package object in the hash table
            hash_table.add(truck_manual_package_list[closest_index].id, truck_manual_package_list[closest_index])
            truck.onboard_package_list.append(truck_manual_package_list.pop(closest_index))
        # Return trip to hub after all deliveries were made
        distance_to_hub = distance_calculator(current_address_id, 0)
        truck.mileage += distance_to_hub
        truck.time += timedelta(hours = (distance_to_hub / truck.speed))
        truck.location = "4001 South 700 East"
        return
    
    # Calls the queue creator for each truck
    for package in truck1_manual_packages:
        package.status = PackageStatus.TRANSIT
    for package in truck2_manual_packages:
        package.status = PackageStatus.TRANSIT
    make_deliveries(truck1_manual_packages, truck_list[0])
    make_deliveries(truck2_manual_packages, truck_list[1])


    # Setting truck 3's departure time.
    # Cannot leave before 10:20am, so if one of the first 2 trucks finish early, 
    truck3_ideal_departure_time = datetime.strptime("10:20am", "%I:%M%p")
    if min(truck_list[0].time, truck_list[1].time) < truck3_ideal_departure_time:
        truck_list[2].departure_time = truck3_ideal_departure_time
    else:
        truck_list[2].departure_time = min(truck_list[0].time, truck_list[1].time)

    truck_list[2].time = truck_list[2].departure_time
    for package in truck3_manual_packages:
        package.departure_time = truck_list[2].departure_time
        package.status = PackageStatus.TRANSIT

    make_deliveries(truck3_manual_packages, truck_list[2])

    total_distance_all_trucks = truck_list[0].mileage + truck_list[1].mileage + truck_list[2].mileage

    print("\n\n----- WGUPS -----\n\n")
    print("Total mileage for all 3 trucks: " + str(total_distance_all_trucks) + "\n")

    while True:
        user_input = input('\nEnter the time to check the status of a package or all packages. Format as "11:15am".\n').lower()
        user_time = datetime.strptime(user_input, "%I:%M%p")
        user_input = input('Type "all" to see the status of all packages. To see the status of a single package, enter the package ID number.\n').lower()
        if user_input == 'all': # for all packages
            for package in package_list:
                specified_package = hash_table.retrieve(package.id) # looking up the package instance via the hash table
                specified_package.update(hash_table, user_time)
                print(str(specified_package))
        else: # for a single package instance
            specified_package = hash_table.retrieve(int(user_input)) # looking up the package instance via the hash table
            specified_package.update(hash_table, user_time)
            print(str(specified_package))

        user_input = input('Type "exit" to end the program, or enter a blank line to restart.\n').lower()
        if user_input == 'exit':
            exit()
        else:
            print('Restarting status checker.')
            continue
