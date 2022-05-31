from communication import *
import time


def defineFile(channelType):
    global f
    if channelType == "BSC":
        f = open("BSC_Results.txt","w")
    elif channelType == "BEC":
        f = open("BEC_Results.txt","w")
    elif channelType == "Gilbert":
        f = open("Gilbert_Results.txt","w")
    return f


def transmitter():
    data_to_send = numpy.array([0,1,0,1,1,0,1,1])
    packets_to_send = 16
    packets_to_send_temp = packets_to_send
    code_encryption = "Doubling" # 'Even Checksum', 'Doubling', 'CRC32'
    # time for response = 40 (u_sec)
    packets_successfull = 0
    packets_unsucessful_due_to_NACK = 0
    packets_unsucessful_due_to_timeout = 0
    packets_unsucessful_due_to_collision = 0
    channelType = "Gilbert" # 'BSC' / 'BEC' / 'Gilbert'
    channelOverflow = 0 # max 30 same packets

    while(packets_to_send_temp>0):
        if channelOverflow >= 30:
            print("\nChannel Overflow!\nPacket lost!\n")
            packets_to_send_temp-=1
            channelOverflow = 0
            continue
        to_send = 0
        if code_encryption == "Even Checksum":
            to_send = appendParityBit(data_to_send)
        if code_encryption == "Doubling":
            to_send = generateDouble(data_to_send)
        if code_encryption == "CRC32":
            to_send = generateAndAppendCRC32(data_to_send)

        print("========= PACKET SENT =========\n")
        answer,receivedArray = sendPacket(to_send, code_encryption,channelType)
        if (answer == 2) or (answer == 3):
            packets_unsucessful_due_to_timeout += 1
            channelOverflow+=1
            print("==================================\n")
            time.sleep(1)
            continue
        elif answer == 4:
            packets_unsucessful_due_to_NACK += 1
            channelOverflow+=1
            print("==================================\n")
            time.sleep(1)
            continue
        elif answer == 5:
            if checkCollision(data_to_send,receivedArray,code_encryption):
                print("ACK deliviered!\nSending next package!\n")
                packets_to_send_temp-=1
                packets_successfull+=1
                channelOverflow = 0
                print("==================================\n")
                time.sleep(1)
            else:
                print("Collision detected!")
                packets_unsucessful_due_to_collision+=1
                channelOverflow+=1
                print("==================================\n")
                time.sleep(1)

        # statistics:

    print("\n\n===========Statistics===========\n")
    print('Packets ought to be delivered:',packets_to_send)
    print('\nPackets Successfully delivered:', packets_successfull)
    print('\nPackets lost due to timeout:',packets_unsucessful_due_to_timeout)
    print('\nPackets lost due to noise channel:', packets_unsucessful_due_to_NACK)
    print('\nPackets lost due to collision:', packets_unsucessful_due_to_collision)
    print("\n================================")

    f = defineFile(channelType)
    f.write("Channel Type: " + channelType
            + "\nCode Encryption: " + code_encryption
            + "\n\n----Statistics of simulation----"
            + "\nPackets ought to be delivered: " + str(packets_to_send)
            + "\nPackets successfully delivered: " + str(packets_successfull)
            + "\nPackets lost due to timeout: " + str(packets_unsucessful_due_to_timeout)
            + "\nPackets lost due to noise channel: " + str(packets_unsucessful_due_to_NACK)
            + "\nPackets lost due to collision: " + str(packets_unsucessful_due_to_collision)
            + "\n------------------------------------\n"
            + "Total frames lost: " + str(packets_unsucessful_due_to_NACK + packets_unsucessful_due_to_collision + packets_unsucessful_due_to_timeout))



# Main engine:
transmitter()




