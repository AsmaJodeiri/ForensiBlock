import json
import os
import unittest
import rsa
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15 
from Cryptodome.Hash import SHA256
import json
import hashlib



class TransactionProcessor:
    def __init__(self, sender_public_key, sender_private_key):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key

    def sign_transaction(self, transaction_data):
        key = RSA.import_key(self.sender_private_key)
        h = SHA256.new(json.dumps(transaction_data, sort_keys=True).encode())
        signature = pkcs1_15.new(key).sign(h)
        return signature.hex()

    def add_transactions(self, transaction_list):
        transactions = {}
        for i, transaction in enumerate(transaction_list):
            transaction_name = transaction['transaction_name']
            transaction_args = transaction['args']
            transaction_method = getattr(self, transaction_name.lower() + '_transaction')
            transaction_dict = transaction_method(*transaction_args)

            signature = self.sign_transaction(transaction_dict)
            transaction_dict['signature'] = signature

            # Create a unique key for each transaction using the transaction name and its index
            transaction_key = f"{transaction_name}_{i}"
            transactions[transaction_key] = transaction_dict

        return transactions


    def initial_upload_transaction(self, case_number,current_stage):
        return {
            'transaction_name': 'initial_upload_transaction',
            'case_number': case_number,
            'current_stage': current_stage,
            'sender_public_key': self.sender_public_key
            
        }
    def read_transaction(self, case_number):
        return {
            'transaction_name': 'read_transaction',
            'case_number': case_number,
            'sender_public_key': self.sender_public_key
            
        }
    def write_transaction(self, case_number):
        return {
            'transaction_name': 'write_transaction',
            'case_number': case_number,
            'sender_public_key': self.sender_public_key
            
        }
    def verification_transaction(self, case_number):
        return {
            'transaction_name': 'verification_transaction',
            'case_number': case_number,
            'sender_public_key': self.sender_public_key
            
        }

    def file_upload_transaction(self, case_number, hash_of_data):
        return {
            'transaction_name': 'file_upload_transaction',
            'case_number': case_number,
            'hash_of_data': hash_of_data,
            'sender_public_key': self.sender_public_key
        }

    def create_token_transaction(self, new_token, case_number, hash_of_data, base_tokens):
        return {
            'transaction_name': 'create_token_transaction',
            'case_number': case_number,
            'new_token': new_token,
            'base_tokens': base_tokens,
            'hash_of_data': hash_of_data,
            'sender_public_key': self.sender_public_key
        }

    def create_storage_transaction(self, new_token, case_number, hash_of_data):
        return {
            'transaction_name': 'create_storage_transaction',
            'case_number': case_number,
            'new_token': new_token,
            'hash_of_data': hash_of_data,
            'sender_public_key': self.sender_public_key
        }

    def create_access_transaction(self, token,current_stage, case_number, req_info):
        return {
            'transaction_name': 'create_access_transaction',
            'case_number': case_number,
            'token': token,
            'req_info': req_info,
            'current_stage': current_stage,
            'sender_public_key': self.sender_public_key
        }

    def create_analysis_transaction(self, actions, hash_of_data, case_number, base_tokens):
        return {
            'transaction_name': 'create_analysis_transaction',
            'case_number': case_number,
            'base_tokens': base_tokens,
            'actions': actions,
            'hash_of_data': hash_of_data,
            'sender_public_key': self.sender_public_key
        }

    def stage_change_transaction(self,case_number,stage):
        return {
            'transaction_name': 'stage_change_transaction',
            'case_number': case_number,
            'current_stage': stage,
            'sender_public_key': self.sender_public_key
            
        }