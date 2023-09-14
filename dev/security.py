
import json
import os
import rsa
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import base64
import user_index
''''
class Security:
    def __init__(self):
        self.load_users()

    def load_users(self):
        if os.path.exists("users.json"):
            # Load existing users from users.json
            with open("users.json", "r") as file:
                self.users = json.load(file)
        else:
            # Create an empty users file if users.json doesn't exist
            self.users = []

    def generate_key_pair(self, user_index):
        # Generate a new RSA key pair for the user
        key = RSA.generate(1024)

        # Save the public and private keys to the users list
        self.users.append({
            'index': user_index,
            'public_key': key.publickey().export_key().decode(),
            'private_key': key.export_key().decode()
        })

        # Save the users list to users.json
        with open("users.json", "w") as file:
            json.dump(self.users, file, indent=4)

        # Return the generated key pair
        return key.publickey().export_key().decode(), key.export_key().decode()

    def save_keys_to_file(self, public_key, private_key):
            keys = {}

            # Check if the keys file already exists
            if os.path.exists('keys.json'):
                # Load existing keys from keys.json
                with open('keys.json', 'r') as file:
                    keys = json.load(file)

            # Update the keys dictionary with the new keys
            keys={
                "public_key": public_key,
                "private_key": private_key
            }

            # Save the updated keys dictionary to keys.json
            with open('keys.json', 'w') as file:
                json.dump(keys, file, indent=4)


    def retrieve_keys_from_file(self):
        try:
            with open('keys.json', 'r') as file:
                keys = json.load(file)
                return keys.get('public_key'), keys.get('private_key')
        except FileNotFoundError:
            return None, None

    def enc(self, message, recipient_public_key):
        recipient_key = RSA.import_key(recipient_public_key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        ciphertext = cipher_rsa.encrypt(message.encode())
        return ciphertext

    def dec(self, ciphertext, private_key):
        private_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        message = cipher_rsa.decrypt(ciphertext).decode()
        return message
'''
import json
import os
import rsa
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


class Security:
    def __init__(self):
        self.load_users()

    def load_users(self):
        if os.path.exists("users.json"):
            # Load existing users from users.json
            with open("users.json", "r") as file:
                self.users = json.load(file)
        else:
            # Create an empty users file if users.json doesn't exist
            self.users = []

    def generate_key_pair(self, user_index):
        # Generate a new RSA key pair for the user
        key = RSA.generate(4096)

        # Save the public and private keys to the users list
        self.users.append({
            'index': user_index,
            'public_key': key.publickey().export_key().decode(),
            'private_key': key.export_key().decode()
        })

        # Save the users list to users.json
        with open("users.json", "w") as file:
            json.dump(self.users, file, indent=4)

        # Return the generated key pair
        return key.publickey().export_key().decode(), key.export_key().decode()

    def save_keys_to_file(self, public_key, private_key):
        keys = {}

        # Check if the keys file already exists
        if os.path.exists('keys.json'):
            # Load existing keys from keys-storage.json
            with open('keys.json', 'r') as file:
                keys = json.load(file)

        # Update the keys dictionary with the new keys
        keys = {
            "public_key": public_key,
            "private_key": private_key
        }

        # Save the updated keys dictionary to keys-storage.json
        with open('keys.json', 'w') as file:
            json.dump(keys, file, indent=4)

    def retrieve_keys_from_file(self):
        try:
            
            with open('keys.json', 'r') as file:
                keys = json.load(file)
                for key_data in keys:
                    if key_data['user_index'] == user_index.user_index:
                        return key_data['public_key'], key_data['private_key']
        except FileNotFoundError:
            return None, None

    def enc(self, message, recipient_public_key):
        recipient_key = RSA.import_key(recipient_public_key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)

        chunk_size = 190  # Adjust chunk size based on key size
        chunks = [message[i : i + chunk_size] for i in range(0, len(message), chunk_size)]

        encrypted_chunks = []
        for chunk in chunks:
            ciphertext = cipher_rsa.encrypt(chunk.encode())
            encrypted_chunks.append(ciphertext)

        return encrypted_chunks

    def dec(self, encrypted_chunks, private_key):
        private_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key)

        decrypted_chunks = []
        for chunk in encrypted_chunks:
            decrypted_chunk = cipher_rsa.decrypt(chunk).decode()
            decrypted_chunks.append(decrypted_chunk)

        return "".join(decrypted_chunks)



#security = Security()
#public_key, private_key = security.generate_key_pair(452)
#security.save_keys_to_file(public_key, private_key)
##print(public_key)
# Generate or retrieve keys
#public_key, private_key = security.retrieve_keys_from_file()

# Encrypt and decrypt a message
#message = transaction
# Encrypt and decrypt a message
#message = json.dumps(transaction)
#encrypted_message = security.enc(message, public_key)
#decrypted_message = security.dec(encrypted_message, private_key)
#decrypted_message = json.loads(decrypted_message)

#encrypted_message = security.enc(message, public_key)
#decrypted_message = security.dec(encrypted_message, private_key)
##print(encrypted_message)
##print(decrypted_message)

# Example usage:
#security = Security()
#public_key, private_key = security.generate_key_pair(452)
#security.save_keys_to_file(public_key, private_key)
##print(public_key)
# Generate or retrieve keys
#public_key, private_key = security.retrieve_keys_from_file()

# Encrypt and decrypt a message
#message = "Hello, world!"
#encrypted_message = security.enc(message, public_key)
#decrypted_message = security.dec(encrypted_message, private_key)

##print("Original message:", message)
##print("Encrypted message:", encrypted_message)
##print("Decrypted message:", decrypted_message)

