#|**********************************************************************
#* Project      : BB200
#* Program name : module_3.py
#* Author       : Geir V. Hagen (geha0002)
#* Date created : 2018-03
#* Purpose      : Exercise to print and get information 
#*                from Edu-blockchain depending on the users input.
#|**********************************************************************


# IMPORTS
import requests
import json
import datetime
import time
import sys

#  GLOBAL VARIABLES
rpc_user = "username"
rpc_pass = "password"
url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
headers = {"content-type": "application/json"}


#|*************************************************
#   Method : postRequest(post)
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-05-02
#   Purpose: Handle all the API-requests
#|*************************************************
def postRequest(post):
    if post:
        return requests.post(url, data=json.dumps(post), headers=headers).json()


#|*************************************************
#   Method : viewBlockFromNumber(number)
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-08
#   Purpose: Print the selceted block number
#|*************************************************
def viewBlockFromNumber(blockNumber):
    print("------------------------------------------")
    getBlockHash = {
        "method": "getblockhash",
        "params": [ int(blockNumber) ],
    }
    try:
        blockNumberResponse = postRequest(getBlockHash)

        getBlock = {
            "method": "getblock",
            "params": [ blockNumberResponse['result'] ],
        }
    
        block = postRequest(getBlock)
        #print(json.dumps(block, indent=2, sort_keys=True))
        print("Block hash:", block['result']['hash'])
        if 'previousblockhash' in block['result']:
            print("Prev. hash:", block['result']['previousblockhash'])
            print("Merkle root:", block['result']['merkleroot'])
            print("Height:", blockNumber)
            print("Tid:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(block['result']['time'])))
            print("Difficulty:", block['result']['difficulty'])
            print("Transactions:", len(block['result']['tx']))
            nTx = 0
            for i in block['result']['tx']:
                print("  tx%s: %s" % (nTx, i))
                nTx+=1
    except:
        print("Something went wrong, please try again...")
    
    print()
    blockExplorerMenu()


#|*************************************************
#   Method : viewBlockFromHash(hash)
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-12
#   Purpose: Print the block from the users
#            hash intput
#|*************************************************
def viewBlockFromHash(hash):
    print("------------------------------------------")
    getBlock = {
        "method": "getblock",
        "params": [ hash ],
    }
    try:
        block = postRequest(getBlock)
        #print(json.dumps(block, indent=2, sort_keys=True))
        print("Block hash:", block['result']['hash'])
        if 'previousblockhash' in block['result']:
            print("Prev. hash:", block['result']['previousblockhash'])
        print("Merkle root:", block['result']['merkleroot'])
        print("Height:", block['result']['height'])
        print("Tid:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(block['result']['time'])))
        print("Difficulty:", block['result']['difficulty'])
        print("Transactions:", len(block['result']['tx']))
        nTx = 0
        for i in block['result']['tx']:
            print("  tx%s: %s" % (nTx, i))
            nTx+=1
    except:
        print("Something went wrong, please try again...")
    
    print()
    blockExplorerMenu()


#|*************************************************
#   Method : viewTransaction(transactionHash)
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-12
#   Purpose: 
#|*************************************************
def viewTransaction(transactionHash):
    print("------------------------------------------")
    getTransaction = {
        "method": "getrawtransaction",
        "params": [ transactionHash, True ],
    }
    try:
        block = postRequest(getTransaction)
        #print(json.dumps(block, indent=2, sort_keys=True))
        print("Txid (hash):", block['result']['txid'])
        print("Med i block:", block['result']['blockhash'])
        print("Inputs:", len(block['result']['vin']))
        print("Outputs:", len(block['result']['vout']))
        nVout = 0
        for i in block['result']['vout']:
            if 'addresses' in i['scriptPubKey']:
                print("  output %s: %f BTE till adress %s" % (nVout, float(i['value']), str(i['scriptPubKey']['addresses']).strip("['''']")))
            else:
                print("  output %s: ingen adress" % (nVout))

            nVout+=1
    except:
        print("Something went wrong, please try again...")

    print()
    blockExplorerMenu()


#|*************************************************
#   Method : listOutputsForAddress(address)
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-13
#   Purpose: List information where an address has
#            recived payment.
#|*************************************************
def listOutputsForAddress(address):
    print("------------------------------------------")
    print("Söker efter adress:", address)
    getBlockCount = {
        "method": "getblockcount",
    }
    try:
        block = postRequest(getBlockCount)
        #print(json.dumps(block, indent=2, sort_keys=True))
        noOfBlocks = block['result']
        startBlock = 0

        for n in range(0, noOfBlocks):
            if n == startBlock:
                print(n)
                startBlock+=500

            getBlockHash = {
                "method": "getblockhash",
                "params": [ int(n) ],
            }
            block = postRequest(getBlockHash)
            #print(json.dumps(block, indent=2, sort_keys=True))
            blockHash = block['result']
            
            getBlock = {
                "method": "getblock",
                "params": [ blockHash ],
            }
            block = postRequest(getBlock)
            #print(json.dumps(block, indent=2, sort_keys=True))
            txId = block['result']['tx']

            for transaction in txId:
                getTransaction = {
                    "method": "getrawtransaction",
                    "params": [ transaction, True ],
                }
                block = postRequest(getTransaction)
                #print(json.dumps(block, indent=2, sort_keys=True))
                if block['result']:
                    if 'vout' in block['result']:
                        for i in block['result']['vout']:
                            if 'addresses' in i['scriptPubKey']:
                                if str(i['scriptPubKey']['addresses']).strip("['''']") == address:
                                    print("Block: %s, Tx: %s output %s: %f BTE" % (n, transaction, str(i['n']), float(i['value'])))
    except:
        print("Something went wrong, please try again...")
    
    print()
    blockExplorerMenu()


#|*************************************************
#   Method : viewInputError()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-08
#   Purpose: Print an error if the menu input is
#            not valid.
#|*************************************************
def viewInputError():
    print("You're choice is invalid. Please try again")
    blockExplorerMenu()


#|*************************************************
#   Method : convertToMB(value)
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-15
#   Purpose: Convert byte to MB.
#|*************************************************
def convertByteToMB(value):
    value /= 1024.0 * 1024.0
    return value


#|*************************************************
#   Method : fetchStartupValues()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-08
#   Purpose: Fetch the startup values and put it
#            into an array that is return to caller.
#|*************************************************
def fetchStartupValues():
    noOfBlocks = {
            "method": "getblockcount",
    }
    noOfBlocksResponse = postRequest(noOfBlocks)
    #print(json.dumps(noOfBlocksResponse, indent=2, sort_keys=True))

    blockStorageSize = {
            "method": "getblockchaininfo",
    }
    storageSizeResponse = postRequest(blockStorageSize)
    #print(json.dumps(storageSizeResponse, indent=2, sort_keys=True))

    latestBlock = {
            "method": "getbestblockhash",
    }
    latestBlockResponse = postRequest(latestBlock)
    #print(json.dumps(latestBlockResponse, indent=2, sort_keys=True))

    memPoolSize = {
            "method": "getmempoolinfo",
    }
    memPoolSizeResponse = postRequest(memPoolSize)
    #print(json.dumps(memPoolSizeResponse, indent=2, sort_keys=True))

    noOfConnections = {
            "method": "getconnectioncount",
    }
    noOfConnectionsRespose = postRequest(noOfConnections)
    #print(json.dumps(noOfConnectionsRespose, indent=2, sort_keys=True))
    
    values = (noOfBlocksResponse['result'], 
              storageSizeResponse['result']['size_on_disk'],
              latestBlockResponse['result'],
              memPoolSizeResponse['result']['size'],
              noOfConnectionsRespose['result'])

    return values


#|*************************************************
#   Method : blockExplorerStartup()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-08
#   Purpose: Print the startup values to screen.
#|*************************************************
def blockExplorerStartup():
    values = fetchStartupValues()
    print("    Bitcoin Edu utforskare")
    print("==============================")
    print("Antal block    :", values[0])
    print("Lagringsstorlek: %3.2f %s" % (convertByteToMB(float(values[1])), "MB"))
    print("Senaste block  :", values[2])
    print("Mempool (size) :", values[3], "st transaktioner")
    print("Connections    :", values[4], "noder")
    print("==============================")
    blockExplorerMenu()


#|*************************************************
#   Method : blockExplorerMenu()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-03-08
#   Purpose: Print the menu to screen and fetch
#            user input.
#|*************************************************

def blockExplorerMenu():
    done = True
    print("Meny")
    print(" 1. Visa block (ange nr)")
    print(" 2. Visa block (ange hash)")
    print(" 3. Visa transaktion")
    print(" 4. Lista outputs för adress")
    print(" 5. Exit\n")
    choice = input("Välj funktion: ")

    while done:
        if choice == "1":
            number = input("Ange blocknr: ")
            viewBlockFromNumber(number)
        elif choice == "2":
            hash = input("Ange blockhash: ")
            viewBlockFromHash(hash)
        elif choice == "3":
            transactionHash = input("Ange transaktionshash: ")
            viewTransaction(transactionHash)
        elif choice == "4":
            address = input("Ange adress: ")
            listOutputsForAddress(address)
        elif choice == "5":
            sys.exit(1)
        else:
            viewInputError()


# START METHOD
blockExplorerStartup()