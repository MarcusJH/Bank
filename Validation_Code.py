#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 10:51:33 2018

@author: yasminecalvo
"""

'''THIS IS THE BEGINING IF THE ATM-Bank Interaction CODE'''

import random
import string 
import json
import os
import os.path
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
#import struct
from ID_Key_Database import *
#import ID_Key_Database.json
from Bank_Server_Code import *




'''ignore this stuff it's for debugging purposes (it imitates the ATM's package)'''




#THIS WOULD HAVE BEEN TAKEN FROM THE ID-KEY DATABASE
transaction_AES_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])

IV = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])

obj = AES.new(transaction_AES_key, AES.MODE_CBC, IV)


ATM_Package_Encrypted= obj.encrypt("11111111111111112222222222222222333333333333333344444444444444455555555555555555")

ATM_Package_Hashed = SHA256.new("11111111111111112222222222222222333333333333333344444444444444455555555555555555").hexdigest()



print ATM_Package_Encrypted.encode("hex")


'''The Code Starts Here'''



#DECRYPT PACKAGE FROM ATM USING THE AES KEY and assigns the info to variables


#gets the key,
#transaction_AES_key = transactions.get_key(transaction_id)

obj2 = AES.new(transaction_AES_key, AES.MODE_CBC, IV)


ATM_Package_Decrypted = obj2.decrypt(ATM_Package_Encrypted)

print ATM_Package_Decrypted

CCN_Decrypted= ATM_Package_Decrypted[0:15]

Balance_Value_Decrypted = ATM_Package_Decrypted[16:31]

Tamper_Code_Decrypted = ATM_Package_Decrypted[32:48]

Pin_Decrypted  = ATM_Package_Decrypted[49:64]

ATM_id_Decrypted = ATM_Package_Decrypted[65:80]

#Hash the Decrypted ATM package

ATM_Package_Decrypted_Hashed = SHA256.new(ATM_Package_Decrypted).hexdigest()

#Compare the newly hashed package and package hashed by the ATM


#Compare the newly-hashed package to the hashed package that the ATM sent
if ATM_Package_Decrypted_Hashed == ATM_Package_Hashed:
    print("yes")
    
    #Get the balance and tamper code from the Bank_Sever database
    Balance_Value_Bank = accounts.admin_get_balance(CCN_Decrypted)
    Tamper_Code_Bank = accounts.admin_get_tamper(CCN_Decrypted)
    print ("Balance:", Balance_Value_Bank)
    print ("TamperCode:" ,Tamper_Code_Bank)
    
    #Decrypt the Balance with the hashed Tamper Code from the bank as an AES key
    Tamper_Code_Hashed_ATM= ATM_Package_Hashed[32:48]
    obj3 = AES.new(Tamper_Code_Hashed_ATM, AES.MODE_CBC, IV)
    Balance_Value_Bank_Decrypted = obj3.decrypt( Balance_Value_Bank)
    print Balance_Value_Bank_Decrypted 
    
    
    
else:
    print("no")

































