import pandas as pd

'''
Raw Matrix Format:
Row 1    Default values for parameters
Row 2    Flag values for parameters
Row 3    Definition names, 'None' for every column except <DATA>
Row 4    Definition values, 'None' for every column except <DATA>
Row 5    Definition flags, 'None' for every column except <DATA>

example:

<GROUP>	                Run         Group       Priority
<PARAMETER DEFAULTS>    #TESTPOINT  &GROUP      1
<PARAMETER FLAGS>       -           -           -
<DEFINITION NAMES>      None        None        None
<DEFINITION VALUES>     None        None        None
<DEFINITION FLAGS>      None        None        None
g1                      #TESTPOINT  &GROUP      1

'''

def SaveTestMatrix_Raw(TestName,TestMatrix):
    # ---- RAW MATRIX ----
    # Make a new output matrix with the defaults column as the first one
    FinalMatrix = pd.DataFrame(MakeParamDict(TestMatrix.Parameters,'VALUE'), index=[0])
    # Add GROUP as a column. Since currently only the defaults values exist in the test matrix, makes its column value default
    FinalMatrix.insert(0, '<GROUP>', '<PARAMETER DEFAULTS>')
    # Add DATA as a column for datat that is not associated with a parameter
    FinalMatrix.insert(len(FinalMatrix.columns), '<DATA>', 'None')
    # Add the parameter flags as the next row
    temp = MakeParamDict(TestMatrix.Parameters,'FLAG')
    temp['<GROUP>'] = '<PARAMETER FLAGS>'
    temp['<DATA>'] = 'None'
    FinalMatrix = FinalMatrix.append(temp, ignore_index=True)
    # Add the definitions as the third row
    Defs,Values,Flags = SplitDefs(TestMatrix.Definitions)
    # Definition names
    temp = ['None']*(len(FinalMatrix.columns)-1)
    temp[0] = '<DEFINITION NAMES>'
    temp.append(Defs)
    FinalMatrix = FinalMatrix.append(pd.DataFrame([temp], columns=FinalMatrix.columns), ignore_index=True)
    # Definition values
    temp = ['None']*(len(FinalMatrix.columns)-1)
    temp[0] = '<DEFINITION VALUES>'
    temp.append(Values)
    FinalMatrix = FinalMatrix.append(pd.DataFrame([temp], columns=FinalMatrix.columns), ignore_index=True)
    # Definition flags
    temp = ['None']*(len(FinalMatrix.columns)-1)
    temp[0] = '<DEFINITION FLAGS>'
    temp.append(Flags)
    FinalMatrix = FinalMatrix.append(pd.DataFrame([temp], columns=FinalMatrix.columns), ignore_index=True)
    
    # Combine all the test point groups
    for i in range(len(TestMatrix.GroupTestPoints)):
        for j in range(TestMatrix.GroupTestPoints[i].shape[0]):
            # Test point matrix values
            temp = list(TestMatrix.GroupTestPoints[i].iloc[j].values)
            # Add <GROUP> name
            temp.insert(0,TestMatrix.GroupNames[i])
            # Add <DATA> value (none)
            temp.insert(len(temp),'None')
            # Append to final matrix
            FinalMatrix.loc[FinalMatrix.shape[0]] = temp
    # Write the matrix to a file
    FinalMatrix.to_csv(TestName+'.tm',index=False)


def MakeParamDict(Parameters,Type):
    Dict = {}
    for key,value in Parameters.items():
        Dict[key] = value[Type]     
    return Dict


def SplitDefs(Definitions):
    Defs   = []
    Values = []
    Flags  = []
    for key,value in Definitions.items():
        Defs.append(key)
        Values.append(value['VALUE'])
        Flags.append(value['FLAG'])
    return Defs,Values,Flags
