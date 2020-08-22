import pandas as pd

def Basic_CSV(TestName,TestMatrix):
    # ---------- Test Point Matrix -----------
    # Iterate through each of the parameter flags and apply the flag
    ColList = []
    IgnoreColIdx = []
    Idx = 0
    for key,value in TestMatrix.Parameters.items():
        if '*' in TestMatrix.Parameters[key]['FLAG']:
            IgnoreColIdx.append(Idx)
        else:
            ColList.append(key)
        Idx += 1
    # Iterate through definitions and track flags
    DefReplaceList = []
    for key,value in TestMatrix.Definitions.items():
        if 'R' in TestMatrix.Definitions[key]['FLAG']:
            DefReplaceList.append(key)
    # Create an empty data frame
    FinalMatrix = pd.DataFrame(columns=ColList)
    # Reverse the ignore list
    IgnoreColIdx = IgnoreColIdx[::-1]
    # Combine all the test point groups
    for i in range(len(TestMatrix.GroupTestPoints)):
        for j in range(TestMatrix.GroupTestPoints[i].shape[0]):
            # Test point matrix values
            temp = list(TestMatrix.GroupTestPoints[i].iloc[j].values)
            # Remove ignore columns
            for k in IgnoreColIdx:
                del temp[k]
            # Replace the parameter tags
            for k in range(len(temp)):
                # Parameters
                if '#TESTPOINT' in str(temp[k]):
                    temp[k] = temp[k].replace('#TESTPOINT',str(j+1))
                if '#IDX' in str(temp[k]):
                    temp[k] = temp[k].replace('#IDX',str(FinalMatrix.shape[0]+1))
                if '#GROUP' in str(temp[k]):
                    temp[k] = temp[k].replace('#GROUP',str(i+1))
                if '&GROUP' in str(temp[k]):
                    temp[k] = temp[k].replace('&GROUP',str(TestMatrix.GroupNames[i]))
                # Definitions
                if str(temp[k]) in DefReplaceList:
                    temp[k] = TestMatrix.Definitions[str(temp[k])]['VALUE']            
            # Then append it to the final matrix
            FinalMatrix.loc[FinalMatrix.shape[0]] = temp

    # ---------- Header information -----------
    FID = open(TestName+'.csv', 'w')
    # Write header information
    FID.write('Test Name:,{0}\n\n'.format(TestName))
    # Test point summary
    FID.write('Test Matrix Summary:\n')
    FID.write(',Test Points:,{0}\n'.format(FinalMatrix.shape[0]))
    FID.write(',Groups:,{0}\n'.format(len(TestMatrix.GroupTestPoints)))
    FID.write(',Test Points per Group:\n')
    for i in range(len(TestMatrix.GroupTestPoints)):
        FID.write(',,{0}:,{1}\n'.format(TestMatrix.GroupNames[i],TestMatrix.GroupTestPoints[i].shape[0]))
    FID.write('\n')
    FID.write('Definitions:\n')
    for key,value in TestMatrix.Definitions.items():
        for key2,value2 in value.items():
            if key2 == 'VALUE':
                value2 = value2.replace(',',' ')
                FID.write(',{0}:,{1}\n'.format(key,value2))
    FID.write('\n')
    FID.close()
    
    # Append test matrix to file
    FinalMatrix.to_csv(TestName+'.csv',mode='a',index=False)
