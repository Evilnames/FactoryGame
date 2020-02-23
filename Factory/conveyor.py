class conveyor:

    def __init__(self):
        #Location on Grid
        self.coords = {'x':0,'y':0,'xSize':1,'ySize':1}

        self.inCoords = {'x':0, 'y':0}
        self.outCoords = {'x':0, 'y':0}

        self.timeSinceLastMoved = 0
        self.timeToMove = 1
        self.maximumAllowedQuantity = 2
        self.currentQuantityAmount = 0

        # {inputGood : "Cement", quantity:2}
        self.inputGoods = {}

    def getCurrentTopOfConvoyer(self):
        if(len(self.inputGoods) > 0):
            return self.inputGoods[0]

    def removeOutgoingGood(self, quantity):
        self.inputGoods[0]['quantity'] -= quantity
        self.currentQuantityAmount -= quantity
        if(self.inputGoods[0]['quantity'] == 0):
            #Remove this item from the dictionary
            self.inputGoods.pop(0)

    #Convoyers can take any good
    def howMuchOfGoodCanITake(self):
        allowed = self.maximumAllowedQuantity - self.currentQuantityAmount
        return allowed

    def acceptIncomingGood(self, good, quantity):
        curSize = len(self.inputGoods)
        self.currentQuantityAmount += quantity
        #Convoyer empty, add me
        if(curSize == 0):
            self.inputGoods[0] = {'inputGood' : good, 'quantity' : quantity}
        #There is one thing on the stack
        elif(curSize == 1):
            if(self.inputGoods[0]['inputGood'] == good):
                self.inputGoods[0]['quantity'] += quantity
            else:
                self.inputGoods[1] = {'inputGood' : good, 'quantity' : quantity}
        else:
            if(self.inputGoods[curSize - 1]['inputGood'] == good):
                self.inputGoods[curSize - 1] += quantity 
            else:
                self.inputGoods[curSize] = {'inputGood' : good, 'quantity' : quantity} 



    #Called each time
    def tick(self):
        pass
