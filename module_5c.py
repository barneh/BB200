# |**********************************************************************
# * Project      : BB200
# * Program name : module_5c.py
# * Author       : Geir V. Hagen (geha0002)
# * Date created : 2018-04
# * Purpose      : Create, sign and send transaction
# |**********************************************************************


# IMPORTS
import requests
import json
import sys

#  GLOBAL VARIABLES
rpc_user = "username"
rpc_pass = "password"
url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
headers = {"content-type": "application/json"}


# |*************************************************
#   Method : getUnspentTransaction()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-23
#   Purpose: List unspent transaction.
# |*************************************************
def getUnspentTransaction():
    listUnspentTransaction = {
        'method': "listunspent"
    }
    response = requests.post(url, data=json.dumps(listUnspentTransaction), headers=headers).json()
    #print("getUnspentTransaction: ", json.dumps(response, indent=2, sort_keys=True))
    
    if response.get("result")[0].get('txid'):
        return response.get("result")[0].get('txid')
    else:
        print("\n\tError: ", response.get("error"))
        return ""
    

# |*************************************************
#   Method : createTransaction()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-19
#   Purpose: Create an transcation.
# |*************************************************
def createTransaction(txId, toAddress, toAmount):
    # Input parameters - txId and vout
    inputs = [
        {
            'txid': txId,
            "vout" : 0
        }
    ]
    
    # Output parameters - The address that is gone get the spendings and the amount
    outputs = {
        toAddress: toAmount
    }

    createTransaction = {
        "method": "createrawtransaction",
        "params": [inputs, outputs]
    }

    response = requests.post(url, data=json.dumps(createTransaction), headers=headers).json()
    #print("CreateRawTransaction: ", json.dumps(response, indent=2, sort_keys=True))
    
    if response.get("error") == None:
        if response.get("result"):
            return response.get('result')
        else:
            return ""
    else:
        print("\n\tError: ", response.get("error"))
        return ""


# |*************************************************
#   Method : signTranscation()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-19
#   Purpose: Signing an transcation.
# |*************************************************
def signTranscation(transactionToBeSigned, privateKey):
    signTransaction = {
        "method": "signrawtransaction",
        "params": [transactionToBeSigned, None,  [privateKey]]
        #"params": [transactionToBeSigned, None,  None]
    }

    response = requests.post(url, data=json.dumps(signTransaction), headers=headers).json()
    #print("SignRawTransaction: ", json.dumps(response, indent=2, sort_keys=True))
    
    if response.get("result").get("errors") == None:
        if response.get("result").get("complete") == True:
            return response.get("result").get("hex")
        else:
            return ""
    else:
        print("\n\tErrorCode: ", response.get("result").get("errors"))
        return ""


# |*************************************************
#   Method : sendTransaction()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-24
#   Purpose: Sending an transcation.
# |*************************************************
def sendTransaction(hex):
    sendTransaction = {
        "method": "sendrawtransaction",
        "params": [hex]
    }

    response = requests.post(url, data=json.dumps(sendTransaction), headers=headers).json()
    #print("SendRawTransaction: ", json.dumps(response, indent=2, sort_keys=True))

    if response.get("error") == None:
        if response.get("txid"):
            return response.get("txid")
        else:
            return ""
    else:
        print("\n\tErrorCode: ", response.get("error").get("code"))
        print("\tErrorMessage: ", response.get("error").get("message"), "\n")
        return ""


# |*************************************************
#   Method : validateAddress(inputAddress)
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-24
#   Purpose: Check if the input address is valid?
# |*************************************************
def validateAddress(inputAddress):
    validateInputAddress = {
        "method": "validateaddress",
        "params": [inputAddress]
    }
    response = requests.post(url, data=json.dumps(validateInputAddress), headers=headers).json()
    
    return response['result']['isvalid']


# |*************************************************
#   Method : sendBitCoin()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-19
#   Purpose: Print the main menu to screen and 
#            fetch user input.
# |*************************************************
def sendBitCoin(data):
    '''
    fromAddress = input("Ange adress att sicka från: ")
    while validateAddress(fromAddress) != True:
        print("Adressen du angav ", fromAddress, " är inte giltig. Prova igen!")
        fromAddress = input("Ange adress att sicka från: ")

    toAddress = input("Ange adress att skicka till: ")
    while validateAddress(toAddress) != True:
        print("Adressen du angav ", toAddress, " är inte giltig. Prova igen!")
        toAddress = input("Ange adress att skicka till: ")

    amount = input("Ange belopp: ")
    exchangeAddress = input("Ange växeladress: ")
    exchangeRate = input("Ange fee per kB: ")
    '''

    #DEBUG DATA
    fromAddress = "17fsyTAEDYu2SXtvgSrwGa6gf529AU46NF"
    toAddress = "1MNaz9VrCdyDQ8G3aNqJWsaZqvxCHP9TRW"
    amount = "0.00000613"
    exchangeAddress = ""
    exchangeRate = ""
    privateKey = ["5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreDEUj22G"]

    txId = getUnspentTransaction()
    if txId != "":
        print("Skapar transaktionen...")
        createdTrans = createTransaction(txId, data[6], amount)
        #createdTrans = createTransaction(txId, toAddress, amount)
    else:
        return
    
    if createdTrans != "":
        print("\tTransaktionen skapat...")
        print("Signerar transaktionen...")
        signHex = signTranscation(createdTrans, data[2])
        #signHex = signTranscation(createdTrans, privateKey)
    else:
        print("Något gick fel vid skapande av transaktionen.\n")
        return
    
    if signHex != "":
        print("\tTransaktionen signerat...")
        print("Sänder transaktionen...")
        sendHex = sendTransaction(signHex)
    else:
        print("Något gick fel vid signering av transaktionen.\n")
        return

    if sendHex != "":
        print("\tTransaktionen sänt!")
    else:
        print("Något gick fel vid sänding av transaktionen.\n")
        return

    return
