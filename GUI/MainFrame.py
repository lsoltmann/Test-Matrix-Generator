import tkinter as tk
from Core.GenerateTestPoint import GenerateTestPoint
from GUI.IOFrame import IOFrame

'''
TODO:
HIGH PRIORITY
1. Timing stuff

MEDIUM PRIORITY
1.

LOW PRIORITY
1. Make setup window blocking like overwrite window - focus appears to be lost when the window is blocking and then closed, although this doesn't appear to happen with overwrite box
2. Add logo
'''

class MainFrame:
    def __init__(self,Master,TestMatrix,Summary,Status):
        self.TestMatrix = TestMatrix
        self.Master = Master
        self.Status = Status
        self.Summary = Summary
        
        # Default column width
        defaultWidth = 20
        # Default box height
        defaultHeight = 20
        
        # Window location
        xpos = 5
        ypos = 65
        
        # Create the subframe
        Subframe = tk.Frame(Master, relief=tk.GROOVE, borderwidth=0)

        # Add list box headers
        GroupBoxLabel           = tk.Label(Subframe, text='GROUPS')
        TestPointBoxLabel       = tk.Label(Subframe, text='TEST POINTS')
        TestPointParamsBoxLabel = tk.Label(Subframe, text='PARAMETERS')

        # Add list boxes
        #Scrollbar1              = tk.Scrollbar(Subframe)
        #Scrollbar2              = tk.Scrollbar(Subframe)
        #Scrollbar3              = tk.Scrollbar(Subframe)
        self.GroupBox           = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=False)#,yscrollcommand=Scrollbar1.set)
        self.TestPointBox       = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=False)#,yscrollcommand=Scrollbar2.set)
        self.TestPointParamsBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=False)#,yscrollcommand=Scrollbar3.set)
        #Scrollbar1.configure(command=self.GroupBox.yview)
        #Scrollbar2.configure(command=self.TestPointBox.yview)
        #Scrollbar3.configure(command=self.TestPointParamsBox.yview)

        # Listbox bindings
        self.GroupBox.bind('<<ListboxSelect>>', lambda x:self.PopulateTestPointBox())
        self.TestPointBox.bind('<<ListboxSelect>>', lambda x:self.PopulateParametersBox())

        # Add buttons
        AddGroupButton           = tk.Button(Subframe, text='ADD',justify=tk.CENTER, command=self.AddGroup, width = int(defaultWidth/2))
        MoveGroupUpButton        = tk.Button(Subframe, text=u"\u25B2",justify=tk.CENTER, command=lambda:self.MoveGroup('UP'), width = int(defaultWidth/2))
        MoveGroupDownButton      = tk.Button(Subframe, text=u"\u25BC",justify=tk.CENTER, command=lambda:self.MoveGroup('DOWN'), width = int(defaultWidth/2))
        RemoveGroupButton        = tk.Button(Subframe, text='REMOVE',justify=tk.CENTER, command=self.RemoveGroup, width = int(defaultWidth/2))
        CopyGroupButton          = tk.Button(Subframe, text='COPY',justify=tk.CENTER, command=self.CopyGroup, width = int(defaultWidth/2))
        RenameGroupButton        = tk.Button(Subframe, text='RENAME',justify=tk.CENTER, command=self.RenameGroup, width = int(defaultWidth/2))

        AddTestPointButton       = tk.Button(Subframe, text='ADD',justify=tk.CENTER, command=self.AddTestPoint, width = int(defaultWidth/2))
        RemoveTestPointButton    = tk.Button(Subframe, text='REMOVE',justify=tk.CENTER, command=self.RemoveTestPoint, width = int(defaultWidth/2))
        MoveTestPointUpButton    = tk.Button(Subframe, text=u"\u25B2",justify=tk.CENTER, command=lambda:self.MoveTestPoint('UP'), width = int(defaultWidth/2))
        MoveTestPointDownButton  = tk.Button(Subframe, text=u"\u25BC",justify=tk.CENTER, command=lambda:self.MoveTestPoint('DOWN'), width = int(defaultWidth/2))

        UpdateParameterButton    = tk.Button(Subframe, text='UPDATE',justify=tk.CENTER, command=self.UpdateParameter, width = defaultWidth)

        # Add input fields
        self.TestPointInput = tk.StringVar(Subframe, value = '')
        TestPointInputField  = tk.Entry(Subframe, width=defaultWidth, textvariable=self.TestPointInput)
        self.ParameterInput = tk.StringVar(Subframe, value = '')
        ParameterInputField = tk.Entry(Subframe, width=defaultWidth, textvariable=self.ParameterInput)
        self.GroupNameInput = tk.StringVar(Subframe, value = '')
        GroupNameInputField = tk.Entry(Subframe, width=defaultWidth, textvariable=self.GroupNameInput)

        # Create test point add type menu
        self.TPAddType  = tk.StringVar()
        self.TPAddType.set('SINGLE') #default value
        TPAddMenu = tk.OptionMenu(Subframe,self.TPAddType,'SINGLE','MULTIPLE','COMBINATION')

        # Grid the items
        GroupBoxLabel.grid(               row=0, column=0, columnspan=2)
        TestPointBoxLabel.grid(           row=0, column=2, columnspan=2)
        TestPointParamsBoxLabel.grid(     row=0, column=4)
        
        self.GroupBox.grid(               row=1, column=0, columnspan=2)
        self.TestPointBox.grid(           row=1, column=2, columnspan=2)
        self.TestPointParamsBox.grid(     row=1, column=4)

        GroupNameInputField.grid(         row=2, column=0, columnspan=2)
        AddGroupButton.grid(              row=3, column=0)
        RemoveGroupButton.grid(           row=3, column=1)
        CopyGroupButton.grid(             row=4, column=0)
        RenameGroupButton.grid(           row=4, column=1)
        MoveGroupUpButton.grid(           row=5, column=0)
        MoveGroupDownButton.grid(         row=5, column=1)

        TestPointInputField.grid(         row=2, column=2, columnspan=2)
        TPAddMenu.grid(                   row=3, column=2, columnspan=2, sticky='WE')
        AddTestPointButton.grid(          row=4, column=2)
        RemoveTestPointButton.grid(       row=4, column=3)
        MoveTestPointUpButton.grid(       row=5, column=2)
        MoveTestPointDownButton.grid(     row=5, column=3)
        
        UpdateParameterButton.grid(       row=3, column=4)
        ParameterInputField.grid(         row=2, column=4)

        # Place frame
        Subframe.place(x=xpos, y=ypos)

        # Create IO frame
        self.IO = IOFrame(self.Master,self.TestMatrix,self.Summary,self.Status)

        # Create an observer on 'TMLoaded' in IOFrame to populate the group list
        # when a test matrix is loaded from a file.
        self.IO.TMLoaded.trace_variable("w",self.LoadGroups)


    def AddGroup(self):
        if self.CheckForSetup() == 1:
            NewName = self.GroupNameInput.get()
            if NewName == '':
                self.Status.SetStatus('No group name given.\n','Error')
            else:
                if (self.TestMatrix.AddGroup(NewName)):
                    self.GroupBox.insert(tk.END, NewName)
                    self.Status.SetStatus('Group \'{0}\' added.\n'.format(NewName))
                    # Update the summary
                    self.Summary.Update()
                else:
                    self.Status.SetStatus('Group \'{0}\' already exists.\n'.format(NewName),'Error')
        else:
            self.Status.SetStatus('No setup exists.\n','Error')
        return None

        
    def RemoveGroup(self):
        if self.CheckForSetup() == 1:
            # Get highlighted group
            Selection = self.GroupBox.curselection()
            if Selection == ():
                self.Status.SetStatus('No group selected.\n','Error')
                return None
            # Remove the group from the test matrix
            self.TestMatrix.RemoveGroup(self.GroupBox.get(Selection[0]))
            # then update stats
            self.Status.SetStatus('Group \'{0}\' removed.\n'.format(self.GroupBox.get(Selection[0])))
            # Update the summary
            self.Summary.Update()
            # and then finally remove from the list box
            self.GroupBox.delete(Selection[0])
        return None


    def CopyGroup(self):
        # Get highlighted group
        Selection = self.GroupBox.curselection()
        if Selection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName = self.GroupBox.get(Selection[0])
        self.TestMatrix.CopyGroup(GroupName,GroupName+'_copy')
        self.GroupBox.insert(Selection[0]+1, GroupName+'_copy')
        self.Status.SetStatus('Group \'{0}\' copied.\n'.format(GroupName))
        # Update the summary
        self.Summary.Update()
        return None


    def RenameGroup(self):
        # Get highlighted selections in listbox
        Selection = self.GroupBox.curselection()
        NewName = self.GroupNameInput.get()
        if Selection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName = self.GroupBox.get(Selection[0])
        if NewName == '':
            self.Status.SetStatus('No group name given.\n','Error')
        else:
            # Rename in test matrix
            self.TestMatrix.RenameGroup(GroupName,NewName)
            # Rename in list box
            self.GroupBox.delete(Selection[0])
            self.GroupBox.insert(Selection[0], NewName)
        return None
    

    def MoveGroup(self,Dir):
        # Get highlighted selections in listbox
        Selection = self.GroupBox.curselection()
        if Selection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName = self.GroupBox.get(Selection[0])
        # Check for corner cases
        if Dir == 'UP' and Selection[0]==0:
            return None
        elif Dir == 'DOWN' and Selection[0]==self.GroupBox.size()-1:
            return None
        else:
            # Move inside the test matrix
            self.TestMatrix.MoveGroup(GroupName,Dir)
            # Move inside the list box
            if Dir == 'UP':
                self.GroupBox.delete(Selection[0])
                self.GroupBox.insert(Selection[0]-1, GroupName)
                self.GroupBox.selection_set(Selection[0]-1)
                self.Status.SetStatus('Group \'{0}\' moved up.\n'.format(GroupName))
            elif Dir == 'DOWN':
                self.GroupBox.delete(Selection[0])
                self.GroupBox.insert(Selection[0]+1, GroupName)
                self.GroupBox.selection_set(Selection[0]+1)
                self.Status.SetStatus('Group \'{0}\' moved down.\n'.format(GroupName))
        return None


    def LoadGroups(self,*args): #args not needed, extra stuff passed in by trace
        # Clear the list box first
        self.GroupBox.delete(0,tk.END)
        # Add the loaded test matrix groups
        for item in self.TestMatrix.GroupNames:
            self.GroupBox.insert(tk.END, item)
        # Update the summary
        self.Summary.Update()
        return None


    def PopulateTestPointBox(self):
        # Clear the test point box
        self.TestPointBox.delete(0, tk.END)
        # Clear the parameters box
        self.TestPointParamsBox.delete(0, tk.END)
        # Get group box selection
        Idx = self.GroupBox.curselection()[0]
        # Isolate the test point group
        TestPointFrame = self.TestMatrix.GroupTestPoints[Idx]

        ##### METHOD 1 #####
        '''
        # Iterate through each row and column and see if each row value in the given
        # column is unique, if it is, add it to the tag
        # Row iteration
        for i in range(len(TestPointFrame)):
            Tag = str(i)+': '
            # Column iteration
            for j in range(len(TestPointFrame.columns)):
                # Get the number of occurances of each unique item in column
                item   = TestPointFrame[TestPointFrame.columns[j]].value_counts().keys().tolist() #value of the row item
                counts = TestPointFrame[TestPointFrame.columns[j]].value_counts().tolist()        #number of occurances of the row item
                # Iterate through the results and add the items that have 1 occurance and are in the current tespoint to the tag 
                for k in range(len(item)):
                    if (counts[k] == 1) and (item[k] == TestPointFrame[TestPointFrame.columns[j]].values[i]):
                        Tag = Tag + TestPointFrame.columns[j] + '=' + str(item[k]) + ','
            Tag = Tag[:-1]
            self.TestPointBox.insert(tk.END, Tag)
        '''

        ##### METHOD 2 #####
        # Check if all values in each column are the same
        TagCol = []
        for i in range(len(TestPointFrame.columns)):
            temp = TestPointFrame[TestPointFrame.columns[i]].unique()
            # If there is more than one unique value, then add the column name
            # to the tag list
            if len(temp) != 1:
                TagCol.append(TestPointFrame.columns[i])
        for i in range(len(TestPointFrame)):
            # Iterate through each row and add the 'TagCol' value to the testpoint tag
            if TagCol != []:
                Tag = str(i) + ': '
                for j in TagCol:
                    Tag = Tag + j + '=' + str(TestPointFrame[j].values[i]) + ','
                Tag = Tag[:-1]
                self.TestPointBox.insert(tk.END, Tag)
            # If the 'TagCol' is empty, add all columns to the tag
            else:
                Tag = str(i) + ': '
                for j in TestPointFrame.columns:
                    Tag = Tag + j + '=' + str(TestPointFrame[j].values[i]) + ','
                self.TestPointBox.insert(tk.END, Tag)
        return None


    def PopulateParametersBox(self):
        # Clear the parameters box
        self.TestPointParamsBox.delete(0, tk.END)
        # Get the currently selected test point and group
        # First get test point and see if one is selcted, otherwise pass
        Idx_testpoint = self.TestPointBox.curselection()
        if Idx_testpoint != ():
            # Just save the first element of the tuple
            Idx_testpoint = Idx_testpoint[0]
            Idx_group     = self.GroupBox.curselection()[0]
            # Isolate the test point group
            TestPointFrame = self.TestMatrix.GroupTestPoints[Idx_group]
            # Isolate the test point itself
            Vals = TestPointFrame.iloc[Idx_testpoint].values
            # Iterate through all the parameters and populate the box
            for i in range(len(TestPointFrame.columns)):
                self.TestPointParamsBox.insert(tk.END, TestPointFrame.columns[i] + ': ' + str(Vals[i]))
        else:
            pass
        return None

    def AddTestPoint(self):
        # Get group selection in listbox
        Selection = self.GroupBox.curselection()
        if Selection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName = self.GroupBox.get(Selection[0])
        # Get testpoint input field data
        InputStr = self.TestPointInput.get()
        # Generate the test point
        Errors, TestPointList = GenerateTestPoint(InputStr,self.TPAddType.get(),self.TestMatrix.Parameters)
        if Errors != 0:
            if Errors == 1:
                self.Status.SetStatus('Input contains an unknown parameter.\n','Error')
                return None
            elif Errors == 2:
                self.Status.SetStatus('Input contains a format error.\n','Error')
                return None
        else:
            # Add test point to matrix
            self.TestMatrix.AddTestPoint(GroupName,TestPointList)
            # Refresh the test point and parameters listbox
            self.PopulateTestPointBox()
            self.PopulateParametersBox()
            # Update status
            self.Status.SetStatus('Testpoint added.\n')
            # Update the summary
            self.Summary.Update()
            return None
    

    def RemoveTestPoint(self):
        # Get highlighted group
        GroupSelection = self.GroupBox.curselection()
        if GroupSelection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        # Get the group name and selected test point
        GroupName    = self.GroupBox.get(GroupSelection[0])
        Selection    = self.TestPointBox.curselection()
        if Selection == ():
            self.Status.SetStatus('No test point selected.\n','Error')
            return None
        # Get test point index
        TestPointIdx = Selection[0]
        # Remove the test point
        self.TestMatrix.RemoveTestPoint(GroupName,TestPointIdx)
        # Refresh the test point box
        self.PopulateTestPointBox()
        self.Status.SetStatus('Testpoint removed.\n')
        # Update the summary
        self.Summary.Update()
        return None
    

    def MoveTestPoint(self,Dir):
        # Get highlighted group
        GroupSelection = self.GroupBox.curselection()
        if GroupSelection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName    = self.GroupBox.get(GroupSelection[0])
        Selection    = self.TestPointBox.curselection()
        if Selection == ():
            self.Status.SetStatus('No test point selected.\n','Error')
            return None
        TestPointIdx = Selection[0]
        # Check for corner cases
        if Dir == 'UP' and TestPointIdx==0:
            return None
        elif Dir == 'DOWN' and TestPointIdx==self.TestPointBox.size()-1:
            return None
        else:
            # Move inside the test matrix
            self.TestMatrix.MoveTestPoint(GroupName,TestPointIdx,Dir)
        # Refresh the test point listbox
        self.PopulateTestPointBox()
        # Update status
        if Dir == 'UP':
            self.Status.SetStatus('Test point {0} moved up.\n'.format(TestPointIdx))
        elif Dir == 'DOWN':
            self.Status.SetStatus('Test point {0} moved down.\n'.format(TestPointIdx))
        return None
    

    def UpdateParameter(self):
        # Get group, testpoint, and parameter selections from listbox
        GroupSelection = self.GroupBox.curselection()
        if GroupSelection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName = self.GroupBox.get(GroupSelection[0])
        TestPointSelection = self.TestPointBox.curselection()
        if TestPointSelection == ():
            self.Status.SetStatus('No test point selected.\n','Error')
            return None
        TestPointIdx = TestPointSelection[0]
        ParamsSelection = self.TestPointParamsBox.curselection()
        if ParamsSelection == ():
            self.Status.SetStatus('No parameter selected.\n','Error')
            return None
        ParameterIdx = ParamsSelection[0]
        ParameterName = self.TestPointParamsBox.get(ParameterIdx).split(':')[0].strip()
        # Get parameter input field data
        Val = self.ParameterInput.get()
        # Update parameter value
        self.TestMatrix.UpdateParameter(GroupName,TestPointIdx,ParameterName,Val)
        # Refresh the test point and parameters listbox
        self.PopulateTestPointBox()
        #   Re-select the testpoint
        self.TestPointBox.selection_set(TestPointIdx)
        self.PopulateParametersBox()
        # Update the summary
        self.Summary.Update()
        return None


    def CheckForSetup(self):
        if self.TestMatrix.Parameters == {}:
            return 0
        else:
            return 1
        

