# |**********************************************************************
# * Project      : BB200
# * Program name : module_5a.py
# * Author       : Geir V. Hagen (geha0002)
# * Date created : 2018-04
# * Purpose      : Print the generated keys and address and 
#                  send BitCoin
# |**********************************************************************


# IMPORTS
from module_5b import generatePrivPubAddressData
from module_5c import sendBitCoin
import sys


# |*************************************************
#   Method : printPrivateKey()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-10
#   Purpose: Print the private key in integer, 
#            hex or wif-format.
# |*************************************************
def printPrivateKey(data):
    print("")
    print("=============================")
    print("    PRINTING PRIVATE KEY")
    print("=============================")
    print(" * PrivateKey (integer)   :", data[0])
    print(" * The Hexified PrivateKey:", data[1])
    print(" * Wif PrivateKey         :", data[2], "\n")


# |*************************************************
#   Method : printPublicKey()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-10
#   Purpose: Print the public key in compressed or 
#            uncompressed format.
# |*************************************************
def printPublicKey(data):
    print("")
    print("=============================")
    print("     PRINTING PUBLIC KEY")
    print("=============================")
    print(" * The Uncompressed publicKey:", data[3])
    print(" * The Compressed publicKey  :", data[4], "\n")


# |*************************************************
#   Method : printBitcoinAddress()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-10
#   Purpose: Print the bitcoin address from the
#            compressed or uncompressed public key.
# |*************************************************
def printBitcoinAddress(data):
    print("")
    print("=============================")
    print("      PRINTING ADDRESS")
    print("=============================")
    print(" * From the Uncompressed publicKey:", data[5])
    print(" * From the Compressed publicKey  :", data[6], "\n")


# |*************************************************
#   Method : viewInputError()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-10
#   Purpose: Print an error if the menu input is
#            not valid.
# |*************************************************
def viewInputError():
    print("")
    print("You're choice is invalid. Please try again!")
    print("")


# |*************************************************
#   Method : MainMenu()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-10
#   Purpose: Print the main menu to screen and fetch
#            user input.
# |*************************************************
def MainMenu(data):
    done = True
    print("=============================")
    print("    MODULE 5 - EXERCISE")
    print("=============================")
    print(" 1. Skriv ut privata nycklar")
    print(" 2. Skriv ut publika nycklar")
    print(" 3. Skriv ut bitcoin adress")
    print(" 4. Skicka bitcoin")
    print(" 5. Exit\n")
    choice = input("Välj funktion: ")

    while done:
        if choice == "1":
            printPrivateKey(data)
            MainMenu(data)
        elif choice == "2":
            printPublicKey(data)
            MainMenu(data)
        elif choice == "3":
            printBitcoinAddress(data)
            MainMenu(data)
        elif choice == "4":
            sendBitCoin(data)
            MainMenu(data)
        elif choice == "5":
            sys.exit(1)
        else:
            viewInputError()
            MainMenu(data)


# START METHOD
data = generatePrivPubAddressData()
MainMenu(data)