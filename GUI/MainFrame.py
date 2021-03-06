import tkinter as tk
from Core.GenerateTestPoint import GenerateTestPoint
from GUI.IOFrame import IOFrame

'''
TODO:
HIGH PRIORITY
1. 

MEDIUM PRIORITY
1.

LOW PRIORITY
1. 
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
        self.TestPointBox       = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=False,selectmode=tk.EXTENDED)#,yscrollcommand=Scrollbar2.set)
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
        CopyBelowButton          = tk.Button(Subframe, text='COPY BELOW',justify=tk.CENTER, command=self.CopyBelow, width = int(defaultWidth/2))
        CopyBottomButton         = tk.Button(Subframe, text='COPY BOTTOM',justify=tk.CENTER, command=self.CopyBottom, width = int(defaultWidth/2))

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
        CopyBelowButton.grid(             row=6, column=2)
        CopyBottomButton.grid(            row=6, column=3)
        
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
        self.TestMatrix.CopyGroup(GroupName,GroupName+'_copy',Selection[0]+1)
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
        # Clear all the list boxes first
        self.GroupBox.delete(0,tk.END)
        self.TestPointBox.delete(0,tk.END)
        self.TestPointParamsBox.delete(0,tk.END)
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
        # Populate the group entry field with the group name
        GrpName = self.GroupBox.get(Idx)
        self.GroupNameInput.set(GrpName)
        # Isolate the test point group
        TestPointFrame = self.TestMatrix.GroupTestPoints[Idx]
        # Check if all values in each column are the same
        TagCol = []
        for i in range(len(TestPointFrame.columns)):
            temp = TestPointFrame[TestPointFrame.columns[i]].unique()
            # If there is more than one unique value, then add the column name
            # to the tag list
            if len(temp) != 1:
                TagCol.append(TestPointFrame.columns[i])
        # If all values are unique (i.e. they are the same across all rows), add
        # all the columns to the tag
        if TagCol == []:
            TagCol = list(TestPointFrame.columns)
        # Check for ignore columns and remove them if found
        for item in TagCol:
            if '!' in self.TestMatrix.Parameters[item]['FLAG']:
                del TagCol[TagCol.index(item)]
        for i in range(len(TestPointFrame)):
            # Iterate through each row and add the 'TagCol' value to the testpoint tag
            Tag = str(i+1) + ': '
            for j in TagCol:
                # Check if value is a string or number
                try:
                    # If the value is a number, check if it's in integer or a float
                    TagVal = float(TestPointFrame[j].values[i])
                    if TagVal.is_integer():
                        TagVal = '{0:d}'.format(TagVal)
                    else:
                        # If it's a float, limit the number of decimal places shown
                        TagVal = '{0:.2f}'.format(TagVal)
                except:
                    TagVal = str(TestPointFrame[j].values[i])
                Tag = Tag + j + '=' + TagVal + ','
            Tag = Tag[:-1]
            self.TestPointBox.insert(tk.END, Tag)
        return None


    def PopulateParametersBox(self):
        # Clear the parameters box
        self.TestPointParamsBox.delete(0, tk.END)
        # Get the currently selected test point and group
        Idx_testpoint = self.TestPointBox.curselection()
        Idx_group     = self.GroupBox.curselection()[0]
        if Idx_testpoint == ():
            pass
        else:
            # Turn the tuple into a list
            Idx_testpoint = list(Idx_testpoint)
            # Grab the parameter names
            ParamNames = self.TestMatrix.GroupTestPoints[Idx_group].columns
            # Grab the parameter values from the first selection
            # NOTE: assigning df.values to variable does not create a copy, it creates a link. We need a
            # copy so iterate through to create a new list.
            ParamVals  = [x for x in self.TestMatrix.GroupTestPoints[Idx_group].iloc[Idx_testpoint[0]].values]
            # Remove the first selection entry since we already copied it
            del Idx_testpoint[0]
            for i in Idx_testpoint:
                temp = self.TestMatrix.GroupTestPoints[Idx_group].iloc[i].values
                for j in range(len(temp)):
                    if temp[j] != ParamVals[j]:
                        ParamVals[j] = '<VARIES>'
            # Iterate through all the parameters and populate the box
            for i in range(len(ParamVals)):
                # Check if value is a string or number
                try:
                    # If the value is a number, check if it's in integer or a float
                    ParamVal = float(ParamVals[i])
                    if ParamVal.is_integer():
                        ParamVal = '{0:d}'.format(ParamVal)
                    else:
                        # If it's a float, limit the number of decimal places shown
                        ParamVal = '{0:.4f}'.format(ParamVal)
                except:
                    ParamVal = str(ParamVals[i])
                self.TestPointParamsBox.insert(tk.END, ParamNames[i] + ': ' + ParamVal)

        
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
            # Update the summary
            self.Summary.Update()
            # Refresh the test point and parameters listbox
            self.PopulateTestPointBox()
            self.PopulateParametersBox()
            # Update status
            self.Status.SetStatus('Testpoint added.\n')
            # Move the window view to the bottom
            self.TestPointBox.yview_moveto(1.0)
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
            self.Status.SetStatus('No test point(s) selected.\n','Error')
            return None
        # Convert selection to list
        Selection = list(Selection)
        # Reverse order of selection, this prevents reindexing during removal
        Selection.reverse()
        for Idx in Selection:
            # Remove the test point
            self.TestMatrix.RemoveTestPoint(GroupName,Idx)
        # Update the summary
        self.Summary.Update()
        # Refresh the test point box
        self.PopulateTestPointBox()
        self.Status.SetStatus('Testpoint removed.\n')
        return None
    

    def MoveTestPoint(self,Dir):
        # Get highlighted group
        GroupSelection = self.GroupBox.curselection()
        if GroupSelection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName    = self.GroupBox.get(GroupSelection[0])
        Selection    = self.TestPointBox.curselection()
        Selection    = list(Selection)
        if Selection == ():
            self.Status.SetStatus('No test point(s) selected.\n','Error')
            return None        
        # Check for corner cases
        # Note that the selection tuple is in increasing order
        if Dir == 'UP' and Selection[0]==0:
            return None
        elif Dir == 'DOWN' and Selection[-1]==self.TestPointBox.size()-1:
            return None
        else:
            # If direction is down, reverse the index order
            if Dir == 'DOWN':
                Selection.reverse()
            # Move each test point inside the test matrix
            for IDX in Selection:
                self.TestMatrix.MoveTestPoint(GroupName,IDX,Dir)
        # Update the summary
        self.Summary.Update()
        # Refresh the test point listbox
        self.PopulateTestPointBox()
        # Update status and highlight the moved test point
        if Dir == 'UP':
            Selection =[i-1 for i in Selection]
            self.Status.SetStatus('Test point(s) moved up.\n')
        elif Dir == 'DOWN':
            Selection =[i+1 for i in Selection]
            self.Status.SetStatus('Test point(s) moved down.\n')
        for IDX in Selection:
            self.TestPointBox.selection_set(IDX)
        # Populate the parameters box
        self.PopulateParametersBox()
        return None


    # Puts a copy of the testpoint(s) directly below the orginal
    def CopyBelow(self):
        # Get the current window view
        ScrollView = self.TestPointBox.yview()
        # Get the selected test points and run checks
        BaseSelection,GroupName = self.CopyTestPointCommon()
        # Reverse order of base selection, this prevents reindexing during copying
        BaseSelection.reverse()
        # Get the indices of the copy locations
        CopySelection = [x+1 for x in BaseSelection]
        for i in range(len(BaseSelection)):
            self.TestMatrix.CopyTestPoint(GroupName,BaseSelection[i],CopySelection[i])
        # Update the summary
        self.Summary.Update()
        # Refresh the test point box
        self.PopulateTestPointBox()
        # Select the copied testpoint(s)
        # Reverse the selection order again
        CopySelection.reverse()
        for i in range(len(CopySelection)):
            self.TestPointBox.selection_set(CopySelection[i]+i)
        # Populate the parameters box
        self.PopulateParametersBox()
        # Set the window view back to what it was
        self.TestPointBox.yview_moveto(ScrollView[0])
        return None


    # Puts a copy of the testpoint(s) at the bottom of the matrix (for the specified group)
    def CopyBottom(self):
        # Get the selected test points and run checks
        BaseSelection,GroupName = self.CopyTestPointCommon()
        LastIdx = self.TestPointBox.size()-1
        CopySelection = [x+1 for x in range(len(BaseSelection))]
        CopySelection = [x+LastIdx for x in CopySelection]
        for i in range(len(BaseSelection)):
            self.TestMatrix.CopyTestPoint(GroupName,BaseSelection[i],CopySelection[i])
        # Update the summary
        self.Summary.Update()
        # Refresh the test point box
        self.PopulateTestPointBox()
        # Select the copied testpoint(s)
        for i in CopySelection:
            self.TestPointBox.selection_set(i)
        # Populate the parameters box
        self.PopulateParametersBox()
        # Move the window view to the bottom
        self.TestPointBox.yview_moveto(1.0)
        return None


    def CopyTestPointCommon(self):
        # Get highlighted group
        GroupSelection = self.GroupBox.curselection()
        if GroupSelection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName    = self.GroupBox.get(GroupSelection[0])
        Selection    = self.TestPointBox.curselection()
        Selection    = list(Selection)
        if Selection == ():
            self.Status.SetStatus('No test point(s) selected.\n','Error')
            return None
        Selection = list(Selection)
        return Selection,GroupName
    

    def UpdateParameter(self):
        # Get the current test point window view
        ScrollView = self.TestPointBox.yview()
        # Get group, testpoint, and parameter selections from listbox
        GroupSelection = self.GroupBox.curselection()
        if GroupSelection == ():
            self.Status.SetStatus('No group selected.\n','Error')
            return None
        GroupName = self.GroupBox.get(GroupSelection[0])
        TestPointSelection = self.TestPointBox.curselection()
        if TestPointSelection == ():
            self.Status.SetStatus('No test point(s) selected.\n','Error')
            return None
        TestPointIdx = TestPointSelection
        ParamsSelection = self.TestPointParamsBox.curselection()
        if ParamsSelection == ():
            self.Status.SetStatus('No parameter selected.\n','Error')
            return None
        ParameterIdx = ParamsSelection[0]
        ParameterName = self.TestPointParamsBox.get(ParameterIdx).split(':')[0].strip()
        # Get parameter input field data
        Val = self.ParameterInput.get()
        # Update parameter value
        for i in TestPointIdx:
            self.TestMatrix.UpdateParameter(GroupName,i,ParameterName,Val)
        # Update the summary
        self.Summary.Update()
        # Refresh the test point and parameters listbox
        self.PopulateTestPointBox()
        #   Re-select the testpoint
        for i in TestPointIdx:
            self.TestPointBox.selection_set(i)
        self.PopulateParametersBox()
        # Set the test point window view back to what it was
        self.TestPointBox.yview_moveto(ScrollView[0])
        return None


    def CheckForSetup(self):
        if self.TestMatrix.Parameters == {}:
            return 0
        else:
            return 1
        

