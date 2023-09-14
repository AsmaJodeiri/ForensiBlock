import json
import os
import rsa
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


class Securitystorage:
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
        if os.path.exists('keys-storage.json'):
            # Load existing keys from keys-storage.json
            with open('keys-storage.json', 'r') as file:
                keys = json.load(file)

        # Update the keys dictionary with the new keys
        keys = {
            "public_key": public_key,
            "private_key": private_key
        }

        # Save the updated keys dictionary to keys-storage.json
        with open('keys-storage.json', 'w') as file:
            json.dump(keys, file, indent=4)

    def retrieve_keys_from_file(self):
        try:
            with open('keys-storage.json', 'r') as file:
                keys = json.load(file)
                return keys.get('public_key'), keys.get('private_key')
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


transaction = {
    'transaction_name': 'initial_upload_transaction',
    'current_stage': 'current_stage',
    'sender_public_key': '-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwXjJ8QVhpmYneZ24i4+K\nAR+ZgzC2LLLwJqT/bGJwJbcj3NXHk1RzhKL4QQMQe9N9T30qp9Uko+QbWOSAF3nF\n1xoZ17OnuQBDCe1+0W9B/81HiGg62gEgr/uwBSxbYmY/1d7r0Ia7AEveuWsZXXkr\noQQfBj6RcqOSHv7iJ5ZGeEx+tHDYT0/LjR4Z4KvDXQwL44PECKrRe2rsIj575QVM\nyLjH4eu+QUS4ZY6lMSqSr+ZuO5PsEoy3RH9l9Taah+q2zjssD2HaAzabw47QfCnQ\nIyrc0kAoXOZ2b3G/9dHUWJiQtVCxHfiHRO1tXh5LwAYOALelYG5F6MNWIF6ByOGG\nAUBT8V9yFyBEBHWJeF5AhDvpG/kRNeSAfBSTj1e6OmqqRBlu660ZfFzmX3SAFwYx\n2/t3wJfvAjSmNrWH6Q6rInEPndJ30cZYkQsAM5EizWHv4yoX2nY9WAFnKAjzm+Jh\nQKu6XpHaRcgL1P1xf6eCvFFIxwn6lGg/1F1/uJzyJpplzbpOKh4PkSO9IwTMhGrn\nqpLIm38sCstm3f1NIZwpgVNfqSAWgiWE5TS+kF+AJsdazDrgGsX7fEn4DJYQlSSC\n5K7FM19VTROeFEes050OyR6K/i0/L2Y5t34bPkeVhaY68aaQN/mwpGlG/6z4gtEs\nxrJwurL1B7HNe8ei2BJ1G6kCAwEAAQ==\n-----END PUBLIC KEY-----',
    'case_number': '2',
    'signature': '8ba88ba8d0042ea77fed46cc1c7895c4646d0f6ceb58936a335ccb63ec2b6d9f319d3f1e5655336ed3706b822a86325573be4cefc393acdf8077f6ec4a8b2cd05ec2b13a1d5fbe13fe9026a53695f0a36d6ff9f1eda6272bded7025476923243d965784efe83374205d7c2f1c0bc7eee41711d6cb8c9039abcaacc7d9cfc9a3f447e6bf59352535500d74372e760c39b13305a7a8c0a1fb7eea908e9684a602270b45b88609a952979d589d9088632e718658323344558cc86cfd7ab117e5a978d8bb08c0ac63e3aa4b39b6165e5c21aa5a9f6d1159445de32fa2d6635fe340fbf66ebd64149109ca575b10512d846a4dbc30449149ba3cfb7ecd929374e038a23fc2e51ef35d6b08b5b517017a4739571502759568dd92dbb561aa79c79fa3c7402113dd0fb5d9204f34dbaacdbb7a04146f74523f6743197a092d2fbc779c38f8aef169be1324cd9fc3848685e273a1e4323f9374460f4a213de7059e1a8c05afc5eee26377a7b70d8e844abd359fa26d1947d11711500d9cf633a9e9117c992d1a1c4b37d9982d2cdfac82124b8f959747e03039db753dc7a29a8c677572e8c4a39755a1be952ce509b2501caf6bc9aba1645a38f14c271797082d596d8abcb8c7596ebdc024638d1c0392fc6a395e59e4b68faa8167c5dac7fdeeadc13614e2167632cfa0e5f7719c858a73b6d1a85bc3a3810837890f81814f55b3b21df'
}
#security = Securitystorage()
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