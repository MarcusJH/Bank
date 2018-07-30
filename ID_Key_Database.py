"""THIS IS THE CODE FOR THE TRANSACTION_ID - AES_KEY DATABASE (NOT TO BE CONFUSED WITH THE BANK-SERVER 
DATABASE (STORES THE CARD NUMBER AND BALANCE)
"""

import json
import os
import os.path
import random
import string
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import struct


# don't forget!!!! using AES mode CTR

#These are the functions for the ID-Key database
class DB(object):
    def __init__(self, db_path="transactions.json"):
        self.path = db_path

    def close(self):
        """close the database connection"""
        pass

    def init_db(self):
        """initialize database with file at filepath"""
        with open(self.path, 'w') as f:
            f.write(json.dumps({'Transaction ID': {}}))

    def exists(self):
        return os.path.exists(self.path)

    def modify(self, table, k, subks, vs):
        with open(self.path, 'r') as f:
            db = json.loads(f.read())

        try:
            for subk, v in zip(subks, vs):
                if k not in db[table]:
                    db[table][k] = {}
                db[table][k][subk] = v
        except KeyboardInterrupt:
            return False

        with open(self.path, 'w') as f:
            f.write(json.dumps(db))

        return True

    def read(self, table, k, subk):
        with open(self.path, 'r') as f:
            db = json.loads(f.read())

        try:
            return db[table][k][subk]
        except KeyError:
            return None

    def new_transaction(self, trans_id, trans_key):
        return self.modify("Transaction ID", trans_id, ["Transaction AES key"], [trans_key])

    def get_key(self, trans_id):
        return self.read("Transaction ID", trans_id, "Transaction AES key")


'''THE SECTION UNDER THIS COMMENT IMPLEMENTS THE CODE ABOVE'''


random_generator = Random.new().read

#Generate transaction_id and transaction AES key
transaction_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
transaction_AES_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(128)])


#Hash transaction_id and transaction AES key

transaction_id = SHA256.new(transaction_id).hexdigest()
transaction_AES_key = SHA256.new(transaction_AES_key).hexdigest()


#Store the transaction id and transaction AES key(both hashed) to memory

transactions = DB(db_path="ID-Key_Database.json")
transactions.init_db()
transactions.new_transaction(transaction_id, transaction_AES_key)



# Creating(Encryting and Hashing) a package to send to the ATM

''' this might be easier to recieve as an array 
bank_package_1 = [transaction_id, transaction_AES_key]
bank_package_1_encrypted = [ATM_public_key.encrypt(bank_package_1), ATM_public_key.encrypt(ATM_public_key)]
bank_package_1_hashed = SHA256.new(bank_package_1).hexdigest()
'''
bank_package_1 = transaction_id + ", " + transaction_AES_key
bank_package_1 = struct.pack(">32s128s", transaction_id, transaction_AES_key)
#bank_package_1_encrypted = ATM_public_key.encrypt(bank_package_1, ATM_public_key)
bank_package_1_hashed = SHA256.new(bank_package_1).hexdigest()



# Printing the transaction id and AES key
print transaction_id
print transaction_AES_key


 #Implement the get_key function
print transactions.get_key(transaction_id)

#This prints the bank package encrypted and hashed
#print bank_package_1_encrypted
#print bank_package_1_hashed












