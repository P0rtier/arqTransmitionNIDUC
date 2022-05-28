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
        return False
    check = input[0:7]
    pCheck = generate_parity_bit(check)
    if pCheck == input[8]:
        return True
    else:
        return False


# crc32
def getIntFromBin(input):
    a = 0
    init = 0
    for i in range(input.size-1,-1,-1):
        init = init +  pow(2,a) * input[i]
        a= a+1
    return init


def generateAndAppendCRC32(input):
    crc32 = binascii.crc32(input)
    crc32List = num.array([int(x) for x in bin(crc32)[2:]])
    return crc32, num.append(input, crc32List)


def rollBackCRC32(input):
    if input < 40:
        return False
    pure_data_32 = input[0:31]
    control = input[32:39]
    if binascii.crc32(pure_data_32) == getIntFromBin(control):
        return True
    else:
        return False


# dublowanie
def generateDouble(input):
    out = num.array(0)
    for i in input:
        out = num.append(out,i,i)
    return out


def rollBackDouble(input):
    if input % 2 != 0:
        return False
    for i in range(0,input.size,2):
        if input[i] != input[i+1]:
            return False
        else:
            return True