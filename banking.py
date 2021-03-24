import random
import math
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

conn.execute(''' CREATE TABLE IF NOT EXISTS card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER) ''')


def insert_card(id, number, pin, balance):
    cur.execute('''INSERT INTO card(id, number, pin, balance) VALUES(?,?,?,?)''', (id, number, pin, balance))

    conn.commit()


def check_card(card_number, pin="0"):
    cur.execute(''' SELECT number FROM card WHERE number=(?)''', [int(card_number)])
    x = cur.fetchall()

    cur.execute(''' SELECT pin FROM card WHERE pin=(?)''', [int(pin)])
    y = cur.fetchall()

    if pin == "0":
        if x != []:
            return True

    elif pin != "0":
        if x == [] or y == []:
            return False
        else:
            return True


def luhn_check(number):
    number_array = []
    number_array[:0] = number[:-1]
    number_array = [int(i) for i in number_array]
    for i in range(len(number_array)):
        if i % 2 == 0:
            number_array[i] *= 2
    for j in range(len(number_array)):
        if number_array[j] > 9:
            number_array[j] -= 9
    number_sum = sum(number_array)
    luhn_sum = (math.ceil(number_sum / 10) * 10) - number_sum
    if int(number[-1]) == luhn_sum:
        return True
    else:
        return False


option = -1
card_number = ""
pin = ""
id = 0
balance = 0
while option != 0:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    option = int(input())

    if option == 1:
        print("\nYour card has been created")
        print("Your card number:")
        random_card_number = random.randint(100000000, 999999999)
        card_number_array = []
        card_number_array[0:] = "400000" + str(random_card_number)
        card_number_array = [int(i) for i in card_number_array]
        for i in range(len(card_number_array)):
            if i % 2 == 0:
                card_number_array[i] *= 2
        for j in range(len(card_number_array)):
            if card_number_array[j] > 9:
                card_number_array[j] -= 9
        card_number_sum = sum(card_number_array)
        checksum = (math.ceil(card_number_sum / 10) * 10) - card_number_sum
        card_number = "400000" + str(random_card_number) + str(checksum)
        print(card_number)
        print("Your card PIN")
        pin = str(random.randint(1000, 9999))
        print(pin + "\n")
        id += 1
        insert_card(id, card_number, pin, balance)

    elif option == 2:
        print("\nEnter your card number:")
        card_number = input()
        print("Enter your PIN")
        pin = input()
        if check_card(card_number, pin):
            print("\nYou have successfully logged in!\n")
            logged_in = True
            account_option = -1

            while logged_in == True:
                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")
                account_option = int(input())

                if account_option == 1:
                    print("\nBalance: " + balance + "\n")

                elif account_option == 2:
                    print("\nEnter income:")
                    balance += int(input())
                    cur.execute(''' UPDATE card set balance=(?) WHERE number=(?) ''', (balance, card_number))
                    conn.commit()
                    print("Income was added!\n")

                elif account_option == 3:
                    print("\nTransfer")
                    print("Enter card number:")
                    transfer_card_number = input()

                    if transfer_card_number == card_number:
                        print("You can't transfer money to the same account!")

                    elif luhn_check(transfer_card_number) and check_card(transfer_card_number):
                        print("Enter how much money you want to transfer:")
                        amount = int(input())
                        if amount > balance:
                            print("Not enough money!\n")
                        else:
                            balance -= amount
                            cur.execute(''' UPDATE card set balance=(?) WHERE number=(?) ''', (balance, card_number))
                            cur.execute(''' SELECT balance FROM card WHERE number=(?)''', [transfer_card_number])
                            transfer_balance = cur.fetchall()[0][0]
                            transfer_balance += amount
                            cur.execute(''' UPDATE card set balance=(?) WHERE number=(?) ''',
                                        (transfer_balance, transfer_card_number))
                            conn.commit()
                            print("Success!\n")

                    elif not luhn_check(transfer_card_number):
                        print("Probably you made a mistake in the card number.")
                        print("Please try again!\n")

                    else:
                        print("Such card does not exist.\n")


                elif account_option == 4:
                    cur.execute(''' DELETE from card WHERE number = (?)''', [card_number])
                    conn.commit()
                    print("The account as been closed!")
                    logged_in = False

                elif account_option == 5:
                    print("\nYou have successfully logged out!\n")
                    logged_in = False

                elif account_option == 0:
                    logged_in = False
                    option = account_option
        else:
            print("Wrong card number or PIN!")

print("\nBye!")
