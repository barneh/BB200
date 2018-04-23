import binascii
import time

done = False
myInt = 0
myName = "Geir"
#myName = "Thomas2077614111"
myNewName = ""
myHashedName = ""
myNewHashedName = ""

myHashedName = binascii.crc32(myName.encode())
myList = {myName: "{:#010x}".format(myHashedName)}
print(myName)

while done == False:
    myInt += 1
    myNewName = myName + str(myInt)
    #myNewName = "Thomas3191202540"
    print(myNewName)

    myNewHashedName = binascii.crc32(myNewName.encode())
    for name, hashedName in myList.items():
        #print(hashedName, " compare to ", "{:#010x}".format(myNewHashedName))
        if hashedName == "{:#010x}".format(myNewHashedName):
            print("name", name, "and ", myNewName, "has the same hashed value", myHashedName, myNewHashedName)
            done = True

    myList[myNewName] = "{:#010x}".format(myNewHashedName)
    #print(myNewName, "{:#010x}".format(myNewHashedName))
    #print(len(myList))
    #time.sleep(0.2)