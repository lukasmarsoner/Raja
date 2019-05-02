import json
import firebase_admin
from firebase_admin import firestore, credentials

with open('geschichte.json', 'r', encoding='utf-8') as jsonFile:
    jsonStr = jsonFile.read()
    storyIn = json.loads(jsonStr)

#Collect all the sotry-metadata from the json file
#This will be uploaded to a different firebase file
metaTags = ['name','version','image']
metadata = {}
for key in metaTags:
    metadata[key] = storyIn[key]

screens = {}
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
        elif key == 'text':
            _screen[key] = storyIn['screens'][i][key]
    screens[str(storyIn['screens'][i]['number'])] = _screen


#From here on we actually upload the data to firebase

#Authenticate via service user
cred = credentials.Certificate('hundetage_key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

#Update screens
storyRef = db.collection('abenteuer').document(storyIn['name'])
storyRef.update(screens)

#Update metadata
storyRef = db.collection('abenteuer_metadata').document(storyIn['name'])
storyRef.update(metadata)


