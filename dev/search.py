import json
import time
import os
def search_case_number(case_number):
    with open('blocks.json', 'r') as file:
        blocks = file.read()
        block_list = json.loads(blocks)

        matching_transactions = []
        for index, block in enumerate(block_list, start=1):
            transactions = block.get('transactions', [])
            for transaction in transactions:
                if isinstance(transaction, str):
                    try:
                        transaction_obj = json.loads(transaction.replace("'", "\""))
                        if transaction_obj.get('case_number') == case_number:
                            matching_transactions.append((index, transaction))
                            break
                    except json.JSONDecodeError:
                        continue

        return matching_transactions


# Example usage
case_numbers = range(1, 11)
execution_times = {}

for case_number in case_numbers:
    total_time = 0
    for _ in range(20):
        start_time = time.time()
        matching_transactions = search_case_number(case_number)
        end_time = time.time()
        execution_time = end_time - start_time
        total_time += execution_time
        
    average_time = total_time /20
    execution_times[case_number] = average_time

    #print(f"Matching transactions for case number {case_number}:")
    #for transaction in matching_transactions:
     #   print(transaction)

# Save execution times to times.json
with open('times.json', 'w') as file:
    json.dump(execution_times, file)

if os.path.exists('times.json'):
    try:
        with open('times.json', 'r') as file:
            data = json.load(file)
        times = list(data.values())
        average_time = sum(times) / len(times)
        print(average_time)
    except ValueError:
        print("Invalid JSON data in file 'times_storage.json'.")
else:
    print("File 'times_storage.json' does not exist.")
