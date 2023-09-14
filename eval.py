import json
import os.path
from blockchain import Blockchain
from transactions import TransactionProcessor
import random
import shutil

selected_ids = []


def test_blockchain(case_count, n_blocks, min_transaction, max_transaction):
    def create_transaction_list(case_count, n_blocks, min_transactions_per_block, max_transactions_per_block):
        
        base_tokens = ['1e4a415e66b28127e91abc4cfdc2ea797db1feddc3ac8d88444be15b6fde44b9']
        transaction_list = []
        selected_for_block = []
        # Load records from records.json if it exists
        if os.path.exists('./dev/records.json'):
            with open('./dev/records.json', 'r') as file:
                records = json.load(file)
        else:
            records = []
            
        for case_number in range(1, case_count + 1):
            # Check if case_number exists in records
            case_exists = any(record['case_number'] == case_number for record in records)
            
            if not case_exists:
                prob = random.random()

                if prob > 0.80:
                    
                    # Create transaction for new case_number
                    case_data = {'case_number': case_number}
                    records.append(case_data)

                    # Update records.json
                    with open('./dev/records.json', 'w') as file:
                        json.dump(records, file)

                    # Add initial_upload transaction for the case
                    stage = random.choice(['Affidavit', 'Warrant', 'Investigation', 'Analysis',
                                        'Presented in Court', 'Judgement Day', 'Case Closed', 'Potential Appeal'])
                    initial_upload_transaction = {
                        'transaction_name': 'initial_upload',
                        'args': [case_number, stage]
                    }
                    transaction_list.append(initial_upload_transaction)
                    # print(len(transaction_list))
                    selected_for_block.append(case_number)
                

        # Determine the total number of transactions for this block
        total_transactions = random.randint(min_transactions_per_block, max_transactions_per_block)
        
        # print(len(transaction_list))
        # Shuffle the case numbers
        random.shuffle(records)
        
        for case_data in records:
            
            case_number = case_data['case_number']
            if case_number in selected_ids and case_number not in selected_for_block:
                stage = random.choice(['Affidavit', 'Warrant', 'Investigation', 'Analysis',
                                    'Presented in Court', 'Judgement Day', 'Case Closed', 'Potential Appeal'])

                if total_transactions <= 0:
                    break
                    
                num_transactions = random.randint(1, total_transactions)
                total_transactions -= num_transactions

                for _ in range(num_transactions):
                    transaction_name = random.choice(['read',
                                                    'write','create_analysis','file_upload','create_access'])
                    if transaction_name == 'create_analysis':
                        transaction_args = ['actions', 'hash_of_data', case_number, base_tokens]
                    elif transaction_name == 'create_access':
                        transaction_args = ['token', stage, case_number, 'write']
                    elif transaction_name == 'file_upload':
                        transaction_args = [case_number, f'hash_of_data{random.randint(1, 10)}']
                    elif transaction_name == 'stage_change':
                        transaction_args = [case_number, stage]
                    elif transaction_name == 'read':
                        transaction_args = [case_number]
                    elif transaction_name == 'write':
                        transaction_args = [case_number]
                    transaction_dict = {
                        'transaction_name': transaction_name,
                        'args': transaction_args
                    }
                    transaction_list.append(transaction_dict)
                    
                    
        selected_ids.extend(selected_for_block)
        return transaction_list

    def save_keys_to_file(public_key, private_key):
        keys = {
            "public_key": public_key,
            "private_key": private_key
        }

        with open('./dev/keys.json', 'w') as file:
            json.dump(keys, file, indent=4)

    def retrieve_keys_from_file(user_index):
        try:
            with open('./dev/keys.json', 'r') as file:
                keys = json.load(file)
                for key_data in keys:
                    if key_data['user_index'] == user_index:
                        return key_data['public_key'], key_data['private_key']
                return None, None
        except FileNotFoundError:
            return None, None

    user_index = 4
    public_key, private_key = retrieve_keys_from_file(user_index)

    blockchain = Blockchain()  # Initialize the blockchain
    for block in range(1, n_blocks):
        print(block)
        transaction_list = create_transaction_list(case_count, n_blocks, min_transaction, max_transaction)
        # print(len(transaction_list))
        transaction_processor = TransactionProcessor(public_key, private_key)  # Create an instance of TransactionProcessor

        transaction_dict = transaction_processor.add_transactions(transaction_list)
        # print(transaction_dict)
        blockchain.add_block(transaction_dict)

    blockchain.save_blocks()

    # Remove records.json after all blocks have been processed
    
# Run the test
#cases = [100, 500, 1000]
cases = [30]
#blocks = [10, 100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
blocks = [1000]

for i in range(len(cases)):
    for j in range(len(blocks)):
        block_count = blocks[j]
        if j != 0:
            block_count = blocks[j]-blocks[j-1]

        test_blockchain(cases[i], block_count, 1, 30)       
        dir_name = 'c_'+str(cases[i])+'_b_'+str(blocks[j])

        os.mkdir('./eval_files/'+dir_name)

        test_dir = './eval_files/' + dir_name

        shutil.copyfile('./dev/blocks.json', test_dir + '/blocks.json')        
        shutil.copyfile('./dev/case.json', test_dir + '/case.json')        
        shutil.copyfile('./dev/case_tk.json', test_dir + '/case_tk.json')        
        shutil.copyfile('./dev/records.json', test_dir + '/records.json')        
        shutil.copyfile('./dev/storage.json', test_dir + '/storage.json')        
        shutil.copyfile('./dev/client.json', test_dir + '/client.json') 
