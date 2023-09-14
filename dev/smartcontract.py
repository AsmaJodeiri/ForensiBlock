from hashlib import sha256
import time
import os
import json
from security import Security
from storage import Storage
from securitystorage import Securitystorage
from client import Client
from verification import Verification
import  user_index 

class TokenizedSmartContract:
    
    def __init__(self):
        self.smart_contracts = {}
        #role_file_path = r"C:\Users\ajodeiriakbarfam\Desktop\courses\BC\BC-test\role_file.txt"
       # access_info_file_path = r"C:\Users\ajodeiriakbarfam\Desktop\courses\BC\BC-test\access_info_file.txt"

        self.authenticate_contract = AuthenticateSmartContract()  # Create an instance of AuthenticateSmartContract
    def tokenize(self, data):
        # Create token based on hash of data
        return sha256(str(data).encode()).hexdigest()
    
    def create_smart_contract(self, case_number, initial_block_number, current_stage, sender_public_key):
        # Create new smart contract
        timestamp = int(time.time())
        smart_contract = {
            'case_number': case_number,
            'timestamp': timestamp,
            'initial_block_number': initial_block_number,
            'current_stage': current_stage,
            'creator': sender_public_key,
            'token_list': [],
            'last_merkle_root':[]
        }

        # Check if case_number already exists in the JSON file
        if os.path.exists('case_tk.json'):
            with open('case_tk.json', 'r') as file:
                case_dict = json.load(file)
        else:
            case_dict = []

        # Get the case_number from the function argument
        case_number = int(case_number)

        index = AuthenticateSmartContract.binary_search(case_dict, case_number)
        if index < len(case_dict) and case_dict[index]['case_number'] == case_number:
            return 'failed already there'

        new_case = {
            'case_number': case_number,
            'current_stage': current_stage,
            'timestamp': timestamp,
            'creator': sender_public_key,
            'initial_block_number': initial_block_number,
            'token_list': [],
            'last_merkle_root':[]
        }
        case_dict.insert(index, new_case)
        #print('New case added')

        # Write the updated data back to the JSON file
        with open('case_tk.json', 'w') as file:
            json.dump(case_dict, file)
        #print(f"Request sent to authenticate smart contract with case number {case_number} and current stage {current_stage}")
        self.authenticate_contract.update_case_stage(case_number,current_stage)

        return 'New case added'






        #security = Security()
       # public_key, private_key = security.retrieve_keys_from_file()
        #storage_message = security.enc(str(case_number) +','+ str(initial_block_number) +','+ str(current_stage)+','+ str(timestamp),public_key)
       # storage = Storage()
       # storage.initial_upload(storage_message)
    
    def storage_comunication(self,transaction_dict,block_number):
        ##print('####',transaction_dict)
        #transaction_values = ','.join(str(value) for value in transaction_dict.values())
       # timestamp = int(time.time())

        security = Securitystorage()
        public_key, private_key = security.retrieve_keys_from_file()
        ##print(transaction_values)
        storage_message = security.enc(str(transaction_dict) + ', block_number:' + str(block_number), public_key)
        
        ##print(security.dec(storage_message,private_key))
        storage = Storage()
        storage.initial_upload(storage_message)

    def client_comunication(self,public_key,case_number,action):

        security = Security()
        
        storage_message = security.enc('case number: '+str(case_number) + ' result: ' + str(action), public_key)
        client = Client()
        client.receive(storage_message)

    def process_transactions(self, transaction, block_number):
        transaction_type = transaction.get('transaction_name')
        if transaction_type in ['initial_upload_transaction']:
            result=self.create_smart_contract(transaction['case_number'],block_number, transaction['current_stage'],transaction['sender_public_key'])
            transaction['SC_Token_output'] = result
            self.storage_comunication(transaction,block_number)
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],result)


        if transaction_type in ['file_upload_transaction']:
            result=self.tokenize_and_add_token(transaction['case_number'], transaction['hash_of_data'])
            transaction['SC_Token_output'] = result
            self.storage_comunication(transaction,block_number)
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],result)

        if transaction_type in ['stage_change_transaction']:
            result=AuthenticateSmartContract.update_case_stage(transaction['case_number'], transaction['current_stage'])
            transaction['SC_Authenticate_output']=result
            self.storage_comunication(transaction,block_number)
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],result)
        if transaction_type in ['read_transaction']:
            result='read'
            transaction['SC_Token_output'] = result
            self.storage_comunication(transaction,block_number)
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],result)  
        if transaction_type in ['write_transaction']:
            result='write'
            transaction['SC_Token_output'] = result
            self.storage_comunication(transaction,block_number)
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],result)  
        elif transaction_type in ['create_analysis_transaction']:
            result=self.tokenize_and_add_token_base(transaction['case_number'], transaction['hash_of_data'],transaction['base_tokens']#transaction['actions']
                                        )
            transaction['SC_Token_output'] = result
            self.storage_comunication(transaction,block_number)
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],result)
        return(result)
    
    def tokenize_and_add_token(self, case_number, data):
        # Create new token based on data
        token = self.tokenize(data)

        # Load case_dict from case_tk.json
        if os.path.exists('case_tk.json'):
            with open('case_tk.json', 'r') as file:
                case_dict = json.load(file)
        else:
            case_dict = []

        # Get the case_number from the function argument
        case_number = int(case_number)

        # Find the case with matching case_number using binary search
        index = AuthenticateSmartContract.binary_search(case_dict, case_number)
        if index < len(case_dict) and case_dict[index]['case_number'] == case_number:
            # Add token to the token_list of the smart contract
            case_dict[index]['token_list'].append(token)
            #print('Token added to case:', case_number)
        else:
            return 'no such case_number'

        # Write the updated data back to the JSON file
        with open('case_tk.json', 'w') as file:
            json.dump(case_dict, file)

        return token


    def tokenize_and_add_token_base(self, case_number, data, base_tokens):
        # Concatenate base tokens into a single string
        concatenated_tokens = ''.join(base_tokens)

        # Create new token based on concatenated tokens and data
        token = self.tokenize(concatenated_tokens)
        token_with_base_tokens = token + " base: " + ''.join(base_tokens)

        # Load case_dict from case_tk.json
        if os.path.exists('case_tk.json'):
            with open('case_tk.json', 'r') as file:
                case_dict = json.load(file)
        else:
            case_dict = []

        # Get the case_number from the function argument
        case_number = int(case_number)

        # Find the case with matching case_number using binary search
        index = AuthenticateSmartContract.binary_search(case_dict, case_number)
        if index < len(case_dict) and case_dict[index]['case_number'] == case_number:
            # Add token to the token_list of the smart contract
            case_dict[index]['token_list'].append(token)
            #print('Token with base added to case:', case_number)
        else:
            return 'no such case_number'

        # Write the updated data back to the JSON file
        with open('case_tk.json', 'w') as file:
            json.dump(case_dict, file)

        return token_with_base_tokens





