import communication as comm
from checksums import *

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
        return comm.sendResponse("ACK",response)
    else:
        print("Wrong packet decoded! The frame has been altered in the noise channel!")
        return comm.sendResponse("NACK",response)

