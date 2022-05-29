import commpy.channels as channel
import numpy as num
import random

def getBecChannel(inputStream,prob):
    result = channel.bec(inputStream,prob)
    return num.delete(result,num.where(result==-1))

def getBscChannel(inputStream, prob):
    return channel.bsc(inputStream,prob)


# Gilbert channel
def changeState(curr_state,st_1_to2,st_2_to_1):
    check = random.random()
    if curr_state == 1: # state good
        if check < st_1_to2:
            return 2
        else:
            return 1
    if curr_state == 2: # state bad
        if check < st_2_to_1:
            return 2
        else:
            return 1



# defining state 1 chance to 0
def getGilbertChannel(inputStream,state_2,st_1_to2,st_2_to_1):
    current_state = 1 # 1 - state_good, 2 - state_bad
    out = inputStream
    for i in range(0,out.size):
        check = random.random()
        current_state = changeState(current_state,st_1_to2,st_2_to_1)
        if current_state == 2 and check > state_2:
            out[i] ^= True
        else:
            out[i] ^= False
    return out



