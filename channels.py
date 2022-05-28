import commpy.channels as channel
import numpy as num

def getBecChannel(inputStream,prob):
    result = channel.bec(inputStream,prob)
    return num.delete(result,num.where(result==-1))

def getBscChannel(inputStream, prob):
    return channel.bsc(inputStream,prob)

