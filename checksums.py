import numpy as num
import binascii


# bit parzystosci
def generate_parity_bit(input):
    checksum = 0
    for i in input:
        checksum+=i
    return checksum % 2

def appendParityBit(input):
    if input.size>8:
        return "Error"
    else:
        return num.append(input,generate_parity_bit(input))

def rollBackParity(input):
    if input.size > 9:
        return False,input
    check = input[0:8]
    pCheck = generate_parity_bit(check)
    if pCheck == input[8]:
        return True,input
    else:
        return False,input


# crc32
def getIntFromBin(input):
    a = 0
    init = 0
    for i in range(input.size-1,-1,-1):
        init = init + pow(2,a) * input[i]
        a = a+1
    return init




def generateAndAppendCRC32(input):
    crc32Dec = binascii.crc32(input)
    crc32Bin = num.array([int(x) for x in bin(crc32Dec)[2:]])
    all_crc32 = num.zeros(32-crc32Bin.size,dtype=num.uint8)
    crc32List = num.concatenate((all_crc32,crc32Bin))
    return num.append(input, crc32List)


def rollBackCRC32(input):
    if input.size < 40:
        return False,input
    data_wo_packet_send = input[0:8]
    control = input[8:]
    if binascii.crc32(data_wo_packet_send) == getIntFromBin(control):
        return True,input
    else:
        return False,input


# dublowanie
def generateDouble(input):
    out = num.empty(0,dtype=num.uint8)
    for i in input:
        out = num.append(out,[i,i])
    return out


def rollBackDouble(input):
    out = num.array([])
    if input.size % 2 != 0:
        return False,input
    for i in range(0,input.size,2):
        if input[i] != input[i+1]:
            return False,out
        else:
            num.append(out,input[i])
    return True,out