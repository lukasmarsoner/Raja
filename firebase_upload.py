import json
import firebase_admin
import os
from firebase_admin import firestore

with open('geschichte.json', 'r', encoding='utf-8') as jsonFile:
    jsonStr = jsonFile.read()
    storyIn = json.loads(jsonStr)

metadata = ['name','version','image']
#Add all data but the screens to the output
storyOut = {}
for key in metadata:
    storyOut[key] = storyIn[key]

#Transform lists into dictionaries for firebase-upload
for i in range(len(storyIn['screens'])):
    _screen = {}
    for key in storyIn['screens'][i].keys():
        if key not in ['number', 'text']:
            _map = {}
            for j,value in enumerate(storyIn['screens'][i][key]):
                #Use only strings for compatability to json/firebase
                _map[str(j)] = str(value)
            _screen[key] = _map
    storyOut[str(storyIn['screens'][i]['number'])] = _screen

#Add number of screens
storyOut['nscreens'] = len(storyIn['screens'])

#Here we actually upload the data to firebase
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="hundetage_key.json"
db = firestore.Client()

colRef = db.collection('abenteuer').document(story['name'])

