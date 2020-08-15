import pandas as pd

class TestMatrix:
    def __init__(self):
        # List of test point group names
        self.GroupNames = []
        # List of test point group dataframes
        self.GroupTestPoints = []
        
        # Nested dictionary of test point parameter column names, their default values, and flags
        # Format: {'<ParamName>':{'VALUE':<Value>,'FLAG':<Flag>},...}
        self.Parameters = {}
        # Parameter flag options
        # NOTE: first entry must be the 'null flag'
        self.ParametersFlagsOptions = ['-','*','S']
        
        # Nested dictionary containing the definitions used in the test matrix and their flags
        # Format: {'<DefName>':{'VALUE':<Value>,'FLAG':<Flag>},...}
        self.Definitions = {}
        # Definitions flag options
        # NOTE: first entry must be the 'null flag'
        self.DefinitionsFlagsOptions = ['-','R']


    def ClearTestMatrix(self):
        # Clear storage containers
        self.GroupNames       = []
        self.GroupTestPoints  = []
        self.Parameters       = {}
        self.Definitions      = {}
        return None


    def CheckExistence(self):
        # Check to see if a test matrix already exists
        if (self.GroupNames == [] and
            self.GroupTestPoints == [] and
            self.Parameters == {} and
            self.Definitions == {}):
            return 0
        else:
            return 1
    

    def RenameGroup(self,GroupName,NewName):
        # Get the group index
        Idx = self.GroupNames.index(GroupName)
        # Change the name
        self.GroupNames[Idx] = NewName
        return None
    

    def AddParameter(self,Name,Val,Flag):
        # Add to parameters dictionary
        self.Parameters[Name] = {'VALUE':Val,'FLAG':Flag}
        # If a test matrix exists, add the parameter with default value to every group
        if self.CheckExistence() == 1:
            for df in self.GroupTestPoints:
                df.insert(len(df.columns), Name, [Val]*len(df))
        else:
            # Do nothing
            pass
        return None


    def ModifyParameter(self,Name,Val,Flag):
        NewVal = Val
        OldVal = self.Parameters[Name]['VALUE']
        # Modify the default
        self.Parameters[Name] = {'VALUE':Val,'FLAG':Flag}
        # Change in all test point groups IF AND ONLF IF the value
        # was still set to the default
        for i in range(len(self.GroupTestPoints)):
            self.GroupTestPoints[i][Name] = self.GroupTestPoints[i][Name].replace(OldVal,NewVal)
        return None
        

    def ReorderParameters(self,NewOrder):
        # Reorder the parameters dictionary
        self.Parameters = {k: self.Parameters[k] for k in NewOrder}
        # Reorder the columns in each test point group
        for i in range(len(self.GroupTestPoints)):
            self.GroupTestPoints[i] = self.GroupTestPoints[i][NewOrder]


    def RemoveParameter(self,Name):
        # Remove from parameters dictionary
        del self.Parameters[Name]
        # Remove from each test matrix group
        for i in range(len(self.GroupTestPoints)):
            self.GroupTestPoints[i] = self.GroupTestPoints[i].drop(Name, axis=1)
        return None


    def AddDefinition(self,Name,Val,Flag):
        # Add to definition dictionary
        self.Definitions[Name] = {'VALUE':Val,'FLAG':Flag}
        return None

    def ModifyDefinition(self,Name,Val,Flag):
        self.AddDefinition(Name,Val,Flag)
        return None


    def RemoveDefinition(self,Name):
        # Remove from definitions dictionary
        del self.Definitions[Name]
        return None


    def AddGroup(self,Name):
        # Check if the group name already exists
        if Name in self.GroupNames:
            return 0
        else:
            # Append new group name
            self.GroupNames.append(Name)
            # Add new blank dataframe
            self.GroupTestPoints.append(pd.DataFrame(data=[[self.Parameters[x]['VALUE'] for x in self.Parameters.keys()]],
                                                     columns=self.Parameters.keys(), index=[0]))
            return 1


    def CopyGroup(self,GroupName,CopyName):
        # Append copied group name
        self.GroupNames.append(CopyName)
        # Get the group index
        Idx = self.GroupNames.index(GroupName)
        # Copy the test point group
        self.GroupTestPoints.append(self.GroupTestPoints[Idx])
        return None


    def RemoveGroup(self,Name):
        Idx = self.GroupNames.index(Name)
        del self.GroupNames[Idx]
        del self.GroupTestPoints[Idx]
        return None


    def MoveGroup(self,GroupName,Dir):
        Idx = self.GroupNames.index(GroupName)
        if Dir == 'DOWN':
            # Reorder group names list
            self.GroupNames[Idx], self.GroupNames[Idx+1] = self.GroupNames[Idx+1], self.GroupNames[Idx]
            # Reorder group test point dataframes list
            self.GroupTestPoints[Idx], self.GroupTestPoints[Idx+1] = self.GroupTestPoints[Idx+1], self.GroupTestPoints[Idx]
        elif Dir == 'UP':
            # Reorder group names list
            self.GroupNames[Idx-1], self.GroupNames[Idx] = self.GroupNames[Idx], self.GroupNames[Idx-1]
            # Reorder group test point dataframes list
            self.GroupTestPoints[Idx-1], self.GroupTestPoints[Idx] = self.GroupTestPoints[Idx], self.GroupTestPoints[Idx-1]
        return None


    def AddTestPoint(self,GroupName,Data):
        # 'Data' is list containing copies of the parameters dictionary with user specified modifications
        # Find the index for the specified group
        Idx = self.GroupNames.index(GroupName)
        # Add the new testpoint to the matrix
        for x in Data:
            self.GroupTestPoints[Idx] = self.GroupTestPoints[Idx].append(x, ignore_index=True)
        return None


    def RemoveTestPoint(self,GroupName,TestPointIdx):
        # Find the index for the specified group
        Idx = self.GroupNames.index(GroupName)
        # Drop the test point
        self.GroupTestPoints[Idx] = self.GroupTestPoints[Idx].drop(TestPointIdx,axis=0)
        return None

    def MoveTestPoint(self,GroupName,TestPointIdx,Dir):
        # Get testpoint group index
        Idx = self.GroupNames.index(GroupName)
        # Get the index order of the test point group
        Order = list(self.GroupTestPoints[Idx].index.values)
        # Reorder the test point index order list
        if Dir == 'DOWN':
            Order[TestPointIdx], Order[TestPointIdx+1] = Order[TestPointIdx+1], Order[TestPointIdx]
        elif Dir == 'UP':
            Order[TestPointIdx-1], Order[TestPointIdx] = Order[TestPointIdx], Order[TestPointIdx-1]
        # Update the dataframe order
        self.GroupTestPoints[Idx] = self.GroupTestPoints[Idx].iloc[Order]
        # Renumber the dataframe index
        self.GroupTestPoints[Idx] = self.GroupTestPoints[Idx].reset_index(drop=True)
        return None


    def UpdateParameter(self,GroupName,TestPointIdx,Parameter,Val):
        # Get the group index
        Idx = self.GroupNames.index(GroupName)
        # Modify the parameter
        self.GroupTestPoints[Idx][Parameter].values[TestPointIdx] = Val            
        return None


    # DEBUG FUNCTION
    def DebugPrint(self):
        print('-----------------------------------------')
        print(self.Parameters)
        print(self.Definitions)
        print(self.GroupNames)
        for x in self.GroupTestPoints:
            print(x)
        return None
