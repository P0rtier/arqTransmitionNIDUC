import numpy
import random
from checksums import *
from channels import *
from receiver import *
import time


def checkCollision(data_to_send, reply, encryption):
    if encryption == "Even Checksum":
        return numpy.array_equal(data_to_send,reply[:8])
    if encryption == "Doubling":
        return numpy.array_equal(data_to_send,reply[::2])
    if encryption == "CRC32":
        return numpy.array_equal(data_to_send,reply[:8])


def sendPacket(to_send,codeE,channelType): #1 - internal error, 2 - timeout,
    setChannelProb = 0.2
    received_array = numpy.array([0])
    noise_time = random.randint(10,60)
    received_msg = -1
    if(noise_time>40):
        print("Packet lost in the noise channel due to timeout!")
        return 2,received_array
    if(channelType == "BEC"):
        after_noise = getBecChannel(to_send,setChannelProb)
        equalArrays = numpy.array_equal(after_noise,to_send)
        if not equalArrays:
            return 2,received_array
        received_msg,received_array = receiver(after_noise,codeE)
    if(channelType == "BSC"):
        after_noise = getBscChannel(to_send,setChannelProb)
        received_msg,received_array = receiver(after_noise,codeE)
    return received_msg,received_array # 3 - lost due to timeout, 4 - NACk, 5 - ACK



def transmitter():
    data_to_send = numpy.array([0,0,0,1,1,1,1,0])
    packets_to_send = 15
    packets_to_send_temp = packets_to_send
    code_encryption = "Even Checksum"
    time_to_wait = random.randint(30,40)
    packets_successfull = 0
    packets_unsucessful_due_to_NACK = 0
    packets_unsucessful_due_to_timeout = 0
    packets_unsucessful_due_to_collision = 0
    channelType = "BSC"

    while(packets_to_send_temp>0):
        to_send = 0
        if(code_encryption == "Even Checksum"):
            to_send = appendParityBit(data_to_send)
        if(code_encryption == "Doubling"):
            to_send = generateDouble(data_to_send)
        if(code_encryption == "CRC32"):
            to_send = generateAndAppendCRC32(data_to_send)

        answer,receivedArray = sendPacket(to_send, code_encryption,channelType)
        if (answer == 2) or (answer == 3):
            packets_unsucessful_due_to_timeout += 1
            continue
        elif answer == 4:
            print("NACK request delivered!\nResending package!\n")
            packets_unsucessful_due_to_NACK += 1
            continue
        elif answer == 5:
            if(checkCollision(data_to_send,receivedArray,code_encryption)):
                print("ACK deliviered!\nSending next package!\n")
                packets_to_send_temp-=1
                packets_successfull+=1
            else:
                print("Collision detected!")
                packets_unsucessful_due_to_collision+=1

        # statistics:

    print("\n\n======Stats======\n\n")
    print('Packets ought to be delivered:',packets_to_send)
    print('\nPackets Successfully delivered:', packets_successfull)
    print('\nPackets lost due to timeout:',packets_unsucessful_due_to_timeout)
    print('\nPackets lost due to noise channel:', packets_unsucessful_due_to_NACK)
    print('\nPackets lost due to collision:', packets_unsucessful_due_to_collision)



transmitter()




