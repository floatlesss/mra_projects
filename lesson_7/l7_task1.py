# TODO: Project is done, with all extensions complete.

# 'accountNumber' and 'ID' are used interchangeably.

import os
import time
import random

os_name = os.name

def clear_cl():
    os.system("cls" if os_name == "nt" else "clear")


class NegativeValueError(ValueError):
    """A negative value has been given when it is not permitted."""
    def __init__(self, message=None):
        super().__init__(message)
class InsufccicientFundsError(Exception):
    """The account does not have sufficient funds to perform this operation."""
    def __init__(self, message=None):
        super().__init__(message)

class Bank:
    __accounts_dict = {}

    def create_account(self, name, balance):
        id = None

        def generate_id():
            id = ''.join(str(random.randint(0, 9)) for _ in range(8))
            return id
        
        id = generate_id()
        while id in self.__accounts_dict:
            id = generate_id()

        bank_account = BankAccount(id, name, balance)
        self.__accounts_dict[id] = bank_account

        return bank_account
    
    def get_accounts(self):
        return self.__accounts_dict

class BankAccount:
    def __init__(self, accountNumber: str, ownerName: str, balance: int):
        self.__accountNumber = accountNumber
        self.__ownerName = ownerName
        self.__balance = balance

    def get_info(self):
        return {"id": self.__accountNumber,
                "name": self.__ownerName
            }

    def get_balance(self):
        return self.__balance

    def deposit(self, amount: int):
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        self.__balance += amount

    def withdraw(self, amount: int):
        if self.__balance - amount < 0:
            raise InsufccicientFundsError
        elif amount < 0:
            raise NegativeValueError("User attempted to withdraw a negative value")
        self.__balance -= amount



def show_balance(account):
    info = account.get_info()

    print(f"LOGGED IN / NAME: {info["name"]} | ID: {info["id"]} / BALANCE\n")
    print(f"    BALANCE: {account.get_balance()}")

    input("\n    Press enter to return to your accountscreen.")
    accountscreen(account)

def deposit_funds(account):
    info = account.get_info()

    while True:
        print(f"LOGGED IN / NAME: {info["name"]} | ID: {info["id"]} / DEPOSIT")
        print("You can enter \'!exit\' at any time to return to your accounscreen.\n")

        try:
            deposit_value = input("    How much would you like to deposit?: ")
            if deposit_value == "!exit":
                accountscreen(account)
            else:
                deposit_value = int(deposit_value)
                account.deposit(deposit_value)
        except ValueError:
            print("    ERROR: Please enter a valid value.")
            time.sleep(1.3)
            clear_cl()
        else:
            print(f"\n    Done.\n    You now have {account.get_balance()} funds in your account.")
            input("\n    Press enter to return to your account's menu.")
            accountscreen(account)

def withdraw_funds(account):
    info = account.get_info()

    while True:
        print(f"LOGGED IN / NAME: {info["name"]} | ID: {info["id"]} / WITHDRAW")
        print("You can enter \'!exit\' at any time to return to your accounscreen.\n")

        try:
            withdraw_value = input("    How much would you like to withdraw?: ")
            if withdraw_value == "!exit":
                accountscreen(account)
            else:
                withdraw_value = int(withdraw_value)
                account.withdraw(withdraw_value)
        except InsufccicientFundsError:
            print(f"    ERROR: You do not have enough funds ({account.get_balance()} funds) in your account to perform this operation.")
            input("    \n    Press enter to return to your account's menu.")
            accountscreen(account)
        except NegativeValueError:
            print("    ERROR: You cannot withdraw a negative value")
        else:
            print(f"\n    Done.\n    You now have {account.get_balance()} funds in your account.")
            input("    \n    Press enter to return your account's menu.")
            accountscreen(account)

def transfer(account):
    info = account.get_info()

    exited = False
    while not exited:
        print(f"LOGGED IN / NAME: {info["name"]} | ID: {info["id"]} / TRANSFER")
        print("You can enter \'!exit\' at any time to return to your accounscreen.\n")

        def check_account_exists(id, name):
            try:
                dest_bank_account = bank.get_accounts()[id]
            except KeyError:
                return False
            else:
                if bank.get_accounts()[id].get_info()["name"] == name:
                    return dest_bank_account
                else:
                    return False

        def transfer(dest_account: object, amount: int):
            account.withdraw(amount)
            dest_account.deposit(amount)


        # not verifying if id exists now, only do it when user enters the account's name
        # for security purposes. (account ids are usually semi-private)
        dest_account_id = input("    To what account ID would you like to transfer to?: ")
        if dest_account_id == "!exit":
            break
        elif dest_account_id == info["id"]:
            print("    You cannot transfer to your own account.")
            time.sleep(1.5)
            clear_cl()
            continue
        else:
            try:
                dest_account_id = int(dest_account_id)
                dest_account_id = str(dest_account_id)
            except ValueError:
                print("    Please enter a numerical ID. e.g: \'12345678\'")
                time.sleep(2)
                clear_cl()
                continue
        dest_account_name = input("    What is the name associated with this account?: ")
        if dest_account_name == "!exit":
            break

        dest_bank_account = check_account_exists(dest_account_id, dest_account_name)
        if dest_bank_account != False:
            while True:
                transfer_amount = input(f"\n    How much would you like to transfer to account ID {dest_account_id}?: ")
                if transfer_amount == "!exit":
                    exited = True
                    break
                else:
                    try:
                        transfer_amount = int(transfer_amount)
                    except ValueError:
                        print("    Please enter a positive numerical value.")
                    else:
                        if transfer_amount < 0:
                            print("    Please enter a positive numerical value.")
                        else:
                            # this is the final battle
                            try:
                                transfer(dest_bank_account, transfer_amount)
                            except InsufccicientFundsError:
                                print(f"\n    You do not have enough to transfer {str(transfer_amount)} funds.")
                                input("    Press enter to return to your accountscreen.")
                                accountscreen(account)
                            else:
                                print("\n    Done!")
                                time.sleep(2)
                                clear_cl()

                                print(f"LOGGED IN / NAME: {info["name"]} | ID: {info["id"]} / TRANSFER / SUCCESS\n")
                                print("    TRANSFER INFO:")
                                print(f"        Amount transferred: {str(transfer_amount)}")
                                print(f"        Your account's balance after transfer: {str(account.get_balance())}")
                                print(f"\n    ->  Source account's info:\n            ID: {info["id"]}\n            NAME: {info["name"]}")
                                print(f"    <-  Destination account's info:\n            ID: {dest_account_id}\n            NAME: {dest_account_name}")
                                input("\n\n    Press enter to return to your account's accountscreen.")
                                accountscreen(account)
        else:
            print("\n    This bank account doesn't exist. try again.")
            time.sleep(2)
            
            clear_cl()

    accountscreen(account)
    # maybe it's time to go to sleep. 10:54, 15/03/2025

