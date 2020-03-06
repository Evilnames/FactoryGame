from Factory.building import building
from Factory.conveyor import conveyor
import os, time

def allowedQuantity(quantity, howMuchAllowed):
    allowed = 0
    difference = howMuchAllowed - quantity

    if(difference >= 0):
        allowed = quantity
    else:
        #1 Space but 2 quantity, we should accept 1
        #1-2 = -1
        allowed = howMuchAllowed

    return allowed


def testConveyors(buildings, conveyors):
    for building in buildings:
        if(len(building.connectedConveyor) > 0):
            #Will be the name of the conveyor belt
            for connectedItem in building.connectedConveyor:
                buildingPullConveyor(building, conveyors, connectedItem)

def buildingPullConveyor(building, conveyors, connectedItem):

    #Loop through each conveyor here
    for conveyor in conveyors:
        #If the conveyor is matching what is connected -- we could also create an index
        #Of all conveyor belts with an ending point that falls within the factory...
        if(conveyor.name == connectedItem):
            #Get the top layer of the stack
            convoyerFrontOfStack = conveyor.getCurrentTopOfConvoyer()
            conveyor.processedThisTick = 1
            if(convoyerFrontOfStack != None):
                howMuchAllowed = building.howMuchOfGoodCanITake(convoyerFrontOfStack["inputGood"])
                if(howMuchAllowed > 0):
                    quantityToAccept = allowedQuantity(convoyerFrontOfStack["quantity"], howMuchAllowed)
                    building.acceptIncomingGood(convoyerFrontOfStack["inputGood"], quantityToAccept)
                    conveyor.removeOutgoingGood(quantityToAccept)

            #check Connecting conveyors
            checkConnectingConveyors(conveyor, conveyors, buildings)
    

def checkConnectingConveyors(conveyor, conveyors, buildings):
    #Check to see if something is connected too me
    conveyorFound = 0
    for conveyorSister in conveyors:
        if(conveyorSister.outCoords['x'] == conveyor.coords['x'] and conveyorSister.outCoords['y'] == conveyor.coords['y']):
            conveyorFound = 1
            pullConveyor(conveyorSister, conveyor)
            checkConnectingConveyors(conveyorSister, conveyors, buildings)
    #If we didn't find anything check the buildings
    if(conveyorFound == 0):
        for building in buildings:
            if(building.coords['x'] == conveyor.inCoords['x'] and building.coords['y'] == conveyor.inCoords['y']):
                pullFromBuilding(conveyor, building)

def pullConveyor(conveyorDownstream, conveyorUpstream):
    #Conv 1 pull from Conv 2
    frontOfStack = conveyorDownstream.getCurrentTopOfConvoyer()
    conveyorDownstream.processedThisTick = 1
    if(frontOfStack != None):
        allowedC1 = conveyorUpstream.howMuchOfGoodCanITake()
        if(allowedC1 > 0):
            quantityToAccept = allowedQuantity(frontOfStack["quantity"], allowedC1)
            conveyorUpstream.acceptIncomingGood(frontOfStack["inputGood"], quantityToAccept)
            conveyorDownstream.removeOutgoingGood(quantityToAccept)

def pullFromBuilding(conveyor, building):
    #Conv 3 pull from Oil factory
    getQueue = building.getOutputQuantity()
    if(getQueue != 0):
        allowedPullAmount = conveyor.howMuchOfGoodCanITake()
        if(allowedPullAmount > 0):
            quantityToAccept = allowedQuantity(getQueue, allowedPullAmount)
            conveyor.acceptIncomingGood(building.outputGood, quantityToAccept)
            building.removeOutgoingGood(quantityToAccept)


buildings = []
conveyors = []

tickElapsed = 0

conveyor1 = conveyor()
conveyor1.coords['x'] = 3
conveyor1.coords['y'] = 2
conveyor1.inCoords['x'] = 4
conveyor1.inCoords['y'] = 2
conveyor1.outCoords['x'] = 2
conveyor1.outCoords['y'] = 2
conveyor1.name = "C1"

