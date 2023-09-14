import json
from merkle_tools import MerkleTools

class Verification:
    def __init__(self):
        self.file_path = "storage.json"

    def filter_and_sort_transactions(self, case_number):
        with open(self.file_path) as f:
            data = json.load(f)

        filtered_transactions = [
            transaction for transaction_list in data
            if isinstance(transaction_list, list)
            for transaction in transaction_list
            if isinstance(transaction, dict) and transaction.get("case_number") == case_number
        ]

        sorted_transactions = sorted(filtered_transactions, key=lambda t: int(t.get("block_number", 0)))

        merkle_root = None

        current_block_number = None
        block_transaction_strings = []

        for transaction in sorted_transactions:
            block_number = transaction.get("block_number")
            if block_number != current_block_number:
                # New block number, generate Merkle root for the previous block
                if current_block_number is not None:
                    block_root = self.merkle_generation_per_case_verification(block_transaction_strings)
                    if merkle_root is None:
                        merkle_root = block_root
                    else:
                        merkle_root = self.combine_merkle_roots(merkle_root, block_root)
                
                # Reset for the new block
                current_block_number = block_number
                block_transaction_strings = []

            block_transaction_strings.append(self.serialize_transaction(transaction))

        # Generate Merkle root for the last block
        if current_block_number is not None:
            block_root = self.merkle_generation_per_case_verification(block_transaction_strings)
            if merkle_root is None:
                merkle_root = block_root
            else:
                merkle_root = self.combine_merkle_roots(merkle_root, block_root)

        return merkle_root,filtered_transactions

    def merkle_generation_per_case_verification(self, sorted_transactions):
        merkle_tools = MerkleTools()
        for transaction in sorted_transactions:
            merkle_tools.add_leaf(transaction, do_hash=True)
        merkle_tools.make_tree()
        merkle_root = merkle_tools.get_merkle_root()
        return merkle_root

    def combine_merkle_roots(self, merkle_root1, merkle_root2):
        merkle_tools = MerkleTools()
        merkle_tools.add_leaf(merkle_root1, do_hash=True)
        merkle_tools.add_leaf(merkle_root2, do_hash=True)
        merkle_tools.make_tree()
        combined_merkle_root = merkle_tools.get_merkle_root()
        return combined_merkle_root

    def serialize_transaction(self, transaction):
        transaction_copy = transaction.copy()
        transaction_copy.pop("block_number", None)
        transaction_copy.pop("end", None)
        return str(transaction_copy)









transaction_sorter = Verification()
sorted_transactions = transaction_sorter.filter_and_sort_transactions(123)
#print(sorted_transactions)
