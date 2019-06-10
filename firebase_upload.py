import json
import os
from base64 import b64decode
import firebase_admin
from firebase_admin import firestore, credentials

with open('geschichte.json', 'r', encoding='utf-8') as jsonFile:
    jsonStr = jsonFile.read()
    storyIn = json.loads(jsonStr)

#Collect all the sotry-metadata from the json file
#This will be uploaded to a different firebase file
metaTags = ['name','image']
metadata = {}
for key in metaTags:
    metadata[key] = storyIn[key]
version = storyIn['version']

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

#Vrite enviormental variable to file - thank you Vincent!
with open('hundetage_key.json', 'w') as fd:
    print(b64decode(os.environ['FIREBASE_KEY']).decode('utf-8'), file=fd)

#Authenticate via service user
cred = credentials.Certificate('hundetage_key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

#Update screens
storyRef = db.collection('abenteuer').document(storyIn['name'])
storyRef.update(screens)

#Update story version
versionRef = db.collection('general_data').document('firebase_versions')
versions = versionRef.get()
versions[storyIn['name']] = version
versionRef.update(versions)