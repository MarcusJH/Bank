""" DB
This module implements an interface to the bank_server database.
"""

import json
import os.path


class DB(object):
    """Implements a Database interface for the bank server and admin interface"""
    def __init__(self, db_path="example_db.json"):
        self.path = db_path

    def close(self):
        """close the database connection"""
        pass

    def init_db(self):
        """initialize database with file at filepath"""
        with open(self.path, 'w') as f:
            f.write(json.dumps({'atms': {}, 'cards': {}}))

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

     ##########################
    # BANK INTERFACE FUNCTIONS #
     ##########################

    def set_balance(self, card_id, balance):
        """set balance of account: card_id
        Returns:
            (bool): Returns True on Success. False otherwise.
        """
        return self.modify("cards", card_id, ["bal"], [balance])

    def get_balance(self, card_id):
        """get balance of account: card_id
        Returns:
            (string or None): Returns balance on Success. None otherwise.
        """
        return self.read("cards", card_id, "bal")

    def get_atm(self, atm_id):
        """get atm_id of atm: atm_id
        this is an obviously dumb function but maybe it can be expanded...
        Returns:
            (string or None): Returns atm_id on Success. None otherwise.
        """
        if self.get_atm_num_bills(atm_id):
            return atm_id
        return None

    def get_atm_num_bills(self, atm_id):
        """get number of bills in atm: atm_id
        Returns:
            (string or None): Returns num_bills on Success. None otherwise.
        """
        return self.read("atms", atm_id, "nbills")

    def set_atm_num_bills(self, atm_id, num_bills):
        """set number of bills in atm: atm_id
        Returns:
            (bool): Returns True on Success. False otherwise.
        """
        return self.modify("atms", atm_id, ["nbills"], [num_bills])

    #############################
    # ADMIN INTERFACE FUNCTIONS #
    #############################

    def admin_create_account(self, card_id, amount, code):
        """create account with account_name, card_id, and amount
        Returns:
            (bool): Returns True on Success. False otherwise.
        """
        return self.modify('cards', card_id, ["bal"], [amount])
        return self.modify('cards', card_id,["tamper codes"], [code])

    def admin_create_atm(self, atm_id):
        """create atm with atm_id
        Returns:
            (bool): Returns True on Success. False otherwise.
        """
        return self.modify("atms", atm_id, ["nbills"], [128])

    def admin_get_balance(self, card_id):
        """get balance of account: card_id
        Returns:
            (string or None): Returns balance on Success. None otherwise.
        """
        return self.read("cards", card_id, "bal")

    def admin_set_balance(self, card_id, balance):
        """set balance of account: card_id
        Returns:
            (bool): Returns True on Success. False otherwise.
        """
        return self.modify("cards", card_id, ["bal"], [balance])
    
    def admin_get_tamper(self, card_id):
        """get tamper code of account: card_id
        Returns:
            (string or None): Returns balance on Success. None otherwise.
        """
        return self.read("cards", card_id, "tamper code")

    def admin_set_tamper(self, card_id, code):
        """set tamper code of account: card_id
        Returns:
            (bool): Returns True on Success. False otherwise.
        """
        return self.modify("cards", card_id, ["tamper code"], [code])

'''THE SECTION UNDER THIS COMMENT IMPLEMENTS THE CODE ABOVE'''

# THIS CREATES AN ACCOUNT, SETS THE BALANCE 
accounts = DB(db_path="Bank_Server_Database.json")
print accounts.init_db()
print accounts.admin_create_account("111111111111111", "625", "3333333333333333" )
print accounts.set_balance("111111111111111", "1025")
print accounts.admin_set_tamper("111111111111111", "3333333333333333")
print accounts.admin_get_balance("111111111111111")
print accounts.admin_get_tamper("111111111111111")