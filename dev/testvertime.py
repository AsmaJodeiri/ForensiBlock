import json
import time
from blockchain import Blockchain
from transactions import *
from security import Security
from transactions import *

def test_blockchain(case_number):
    base_tokens = ['1e4a415e66b28127e91abc4cfdc2ea797db1feddc3ac8d88444be15b6fde44b9']
    transaction_list = [
        {
            'transaction_name': 'verification',
            'args': [case_number]
        }
    ]

    def save_keys_to_file(public_key, private_key):
        keys = {
            "public_key": public_key,
            "private_key": private_key
        }

        with open('keys.json', 'w') as file:
            json.dump(keys, file, indent=4)

    def retrieve_keys_from_file(user_index):
        try:
            with open('keys.json', 'r') as file:
                keys = json.load(file)
                for key_data in keys:
                    if key_data['user_index'] == user_index:
                        return key_data['public_key'], key_data['private_key']
                return None, None
        except FileNotFoundError:
            return None, None

    user_index = 4
    public_key, private_key = retrieve_keys_from_file(user_index)

    blockchain = Blockchain()
    transaction_processor = TransactionProcessor(public_key, private_key)
    transaction_dict = transaction_processor.add_transactions(transaction_list)
    blockchain.add_block(transaction_dict)

# Specify the range of case numbers for which you want to measure the execution time
start_case = 1
end_case = 11

# Load existing case times from time-ver.json


# Measure the execution time for each case number
for case_number in range(start_case, end_case):
    
    test_blockchain(case_number)
    # Insert the case_data dictionary into case_times list
    

# Save case times to time-ver.json


if os.path.exists('time-ver.json'):
    try:
        with open('time-ver.json', 'r') as file:
            data = json.load(file)
        times = list(data.values())
        average_time = sum(times) / len(times)
        print(average_time)
    except ValueError:
        print("Invalid JSON data in file 'times_storage.json'.")
else:
    print("File 'times_storage.json' does not exist.")
