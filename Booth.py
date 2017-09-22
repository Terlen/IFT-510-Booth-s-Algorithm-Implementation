# Aidan Payne
# IFT 510 Booth's Algorithm Implementation

# Import deque to help implement arithmetic shifting
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
    # Reverse string so addition occurs from LSB to MSB
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
    # Once addition is completed, reverse string back into correct MSB -> LSB
    compliment.reverse()
    return compliment

# Function to perform binary addition of two values
def binaryAddition(value1,value2):
    binarySum = []
    reverseValue2 = list(value2)
    # Reverse values to perform addition from LSB to MSB
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

# Function to perform arithmetic right shift. Pass a value to be shifted and an optional bit being carried into the shift (A0 -> Qn)
def shiftRight(value, addedBit=None):
    shiftedValue = deque(value)
    if shiftedValue[0] == 0 and addedBit is None:
        shiftedValue.appendleft(0)
    elif shiftedValue[0] == 1 and addedBit is None:
        shiftedValue.appendleft(1)
    elif addedBit is not None:
        shiftedValue.appendleft(addedBit)
    # Bit shifted off the end of multiplier should be preserved and stored in Q-1
    extraBit = shiftedValue.pop()
    shiftedExtra = [list(shiftedValue),extraBit]
    return shiftedExtra

# Main function to perform Booth's algorithm given a decimal or binary multiplicand and multiplier
def main():
    q1 = 0
    count = 8
    runningproduct = [0,0,0,0,0,0,0,0]
    product = '0b'
    productPositive = []
    paddingStop = 0
    negate = 0
    multiplicandBinary = []
    multiplierBinary = []
    negativeMultiplier = 0
    negativeMultiplicand = 0
    multiplicand = input("Please enter the multiplicand: ")
    multiplier = input("Please enter the multiplier: ")
    # Input is two 8 bit values
    if len(multiplicand) == 8 and len(multiplier)== 8:
        for char in multiplicand:
            multiplicandBinary.append(int(char))
            #print
        for char in multiplier:
            multiplierBinary.append(int(char))
    # Input is one 8 bit value and one decimal value
    elif len(multiplicand) == 8 and len(multiplier) != 8:
        print("Please enter two binary or two decimal values")
        exit()
    elif len(multiplicand) !=8 and len(multiplier) == 8:
        print("Please enter two binary or two decimal values")
        exit()
    # Input is two decimal values
    else:
        if multiplicand[0] is '-':
            negativeMultiplicand = 1
            multiplicand = multiplicand[1:]
        if multiplier[0] is '-':
            negativeMultiplier = 1
            multiplier = multiplier[1:]
        # Convert decimal value to binary string representation
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
        elif negativeMultiplicand == 0:
            padding = 8 - len(multiplicand)
            while padding > 0:
                multiplicandBinary.append(0)
                padding -= 1
            for char in multiplicand:
                multiplicandBinary.append(int(char))
    # Calculate compliment of multiplcand for later operations
    multiplicandCompliment = list(multiplicandBinary)
    multiplicandCompliment = twosCompliment(multiplicandCompliment)
    # Booth Algorithm
    while count != 0:
        # A = A - M and Shift
        if multiplierBinary[-1] == 1 and q1 == 0:
            runningproduct = binaryAddition(runningproduct, multiplicandCompliment)
            shiftResult = shiftRight(runningproduct)
            runningproduct = shiftResult[0]
            shiftResult = shiftRight(multiplierBinary, shiftResult[1])
            q1 = shiftResult[1]
            multiplierBinary = shiftResult[0]
            count -= 1
        # A = A + M and Shift
        elif multiplierBinary[-1] == 0 and q1 == 1:
            runningproduct = binaryAddition(runningproduct, multiplicandBinary)
            shiftResult = shiftRight(runningproduct)
            runningproduct = shiftResult[0]
            shiftResult = shiftRight(multiplierBinary, shiftResult[1])
            q1 = shiftResult[1]
            multiplierBinary = shiftResult[0]
            count -=1
        # Only Shift
        else:
            shiftResult = shiftRight(runningproduct)
            runningproduct = shiftResult[0]
            shiftResult = shiftRight(multiplierBinary, shiftResult[1])
            q1 = shiftResult[1]
            multiplierBinary = shiftResult[0]
            count -=1
    # Combine multiplier and runningproduct to create 16 bit result
    for bit in multiplierBinary:
        runningproduct.append(bit)
    for bit in runningproduct:
        product += str(bit)
    # If either multiplier or multiplicand were negative, change sign of final product
    if ((negativeMultiplicand == 1 or negativeMultiplier == 1) and not (negativeMultiplicand == 1 and negativeMultiplier == 1)) or product[3] is '1':
        # Undo two's compliment to obtain positive binary value
        product = bin(int(product,2)-1)[2:]
        for bit in product:
            productPositive.append(int(bit))
        productPositive = bitInversion(productPositive)
        product = '0b'
        for bit in productPositive:
            product += str(bit)
        negate = 1
    # Print output. If answer should be negative, negate the value.
    if negate == 1:
        print(int(product,2)*-1)
    else:
        print(int(product,2))

# Main function call
main()
