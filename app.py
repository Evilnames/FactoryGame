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

tickElapsed = 0

conveyor1 = conveyor()
conveyor1.coords['x'] = 3
conveyor1.coords['y'] = 2
conveyor1.inCoords['x'] = 4
conveyor1.inCoords['y'] = 2
conveyor1.outCoords['x'] = 2
conveyor1.outCoords['y'] = 2

conveyor2 = conveyor()
conveyor2.coords['x'] = 4
conveyor2.coords['y'] = 2
conveyor2.inCoords['x'] = 4
conveyor2.inCoords['y'] = 3
conveyor2.outCoords['x'] = 3
conveyor2.outCoords['y'] = 2

conveyor3 = conveyor()
conveyor3.coords['x'] = 4
conveyor3.coords['y'] = 3
conveyor3.inCoords['x'] = 4
conveyor3.inCoords['y'] = 4
conveyor3.outCoords['x'] = 4
conveyor3.outCoords['y'] = 2


# conveyor[0] = conveyor()
# conveyor[1] = conveyor()
# conveyor[2] = conveyor()
#   0  1  2  3  4  5  6
# 0 
# 1    x  x
# 2    x  x  =  =
# 3             =
# 4             x  x
# 5             x  x
# 6




#Define a sample building
oil = building()
oil.name = "Oil Producer"
oil.outputGood = "Oil"
oil.maxOutputProduction = 2
oil.productionTime = 2
oil.outputStorageCapcity = 30
oil.coords['x'] = 1
oil.coords['y'] = 1
oil.coords['xSize'] = 2
oil.coords['ySize']= 2

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
cement.coords['x'] = 4
cement.coords['y'] = 4
cement.coords['xSize'] = 2
cement.coords['ySize']= 2


# Main game loop
while(1):
    os.system('clear')
    print(tickElapsed)

    #All buildings produce things
    cement.tick()
    oil.tick()


    #Convoyers that are connected to buildings pull forward
    #Test version to test convoyers working with specific inputs/outputs
    convoyerFrontOfStack = conveyor1.getCurrentTopOfConvoyer()
    if(convoyerFrontOfStack != None):
        howMuchAllowed = cement.howMuchOfGoodCanITake(convoyerFrontOfStack["inputGood"])
        if(howMuchAllowed > 0):
            quantityToAccept = allowedQuantity(convoyerFrontOfStack["quantity"], howMuchAllowed)
            cement.acceptIncomingGood(convoyerFrontOfStack["inputGood"], quantityToAccept)
            conveyor1.removeOutgoingGood(quantityToAccept)

    #Conv 1 pull from Conv 2
    conv2FrontOfStack = conveyor2.getCurrentTopOfConvoyer()
    if(conv2FrontOfStack != None):
        allowedC1 = conveyor1.howMuchOfGoodCanITake()
        if(allowedC1 > 0):
            quantityToAccept = allowedQuantity(conv2FrontOfStack["quantity"], allowedC1)
            conveyor1.acceptIncomingGood(conv2FrontOfStack["inputGood"], quantityToAccept)
            conveyor2.removeOutgoingGood(quantityToAccept)

    #Conv 2 pull from Conv 3
    conv3FrontOfStack = conveyor3.getCurrentTopOfConvoyer()
    if(conv3FrontOfStack != None):
        allowedC2 = conveyor2.howMuchOfGoodCanITake()
        if(allowedC2 > 0):
            quantityToAccept = allowedQuantity(conv3FrontOfStack["quantity"], allowedC2)
            conveyor2.acceptIncomingGood(conv3FrontOfStack["inputGood"], quantityToAccept)
            conveyor3.removeOutgoingGood(quantityToAccept)

    #Conv 3 pull from Oil factory
    oilGetQueue = oil.getOutputQuantity()
    if(oilGetQueue != 0):
        allowedC3 = conveyor3.howMuchOfGoodCanITake()
        if(allowedC3 > 0):
            quantityToAccept = allowedQuantity(oilGetQueue, allowedC3)
            conveyor3.acceptIncomingGood("oil", quantityToAccept)
            oil.removeOutgoingGood(quantityToAccept)

    print("C1 : ", conveyor1.inputGoods)
    print("C2 : ", conveyor2.inputGoods)
    print("C3 : ", conveyor3.inputGoods)
        
    print("Current Oil Output Pending ", oil.outputGoodsWaiting)
    print("Current Cement Output:", cement.outputGoodsWaiting)
    print("Current Cement Oil Input:", cement.inputGoods[0]['currentInputStorage'])

    tickElapsed += 1
    time.sleep(1)

