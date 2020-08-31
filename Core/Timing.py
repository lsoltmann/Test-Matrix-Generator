import pandas as pd

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
    ConstParams    = {}
    DeltaParams    = {}
    for key,value in TestMatrix.Parameters.items():
        # If at least one parameter is marked for timing, this part of the time
        # check passes.
        if 'T' in value['FLAG']:
            TimeFlagCheck = 1
            # Save the timing data for delta and constant terms
            #     Constant terms
            if TestMatrix.Parameters[key]['TIMING']['FLAG'] == 'C':
                ConstParams[key] = TestMatrix.Parameters[key]['TIMING']['VALUE']
            #     Delta terms
            if TestMatrix.Parameters[key]['TIMING']['FLAG'] == 'D':
                DeltaParams[key] = TestMatrix.Parameters[key]['TIMING']['VALUE']
        # If a timing storage parameter exists, this part of the time check passes.
        if value['FLAG'] == 'Z':
            TimeParamCheck = 1
            TimeParam = key
    if TimeFlagCheck == 0 or TimeParamCheck == 0:
        return TestMatrix.OneMatrix()

    # If all time checks passed ...
    
    # Assemble the entire test matrix
    TM = TestMatrix.OneMatrix()
    # Run through each row of the test matrix
    for i in range(len(TM)):
        # Extract the row
        Row = TM.iloc[i]
        # Reset temporary variables
        SumTime = 0
        
        # ---- Calculate delta times ----
        if DeltaParams != {}:
            #   Do not apply deltas to first row
            if i > 0:
                # Get the previous row
                PrevRow = TM.iloc[i-1]
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


        # ---- Calculate constant times ----
        if ConstParams != {}:
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
                            except:
                                NumOrList = [0]
                        else:
                            NumOrList = [0]
                    # Apply the constant to each term in the list
                    SumTime += float(value)*len(NumOrList)
                else:
                    SumTime += 0
        else:
            # Do nothing
            pass
        # Append the time to the row time storage parameter
        TM[TimeParam][i] = SumTime
    return TM
            

'''
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
