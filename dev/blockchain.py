import json
import os
import time
import hashlib
from smartcontract import *
from merkle_tools import MerkleTools

from block import Block
class Blockchain:
    def __init__(self):
        self.blocks = []
        self.load_blocks()
        self.tokenized_contract = TokenizedSmartContract()  # Create an instance of TokenizedSmartContract
        self.access_smart_contract = AuthenticateSmartContract()  # Create an instance of AuthenticateSmartContract
        self.verification_smart_contract = VerificationSmartContract()
    def load_blocks(self):
        if os.path.exists("blocks.json"):
            # Load existing blocks from blocks.json
            with open("blocks.json", "r") as file:
                blocks_data = json.load(file)
                for block_data in blocks_data:
                    block = Block(
                        block_data['index'],
                        block_data['previous_hash'],
                        block_data['timestamp'],
                        block_data['merkle_root'],
                        block_data['transactions'],
                        block_data['merkle_roots_by_case']
                    )
                    self.blocks.append(block)
        else:
            # Create the genesis block if blocks.json doesn't exist
            self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block manually (genesis block)
        genesis_block = Block(0, "", time.time(), "", [])
        self.blocks.append(genesis_block)
        self.save_blocks()

    def add_block(self, transactions):
        # Get the index of the previous block
        previous_index = self.blocks[-1].index
        # Get the hash of the previous block's header
        previous_hash = self.blocks[-1].hash
        # Get the current timestamp
        timestamp = time.time()
        transactions_by_case = {}
        transaction_strings_by_case = {}
        try:
            with open('read.json', 'r') as file:
             read = json.load(file)
        except FileNotFoundError:
             read = []
        try:
            with open('write.json', 'r') as file:
             write = json.load(file)
        except FileNotFoundError:
             write= []
        try:
            with open('Initial.json', 'r') as file:
             Initial = json.load(file)
        except FileNotFoundError:
             Initial = []
        try:
            with open('Upload.json', 'r') as file:
             Upload = json.load(file)
        except FileNotFoundError:
             Upload= []
        try:
            with open('Analysis.json', 'r') as file:
             Analysis = json.load(file)
        except FileNotFoundError:
             Analysis= []   
        try:
            with open('Access.json', 'r') as file:
             Access = json.load(file)
        except FileNotFoundError:
             Access= []   

        # Process transactions based on their types
        for transaction in transactions.values():
            case_number = transaction['case_number']
            transaction_type = transaction.get('transaction_name')
            ##print(type(transaction))
            if transaction_type in ['initial_upload_transaction']:
                ##print(".............we here......................", transaction,previous_index + 1)
                start_time = time.time()
                result=self.tokenized_contract.process_transactions(transaction,previous_index + 1)
                transaction['SC_Token_output']=result
                end_time = time.time()
                execution_time = end_time - start_time
                Initial.append({"time": execution_time})
                with open('Initial.json', 'w') as file:
                    json.dump(Initial, file)

            if transaction_type in [ 'file_upload_transaction']:
                start_time = time.time()
                result=self.tokenized_contract.process_transactions(transaction,previous_index + 1)
                transaction['SC_Token_output']=result
                end_time = time.time()
                execution_time = end_time - start_time
                Upload.append({"time": execution_time})
                with open('Upload.json', 'w') as file:
                    json.dump(Upload, file)

            if transaction_type in [ 'create_analysis_transaction']:
                start_time = time.time()
                result=self.tokenized_contract.process_transactions(transaction,previous_index + 1)
                transaction['SC_Token_output']=result
                end_time = time.time()
                execution_time = end_time - start_time
                Analysis.append({"time": execution_time})
                with open('Analysis.json', 'w') as file:
                    json.dump(Analysis, file)
            
          
            if transaction_type in ['read_transaction']:
                start_time = time.time()
                ##print(".............we here......................", transaction,previous_index + 1)
                result=self.tokenized_contract.process_transactions(transaction,previous_index + 1)
                transaction['SC_Token_output']=result 
                end_time = time.time()
                execution_time = end_time - start_time
                read.append({"time": execution_time})
                with open('read.json', 'w') as file:
                    json.dump(read, file)
            
            if transaction_type in [ 'write_transaction']:
                    start_time = time.time()
                    ##print(".............we here......................", transaction,previous_index + 1)
                    result=self.tokenized_contract.process_transactions(transaction,previous_index + 1)
                    transaction['SC_Token_output']=result 
                    end_time = time.time()
                    execution_time = end_time - start_time
                    write.append({"time": execution_time})
                    with open('write.json', 'w') as file:
                        json.dump(write, file)

            if transaction_type == 'create_access_transaction':
                start_time = time.time()
                result=self.access_smart_contract.retrieve_access_info(transaction,previous_index + 1)
                transaction['SC_Authenticate_output']=result
                end_time = time.time()
                execution_time = end_time - start_time
                Access.append({"time": execution_time})
                with open('Access.json', 'w') as file:
                    json.dump(Access, file)


            if transaction_type == 'stage_change_transaction':
                result=self.tokenized_contract.process_transactions(transaction,previous_index + 1)
                transaction['SC_Authenticate_output']=result
                
            if transaction_type =='verification_transaction':
                result=self.verification_smart_contract.verify_storage(transaction,previous_index + 1)
                transaction['SC_Verification_output']=result
                ##print("we  are down here", transaction_type)
 # Convert transactions to strings
            if case_number in transactions_by_case:
        # Append the transaction to the existing list
               transactions_by_case[case_number].append(transaction)
            else:
        # Create a new list for the case number and add the transaction
              transactions_by_case[case_number] = [transaction]
       # #print( transactions_by_case )
           
        
        for case_number, transaction_list in transactions_by_case.items():
            transaction_case_strings = [str(transaction) for transaction in transaction_list]  
            transaction_strings_by_case[case_number] = transaction_case_strings
            ##print("trasnction_case string:,",transaction_case_strings)



        
        transaction_strings = [str(transaction) for transaction in transactions.values()]
        ##print("trasnction_string:,",transaction_strings)
       # #print(transaction_strings)
        # Calculate the Merkle root from the transactions
        merkle_root = self.calculate_merkle_root(transaction_strings)
        # Calculate the Merkle root from the transactions for each case_number
        merkle_roots_by_case = {}
        for case_number, transaction_strings1 in transaction_strings_by_case.items():
            merkle_root_special = self.calculate_merkle_root(transaction_strings1)
            #print("thus is the first",merkle_root_special)
            merkle_root_special=self.add_merkle_case(merkle_root_special,case_number)
            #print("thus is the second",merkle_root_special)



            merkle_roots_by_case[case_number] = merkle_root_special



        ##print( merkle_roots_by_case)
        # Create the new block
        block = Block(previous_index + 1, previous_hash, timestamp, merkle_root,transaction_strings,merkle_roots_by_case)
        self.blocks.append(block)
        # self.save_blocks()

    def save_blocks(self):
        # Save the blocks to blocks.json
        blocks_data = []
        for block in self.blocks:
            blocks_data.append(block.to_dict())
        with open("blocks.json", "w") as file:
            json.dump(blocks_data, file, indent=4)

    def calculate_merkle_root(self, transactions):
        # Create an instance of MerkleTools
        merkle_tools = MerkleTools()
       
        # Add the transactions as leaves
        for transaction in transactions:
            merkle_tools.add_leaf(transaction, do_hash=True)
           
        # Make the Merkle tree
        merkle_tools.make_tree()

        # Get the Merkle root
        merkle_root = merkle_tools.get_merkle_root()

        return merkle_root
    

    def calculate_special_merkle_root(self, transactions):
        # Create an instance of MerkleTools
        merkle_tools = MerkleTools()

        # Add the transactions as leaves
        for transaction in transactions:
            ##print(transaction)
            merkle_tools.add_leaf(transaction, do_hash=True)
          
        # Make the Merkle tree
        merkle_tools.make_tree()

        # Get the Merkle root
        merkle_root = merkle_tools.get_merkle_root()

        return merkle_root

    def add_merkle_case(self,merkle_root_special,case_number):
        if os.path.exists('case_tk.json'):
            with open('case_tk.json', 'r') as file:
                case_dict = json.load(file)
        else:
            case_dict = []

        # Get the case_number from the function argument
        case_number = int(case_number)
       
        # Find the case with matching case_number using binary search
        index = self.binary_search(case_dict, case_number)
        if index < len(case_dict) and case_dict[index]['case_number'] == case_number:
            # Add token to the token_list of the smart contract
            if case_dict[index]['last_merkle_root']==[]:
                case_dict[index]['last_merkle_root']=merkle_root_special
                combined_merkle_root=merkle_root_special
            else:
                
                merkle_root=case_dict[index]['last_merkle_root']
               
                merkle_tools = MerkleTools()
                merkle_tools.add_leaf(merkle_root, do_hash=True)
                merkle_tools.add_leaf(merkle_root_special, do_hash=True)
                merkle_tools.make_tree()
                combined_merkle_root = merkle_tools.get_merkle_root()
                #transaction_strings = [str(merkle_root)+str(merkle_root_special)]
                #merkle_root_special = self.calculate_special_merkle_root(transaction_strings)
                case_dict[index]['last_merkle_root']=combined_merkle_root
                #print("added it:",combined_merkle_root)
        else:
            combined_merkle_root=merkle_root_special     
        with open('case_tk.json', 'w') as file:
            json.dump(case_dict, file)
        return combined_merkle_root
        
    def binary_search(self,case_dict, case_number):
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
    


    