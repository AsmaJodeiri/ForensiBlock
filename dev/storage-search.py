import json
import time
import matplotlib.pyplot as plt
import os


def binary_search(case_dict, case_number):
    left = 0
    right = len(case_dict) - 1
    start_index = -1
    end_index = -1

    while left <= right:
        mid = (left + right) // 2
        if case_dict[mid][0]['case_number'] == case_number:
            start_index = mid
            end_index = mid
            break
        elif case_dict[mid][0]['case_number'] < case_number:
            left = mid + 1
        else:
            right = mid - 1

    if start_index == -1:
        return -1, -1

    # Look back to find the actual start index where the sequence begins
    while start_index > 0 and case_dict[start_index - 1][0]['case_number'] == case_number:
        start_index -= 1

    # Find the end index for the given case_number
    for i in range(start_index + 1, len(case_dict)):
        if case_dict[i][0]['case_number'] == case_number:
            end_index = i
        else:
            break

    return start_index, end_index


def extract_transactions(case_number):
    with open('storage.json', 'r') as file:
        data = json.load(file)

    start_index, end_index = binary_search(data, case_number)

    if start_index == -1:
        return []

    matching_transactions = []
    for i in range(start_index, end_index + 1):
        matching_transactions += data[i]

    return matching_transactions


case_numbers = range(1, 11)
average_times = {}

for _ in range(10):
    execution_times = []

    for case_number in case_numbers:
        start_time = time.time()
        matching_transactions = extract_transactions(case_number)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)

        # Print matching transactions if needed...

    if execution_times:
        average_time = sum(execution_times) / len(execution_times)
    else:
        average_time = -1  # Assign default value if no matching transactions

    average_times[_] = average_time

# Save average execution times to times.json
with open('times_storage.json', 'w') as file:
    json.dump(average_times, file)

# Plotting the average execution times
if os.path.exists('times_storage.json'):
    try:
        with open('times_storage.json', 'r') as file:
            data = json.load(file)
        times = list(data.values())
        average_time = sum(times) / len(times)
        print(average_time)
    except ValueError:
        print("Invalid JSON data in file 'times_storage.json'.")
else:
    print("File 'times_storage.json' does not exist.")
