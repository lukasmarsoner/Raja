import json

jsonFile = open('geschichte.json', encoding='utf-8')
jsonStr = jsonFile.read()
screens = json.loads(jsonStr)['screens']

#Find indexes to screens
indexes = []
for i in range(len(screens)):
    indexes.append(screens[i]['number'])

#This array keeps track of paths not taken
openOptions = []
openScreens = []
branchesSeen = []
screensSeenCounter = [0 for i in screens]
atEnd = False

#We will run through all possible paths - endings will
#be marked by fowarting to 999
i = 0
while not(atEnd):
    #See if we have been here before
    if i in openScreens:
        #Find first entry for current screen
        newOpt = openScreens.index(i)
        #Move to next screen
        i = openOptions[newOpt]
        screensSeenCounter[i] += 1
        #Remove existing entry
        openScreens.pop(newOpt)
        openOptions.pop(newOpt)
    else:
        if len(screens[i]['forwards']) > 1 and i not in branchesSeen:
            #Make sure we dont get back to branching-points
            #Already seen and add old paths again
            branchesSeen.append(i)
            for j in screens[i]['forwards'][1:]:
                openOptions.append(j)
                openScreens.append(i)
        #Find the array-index the forward refers to
        try:
            if screens[i]['forwards'][0] != 999:
                forward = indexes.index(screens[i]['forwards'][0])
            else:
                forward = 999
        except:
            print('Incorrect Forward')
        #Check loops - we should not see the same screen more than ten times
        if max(screensSeenCounter) > 10:
            raise ValueError('Circular Forward found at screen {}'.format(indexes[i]))
        #Check if we have reached an endpoint
        if forward == 999:
            #If there any open screens left - move to one of them
            if len(openScreens) != 0:
                newOpt = openScreens[0]
                #Move to next screen
                i = openOptions[0]
                screensSeenCounter[i] += 1
                #Remove existing entry
                openScreens.pop(0)
                openOptions.pop(0)
            #Otherwise we are done
            else:
                atEnd = True
        else:
            i = forward
            screensSeenCounter[i] += 1
