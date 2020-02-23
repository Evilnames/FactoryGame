class building:
    def __init__(self):
        #Filler Text
        self.name                    = ""
        self.outputGood              = ""
        
        #General Attributes

        #Input Rules
        ##What goods do I need?  This should be stored as a dictionaries of dictionaries
        ### IE inputGoods.append('oil' : {'inputGoodName':'cement', inputRequired' : 2, 'maxStorage':80, 'currentInputStorage':0})
        self.inputGoods = {}

        #Connected conveyor
        self.connectedConveyor = {}

        #Output Rules
        ##How many goods can I produce at one time?
        self.maxOutputProduction     = 0
        ##How long does it take to produce one unit?
        self.productionTime          = 0
        ##How many goods can I hold before being backed up?
        self.outputStorageCapcity    = 0


        #Location on Grid
        self.coords = {'x':0,'y':0,'xSize':0,'ySize':0}

        #State
        self.ticksSinceLastOutput    = 0
        self.outputGoodsWaiting      = 0

    def checkProduction(self):
        #Produce something
        if(self.ticksSinceLastOutput >= self.productionTime):
            if((self.outputGoodsWaiting + self.maxOutputProduction <= self.outputStorageCapcity) and self.doIHaveEnoughInputResources()):
                self.outputGoodsWaiting += self.maxOutputProduction
                self.reduceInputResources()
                self.ticksSinceLastOutput = 0
            
    #Checks to see if I have enough input resources.
    #If I have no input requirements I am the start of the chain for
    #production
    def doIHaveEnoughInputResources(self):
        if(len(self.inputGoods) == 0):
            return 1
        else:
            allowProduction = 1

            #Loop through our input goods and see if we have all the required inputs
            for i, item in self.inputGoods.items():
                if(item['inputRequired'] > item['currentInputStorage']):
                    allowProduction = 0
            return allowProduction

    #Reduces the pool of resources sitting in this factory
    def reduceInputResources(self):
        if(len(self.inputGoods) > 0):
            for i,item in self.inputGoods.items():
                self.inputGoods[i]['currentInputStorage'] -=  item['inputRequired']

    #Test's if this factory can accept an incoming good.
    #Used to test from convoyor belts
    def howMuchOfGoodCanITake(self, good):
        howMuchCanIAccept = 0
        for i, item in self.inputGoods.items():
         
            if(item['inputGood'] == good):
                howMuchCanIAccept = item['maxStorage'] - item['currentInputStorage']
        return howMuchCanIAccept

    #Accepts an input of a good
    def acceptIncomingGood(self, good, quantity):
        for i,item in self.inputGoods.items():
            if(item['inputGood'] == good):
                self.inputGoods[i]['currentInputStorage'] += quantity

    def getOutputQuantity(self):
        return self.outputGoodsWaiting

    def removeOutgoingGood(self, quantity):
        self.outputGoodsWaiting -= quantity 

    #Called each time
    def tick(self):
        self.checkProduction()

        #Increase last production time
        self.ticksSinceLastOutput += 1
