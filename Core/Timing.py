import pandas as pd
import numpy as np

def Timing(TestMatrix):
    # Check if any parameters are marked for timing
    # ('T' flag) and that a parameter to store the
    # time exists ('Z' flag), if either one fails
    # the check, don't continue with time calculation.
    TimeFlagCheck  = 0 
    TimeParamCheck = 0
    # Since we are already looping through the parameters dictionary,
    # might as well pull out the other needed information just in case
    # the time check passes.
    TimeParam      = None #Parameter name where time is stored
    ConstParams    = {} # Format: {'ParamName':{'TIME':[val],'VALUE':[val]},...}
    DeltaParams    = {} # Format: {'ParamName':'DeltaTime',...}
    for key,value in TestMatrix.Parameters.items():
        # If at least one parameter is marked for timing, this part of the time
        # check passes.
        if 'T' in value['FLAG']:
            TimeFlagCheck = 1
            # Save the timing data for delta and constant terms
            #     Constant terms
            if TestMatrix.Parameters[key]['TIMING']['FLAG'] == 'C':
                ConstParams[key] = {'TIME':TestMatrix.Parameters[key]['TIMING']['VALUE'],'VALUE':[0]}
            #     Delta terms
            if TestMatrix.Parameters[key]['TIMING']['FLAG'] == 'D':
                DeltaParams[key] = TestMatrix.Parameters[key]['TIMING']['VALUE']
        # If a timing storage parameter exists, this part of the time check passes.
        if value['FLAG'] == 'Z':
            TimeParamCheck = 1
            TimeParam = key
    if TimeFlagCheck == 0 or TimeParamCheck == 0:
        return None

    # If all time checks passed ...
    
    # Run through each row of the test matrix
    for i in range(len(TestMatrix.GroupTestPoints)):
        Frame = TestMatrix.GroupTestPoints[i]
        for j in range(len(Frame)):
            # Extract the row
            Row = Frame.iloc[j]
            # Reset temporary variables
            SumTime = 0

        
            # ---- Calculate delta times ----
            if DeltaParams != {}:
                #   Do not apply deltas to first row
                if (i != 0) or (j != 0):
                    # Get the previous row
                    # If this row is the first row of a new group, get the last row of the last group
                    if j == 0:
                        PrevRow = TestMatrix.GroupTestPoints[i-1].iloc[len(TestMatrix.GroupTestPoints[i-1])-1]
                    else:
                        PrevRow = Frame.iloc[j-1]
                    # Run through each delta
                    DeltaList = []
                    for key,value in DeltaParams.items():
                        if Row[key] != PrevRow[key]:
                            DeltaList.append(float(value))
                    # Apply delta equation
                    if DeltaList != []:
                        SumTime += DeltaFunc(DeltaList)
                    else:
                        pass
                else:
                    pass
            else:
                # Do nothing
                pass



            '''
            --- Constant Time Cacluation ---
            The constant time is calculated using the following equation:

            ConstantTime = max[Cmin*prod(Lists),C(i)*len(List(i)) for i=1:N_List]

            1. If only single items are present (no lists), then the the largest constant time will be used.
            
            2. If lists are present, the time to complete a full ND grid of all combinations using the shortest time
            (it is assumed that the tester will always opt for the shortest time to complete an ND grid) or the
            time to complete a single list will be used, which ever is greater.

            It is assumed that when multiple constant times are present, they are completed in parallel so
            the longest item to complete will always be the final constant time.
            '''
            # ---- Calculate constant times ----
            if ConstParams != {}:
                LenList = []
                for key,value in ConstParams.items():
                    # Check if parent parameter is marked as 'none', if it is, skip that parameter
                    skip = 0
                    try:
                        if Row[key].upper() == 'NONE':
                            skip = 1
                    except:
                        pass

                    if skip == 0:
                        # Check if the parent parameter is a list or not
                        try:
                            # If its not a number or list, it will fail the eval test
                            NumOrList = eval(Row[key])
                            if not isinstance(NumOrList,list):
                                NumOrList = [NumOrList]
                            ConstParams[key]['VALUE'] = NumOrList
                            LenList.append(len(NumOrList))
                        except:
                            # However, it may be using a definition so we
                            # need to check the definitions to see if it
                            # is actually defined as a list or number
                            if Row[key] in TestMatrix.Definitions:
                                # If the 'value' is in the defintions, run the check on its VALUE
                                try:
                                    NumOrList = eval(TestMatrix.Definitions[Row[key]]['VALUE'])
                                    if not isinstance(NumOrList,list):
                                        NumOrList = [NumOrList]
                                    ConstParams[key]['VALUE'] = NumOrList
                                    LenList.append(len(NumOrList))
                                except:
                                    pass
                            else:
                                pass
                    else:
                        pass
                MinC = np.inf
                TList = []
                for key,value in ConstParams.items():
                    # Find small constant time
                    if float(ConstParams[key]['TIME']) < MinC:
                        MinC = float(ConstParams[key]['TIME'])
                    # Get time to complete each item in ConstParams
                    TList.append(float(ConstParams[key]['TIME'])*len(ConstParams[key]['VALUE']))
                TList.append(MinC*np.prod(LenList))
                # Use the max of either: Cmin*prod(LenList) or C(i)*len(L(i))
                SumTime += max(TList)
            else:
                # Do nothing
                pass

            
            # Append the time to the row time storage parameter
            #
            # NOTE: This appending action can be completed using two methods:
            #       chained indexing or .loc. Chained indexing gives this warning
            #       when the timing is calculateda after adding a new parameter.
            #
            # SettingWithCopyWarning: A value is trying to be set on a copy of a
            # slice from a DataFrame. See the caveats in the documentation:
            # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
            #
            # According to the reference, it is recommended to use .loc.
            #
            # --- Chained indexing
            #Frame[TimeParam][j] = SumTime
            # --- .loc
            Frame.loc[j,TimeParam] = SumTime
    return None
            

'''
--- Delta Time Calculation ---
This function determines how multiple deltas are handled.
Assuming that the test has multiple people working it,
parameter changes will probably happen in parallel so the
largest delta time of all the tasks can be used. However,
if many changes are needed, the time may be longer than
the longest delta but not longer than a sum of all deltas.
This function includes a multidelta factor (MDF) that is
applied as follows:

DeltaTime = max(DeltaList) + sum(MDF*DeltaList[i]) - MDF*max(DeltaList)
where i = 0..N

To only use the maximum delta value set MDF = 0
'''
def DeltaFunc(DeltaList):
    # Multidelta factor
    MDF = 0.1
    # Get the largest delta value
    MaxDelta = max(DeltaList)
    MaxIdx   = DeltaList.index(MaxDelta)
    # Remove the largest delta 
    del DeltaList[MaxIdx]
    # Apply equation
    Time = MaxDelta
    for i in DeltaList:
        Time = Time + MDF*i
    return Time