class AuthenticateSmartContract:
    def __init__(self):
        #self.role_file = os.path.abspath(role_file)
        #self.access_info_file = os.path.abspath(access_info_file)
        self.case_dict = {}  # Dictionary to store case numbers and stages

    @staticmethod
    def binary_search(case_dict, case_number):
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

    @staticmethod
    def update_case_stage(case_number, stage):
        if os.path.exists('case.json'):
            with open('case.json', 'r') as file:
                case_dict = json.load(file)
        else:
            case_dict = []

        # Get the case_number from the function argument
        case_number = int(case_number)

        updated = False

        for item in case_dict:
            if isinstance(item, dict) and 'case_number' in item and item['case_number'] == case_number:
                item['current_stage'] = stage
                updated = True
                #print('Stage updated for case:', case_number)
                result= 'Case updated'
                break

        if not updated:
            new_case = {'case_number': case_number, 'current_stage': stage}
            # Find the index to insert the new case_number using binary search
            index = AuthenticateSmartContract.binary_search(case_dict, case_number)
            case_dict.insert(index, new_case)
            #print('New case added:', case_number, 'with stage:', stage)
            result= 'Case added'
        # Write the updated data back to the JSON file
        with open('case.json', 'w') as file:
            json.dump(case_dict, file)
        return result
