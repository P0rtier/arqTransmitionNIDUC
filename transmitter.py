import numpy
import random
from checksums import *
from channels import *
from receiver import *

def sendPacket(to_send,codeE): #1 - internal error, 2 - timeout,
    noise_time = random.randint(10,60)
    if(noise_time>40):
        print("Packet lost in the noise channel due to timeout!")
        return 2
    after_noise = getBscChannel(to_send,0.1)
    received_msg = receiver(after_noise,codeE)
    return received_msg # 3 - lost due to timeout, 4 - NACk, 5 - ACK



def transmitter():
    data_to_send = numpy.array([1,0,1,1,0,1,1,0])
    packets_to_send = 69
    packets_to_send_temp = packets_to_send
    code_encryption = "Even Checksum"
    time_to_wait = random.randint(30,40)
    packets_successfull = 0
    packets_unsucessful_due_to_NACK = 0
    packets_unsucessful_due_to_timeout = 0

    while(packets_to_send_temp>0):
        to_send = 0
        if(code_encryption == "Even Checksum"):
            to_send = appendParityBit(data_to_send)
        if(code_encryption == "Doubling"):
            to_send = generateDouble(data_to_send)
        if(code_encryption == "CRC32"):
            to_send = generateAndAppendCRC32(data_to_send)

        answer = sendPacket(to_send, code_encryption)
        if (answer == 1) or (answer ==  2) or (answer == 3):
            packets_unsucessful_due_to_timeout += 1
            continue
        elif answer == 4:
            print("NACK request delivered!\nResending package!\n")
            packets_unsucessful_due_to_NACK += 1
            continue
        elif answer == 5:
            print("ACK deliviered!\nSending next package!\n")
            packets_to_send_temp-=1
            packets_successfull+=1

        # statistics:

    print("\n\n======Stats======\n\n")
    print('Packets ought to be delivered:',packets_to_send)
    print('\nPackets Successfully delivered:', packets_successfull)
    print('\nPackets lost due to timeout:',packets_unsucessful_due_to_timeout)
    print('\nPackets lost due to noise channel:', packets_unsucessful_due_to_NACK)



transmitter()




