import numpy as num
import binascii


# bit parzystosci
def generate_parity_bit(input):
    checksum = 0
    for i in range(0,8):
        checksum+= input[i]
    return checksum % 2

def appendParityBit(input):
    out = num.empty(0,dtype=num.uint8)
    for i in range(0,input.size,8):
        help = input[i:i+8]
        out = num.append(out, help)
        out = num.append(out,generate_parity_bit(help))
    return out

def rollBackParity(input):
    if input.size %9 != 0:
        return False,input
    out = num.empty(0,dtype=num.uint8)
    for i in range(0,input.size,9):
        help = input[i:i+8]
        bit_checksum = input[i+8]
        if generate_parity_bit(help) != bit_checksum:
            return False,input
        out = num.append(out,help)
    return True,out


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
            out = num.append(out,int(input[i]))
    return True,out