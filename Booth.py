# Aidan Payne
# IFT 510 Booth's Algorithm Implementation


# User Input
multiplicand = input("Please enter the multiplicand: ")
multiplier = input("Please enter the multiplier: ")

# Function that inverts a binary value.
def bitInversion(invert):
    for index, item in enumerate(invert):
        if item == 1:
            invert[index] = 0
        elif item == 0:
            invert[index] = 1
    return invert

# Function to find two's compliment value of a given binary value
def twosCompliment(compliment):
    compliment = bitInversion(compliment)
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
        elif item == 1 and carry == 1:
            compliment[index] = 0
            carry = 0
    compliment.reverse()
    return compliment

def binaryAddition(value1,value2):
    binarySum = []
    for f,b in zip(value1, value2):
        print(f, b)

# Array definition
multiplicandBinary = []
multiplierBinary = []
runningproduct = 0
q1 = 0
count = 8

for char in multiplicand:
    multiplicandBinary.append(int(char))
for char in multiplier:
    multiplierBinary.append(int(char))

# print("Binary Multiplicand: ",multiplicandBinary)
# print("Binary Multiplier: ",multiplierBinary)
print(twosCompliment(multiplicandBinary))
print(binaryAddition(multiplicandBinary, multiplierBinary))
