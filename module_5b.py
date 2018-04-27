# |**********************************************************************
# * Project      : BB200
# * Program name : module_5b.py
# * Author       : Geir V. Hagen (geha0002)
# * Date created : 2018-04
# * Purpose      : Generate private, public key and address
# |**********************************************************************


# IMPORTS
from pycoin import ecdsa as secp, key, encoding
import hashlib
import binascii
import codecs
import os


# |*************************************************
#   Method : getDoubleSha256()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-09
#   Purpose: Support function for getting a 
#            double 256 hash of the in-value.
# |*************************************************
def getDoubleSha256(value):
    return hashlib.sha256(hashlib.sha256(binascii.unhexlify(value)).digest()).hexdigest()


# |*************************************************
#   Method : getHash160()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-09
#   Purpose: Support function for getting a 
#            160 hash of the in-value.
# |*************************************************
def getHash160(value):
    return hashlib.new('ripemd160',hashlib.sha256(binascii.unhexlify(value)).digest()).hexdigest()


# |*************************************************
#   Method : GeneratePrivPubAddressData()
#   Author : Geir V. Hagen (geha0002)
#   Date   : 2018-04-08
#   Purpose: Generate the "start" Point for 
#            caluclating the private-, public-Key
#            and the BitCoin addresses.
# |*************************************************
def generatePrivPubAddressData():
    privPubAddressData = {}

#--------------------------[ ECDSA ]------------------------------#
    # Creating the gPoint (also known as G, in the formula P = k * G)
    gPoint = secp.generator_secp256k1

    # Randomize a string of n random bytes for getting the Secret Exponent (also known as k, in the formula P = k * G)
    rand = codecs.encode(os.urandom(32), 'hex').decode()
    secretExponent = int('0x' + rand, 0)
    #secretExponent = 10 # Uses 10 for test, to see that everything matches up!
    privPubAddressData[0] = secretExponent

    # Calculate the public key (point) (also known as the P, in the formula P = k * G)
    publicKeyPoint = secretExponent * gPoint
#-----------------------------------------------------------------#

#-------------------------[ PRIVATE KEY ]-------------------------#
    secretExponentHexified = '%064x' % secretExponent
    privPubAddressData[1] = secretExponentHexified
    # 80 = mainnet, 01 = compressed public key should be generated
    data = '80' + secretExponentHexified + '01'
    # 4 bytes, 8 hex nibbles
    checkSum = getDoubleSha256(data)[:8]
    data = data + checkSum
    wif = encoding.b2a_base58(binascii.unhexlify(data))
    privPubAddressData[2] = wif
#-----------------------------------------------------------------#

#-------------------------[ PUBLIC KEY ]--------------------------#
    # This encoding is standardized by SEC, Standards for Efficient Cryptography Group (SECG).
    # Uncompressed public key has the prefix 0x04
    x = '%064x' % publicKeyPoint.x()
    y = '%064x' % publicKeyPoint.y()
    uncompressedPublicKey = '04' + x + y
    #print('Public key, uncompressed', uncompressedPublicKey)
    privPubAddressData[3] = uncompressedPublicKey 

    # Compressed public key has the prefix 02 if y is even, 03 if y is odd
    compressedPublicKey = ('02' if publicKeyPoint.y() % 2 == 0 else '03') + x
    #print('Public key, compressed', compressedPublicKey)
    privPubAddressData[4] = compressedPublicKey
#-----------------------------------------------------------------#

#-------------------------[ BITCOIN ADDRESS ]---------------------#
    # Add the version byte 00 and get the hash160 of the publicKey from the uncompressed publicKey
    uncompressedH160WithVersion = '00' + getHash160(uncompressedPublicKey)
    
    # Add 4 bytes checkSum from double sha256 encyption
    checkSum = getDoubleSha256(uncompressedH160WithVersion)[:8]
    uncompressedH160WithVersion = uncompressedH160WithVersion + checkSum

    # Convert to base58
    bitCoinAddressUncompressed = encoding.b2a_base58(binascii.unhexlify(uncompressedH160WithVersion))
    #print('Bitcoin address (uncomp):', bitCoinAddressUncompressed)
    privPubAddressData[5] = bitCoinAddressUncompressed


    # Add the version byte 00 and gets the hash160 of the publicKey from the compressed publicKey
    compressedH160WithVersion = '00' + getHash160(compressedPublicKey)

    # Add 4 bytes checkSum from double sha256 encyption
    checkSum = getDoubleSha256(compressedH160WithVersion)[:8]
    compressedH160WithVersion = compressedH160WithVersion + checkSum
    
    # Convert to base58
    bitCoinAddressCompressed = encoding.b2a_base58(binascii.unhexlify(compressedH160WithVersion))
    privPubAddressData[6] = bitCoinAddressCompressed

    return privPubAddressData
#-----------------------------------------------------------------#
