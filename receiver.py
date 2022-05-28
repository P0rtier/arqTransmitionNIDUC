import numpy
from checksums import *
import random

def sendResponse(resp):
    time = random.randint(10,60)
    if(time>=40):
        print("Response lost due to timeout in noise channel")
        return 3
    if(resp=="NACK"):
        print("Nack request sent to transmiter")
        return 4
    else:
        print("ACK sent")
        return 5

def receiver(data_to_receive,code_encryption):
    resp_good = False

    if(code_encryption == "Even Checksum"):
        resp_good = rollBackParity(data_to_receive)
    if (code_encryption == "Doubling"):
        resp_good = rollBackDouble(data_to_receive)
    if (code_encryption == "CRC32"):
        resp_good = rollBackCRC32(data_to_receive)

    if(resp_good):
        print("Packet properly decoded, sending ACK back")
        return sendResponse("ACK")
    else:
        print("Wrong packet decoded, sending NACK request")
        return sendResponse("NACK")

