import hashlib
import time
import json


class Block:
    def __init__(self, index, previous_hash, timestamp, merkle_root, transactions,merkle_roots_by_case ):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.transactions = transactions
        self.merkle_roots_by_case=merkle_roots_by_case 
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.merkle_root)+str(self.merkle_roots_by_case) + str(json.dumps(self.transactions, sort_keys=True))
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'transactions': self.transactions,
            'merkle_roots_by_case':self.merkle_roots_by_case 
        }