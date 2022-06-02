import numpy
import random
from channels import *
from receiver import *

# ---------receiver----------

def sendResponse(respText,responseArray):
    if(respText=="NACK"):
        print("Response lost due to timeout in noise channel\n")
        return 4,responseArray
    else:
        print("ACK sent")
        return 5,responseArray


# ---------transmiter-----------

def checkCollision(data_to_send, reply, encryption):
    if encryption == "Even Checksum":
        return numpy.array_equal(data_to_send,reply)
    if encryption == "Doubling":
        return numpy.array_equal(data_to_send,reply)
    if encryption == "CRC32":
        return numpy.array_equal(data_to_send,reply[:8])


def sendPacket(to_send, codeE, channelType): #1 - internal error, 2 - timeout,
    setChannelProb = 0.9
    # if gilbert channel chosen:
    setGilbState2 = 0.45
    setGilbFromSt1_toSt2 = 0.1
    setGilbFromSt2_toSt1 = 0.45
    received_array = numpy.array([0])
    noise_time = random.randint(10,50)
    received_msg = -1
    if noise_time>40:
        print("Packet lost in the noise channel due to timeout!\n")
        return 2,received_array
    if channelType == "BEC":
        after_noise = getBecChannel(to_send,setChannelProb)
        equalArrays = numpy.array_equal(after_noise,to_send)
        if not equalArrays:
            return 2,received_array
        received_msg,received_array = receiver(after_noise,codeE)
    if channelType == "BSC":
        after_noise = getBscChannel(to_send,setChannelProb)
        received_msg,received_array = receiver(after_noise,codeE)
    if channelType == "Gilbert":
        after_noise = getGilbertChannel(to_send,setGilbState2,setGilbFromSt1_toSt2,setGilbFromSt2_toSt1)
        received_msg,received_array = receiver(after_noise,codeE)
    return received_msg,received_array # 3 - lost due to timeout, 4 - NACk, 5 - ACK
