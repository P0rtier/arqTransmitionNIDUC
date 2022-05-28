import numpy
from checksums import *
import random
import time

def sendResponse(respText,responseArray):
    timer = random.randint(10,60)
    if(timer>=40):
        print("Response lost due to timeout in noise channel")
        return 3,responseArray
    if(respText=="NACK"):
        print("Nack request sent to transmiter")
        return 4,responseArray
    else:
        print("ACK sent")
        return 5,responseArray

def receiver(data_to_receive,code_encryption):
    global response
    resp_good = False

    if(code_encryption == "Even Checksum"):
        resp_good,response = rollBackParity(data_to_receive)
    if (code_encryption == "Doubling"):
        resp_good,response = rollBackDouble(data_to_receive)
    if (code_encryption == "CRC32"):
        resp_good,response = rollBackCRC32(data_to_receive)

    if(resp_good):
        print("Packet properly decoded, sending ACK back")
        return sendResponse("ACK",response)
    else:
        print("Wrong packet decoded, sending NACK request")
        return sendResponse("NACK",response)