# Example usage:
    def storage_comunication(self,transaction_dict,block_number):
        ##print('####',transaction_dict)
        #transaction_values = ','.join(str(value) for value in transaction_dict.values())
       # timestamp = int(time.time())

        security = Securitystorage()
        public_key, private_key = security.retrieve_keys_from_file()
        ##print(transaction_values)
        storage_message = security.enc(str(transaction_dict) + ', block_number:' + str(block_number), public_key)
        
        ##print(security.dec(storage_message,private_key))
        storage = Storage()
        storage.initial_upload(storage_message)

    def client_comunication(self,public_key,case_number,action):

        security = Security()
        storage_message = security.enc('case number: '+str(case_number) + ' result: ' + str(action), public_key)
        client = Client()
        client.receive(storage_message)



    #def retrieve_access_info(self, public_key, case_number, req_info):
 

    def retrieve_access_info(self, transaction,block_number):
    # Read the role information from the JSON file
        with open('case.json', 'r') as file:
            data = json.load(file)

        stage = None
        for item in data:
           if isinstance(item, dict) and 'case_number' in item and item['case_number'] == int(transaction['case_number']):

                        stage = item['current_stage']
                        break
                        #print("stage is :", stage)
                      
        if stage is None or stage != transaction['current_stage']:
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],'the stage is not valid')
            result='the stage is not valid'
            transaction['SC_Authenticate_output']= result
            self.storage_comunication(transaction,block_number)
            
            
            return  result
            
        with open('role_file.json', 'r') as file:
            data = json.load(file)

        public_key_role = None
        
        # Search for the sender's public key in the data list
        for item in data:
            if isinstance(item, dict) and 'key' in item and item['key'] == transaction['sender_public_key']:
                public_key_role = item['role']
                #print("SENDER IS THERE")
                break

        if public_key_role is None:
            #print("NO SUCH PUBLIC KEY")
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],'You are not authurized')
            self.storage_comunication(transaction,block_number)
            transaction['SC_Authenticate_output']='Denied Access'
            result='Denied Access'
            return  result
        
        # Read the access information from the file
        with open('access_info_file.json', 'r') as file:
            data = json.load(file)

        public_key_rights=None
        flag=0
        for item in data:
            
            if isinstance(item, dict) and 'stage' in item and item['stage'] == transaction['current_stage']:
                   # print(item['role'])
                    flag=1
                    print(public_key_role)
                    if 'role' in item and item['role'] == public_key_role:
                        #print("role")
                        public_key_rights = item['rights']
                        if public_key_rights== transaction['req_info']:
                            #print("The access is accepted and can", public_key_rights)
                           
                            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],public_key_rights)
                            transaction['SC_Authenticate_output']='Accepted'
                            self.storage_comunication(transaction,block_number)
                          
                            result='Accepted'
                            return  result
                            break
                        
          
                        else:
                            #print("The access is not accepted and she can only", public_key_rights)
                            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],'your access is denied')
                            transaction['SC_Authenticate_output']={ 'message': 'access is denied','public_key_rights': public_key_rights}
                            self.storage_comunication(transaction,block_number)

                            result={ 'message': 'access is denied','public_key_rights': public_key_rights}
                            return  result
                            break
        if flag==0:
        
            self.client_comunication(transaction['sender_public_key'],transaction['case_number'],'your access is denied')

            print("no such stage")
            transaction['SC_Authenticate_output']={ 'message': 'no such stage','public_key_rights': public_key_rights}
            self.storage_comunication(transaction,block_number)

            result={ 'message': 'no such stage','public_key_rights': public_key_rights}
            return  result
        
        if public_key_rights is None:
            #print("NO right at all")
            #midu a trasnaction
            result={ 'message': 'access is denied','public_key_rights':"none"}
            transaction['SC_Authenticate_output']=result
            self.storage_comunication(transaction,block_number)
            
            return result
            
          
'''
        # Find the access rights for the public key's role in the specified stage
        stage = self.case_dict.get(transaction['case_number'])
        if stage is not None:
            for line in access_info:
                stage_name, roles_access_rights = line.strip().split(',')
                if stage_name == stage:
                    for role_access_rights in roles_access_rights.split(';'):
                        role, access_rights = role_access_rights.split(':')
                        if role == public_key_role:
                            if transaction['req_info'] == access_rights:
                                return public_key_role,transaction['sender_public_key'], access_rights, True
                            else:
                                return public_key_role, transaction['sender_public_key'], access_rights, False

        # If the public key's role or access rights are not found, return None
        return None
        '''
