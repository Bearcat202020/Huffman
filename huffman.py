import operator


class ComparableNode:

    def __init__(self, char, freq, left, right):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def isLeaf(self):
        #will be None if not leaf
        return not (self.char == None)

    def compareTo(self, node):
        #will return 1 for greater, 0 for equal, and -1 for less
        if(self.freq > node.freq):
            return 1
        elif(self.freq == node.freq):
            return 0
        else:
            return -1

    def __repr__(self):
        return "Node-{char: " + str(self.char) + ", freq: " + str(self.freq) + "}"

    def shorterToString(self):
        return "(" + str(self.freq) + "," + str(self.char) + ")"


class HuffmanTree:
    def __init__(self, file):
        self.file = file
        self.nodes = self.__grabFromFile()
        self.root = None

        self.cDict = {}

        #private instance data that helps with __repr__
        self.__arrForPrinting = []
        self.__deepest = 1
        self.__treeBin = ""


        self.__makeTree()

    def __grabFromFile(self):
        #opens file and grabs text
        f = open(self.file + '.txt', 'r')
        text = f.read()

        #makes a dictionary with all the characters and frequencies
        dict = {}
        for char in text:
            if char in dict:
                dict[char] += 1
            else:
                dict[char] = 1

        #sorts the frequencies and puts them into one array of nodes
        nodes = []
        keys = dict.keys()
        vals = dict.values()
        keys2 = []
        vals2 = []
        for key in keys:
            keys2.append(key)
        for value in vals:
            vals2.append(value)
        vals2, keys2 = zip(*sorted(zip(vals2, keys2)))
        for i in range(len(keys2)):
            nodes.append(ComparableNode(keys2[i], vals2[i], None, None))
        return nodes

    def __makeTree(self):
        while(len(self.nodes) > 1):
            combinedFreq = self.nodes[0].freq + self.nodes[1].freq
            newNode = ComparableNode(None, combinedFreq,  self.nodes[0], self.nodes[1])
            self.root = newNode
            self.__addToList(newNode)
            self.nodes = self.nodes[2:]

    def __addToList(self, newNode):
        i = 0
        while(i < len(self.nodes) and newNode.freq > self.nodes[i].freq):
            i += 1
        self.nodes.insert(i, newNode)

    def __getAllOfOneHeight(self, node, height, counter):
        #counter should always start at 1
        if(counter > height):
            pass
        elif(counter == height):
            self.__arrForPrinting.append(node)
        else:
            if(node.right != None):
                self.__getAllOfOneHeight(node.right, height, counter + 1)
            if(node.left != None):
                self.__getAllOfOneHeight(node.left, height, counter + 1)

    def __findDeepest(self, node, counter):
        if(node.right != None):
            self.__findDeepest(node.right, counter + 1)
        if(node.left != None):
            self.__findDeepest(node.left, counter + 1)
        if(counter > self.__deepest):
            self.__deepest = counter


    def __recCompress(self, node, left, right, bit):
        if(left == 1):
            bit += "1"
        elif(right == 1):
            bit += "0"

        if(node.right == None and node.left == None):
            self.cDict[node.char] = bit
        if(node.right != None):
            self.__recCompress(node.right, 0, 1, bit)
        if(node.left != None):
            self.__recCompress(node.left, 1, 0, bit)

    def __recCompressTree(self, node):
        if(node.right != None):
            self.__recCompressTree(node.right)
        if(node.left != None):
            self.__recCompressTree(node.left)
        if(node.char != None):
            self.__treeBin += str(node)

    def getTree(self):
        self.__recCompress(self.root, 0, 0, "")
        self.__recCompressTree(self.root)
        return self.cDict, self.__treeBin


    def __repr__(self):
        self.__findDeepest(self.root, 1)
        i = 1
        printStr = ""
        while(i <= self.__deepest):
            self.__arrForPrinting = []
            self.__getAllOfOneHeight(self.root, i, 1)
            spacing = int((24 /(len(self.__arrForPrinting) + 1)))
            spaces = " " * spacing
            for elem in self.__arrForPrinting:
                #makes it so newline doesn't print on its own
                if(elem.char == "\n"):
                    elem.char = "\\n"
                printStr += spaces + elem.shorterToString()
            printStr += "\n"
            i += 1

        return printStr

def compress(frm, to, h):
    dict, treeBin = h.getTree()
    f = open(to + '.txt', 'w')
    f2 = open(frm + '.txt', 'r')
    text = f2.read()
    compressedText = ""
    compressedText += ''.join(format(ord(x), 'b') for x in treeBin) + "\n"
    for char in text:
        if char in dict:
            compressedText += dict[char]
    f.write(compressedText)

def deCompress(frm, to, h):
    f = open(frm + '.txt', 'r')
    f2 = open(to + '.txt', 'w')
    text = f.read()
    text = text[text.index('\n'):]
    newStr = ""
    node = h.root
    while(len(text) > 1):
        while(node.right != None and node.left != None):
            if(text[0] == "0"):
                node = node.right
            elif(text[0] == "1"):
                node = node.left
            text = text[1:]
        newStr += node.char
        node = h.root
    f2.write(newStr)

def compressionRate(textFile, compressedTextFile):
    f = open(textFile + '.txt', 'r')
    f2 = open(compressedTextFile + '.txt', 'r')
    text = f.read()
    compressedText = f2.read()
    bits1 = 0
    for char in text:
        bits1 += 32
    bits2 = 0
    for char in compressedText:
        bits2 += 1
    return (1 - float(bits2)/bits1) * 100

def main():
    h = HuffmanTree('text')

    compress('text', 'compressed', h)
    deCompress('compressed', 'text2', h)
    print('compression rate:', compressionRate('text', 'compressed'))
    print(h)


if __name__ == "__main__":
    main()
