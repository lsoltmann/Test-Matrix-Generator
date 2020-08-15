import pandas as pd

def LoadTestMatrix(FileName,TestMatrix):
    # Clear any existing data in the test matrix class
    TestMatrix.ClearTestMatrix()
    # Open the raw test matrix file
    RawMatrix = pd.read_csv(FileName)
    
    # ---- STEP 1 ----
    # Save off parameter defaults
    ParamDefaults = RawMatrix.iloc[0].to_dict()
    ParamFlags    = RawMatrix.iloc[1].to_dict()
    ParamDefaults = RemoveInternalNames(ParamDefaults)
    ParamFlags    = RemoveInternalNames(ParamFlags)
    for key,value in ParamDefaults.items():
        TestMatrix.Parameters[key] = {'VALUE':value,'FLAG':ParamFlags[key]}
    # Save off definitions
    DefNames  = eval(RawMatrix.iloc[[2]]['<DATA>'].values[0])
    DefValues = eval(RawMatrix.iloc[[3]]['<DATA>'].values[0])
    DefFlags  = eval(RawMatrix.iloc[[4]]['<DATA>'].values[0])
    for i in range(len(DefNames)):
        TestMatrix.Definitions[DefNames[i]] = {'VALUE':DefValues[i],'FLAG':DefFlags[i]}

    # ---- STEP 2 ----
    # Divide up and save the raw matrix to the test matrix
    # Now remove the first row
    RawMatrix = RawMatrix.drop([0,1,2,3,4],axis=0)
    RawMatrix = RawMatrix.drop(columns='<DATA>')
    # Divide up the remaing rows by group and store in the test matrix
    Groups = RawMatrix['<GROUP>'].unique()
    for x in Groups:
        # Save the group name to the test matrix class
        TestMatrix.GroupNames.append(x)    
        # Save the group dataframe to the test matrix class
        TestMatrix.GroupTestPoints.append(RawMatrix.loc[RawMatrix['<GROUP>'] == x])
        # Remove the internal names
        TestMatrix.GroupTestPoints[-1] = TestMatrix.GroupTestPoints[-1].drop(columns='<GROUP>')
        # Reset index
        TestMatrix.GroupTestPoints[-1] = TestMatrix.GroupTestPoints[-1].reset_index(drop=True)
    return None


def RemoveInternalNames(Dict):
    delkeys = []
    for key,value in Dict.items():
        if key[0] == '<' and key[-1] == '>':
            delkeys.append(key)
    for x in delkeys:
        del Dict[x]
    return Dict