#transaction={'transaction_name': 'create_access_transaction', 'sender_public_key': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoKvrXgr8oEiRhI3yKZBz\ns+RTR5mWurATs3qGByO4EN04QV5S6Mui1YMLJtnHBunby28DXHwcaGgajs3huFf6\naeHdPb7pJwImOl1hXeSwxr7yadkYpTNxdWuxL81acGG//xG1/LWvM1EDkFZ5Tz2u\nzREBkrpGOGEnQTqv3aIioDqLm6x1+vy7Aj1tsol6IzrfxnIdthj2bACsIc5rqU4x\nWWnzInR2WHBDHflgq3qx3TZHo341WxsfhM8iheJhViYQnqqah+zFe12gsIF1aGxp\nrbKBjeJUufqoVc+r9ZNkQYBRx/GC4odFrikJoL8qKSNZ1fPr2ynjAXcDFiXefWuC\ncwIDAQAB\n-----END PUBLIC KEY-----', 'token': 'token', 'case_number': '123', 'req_info': 'req_info', 'signature': '307e887e7eb0db0e200a29b245077d1ca9b7265d9a31733135844be40b60953568511756adfef6224d89872a3a17946ff06dccc7779195d420d8d8fd1211d75bc9213142007d2121ece09a8851aa2fb998fdea43f492c03ca30e4ffab7835c40203478bbe3efac6e2f558137743a352452f7c9f04dec0a44388932f1fa9cc8943bf9fcc91ef9017fa21a84533143af56a1c5a43d06107c84d414491631531f587a286eebc49c97e6f5d79698f0feaad4e7879080a224b1b97c673c2db52e085661b0cb735ae76d7303d960f61584113aaca3a46500e4820c37a11dfac6c7ef6011f7a0bd7eb529e1d68e03f2aba5d27dd9e0485f575de9879ce1e830ae10b8f0'}
#AuthenticateSmartContract.retrieve_access_info(transaction)

class VerificationSmartContract:
    def __init__(self):
        self.case_dict = {} 


    def verify_storage(self, transaction, block_number):
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
       
        
          
           
    
    
    # Insert the case_data dictionary into case_times list
   
        case_number = int(transaction['case_number'])
        start_time = time.time()
        index = AuthenticateSmartContract.binary_search(case_dict, case_number)

        if index < len(case_dict) and case_dict[index]['case_number'] == case_number:
            merkle_root = case_dict[index]['last_merkle_root']
            transaction_sorter = Verification()
            storage_string = transaction_sorter.filter_and_sort_transactions(case_number)
            if merkle_root == storage_string:
                end_time = time.time()
                execution_time = end_time - start_time
                case_data = { case_number: execution_time}
                case_times.append(case_data)
                print("storage verifed")
                transaction['SC_Verification_output']='storage verifed'
                self.storage_comunication(transaction,block_number)
                result='storage verifed'
                with open('time-ver.json', 'w') as file:
                   json.dump(case_times, file)
                return( result)
            
            else:
                end_time = time.time()
                execution_time = end_time - start_time
                case_data = { case_number: execution_time}
                case_times.append(case_data)
                print("storage not verifed")
                transaction['SC_Verification_output']='storage not verifed'
                self.storage_comunication(transaction,block_number)
                result='storage not verifed'
                with open('time-ver.json', 'w') as file:
                   json.dump(case_times, file)
                return( result)
        else:
            #print("No such case")
            transaction['SC_Verification_output']='No such case'
            end_time = time.time()
            execution_time = end_time - start_time
            case_data = { case_number: execution_time}
            case_times.append(case_data)
            self.storage_comunication(transaction,block_number)
            result='No such case'
            with open('time-ver.json', 'w') as file:
                   json.dump(case_times, file)
            return( result)

    def storage_comunication(self,transaction_dict,block_number):
            ##print('####',transaction_dict)
            #transaction_values = ','.join(str(value) for value in transaction_dict.values())
        # timestamp = int(time.time())

            security = Securitystorage()
            public_key, private_key = security.retrieve_keys_from_file()
            ##print(transaction_values)
            storage_message = security.enc(str(transaction_dict) + ', block_number:' + str(block_number), public_key)
            
            ##print(security.dec(storage_message,private_key))
            storage = Storage()
            storage.initial_upload(storage_message)

    def client_comunication(self,public_key,case_number,action):

            security = Security()
            storage_message = security.enc('case number: '+str(case_number) + ' result: ' + str(action), public_key)
            client = Client()
            client.receive(storage_message)
