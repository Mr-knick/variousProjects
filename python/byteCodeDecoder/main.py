import json

filePath = "C:/Users/brent/PycharmProjects/pythonProject/"

commandDecoderDict = {(0x00):{'DU': 0x00, 'Length': 0x00}}
# json.JSONEncoder(commandDecoderDict)
differentSequences = [b"\x00\x00\x00\x00", b"\x42\x42\x42\x42", b"\x01\x00\x00\x00", b"\x02\x00\x00\x04\x01\x00\x00\x70"]

commandDecoderJSON = json.dumps(commandDecoderDict)
with open(filePath + "commandDecoderJSON.json", "w") as file:
    file.write(commandDecoderJSON)

with open(filePath + "commandDecoderJSON.json", "r") as file:
    commandDecoderDict = json.loads(file.read())

# Save new test dat
with open(filePath + "testDatFile.dat", "wb") as file:
    binaryData = differentSequences[3] + differentSequences[2] + differentSequences[3]
    file.write(binaryData)

# Read in a dat
with open(filePath + "testDatFile.dat", "rb") as file:
    hexData = file.read().hex()

bytesArr = [hexData[i:i+2] for i in range(0, len(hexData), 2)]

print("Display Data")
print(binaryData)
print(bytesArr)

chunks = []
index = 0
while(index<len(bytesArr)):
    command = bytesArr[index:index+2]
    length = bytesArr[index+2:index+4]
    print(command)
    print(length)
    dataLen = int(length[0] + length[1])
    data = bytesArr[index+4:dataLen+4]
    print(data)
    index += 4+dataLen
    print(index)

# take binary data. Ignore how it prints to screen
# grab the value of first bit shift left
shiftedLeftVal = binaryData[0]<< 4
shiftedLeftVal += 0x04

print(shiftedLeftVal)

# for searching through dictionary
# always move through binaryData but use hex convert to get decoder data
binaryData[0:2].hex()
{'0200': True}[binaryData[0:2].hex()]

{b'0200': True}
