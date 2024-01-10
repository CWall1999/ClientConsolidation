import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
familydata = pd.read_csv(file_path)

#for each family there are two cases, they are consolidatable or not
#for a family to be consolidatable they must be:
#not in a family room [143,145,147,149,151,153,155,157]
#not in an isolation room [160,162,163,164,165,166,167,168,169]
#must have fewer than 3 family members

#add a column dictating family size
familydata['FamilySize'] = familydata.groupby('FID')['FID'].transform('count')

#add column dictating room occupancy
familydata['RoomOccupancy'] = familydata.groupby('Room')['Room'].transform('count')

#creates column that dictates if a client is an adult male
familydata['AdultMale'] = np.where((familydata['Age'] > 17) & (familydata['Gender'] == 'M'), True, False)

#creates column that dictates if a client is an adult female
familydata['AdultFemale'] = np.where((familydata['Age'] > 17) & (familydata['Gender'] == 'F'), True, False)

#create column that dictates if a client is a male child
familydata['ChildMale'] = np.where((familydata['Age'] <= 17) & (familydata['Gender'] == 'M'), True, False)

#create column that dictates if a client is a female child
familydata['ChildFemale'] = np.where((familydata['Age'] <= 17) & (familydata['Gender'] == 'F'), True, False)

#drops all rooms from the dataframe if they are in a family or isolation room or if they have a family of more than 3 memebers
badRooms = [143,145,147,149,151,153,155,157,160,162,163,164,165,166,167,168,169]
elligableRooms = []
for i in range(len(familydata)):
    if familydata['Room'][i] in badRooms:
        elligableRooms.append(False)
    
    elif familydata['FamilySize'][i] > 3:
        elligableRooms.append(False)

    else:
        elligableRooms.append(True)
        
familyData_mod1 = familydata.loc[elligableRooms,:]

#we now have a dataframe excluding families in invalid rooms

'''
There are two types of families that we can consolidate Single mothers and Single fathers:
    For single mothers we can consolidate them with other single mothers with the same gender child
    IE mom with 6yo son and mom with 4 yo son is valid but not mom with 6yo son and mom with 4yo daughter
    
    For single fathers they can not be consolidated if they have a daughter but with sons they are elligable


Case 1: Single Mother with Daughters
    adult female >= 1, child female >= 1, adult male = 0, child male = 0
Case 2: Single mother with sons
    adult female >= 1, child female = 0, adult male = 0, child male >= 1
Case 3: Single Father with sons
    adult female >= 0, child female = 0, adult male = 1, child male >= 1
Else: Cannot consolidate if families have mixed gender adults or the children 
'''

singleMomDaughter = pd.DataFrame()
singleMomSon      = pd.DataFrame()
singleDadSon      = pd.DataFrame()

for i in familyData_mod1['FID'].unique():
    adultMaleCount = sum(familyData_mod1.loc[familyData_mod1['FID'] == i]['AdultMale'])
    adultFemaleCount = sum(familyData_mod1.loc[familyData_mod1['FID'] == i]['AdultFemale'])
    childMaleCount = sum(familyData_mod1.loc[familyData_mod1['FID'] == i]['ChildMale'])
    childFemaleCount = sum(familyData_mod1.loc[familyData_mod1['FID'] == i]['ChildFemale'])

    #print(familyData_mod1['FID'] == i, childMaleCount)

    if (adultFemaleCount > 0) & (adultMaleCount == 0) & (childFemaleCount > 0) & (childMaleCount == 0):
        #this case represents single mother with daughters and should be appended to the relevent dataframe
        singleMomDaughter= pd.concat([familyData_mod1.loc[familyData_mod1['FID'] == i], singleMomDaughter])
        #print(familyData_mod1.loc[familyData_mod1['FID'] == i])

    elif ((adultFemaleCount > 0) & (adultMaleCount == 0) & (childFemaleCount == 0) & (childMaleCount > 0)):
        singleMomSon = pd.concat([familyData_mod1.loc[familyData_mod1['FID'] == i], singleMomSon])
        #print(familyData_mod1.loc[familyData_mod1['FID'] == i])

    elif ((adultFemaleCount == 0) & (adultMaleCount == 1) & (childFemaleCount == 0) & (childMaleCount > 0)):
        singleDadSon = pd.concat([familyData_mod1.loc[familyData_mod1['FID'] == i], singleDadSon])
        #print(familyData_mod1.loc[familyData_mod1['FID'] == i])

#Trim Dataframes down to input size
singleDadSon = singleDadSon.iloc[:,0:5]
singleMomSon = singleMomSon.iloc[:,0:5]
singleMomDaughter = singleMomDaughter.iloc[:,0:5]

# Write each dataframe to a different worksheet.
singleDadSon.to_csv('SingleFathers.csv',index= False)
singleMomDaughter.to_csv('SingleMomDaughter.csv',index = False)
singleMomSon.to_csv('SingleMomSon.csv',index= False)