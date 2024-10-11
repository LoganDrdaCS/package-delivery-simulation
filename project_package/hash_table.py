# For add, get, delete functions, time complexity is O(1)

# Using constants for quick changes in the future (scalability)
TABLE_SIZE = 32 # chosen to allow for collisions to demonstrate collision handling

class HashTable:
    def __init__(self):
        self.table = [[] for _ in range(TABLE_SIZE)] # create a list of lists to handle collisions later

    # Basic hash function guaranteed to create collisions at some point
    def _generate_hash(self, key):
        return hash(key) % TABLE_SIZE

    def add(self, key, value):
        index = self._generate_hash(key) # AKA the hash of the key
        pair = [key, value]
        # Iterate through the list at the hashed index to see if the [key, value] pair has already been added
        # If so, the value of that key will be updated and no additional append will be performed
        for key_value in self.table[index]:
            if key_value[0] == key:
                key_value[1] = value
                # print(f"Package with ID of '{key}' successfully updated with new value.") # optional
                return
            
        self.table[index].append(pair) # adds the key,value pair to the list at the hashed index
        # print(f"Package with ID of '{key}' added successfully.") # optional

    # REQUIREMENT B FOR TASK 2
    def retrieve(self, key): # the key is the Package ID
        index = self._generate_hash(key) # AKA the hash of the key
        # Searching through the list at the resulting index in the hash table
        for key_value in self.table[index]:
            if key_value[0] == key:
                # print(f"Package with ID of '{key}' retrieved.") # optional
                return key_value[1] # the resulting package object
        print(f"Package with ID of '{key}' not found.")
        return None  # If the key is not found, or if the hash table is empty at that index, returns None

    def delete(self, key):
        index = self._generate_hash(key)  # AKA the hash of the key

        # Iterate to find the key and delete the pair from the hash table
        for i in range(len(self.table[index])):
            if self.table[index][i][0] == key:
                del self.table[index][i]
                print(f"Package with ID of '{key}' successfully deleted.")
                return

        print(f"Package with ID of '{key}' not found.")

    # A function to print all the elements of the hash table
    def display(self):
        for nested in self.table:
            if nested:  # check if the hash table is populated at that index
                for key_value in nested:
                    print(f"Key '{key_value[0]}', Value '{key_value[1]}'")
