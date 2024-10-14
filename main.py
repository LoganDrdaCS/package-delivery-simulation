# Student ID: 011010779

# Overall time complexity is O(n^2)

from project_package.package import load_csv_packages, PackageStatus
from project_package.truck import Truck
from project_package.hash_table import HashTable
import csv
from datetime import datetime, timedelta

# Using constants for quick changes in the future (scalability)
NUMBER_OF_TRUCKS = 3

# --------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    hash_table = HashTable() # creates a hash table
    package_list = load_csv_packages() # instantiates all of the packages, O(n)
    for package in package_list:
        hash_table.add(package.id, package) # adds each package object to the hash table
    truck_list = [] # empty list to hold truck objects
    for i in range(NUMBER_OF_TRUCKS): # this loop is easily scalable if the number of trucks changes, O(n)
        truck_list.append(Truck(i+1))

    # Setting departure times for the first 2 trucks
    truck_list[0].departure_time = datetime.strptime("8:00am", "%I:%M%p")
    truck_list[1].departure_time = datetime.strptime("9:05am", "%I:%M%p")
    truck_list[0].time = truck_list[0].departure_time
    truck_list[1].time = truck_list[1].departure_time

    # Manually creating lists of package IDs which will go on each truck (unordered for now)
    truck1_manual_package_ids = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    truck2_manual_package_ids = [3, 4, 5, 6, 8, 18, 19, 21, 24, 25, 26, 28, 32, 33, 36, 38]
    truck3_manual_package_ids = [2, 7, 9, 10, 11, 12, 17, 22, 23, 27, 35, 39]
    
    # Adding packages chosen above to each truck's onboard package list, O(n)
    for package_id in truck1_manual_package_ids:
        truck_list[0].add_package(package_list[package_id - 1])
        package_list[package_id - 1].truck_number = 1
    for package_id in truck2_manual_package_ids:
        truck_list[1].add_package(package_list[package_id - 1])
        package_list[package_id - 1].truck_number = 2
    for package_id in truck3_manual_package_ids:
        truck_list[2].add_package(package_list[package_id - 1])
        package_list[package_id - 1].truck_number = 3

    # Setting departure time for each package on the first 2 trucks, O(n)
    for package in truck_list[0].onboard_package_list:
        package.departure_time = truck_list[0].departure_time
    for package in truck_list[1].onboard_package_list:
        package.departure_time = truck_list[1].departure_time

    # Reading the address and distance files, O(n)
    with open(r"project_package\data\Addresses.csv") as file:
        address_list = list(csv.reader(file))
    with open(r"project_package\data\Distances.csv") as file:
        distance_list = list(csv.reader(file))
    
    # Defining a function to calculate distance between addresses
    def distance_calculator(x, y):
        distance = distance_list[x][y]
        if distance == '':
            distance = distance_list[y][x] # flips the coordinates to account for the blank spaces
        return float(distance)
    
    # Defining a function to return the address ID (0 through 26) from an address specified
    def address_id_converter(address: str):
        for row in address_list:
            if address in row[2]:
                return int(row[0])
    
    # Assigning the address ID (0 through 26) to all of the packages, O(n)
    for package in package_list:
        package.address_id = address_id_converter(package.address)
    
    # ALGORITHM SEGMENT, O(n^2)
    # Using closest neighbor algorithm to build the queue for each truck and make the deliveries
    def make_deliveries(truck):
        current_address_id = 0 # starts at the hub
        while truck.onboard_package_list:
            least_distance = 1000 # arbitrary distance greater than any expected value
            closest_index = None
            index = -1
            for package in truck.onboard_package_list:
                index += 1
                if distance_calculator(current_address_id, package.address_id) <= least_distance: # finds the closest neighbor
                    least_distance = distance_calculator(current_address_id, package.address_id)
                    closest_index = index
            # Once closest neighbor is found after iterating through all neighbors, assignments are made
            current_address_id = truck.onboard_package_list[closest_index].address_id
            truck.mileage += least_distance
            truck.time += timedelta(hours = (least_distance / truck.speed))
            truck.onboard_package_list[closest_index].delivery_time = truck.time # sets delivery time of package
            truck.location = truck.onboard_package_list[closest_index].address
            truck.onboard_package_list[closest_index].status = PackageStatus.DELIVERED
            # Updating each package object in the hash table
            hash_table.add(truck.onboard_package_list[closest_index].id, truck.onboard_package_list[closest_index])
            # Removing the delivered package from the list of onboard packages
            truck.onboard_package_list.pop(closest_index)
        # Return trip to hub is calculated after all deliveries were made
        distance_to_hub = distance_calculator(current_address_id, 0)
        truck.mileage += distance_to_hub
        truck.time += timedelta(hours = (distance_to_hub / truck.speed))
        truck.location = "4001 South 700 East" # back at the hub
        return
    
    # Calling the algorithm/delivery function for the first 2 trucks
    for package in truck_list[0].onboard_package_list:
        package.status = PackageStatus.TRANSIT # sets packages to 'in transit'
    for package in truck_list[1].onboard_package_list:
        package.status = PackageStatus.TRANSIT # sets packages to 'in transit'
    make_deliveries(truck_list[0]) # first truck
    make_deliveries(truck_list[1]) # second truck

    # Setting truck 3's departure time. It cannot leave before 10:20am, so it
    # will depart either at 10:20am or later if the other trucks aren't finished yet
    truck3_ideal_departure_time = datetime.strptime("10:20am", "%I:%M%p")
    if min(truck_list[0].time, truck_list[1].time) < truck3_ideal_departure_time: # truck 1 or 2 is back by 10:20am
        truck_list[2].departure_time = truck3_ideal_departure_time
    else: # truck 1 and 2 are still out for deliveries at 10:20am
        truck_list[2].departure_time = min(truck_list[0].time, truck_list[1].time)

    # Modifying package variables onboard truck 3 and calling the algorithm/delivery function
    truck_list[2].time = truck_list[2].departure_time
    for package in truck_list[2].onboard_package_list:
        package.departure_time = truck_list[2].departure_time
        package.status = PackageStatus.TRANSIT # sets packages to 'in transit'
    make_deliveries(truck_list[2])

    # Calculating the total distance traveled by all trucks (scalable)
    total_distance_all_trucks = 0
    for truck in truck_list:
        total_distance_all_trucks += truck.mileage

    # USER INTERFACE SEGMENT, O(n)
    print("\n\n----- WGUPS -----\n\n")
    print("Total distance traveled for all trucks: " + str(total_distance_all_trucks) + " miles.\n")

    print("Truck 1 departure time: " + (truck_list[0].departure_time).strftime('%I:%M%p').lower())
    print("Truck 2 departure time: " + (truck_list[1].departure_time).strftime('%I:%M%p').lower())
    print("Truck 3 departure time: " + (truck_list[2].departure_time).strftime('%I:%M%p').lower() + "\n")

    # Creating a loop to obtain user input until they are finished with their entries
    while True:
        while True:
            user_input = input('Enter the time to check the status of a package or all packages. Format as "11:15am".\n').lower()
            try: # checking validity of user input
                user_time = datetime.strptime(user_input, "%I:%M%p")
                break
            except ValueError:
                print("Invalid entry. Try again.")
        
        while True:
            user_input = input('Type "all" to see the summarized status of all packages. Type "all with details" to see detailed attributes of every package.\nTo see the status and detailed attributes of a single package, enter the package ID number.\n').lower()
            if user_input == 'all' or user_input == "all with details": # for all packages
                for package in package_list:
                    specified_package = hash_table.retrieve(package.id) # retrieves the package instance via the hash table
                    specified_package.update(hash_table, user_time) # updates the package instance to reflect the user-entered time
                    if user_input == "all":
                        print(specified_package.print_summary())
                    else:
                        print(specified_package.print_all_details())
                break
            else: # for a single package instance
                try: # checking validity of user input
                    id_of_package = int(user_input)
                    specified_package = hash_table.retrieve(int(id_of_package)) # retrieves the package instance via the hash table
                    specified_package.update(hash_table, user_time) # updates the package instance to reflect the user-entered time
                    print(specified_package.print_all_details())
                    break
                except ValueError:
                    print("Invalid entry. Try again.")

        user_input = input('\nType "exit" to end the program, or enter a blank line to restart.\n').lower()
        if user_input == 'exit':
            exit()
        else:
            continue
