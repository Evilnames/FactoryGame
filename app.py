from Factory.building import building
import os, time

tickElapsed = 0

#Define a sample building
oil = building()
oil.name = "Oil Producer"
oil.outputGood = "Oil"
oil.maxOutputProduction = 2
oil.productionTime = 2
oil.outputStorageCapcity = 30

#Cement factory building
cement = building()
cement.name="Cement Factory"
cement.outputGood = "cement"
cement.maxOutputProduction = 1
cement.productionTime = 4
cement.outputStorageCapcity = 30
cement.inputGoods = {
    0 : {"inputRequired" : 2, "maxStorage" : 30, "currentInputStorage" : 2, "inputGoodName":"gravel"}
}

# Main game loop
while(1):
    os.system('clear')
    print(tickElapsed)

    oil.tick()
    cement.tick()

    print("Current Oil Output Pending ", oil.outputGoodsWaiting)
    print("Current Cement Output", cement.outputGoodsWaiting)

    tickElapsed += 1
    time.sleep(1)