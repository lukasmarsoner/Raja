import json

with open('gendering.json', 'r', encoding='utf-8') as jsonFile:
    jsonStr = jsonFile.read()
    gendering = json.loads(jsonStr)

with open('Raja.txt', 'r', encoding='utf-8') as fd:
    story = fd.read()

story = story.replace('#username', 'Luna')
for map in gendering:
    story = story.replace('#'+map, gendering[map]['w'])

with open('Vorlesen.txt', 'w', encoding='utf-8') as fd:
    print(story, file=fd)
