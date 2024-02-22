import pickle
from datetime import timedelta, date
import requests
import urllib, requests
import json

#Is initiated daily by Task Scheduler

#telegram message function from https://gist.github.com/dlaptev/7f1512ee80b7e511b0435d3ba95d88cc
def sendScriptReminder(message: str,
                          chat_id: str,
                          api_key: str):

    url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (
        api_key, chat_id, urllib.parse.quote_plus(message))
    _ = requests.get(url, timeout=10)



dueMedList = [] #medicines that run out today
dueSoonList = [] #medicines that run out in 3 days time
medList = [] #Overall registered medicine list

class Prescription:
    def __init__(self, name, finishDate, refills):
        self.name = name
        self.finishDate = finishDate
        self.refills = refills

def loadFile():
    with open('prescriptions.pkl', 'rb') as f: # use file that was populated by other PrescriptionReminderModify.py
        try:
            medList = pickle.load(f) # deserialize 
        except:
            medList = []
        finally:
            f.close()
    return medList

def getDateMatches(medList):
    for med in medList:
        d = med.finishDate.split('/') # convert to Python's 'date' type from dd/mm/yyyy format
        expDate = date(int(d[2]), int(d[1]), int(d[0]))
        # using date and timedelta prevents dealing with inaccurate day addition across months
        preReminder = date.today() + timedelta(days=3) 
        if (expDate == date.today()):
            dueMedList.append(med)
        elif (preReminder == expDate):
            dueSoonList.append(med)
    return dueMedList, dueSoonList

def textRemind(mList, urgent):
    # using urgent to determine which list is which without writing extra functions
    for m in mList:
        if (urgent == True):
            sendScriptReminder(f"{m.name} ({m.refills} refills) finishes today", chat_id, api_key)
        else:
            sendScriptReminder(f"{m.name} ({m.refills} refills) finishes on {m.finishDate}", chat_id, api_key)
            
def manualTextCheck(mList):
     # to check if the bot still works without editing medicine list
    sendScriptReminder(f"nothing due", chat_id, api_key)
    
def getBotInfo(file):
    # bot info loaded frm json file
    with open(file) as f:
        keys = json.load(f); 
    return keys
# In this case, it is empty and in the same repository for demonstration purposes 

medList = loadFile()
keys = getBotInfo("telegramInfo.json")
    
chat_id = keys['Chat_Id']
api_key = keys['API_Key']

#getting lists of medication that match, or are three days from todays date
if (len(medList) != 0):
    lists = getDateMatches(medList)
    dueMedList = lists[0]
    dueSoonList = lists[1]

#sending messages if matches are found for the respective categories    
if (len(dueMedList) != 0):
    urgent = True
    textRemind(dueMedList, urgent) 

if (len(dueSoonList) != 0):
    urgent = False
    textRemind(dueSoonList, urgent)