conveyor2 = conveyor()
conveyor2.coords['x'] = 4
conveyor2.coords['y'] = 2
conveyor2.inCoords['x'] = 4
conveyor2.inCoords['y'] = 3
conveyor2.outCoords['x'] = 3
conveyor2.outCoords['y'] = 2
conveyor2.name = "C2"

conveyor3 = conveyor()
conveyor3.coords['x'] = 4
conveyor3.coords['y'] = 3
conveyor3.inCoords['x'] = 4
conveyor3.inCoords['y'] = 4
conveyor3.outCoords['x'] = 4
conveyor3.outCoords['y'] = 2
conveyor3.name = "C3"

conveyor4 = conveyor()
conveyor4.coords['x'] = 1
conveyor4.coords['y'] = 3
conveyor4.inCoords['x'] = 1
conveyor4.inCoords['y'] = 1
conveyor4.outCoords['x'] = 1
conveyor4.outCoords['y'] = 4
conveyor4.name = "C4"

conveyors.append(conveyor1)
conveyors.append(conveyor2)
conveyors.append(conveyor3)
conveyors.append(conveyor4)

# conveyor[0] = conveyor()
# conveyor[1] = conveyor()
# conveyor[2] = conveyor()
#   0  1  2  3  4  5  6
# 0 
# 1    x  x
# 2    x  x  =  =
# 3    =        =
# 4    X  X     x  x
# 5    X  X     x  x
# 6



#Define a sample building
oil = building()
oil.name = "Oil Producer"
oil.outputGood = "oil"
oil.maxOutputProduction = 2
oil.productionTime = 2
oil.outputStorageCapcity = 30
oil.coords['x'] = 4
oil.coords['y'] = 4
oil.coords['xSize'] = 2
oil.coords['ySize']= 2

buildings.append(oil)

#Cement factory building
cement = building()
cement.name="Cement Factory"
cement.outputGood = "cement"
cement.maxOutputProduction = 1
cement.productionTime = 4
cement.outputStorageCapcity = 30
cement.inputGoods = {
    0 : {"inputRequired" : 2, "maxStorage" : 30, "currentInputStorage" : 0, "inputGood":"oil"}
}
cement.coords['x'] = 1
cement.coords['y'] = 1
cement.coords['xSize'] = 2
cement.coords['ySize']= 2
cement.connectedConveyor.append("C1")
buildings.append(cement)

cementSeller = building()
cementSeller.name = "Cement Seller"
cementSeller.outputGood = "money"
cementSeller.maxOutputProduction = 1
cementSeller.productionTime = 2
cementSeller.outputStorageCapcity = 99
cementSeller.productionTime = 1
cementSeller.inputGoods = {
    0 : {"inputRequired" : 1, "maxStorage" : 999, "currentInputStorage":0, "inputGood":"cement"}
}
cementSeller.coords['x'] = 1
cementSeller.coords['y'] = 4
cementSeller.coords['xSize'] = 2
cementSeller.coords['ySize']= 2
cementSeller.connectedConveyor.append("C4")
buildings.append(cementSeller)

# Main game loop
while(1):
    os.system('clear')
    print(tickElapsed)

    # Make sure that the conveyors get reset and dont get processed twice in one turn.
    for conveyor in conveyors:
        conveyor.processedThisTick = 0


    #All buildings produce things
    for building in buildings:
        building.tick()

    #Loop through each building and see if they are at the end of a conveyor belt
    testConveyors(buildings, conveyors)

    for building in buildings:
        print("Current " + building.name + " output pending : " + str(building.outputGoodsWaiting))

    for conveyor in conveyors:
        print(conveyor.name + " Goods : " + str(conveyor.inputGoods))


    tickElapsed += 1
    time.sleep(1)

