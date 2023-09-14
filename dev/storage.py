from hashlib import sha256
import time
import os
import json
from security import Security
from securitystorage import Securitystorage
import re
class Storage:
    def __init__(self):
        # Initialize the storage
        self.data = []

    def initial_upload(self, data):
        # Perform initial upload of data to the storage
        self.data.append(data)
        security = Securitystorage()
        public_key, private_key = security.retrieve_keys_from_file()
        decrypted_message=security.dec(data, private_key)
        block_number = int(decrypted_message.split(":")[-1])
# Remove the "block_number" part from the string to make it a valid dictionary
        decrypted_message = decrypted_message.replace(", block_number:" + str(block_number), "")
        transaction_dict = eval(decrypted_message)
        case_number = int(transaction_dict.get('case_number', 0))
        # Create a list to store the transaction dictionaries
       # transactions = []

        # Append the transaction dictionary and block number to the list
        #transactions.append((transaction_dict, block_number))

        #split_message = decrypted_message.split(',')
        with open('storage.json', 'r') as file:
            data = json.load(file)
        #case_number=int(split_message[0])
        #new_case = {'case_number': int(case_number),'transaction':'initial_upload_transaction','initial_block_number':split_message[1],'current_stage':split_message[2],'time_stamp':split_message[3]}
            # Find the index to insert the new case_number using binary search
        index = self.binary_search(data, case_number)
        #print(index)
        #print(block_number)
        transaction_dict['block_number']=block_number
       # data.insert(index,(transaction_dict, 'block_number',block_number))
        data.insert(index,(transaction_dict,'end'))
        ##print('New case added:', case_number, 'with stage:', split_message[2])

        # Write the updated data back to the JSON file
        with open('storage.json', 'w') as file:
            json.dump(data, file)

    def token(self, transaction):
        # Generate a token for the transaction
        token = sha256(transaction.encode()).hexdigest()
        return token

    def access(self, token):
        # Check if the token is valid and return access status
        if token in self.data:
            return "Access granted"
        else:
            return "Access denied"
        
    
    def binary_search(self, case_dict, case_number):
        left = 0
        right = len(case_dict) - 1

        while left <= right:
            mid = (left + right) // 2
            if case_dict[mid][0]['case_number'] == case_number:
                # Check if the next element has the same case_number
                if mid < len(case_dict) - 1 and case_dict[mid + 1][0]['case_number'] == case_number:
                    left = mid + 1
                else:
                    return mid + 1  # Insert after the last occurrence
            elif case_dict[mid][0]['case_number'] < case_number:
                left = mid + 1
            else:
                right = mid - 1

        return left

