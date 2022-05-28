import commpy.channels as channel
import numpy as num

def getBecChannel(inputStream,prob):
    result = channel.bec(inputStream,prob)
    return num.delete(result,num.where(result==-1))
    #return channel.bec(inputStream,prob)

def getBscChannel(inputStream, prob):
    return channel.bsc(inputStream,prob)

print(getBecChannel(num.array([1,0,1,0,1]),0.2))