def logout():
    clear_cl()
    print("LOGGED OUT\n")
    print("You have been logged out.")

    time.sleep(1.5)
    home_page()








def accountscreen(bank_account):
    clear_cl()
    info = bank_account.get_info()

    bank_account_id = info["id"]
    bank_account_name = info["name"]

    options = {
        "balance": lambda: show_balance(bank_account),
        "deposit": lambda: deposit_funds(bank_account),
        "withdraw": lambda: withdraw_funds(bank_account),
        "transfer": lambda: transfer(bank_account),
        "bye": lambda: logout()
    }

    choice = input(f"""LOGGED IN / NAME: {bank_account_name} | ID: {bank_account_id} /
                   
Welcome to the text prompt interface for the bank.
What would you like to do?

Type in one of the following, and then press enter. (e.g \"balance\")
    balance: Read your current balance
    deposit: Deposit a value into the account
    withdraw: Withdraw a value from the account
    transfer: Transfer an amount of your funds into another account

    bye: Logout


""")
    choice = choice.lower()
    clear_cl()

    action = options.get(choice)
    if action:
        action()
    else:
        print(f"LOGGED IN / NAME: {bank_account_name} | ID: {bank_account_id} /\n")
        print("INVALID ACTION.\nPlease try again.")

        time.sleep(1)
        accountscreen(bank_account)



def account_setup(first_run=False):
    clear_cl()

    print("BANK ACCOUNT SETUP\n\nLet's create a bank account.")
    if not first_run:
        print("You can enter \'!exit\' now to return to the home page.\n")

    username = input("    Enter your name: ")
    username = username.lower()

    if not first_run:
        if username == '!exit':
            home_page()

    print(f"\n    Welcome, {username[0].upper() + username[1:]}! Let's configure your bank account's starting balance.")
    while True:
        try:
            balance = int(input("    > "))
            if balance < 0:
                raise NegativeValueError
        except ValueError or NegativeValueError:
            print("    You can't enter anything other than a positive number.")
        else:
            break

    bank_account = bank.create_account(username, balance)

    print("\n\n    Nice! Everything went smoothly whilst creating your account.")
    print(f"\n    YOUR ID IS: {bank_account.get_info()["id"]} (REMEMBER THIS FOR LOGIN PURPOSES)")

    input(f"    Press enter to go to {username[0].upper() + username[1:]}'s accountscreen.")
    
    return bank_account


def home_page():
    def register():
        account = account_setup()
        accountscreen(account)

        home_page()

    def login():
        login_success = False

        while not login_success:
            clear_cl()

            print("LOGGING IN... /")
            print("You can enter \'!exit\' at any time to return to the home page.\n")

            print("LOGIN")

            id = input("    Please enter your account's id: ")
            if id == '!exit':
                break

            try:
                bank_account = bank.get_accounts()[id]
            except KeyError:
                print("    This account does not exist.")
                time.sleep(1.5)
            else:
                name = input("    What is the name for your account? (security question): ")
                if name == '!exit':
                    break
            
                if bank_account.get_info()["name"] == name:
                    clear_cl()
                    print("LOGGING IN SUCCESS /\n")
                    print("    Login successful. Redirecting you to your homepage!")
                    time.sleep(2)
                    login_success = True
                else:
                    print("\n    The name you entered does not match the one on record with this account.")
                    time.sleep(2)
            
        if login_success:
            accountscreen(bank_account)

    while True:
        clear_cl()
        print("LOGGED OUT / HOME PAGE\n")
        print("Welcome to the bank's login interface.\n")

        options = {
        "login": login,
        "register": register
        }

        choice = input("""Type in one of the following, and then press enter. (e.g \"login\")
    login: Login to an exisitng account, providing it's ID and connected name.
    register: Create a new account

""")
        choice = choice.lower()

        action = options.get(choice)
        if action:
            action()
        else:
            clear_cl()

            print("LOGGED OUT / HOME PAGE\n")
            print("INVALID ACTION.\nPlease try again.")
            time.sleep(1)



if __name__ == "__main__":
    bank = Bank()

    account = account_setup(True)
    accountscreen(account)
    while True:
        home_page()
        clear_cl()
