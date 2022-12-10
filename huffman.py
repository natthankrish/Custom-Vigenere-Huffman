# Global Variable Declaration
listHuffmanCodes = dict()
listEncodedHuffmanCodes = dict()
priorityList = [
    'A', 'B', 'C', 'D', 'E',
    'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y',
    'Z', 'a', 'b', 'c', 'd',
    'e', 'f', 'g', 'h', 'i',
    'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x',
    'y', 'z', ' ', '!', '?',
    ',', '.', '-', '_', '&',
    '(', ')', '[', ']'
]

# Class Declaration
class Node:
    def __init__(self, listchar, frequency, prio, left, right):
        self.frequency = frequency
        self.listchar = listchar
        self.prio = prio
        self.left = left
        self.right = right
        self.code = ''
    
# Function/Procedure Declaration    
def countCharacter(stringinput):
    chartable = dict()

    for charinput in stringinput:
        if chartable.get(charinput) == None:
            chartable[charinput] = 1
        else:
            chartable[charinput] += 1

    return chartable

def huffmanTreeCode(nodeTree, currentCode=''):
    newCode = currentCode + str(nodeTree.code)

    if (nodeTree.left):
        huffmanTreeCode(nodeTree.left, newCode)
    if (nodeTree.right):
        huffmanTreeCode(nodeTree.right, newCode)
    
    if not nodeTree.left and not nodeTree.right:
        listHuffmanCodes[nodeTree.listchar] = newCode
    
    return listHuffmanCodes

def outputHuffmanCode(stringinput, listHuffmanCodes):
    encoding = []
    for charinput in stringinput:
        print(listHuffmanCodes[charinput], end='')
        encoding.append(listHuffmanCodes[charinput])
    string = ''.join([str(item) for item in encoding])
    return string

def totalGain(stringinput, listHuffmanCodes):
    original = len(stringinput)*8
    compressed = 0
    listchar = listHuffmanCodes.keys()
    for char in listchar:
        count = stringinput.count(char)
        compressed += count * len(listHuffmanCodes[char])
    # print("before: ", original)
    # print("after: ", compressed)

def huffmanEncoding(stringinput):
    listcharfrequency = countCharacter(stringinput)
    listchar = listcharfrequency.keys()
    listfrequency = listcharfrequency.values()

    # print("symbols: ", listchar)
    # print("frequency: ", listfrequency)

    huffmanTreeNode = []

    for char in listchar:
        huffmanTreeNode.append(Node(char, listcharfrequency.get(char), priorityList.index(char), None, None))

    while (len(huffmanTreeNode) > 1):
        huffmanTreeNode = sorted(huffmanTreeNode, key=lambda x: (x.frequency, x.prio))


        left = huffmanTreeNode[0]
        right = huffmanTreeNode[1]

        if left.prio > right.prio:
            left, right = right, left

        left.code = 0
        right.code = 1

        if left.prio < right.prio:
            newNodeTree = Node(left.listchar + right.listchar, left.frequency + right.frequency, left.prio, left, right)
        else:
            newNodeTree = Node(left.listchar + right.listchar, left.frequency + right.frequency, right.prio, left, right)

        huffmanTreeNode.remove(left)
        huffmanTreeNode.remove(right)
        huffmanTreeNode.append(newNodeTree)

    huffmanEncodingResult = huffmanTreeCode(huffmanTreeNode[0])
    #print(huffmanEncodingResult)
    totalGain(stringinput, huffmanEncodingResult)
    #print("encoded output: ", outputHuffmanCode(stringinput, huffmanEncodingResult))

def vigenereEncode(stringinput, password):
    encodedText = ''
    for i in range (0, len(stringinput)):
        lengthHuffman = len(listHuffmanCodes[stringinput[i]])
        passwordchar = password[i%len(password)]
        key = priorityList.index(stringinput[i]) + priorityList.index(passwordchar) + lengthHuffman
        encodedChar = priorityList[key%len(priorityList)]
        keyoffset = len(listHuffmanCodes[stringinput[i]])
        while encodedChar in listEncodedHuffmanCodes.keys():
            encodedChar = priorityList[(priorityList.index(encodedChar)+1)%len(priorityList)]
            keyoffset = keyoffset + 1
        listEncodedHuffmanCodes[encodedChar] = keyoffset
        encodedText += encodedChar
    return encodedText

def vigenereDecode(decodedText, password):
    originalText = ''
    for i in range (0, len(decodedText)):
        passwordchar = password[i%len(password)]
        key = priorityList.index(decodedText[i]) - priorityList.index(passwordchar) - listEncodedHuffmanCodes[decodedText[i]]
        originalText += priorityList[key%len(priorityList)]
    return originalText

passkey = input("Enter your password: ")
stringinput = input("Enter your message: ")
huffmanEncoding(stringinput)
print("Psst.. It's a Secret: ", end='')
secrettext = vigenereEncode(stringinput, passkey)
print(secrettext)
print("Check Decode ", end='')
print(vigenereDecode(secrettext, passkey))

