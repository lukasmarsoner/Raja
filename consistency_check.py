import json
import anybadge

def moveToNextScreen(iScreen, options, screens):
    _iScreen = iScreen
    iScreen = screens[iScreen]['forwards'][options[iScreen]['current']]
    options[_iScreen]['current'] += 1
    if options[_iScreen]['current'] == options[_iScreen]['total']:
        options[_iScreen]['current'] -= 1
    return iScreen, options

with open('geschichte.json', 'r', encoding='utf-8') as jsonFile:
    jsonStr = jsonFile.read()
    _screens = json.loads(jsonStr)['screens']

screens = {}
options = {}
nPaths = 1
for i in range(len(_screens)):
    screens[_screens[i]['number']] = _screens[i]
    options[_screens[i]['number']] = {'current': 0,
                                      'total': len(screens[_screens[i]['number']]['forwards'])}
    if options[_screens[i]['number']]['total'] > 1:
        nPaths += options[_screens[i]['number']]['total'] - 1

del _screens

maxStepsToEnding = 200

for _iPath in range(nPaths):
    iScreen = 0
    for i in range(maxStepsToEnding):
        iScreen, options = moveToNextScreen(iScreen, options, screens)
        if iScreen == 888:
            break
        if i == maxStepsToEnding -1:
            raise ValueError('Potential loop found!')
   
print('All checks complete and successful!')

#Define thresholds: <2=red, <4=orange <8=yellow <10=green
thresholds = {2: 'red',
              4: 'orange',
              6: 'yellow',
              10: 'green'}

badge = anybadge.Badge('Anzahl Geschichten', str(int(nPaths)), thresholds=thresholds)

badge.write_badge('paths.svg')
