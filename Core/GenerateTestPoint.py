import itertools as IT
import re

'''
InputType:

SINGLE
Format: PARAM:VAL
        PARAM1:VAL1,PARAM2:VAL2,...
        - VAL can be a list, string, or int/float
        
MULTIPLE
Format: PARAM1:[VAL11,VA12,...],PARAM2:[VAL21,VAL22,...],...
        - Each list item will be added as a separate test point

FACTORIAL
Format: PARAM1:[VAL11,VA12,...],PARAM2:[VAL21,VAL22,...],...
        - Each test will be a unique combination of PARAM1 and PARAM2 using the given values


Status output
0 = no errors
1 = input name error
2 = format error

'''

def GenerateTestPoint(InputStr,InputType,Parameters):
    # Initialize output dictionary
    TestPointList = [] # List of dicts

    NonListInput = re.compile('(\w*\:(?!\[|\])\w*[^,]*)') #finds everything with the format str:str {Note: will not include any strings that contain '[' or ']'
    ListInput = re.compile('(\w*(?:\:\[.*?\]))') #finds everything with the format str:[...]

    #print('---------------------')
    #print(InputStr)
    #print(InputType)
    #print(Parameters)

    if InputType == 'SINGLE':
        # --- CASE 1 --- Input is left blank -> use default values
        if InputStr == '':
            # Nothing to do, just a copy of the defaults
            TestPointDict = MakeParametersDict(Parameters)
            TestPointList.append(TestPointDict)
            return 0,TestPointList
        
        # --- CASE 2 --- Single input(s)
        else:
            # Single inputs are allowed to contain lists, single items, or both
            # so first we check if any lists were given.
            ListItems = ListInput.findall(InputStr)
            # Now remove those lists from the original input string
            for item in ListItems:
                InputStr = InputStr.replace(item,'')
            # Now split a the comma
            SingleItems = NonListInput.findall(InputStr)           
            # Now add the single items to the test points first if there are any
            if SingleItems != []:
                for item in SingleItems:
                    TestPointDict = MakeParametersDict(Parameters)
                    temp = item.split(':')
                    if temp[0].strip() not in Parameters:
                        return 1,[]
                    TestPointDict[temp[0].strip()] = temp[1].strip()
                    TestPointList.append(TestPointDict)
            # And finally add the list items to the test points if there are any
            if ListItems != []:
                for item in ListItems:
                    TestPointDict = MakeParametersDict(Parameters)
                    temp = item.split(':')
                    if temp[0].strip() not in Parameters:
                        return 1,[]
                    TestPointDict[temp[0].strip()] = temp[1].strip()
                    TestPointList.append(TestPointDict)
            return 0,TestPointList
  
    elif InputType == 'MULTIPLE':
        # --- CASE 3 --- Input is left blank -> use default values
        if InputStr == '':
            # Nothing to do, just a copy of the defaults
            TestPointDict = MakeParametersDict(Parameters)
            TestPointList.append(TestPointDict)
            return 0,TestPointList

        # --- CASE 4 --- Single input(s)
        else:
            ListItems = ListInput.findall(InputStr)
            if ListItems == []:
                return 2,[]
            for item in ListItems:
                # Split the parameter and value
                temp = item.split(':')
                # Check to make sure the parameter exists in the test matrix
                if temp[0].strip() not in Parameters:
                    return 1,[]
                # Conver the value to a list
                temp[1] = [x for x in temp[1].strip('][').split(',')]
                for x in temp[1]:
                    TestPointDict = MakeParametersDict(Parameters)
                    TestPointDict[temp[0].strip()] = x.strip()
                    TestPointList.append(TestPointDict)
            return 0,TestPointList

    elif InputType == 'COMBINATION':
        # --- CASE 5 --- Input is left blank -> use default values
        if InputStr == '':
            # Nothing to do, just a copy of the defaults
            TestPointDict = MakeParametersDict(Parameters)
            TestPointList.append(TestPointDict)
            return 0,TestPointList

        # --- CASE 6 --- 
        else:
            CombList = []
            ListItems = ListInput.findall(InputStr)
            if ListItems == []:
                return 2,[]
            for item in ListItems:
                # Split the parameter and value
                temp = item.split(':')
                # Check to make sure the parameter exists in the test matrix
                if temp[0].strip() not in Parameters:
                    return 1,[]
                # Convert the value to a list
                CombList.append([temp[0].strip()+':'+x for x in temp[1].strip('][').split(',')])
            CombList = list(IT.product(*CombList))
            # Add all combinations to the test point list
            for Combo in CombList:
                TestPointDict = MakeParametersDict(Parameters)
                for item in Combo:
                    temp = item.split(':')
                    TestPointDict[temp[0].strip()] = temp[1].strip()
                TestPointList.append(TestPointDict)
            return 0,TestPointList


# Make a dictionary from parameters and their default values, excluding the flags
def MakeParametersDict(Parameters):
    ParamDict = {}
    for key,value in Parameters.items():
        ParamDict[key] = value['VALUE']
    return ParamDict
