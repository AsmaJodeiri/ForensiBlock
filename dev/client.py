from hashlib import sha256
import time
import os
import json
from security import Security
from securitystorage import Securitystorage
import re

class Client:
    def __init__(self):
        # Initialize the storage
        self.data = []

    def receive(self, bc_data):
        # Perform initial upload of data to the storage
        self.data.append(bc_data)  
        security = Security()
        public_key, private_key = security.retrieve_keys_from_file()
        decrypted_message = security.dec(bc_data, private_key)  

        with open('client.json', 'r') as file:
            data = json.load(file)

        data.append(decrypted_message)  

        # Write the updated data back to the JSON file
        with open('client.json', 'w') as file:
            json.dump(data, file)
    


    
