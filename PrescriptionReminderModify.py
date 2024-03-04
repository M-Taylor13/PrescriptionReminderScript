import pickle
import os
import time
import re

medList = []


def loadFile():
    with open('sampleDataPickle.pkl', 'rb') as f:
        try:
            medList = pickle.load(f) # deserialize using load()
        except:
            medList = []
        finally: 
             f.close()
    return medList


# multi-platform console clear function from popcnt 
# https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
def cls(sleepTime):
    time.sleep(sleepTime) # slows down the flow of menu reset
    os.system('cls' if os.name=='nt' else 'clear')
            
class Prescription:
    def __init__(self, name, finishDate, refills):
        self.name = name
        self.finishDate = finishDate
        self.refills = refills
        
def PrintMainMenu():
     print("Welcome to the prescription manager!")
     print("1. View existing prescriptions")
     print("2. Update/delete existing prescriptions")
     print("3. Add new prescriptions")
     print("4. Quit")
     
def UpdateMed(index, medList):
    cls(0)
    med = medList[index]
    upd = True
    while (upd):
        print(f"Medication: {med.name}")
        print("1. Update supply end date")
        print("2. Update number of refills")
        print("3. Delete medicine")
        print("4. Back")
        updateOpt = input("Enter the number of what you want to update: ")
        match updateOpt:
            case "1": 
                updateFinish = input("Enter new date (dd/mm/yyyy): ")
                match = re.search(r'^(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\/)(0[1-9]|1[0-2])(\/)(20[0-9][0-9])$', updateFinish)
                if (match):
                    med.finishDate = updateFinish
                    cls(0.5)
                    print("Updated successfully:")
                    print("Name: " + med.name)
                    print("Suppply finish date: " + med.finishDate)
                    print("Number of refills: " + med.refills)
                    upd = False
                else:
                    upd = True
            case "2": 
                updateRefills = input("Enter new refill amount: ")
                match = re.search(r'^([0-9]|1[0-9]|20)$', updateRefills)
                if (match):
                    med.refills = updateRefills
                    cls(0.5)
                    print("Updated successfully:")
                    print("Name: " + med.name)
                    print("Suppply finish date: " + med.finishDate)
                    print("Number of refills: " + med.refills)
                    upd = False
                else:
                    upd = True
            case "3":
                print("Deleting...")
                cls(0.5)
                del medList[index]
                print(f"{med.name} deleted successfully")
                upd = False
            case "4":
                upd = False
            
        if (upd):
            print("Incorrect input")
            cls(0.5)
    input("Press Enter to continue...")


         
def DataEntry(medList):
    done = False
    while (done == False):
        cls(0)
        
        PrintMainMenu()
        menuChoice = input("Enter the number of your choice: ")
        match menuChoice:
            case "1"  : 
                cls(0)
                if (len(medList) == 0):
                    print("No existing medications")
                
                for m in medList:
                    print("Name: " + m.name)
                    print("Suppply finish date: " + m.finishDate)
                    print("Number of refills: " + m.refills)
                    print("\n")
                input("Press Enter to continue...")
                
            case "2" : 
                cls(0)
                updating = True
                if (len(medList) != 0):
                    while (updating):
                        option = 1
                        print("Current medications:")
                        for m in medList:
                            print(f"{option}. Name: {m.name}")
                            option += 1
                        updateChoice = input("Enter the number of your choice, or 'back' to go back: ")
                        if (updateChoice == "back"):
                            updating = False
                            break;
                        for index, m in enumerate(medList):
                            if ((index + 1) == int(updateChoice)):
                                updating = False
                                UpdateMed(index, medList)
                                break;
                        if (updating):
                            print("invalid input")
                            cls(0.5)

                else:
                    print("No existing medications")
                    input("Press Enter to continue...")        

            case "3" : 
                cls(0)
                print("Enter medication information:")
                newName = input("Name: ")
                newDate = input("Suppply finish date (dd/mm/yyyy): ")
                newRefills = input("Number of refills: ")
                newMed = Prescription(newName, newDate, newRefills)
                medList.append(newMed)
                print (f"added {newMed.name}")
                input("Press Enter to continue...")
            case "4" :
                done = True
            case _  : 
                print("Invalid input")
           
     
    with open('sampleDataPickle.pkl', "wb") as f:
        pickle.dump(medList, f) #serializing to file
    f.close()


medList = loadFile()     
DataEntry(medList)
    
    