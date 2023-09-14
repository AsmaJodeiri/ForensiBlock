import os
import json
import time
from security import Security
from storage import Storage
from securitystorage import Securitystorage
from client import Client
from verification import Verification
import user_index
from hashlib import sha256


class Verification_search:
    def __init__(self):
        self.case_dict = {}

    def verify_storage(self, case_number):
        if os.path.exists('case_tk.json'):
            with open('case_tk.json', 'r') as file:
                case_dict = json.load(file)
        else:
            case_dict = []

        try:
            with open('time-ver.json', 'r') as file:
                case_times = json.load(file)
        except FileNotFoundError:
            case_times = []

        # Measure the execution time for each case number
        transactions = []
        start_time = time.time()
        index = self.binary_search(case_dict, case_number)

        if index < len(case_dict) and case_dict[index]['case_number'] == case_number:
            merkle_root = case_dict[index]['last_merkle_root']
            transaction_sorter = Verification()
            storage_string, transactions = transaction_sorter.filter_and_sort_transactions(case_number)
            if merkle_root == storage_string:
                end_time = time.time()
                execution_time = end_time - start_time
                case_data = {case_number: execution_time}
                case_times.append(case_data)
                print("storage verified")
                #print(transactions)
                result = 'storage verified'
                with open('time-ver.json', 'w') as file:
                    json.dump(case_times, file)
                return result
            else:
                end_time = time.time()
                execution_time = end_time - start_time
                case_data = {case_number: execution_time}
                case_times.append(case_data)
                print("storage not verified")
                result = 'storage not verified'
                with open('time-ver.json', 'w') as file:
                    json.dump(case_times, file)
                return result
        else:
            end_time = time.time()
            execution_time = end_time - start_time
            case_data = {case_number: execution_time}
            case_times.append(case_data)
            result = 'No such case'
            with open('time-ver.json', 'w') as file:
                json.dump(case_times, file)
            return result

    def binary_search(self, case_dict, case_number):
        left = 0
        right = len(case_dict) - 1

        while left <= right:
            mid = (left + right) // 2
            if case_dict[mid]['case_number'] == case_number:
                return mid
            elif case_dict[mid]['case_number'] < case_number:
                left = mid + 1
            else:
                right = mid - 1

        return left

start_case=1
end_case=11
# Example usage
verifier = Verification_search()
for case_number in range(start_case, end_case):
    result = verifier.verify_storage(case_number)
    print(case_number)



if os.path.exists('time-ver.json'):
    with open('time-ver.json', 'r') as file:
        data = json.load(file)
    times = [list(item.values())[0] for item in data]
    average_time = sum(times) / len(times)
    print(average_time)
else:
    print("File 'time_ver.json' does not exist.")