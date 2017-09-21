# Aidan Payne
# IFT 510 Booth's Algorithm Implementation
from collections import deque

# Function that inverts a binary value.
def bitInversion(invert):
    invertedValue = invert
    for index, item in enumerate(invertedValue):
        if item == 1:
            invert[index] = 0
        elif item == 0:
            invert[index] = 1
    return invertedValue

# Function to find two's compliment value of a given binary value
def twosCompliment(multiplicandValue):
    compliment = bitInversion(multiplicandValue)
    print("bit inversion: ",compliment)
    compliment.reverse()
    carry = 0
    for index, item in enumerate(compliment):
        if item == 0 and index == 0:
            compliment[index] += 1
        elif item == 1 and index == 0:
            compliment[index] = 0
            carry = 1
        elif item == 0 and carry == 1:
            compliment[index] += 1
            carry = 0
        elif item == 0 and carry == 0:
            compliment[index] = 0
        elif item == 1 and carry == 1:
            compliment[index] = 0
            carry = 1
        elif item == 1 and carry == 0:
            compliment[index] = 1
            carry = 0
    compliment.reverse()
    return compliment

# Function to perform binary addition
def binaryAddition(value1,value2):
    binarySum = []
    reverseValue2 = list(value2)
    value1.reverse()
    reverseValue2.reverse()
    carry = 0
    for addend1bit,addend2bit in zip(value1, reverseValue2):
        if addend1bit+addend2bit+carry == 2:
            binarySum.append(0)
            carry = 1
        elif addend1bit+addend2bit+carry == 3:
            binarySum.append(1)
            carry = 1
        elif addend1bit+addend2bit+carry == 1:
            binarySum.append(1)
            carry = 0
        else:
            binarySum.append(0)
            carry = 0
    binarySum.reverse()
    return binarySum

def shiftRight(value, addedBit=None):
    shiftedValue = deque(value)
    if shiftedValue[0] == 0 and addedBit is None:
        shiftedValue.appendleft(0)
    elif shiftedValue[0] == 1 and addedBit is None:
        shiftedValue.appendleft(1)
    elif addedBit is not None:
        shiftedValue.appendleft(addedBit)
    extraBit = shiftedValue.pop()
    shiftedExtra = [list(shiftedValue),extraBit]
    return shiftedExtra

def main():
    multiplicand = input("Please enter the multiplicand: ")
    multiplier = input("Please enter the multiplier: ")
    multiplicandBinary = []
    multiplierBinary = []
    negativeMultiplier = 0
    negativeMultiplicand = 0
    if len(multiplicand) == 8 and len(multiplier)== 8:
        for char in multiplicand:
            multiplicandBinary.append(int(char))
        for char in multiplier:
            multiplierBinary.append(int(char))
    else:
        if multiplicand[0] is '-':
            negativeMultiplicand = 1
            multiplicand = multiplicand[1:]
        if multiplier[0] is '-':
            negativeMultiplier = 1
            multiplier = multiplier[1:]
        multiplicand = bin(int(multiplicand))
        multiplier = bin(int(multiplier))
        multiplicand = multiplicand[2:]
        multiplier = multiplier[2:]
    if negativeMultiplier == 1:
        padding = 8 - len(multiplier)
        while padding > 0:
            multiplierBinary.append(0)
            padding -= 1
        for char in multiplier:
            multiplierBinary.append(int(char))
        multiplierBinary = twosCompliment(multiplierBinary)
    elif negativeMultiplier == 0:
        padding = 8 - len(multiplier)
        while padding > 0:
            multiplierBinary.append(0)
            padding -= 1
        for char in multiplier:
            multiplierBinary.append(int(char))
    if negativeMultiplicand == 1:
        padding = 8 - len(multiplicand)
        while padding > 0:
            multiplicandBinary.append(0)
            padding -= 1
        for char in multiplicand:
            multiplicandBinary.append(int(char))
        multiplicandBinary = twosCompliment(multiplicandBinary)
        print("Padded multiplicand",multiplicandBinary)
    elif negativeMultiplicand == 0:
        padding = 8 - len(multiplicand)
        while padding > 0:
            multiplicandBinary.append(0)
            padding -= 1
        for char in multiplicand:
            multiplicandBinary.append(int(char))


        print(multiplicand,multiplier)

    #print("Multiplier: ", multiplierBinary)
    #print("multiplicand: ", multiplicandBinary)
    q1 = 0
    count = 8
    runningproduct = [0,0,0,0,0,0,0,0]
    multiplicandCompliment = list(multiplicandBinary)
    multiplicandCompliment = twosCompliment(multiplicandCompliment)
    #print("Original compliment: ",multiplicandCompliment)
    while count != 0:
        #print("Loop: ",multiplicandCompliment)
        if multiplierBinary[-1] == 1 and q1 == 0:
            print(runningproduct, multiplicandCompliment)
            runningproduct = binaryAddition(runningproduct, multiplicandCompliment)
            #print("total check",multiplicandCompliment)
            shiftResult = shiftRight(runningproduct)
            runningproduct = shiftResult[0]
            # print("Shift2 inputs: ",shiftResult[0], shiftResult[1])
            shiftResult = shiftRight(multiplierBinary, shiftResult[1])
            q1 = shiftResult[1]
            multiplierBinary = shiftResult[0]
            count -= 1
            print("A-M and Shift: ",runningproduct, multiplierBinary, q1, multiplicandBinary)
        elif multiplierBinary[-1] == 0 and q1 == 1:
            runningproduct = binaryAddition(runningproduct, multiplicandBinary)
            shiftResult = shiftRight(runningproduct)
            runningproduct = shiftResult[0]
            shiftResult = shiftRight(multiplierBinary, shiftResult[1])
            q1 = shiftResult[1]
            multiplierBinary = shiftResult[0]
            count -=1
            print("A+M and shift: ", runningproduct, multiplierBinary, q1, multiplicandBinary)
        else:
            shiftResult = shiftRight(runningproduct)
            runningproduct = shiftResult[0]
            shiftResult = shiftRight(multiplierBinary, shiftResult[1])
            q1 = shiftResult[1]
            multiplierBinary = shiftResult[0]
            count -=1
            print("Shift : ", runningproduct, multiplierBinary, q1, multiplicandBinary)
    print(runningproduct, multiplierBinary)

main()
