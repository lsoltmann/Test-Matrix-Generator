import tkinter as tk
import yaml
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


class ParametersWindow:
    def __init__(self,Master,TestMatrix,Summary,Status):
        self.Master = Master
        self.TestMatrix = TestMatrix
        self.Status = Status
        self.Summary = Summary
        self.ParamsYAML = None
        
        # Window size
        WinWidth  = 330
        WinHeight = 575

        # Parameter list box size
        defaultWidth  = 31
        defaultHeight = 25

        MainWindow = tk.Frame(self.Master, width=WinWidth, height=WinHeight)
        self.Master.title('PARAMETERS')
        MainWindow.pack()
        
        # Window location
        xpos = 5
        ypos = 5
        
        # Create the subframe
        Subframe = tk.Frame(self.Master, relief=tk.GROOVE, borderwidth=0)

        # Add list box
        self.ParameterBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)
        self.FlagsBox     = tk.Listbox(Subframe,width=3,height=defaultHeight)

        # Add input fields
        self.ParameterInput = tk.StringVar(Subframe, value = '')
        ParameterInputfield  = tk.Entry(Subframe, width=defaultWidth, textvariable=self.ParameterInput)

        # Add buttons
        LoadTemplateButton    = tk.Button(Subframe, text='LOAD TEMPLATE',justify=tk.CENTER, command=self.LoadTemplate, width = int(defaultWidth/2))
        SaveTemplateButton    = tk.Button(Subframe, text='SAVE TEMPLATE',justify=tk.CENTER, command=self.SaveTemplate, width = int(defaultWidth/2))
        AddParameterButton    = tk.Button(Subframe, text='ADD',justify=tk.CENTER, command=self.Add, width = int(defaultWidth/2))
        RemoveParameterButton = tk.Button(Subframe, text='REMOVE',justify=tk.CENTER, command=self.Remove, width = int(defaultWidth/2))
        SaveCloseButton       = tk.Button(Subframe, text='SAVE AND CLOSE',justify=tk.CENTER, command=self.Export, width = defaultWidth)
        MoveParamUpButton     = tk.Button(Subframe, text=u"\u25B2",justify=tk.CENTER, command=lambda:self.Move('UP'), width = int(defaultWidth/2))
        MoveParamDownButton   = tk.Button(Subframe, text=u"\u25BC",justify=tk.CENTER, command=lambda:self.Move('DOWN'), width = int(defaultWidth/2))
        UpdateParamButton     = tk.Button(Subframe, text='UPDATE',justify=tk.CENTER, command=self.Update, width = int(defaultWidth/2))
        FlagButton            = tk.Button(Subframe, text='SET FLAG',justify=tk.CENTER, command=self.SetFlag, width = int(defaultWidth/2))

        # Grid the items
        LoadTemplateButton.grid(    row=0, column=0)
        SaveTemplateButton.grid(    row=0, column=1)
        self.ParameterBox.grid(     row=1, column=0, columnspan=2)
        self.FlagsBox.grid(         row=1, column=2)
        ParameterInputfield.grid(   row=2, column=0, columnspan=2)
        AddParameterButton.grid(    row=3, column=0)
        RemoveParameterButton.grid( row=3, column=1)
        MoveParamUpButton.grid(     row=4, column=0)
        MoveParamDownButton.grid(   row=4, column=1)
        UpdateParamButton.grid(     row=5, column=0)
        FlagButton.grid(            row=5, column=1)
        SaveCloseButton.grid(       row=6, column=0, columnspan=2)

        # Disable flags listbox
        self.DisableFlags()
        
        # Place frame
        Subframe.place(x=xpos, y=ypos)

        # Check to to see if a test matrix already exists
        self.CheckForExistingTestMatrix()


    def CheckForExistingTestMatrix(self):
        # If test matrix does exist, populate the parameters box
        if self.TestMatrix.CheckExistence() == 1:
            for key,value in self.TestMatrix.Parameters.items():
                self.ParameterBox.insert(tk.END, key+':'+str(value['VALUE']))
                self.EnableFlags()
                self.FlagsBox.insert(tk.END, str(value['FLAG']))
                self.DisableFlags()
        else:
            # If one doesn't exist, don't add anything else
            pass
        return None
    

    def LoadTemplate(self):
        try:
            if self.TestMatrix.CheckExistence() == 1:
                self.Status.SetStatus('PARAMETERS:Can not load a template, a test matrix already exists.\n','Error')
            else:
                # Clear the variable where ther raw YAML data is stored
                self.ParamsYAML = None
                # Clear the list box
                self.ParameterBox.delete(0,tk.END)
                # Get full file path
                FullFilePath = askopenfilename(multiple=False)
                if FullFilePath != '':
                    # Extract the file name
                    TemplateParams = yaml.safe_load(open(FullFilePath,'r'))
                    # Add the user parameters to the listbox
                    for key,value in TemplateParams.items():
                        ParamText  = key+':'+str(value['VALUE'])
                        FlagText   = str(value['FLAG'])
                        for x in FlagText:
                            if x not in self.TestMatrix.ParametersFlagsOptions:
                                self.Status.SetStatus('PARAMETERS:Unknown flag ''{0}''.\n'.format(x),'Error')
                                return None
                        # Parameters box
                        self.ParameterBox.insert(tk.END, ParamText)
                        # Flags box
                        self.EnableFlags()
                        self.FlagsBox.insert(tk.END, FlagText)
                        self.DisableFlags()
                    # Check for duplicates
                    temp = [x.split(':')[0] for x in self.ParameterBox.get(0,tk.END)]
                    if len(temp) != len(set(temp)):
                        self.ParameterBox.delete(0,tk.END)
                        self.FlagsBox.delete(0,tk.END)
                        self.Status.SetStatus('PARAMETERS:Template contains duplicates.\n','Error')
                        return None
                    self.Status.SetStatus('PARAMETERS:Template loaded.\n','Normal')
                    # Save the YAML data
                    self.ParamsYAML = TemplateParams
        except:
            self.Status.SetStatus('PARAMETERS:Template load error.\n','Error')
        return None


    def SaveTemplate(self):
        # Get full file path
        FullFilePath = asksaveasfilename(defaultextension='.yaml', filetypes={('YAML file', '*.yaml')})
        # Open the target save file
        FID = open(FullFilePath,'w')
        # Convert listbox data to a dictionary
        dataout = {}
        for i in range(self.ParameterBox.size()):
            tempparam = self.ParameterBox.get(i)
            tempparam = tempparam.split(':')
            tempflag = self.FlagsBox.get(i)
            # Check for an existing test matrix for the timing data
            if self.TestMatrix.Parameters == {}:
                # If one doesn't exist, use the defaults
                TimeVal  = 0
                TimeFlag = self.TestMatrix.TimingFlagOptions[0]
            else:
                if tempparam[0] in self.TestMatrix.Parameters:
                    TimeVal = self.TestMatrix.Parameters[tempparam[0]]['TIMING']['VALUE']
                    TimeFlag = self.TestMatrix.Parameters[tempparam[0]]['TIMING']['FLAG']
                else:
                    TimeVal  = 0
                    TimeFlag = self.TestMatrix.TimingFlagOptions[0]   
            dataout[tempparam[0].strip()] = {'VALUE':tempparam[1].strip(),'FLAG':tempflag.strip(),
                                             'TIMING':{'VALUE':TimeVal,'FLAG':TimeFlag}}
        # Write the dictionary to the yaml file
        yaml.dump(dataout,FID, default_flow_style=False, sort_keys=False)
        self.Status.SetStatus('PARAMETERS:Template saved.\n','Normal')
        return None


    def Add(self):
        ParamInput = self.ParameterInput.get()
        # Split input
        temp = ParamInput.split(':')
        if len(temp) == 2:
            # Check if parameter already exists
            if temp[0] in [x.split(':')[0] for x in self.ParameterBox.get(0,tk.END)]:
                self.Status.SetStatus('PARAMETERS:Parameter ''{0}'' already exists.\n'.format(temp[0]),'Error')
                return None
            # Add parameter to listbox
            self.ParameterBox.insert(tk.END, temp[0]+':'+temp[1])
            self.EnableFlags()
            self.FlagsBox.insert(tk.END, self.TestMatrix.ParametersFlagsOptions[0])
            self.DisableFlags()
            self.Status.SetStatus('PARAMETERS:Parameter added.\n','Normal')
        else:
            self.Status.SetStatus('PARAMETERS:Input syntax not recognized. Input format is NAME:VAL\n','Error')
        return None
        

    def Remove(self):
        # Get highlighted selections in listbox
        Selection = self.ParameterBox.curselection()
        if Selection != ():
            self.ParameterBox.delete(Selection[0])
            self.EnableFlags()
            self.FlagsBox.delete(Selection[0])
            self.DisableFlags()
            self.Status.SetStatus('PARAMETERS:Parameter removed.\n','Normal')
        return None


    def Move(self,Dir):
        # Get highlighted parameter in listbox
        Selection = self.ParameterBox.curselection()
        if Selection == ():
            self.Status.SetStatus('PARAMETERS:No parameter selected.\n','Error')
            return None
        ParamName = self.ParameterBox.get(Selection[0])
        ParamFlag = self.FlagsBox.get(Selection[0])
        if Selection != ():
            # Check for corner cases
            if Dir == 'UP' and Selection[0]==0:
                return None
            elif Dir == 'DOWN' and Selection[0]==self.ParameterBox.size()-1:
                return None
            else:
                # Move inside the list box
                if Dir == 'UP':
                    # Parameters list box
                    self.ParameterBox.delete(Selection[0])
                    self.ParameterBox.insert(Selection[0]-1, ParamName)
                    self.ParameterBox.selection_set(Selection[0]-1)
                    # Flags list box
                    self.EnableFlags()
                    self.FlagsBox.delete(Selection[0])
                    self.FlagsBox.insert(Selection[0]-1, ParamFlag)
                    self.FlagsBox.selection_set(Selection[0]-1)
                    self.DisableFlags()
                    self.Status.SetStatus('PARAMETERS:Parameter \'{0}\' moved up.\n'.format(ParamName.split(':')[0].strip()))
                elif Dir == 'DOWN':
                    # Parameters list box
                    self.ParameterBox.delete(Selection[0])
                    self.ParameterBox.insert(Selection[0]+1, ParamName)
                    self.ParameterBox.selection_set(Selection[0]+1)
                    # Flags list box
                    self.EnableFlags()
                    self.FlagsBox.delete(Selection[0])
                    self.FlagsBox.insert(Selection[0]+1, ParamFlag)
                    self.FlagsBox.selection_set(Selection[0]+1)
                    self.DisableFlags()
                    self.Status.SetStatus('PARAMETERS:Parameter \'{0}\' moved down.\n'.format(ParamName.split(':')[0].strip()))
            return None


    def Update(self):
        # Get current selection
        Selection = self.ParameterBox.curselection()
        if Selection != ():
            ParameterIdx = Selection[0]
            # Get the parameter name
            ParameterName = self.ParameterBox.get(ParameterIdx).split(':')[0]
            # Get parameter input field data
            Val = self.ParameterInput.get()
            # Make sure input string is formatted  correctly
            if len(Val.split(':')) != 1:
                self.Status.SetStatus('PARAMETERS:Input syntax not recognized. Input must be a value/string only.\n','Error')
            else:
                # Remove the old parameter
                self.ParameterBox.delete(ParameterIdx)
                # Combine and add parameter back to listbox
                self.ParameterBox.insert(ParameterIdx, ParameterName+':'+str(Val))
        return None


    def EnableFlags(self):
        self.FlagsBox.configure(state="normal")
        return None


    def DisableFlags(self):
        self.FlagsBox.configure(state="disabled")
        return None


    def SetFlag(self):
        # Get highlighted selection in listbox
        Selection = self.ParameterBox.curselection()
        if Selection == ():
            self.Status.SetStatus('PARAMETERS:No parameter selected.\n','Error')
            return None
        # Get the parameter index
        ParamIdx = Selection[0]
        # Get input field
        Flag = self.ParameterInput.get()
        # Check validity of input
        Error = 0
        if Flag == '':
            Flag = self.TestMatrix.ParametersFlagsOptions[0]
        elif (self.TestMatrix.ParametersFlagsOptions[0] in Flag) and len(Flag)>1:
            Flag = self.TestMatrix.ParametersFlagsOptions[0]
            self.Status.SetStatus('PARAMETERS:Flag input contains null flag and others. Using null flag only.\n','Warning')
            Error = 1
        else:
            for i in Flag:
                if i not in self.TestMatrix.ParametersFlagsOptions:
                   self.Status.SetStatus('PARAMETERS:Flag \'{0}\' not recognized. Null flag set.\n'.format(i),'Error')
                   Error = 1
            if Error == 1:
                Flag = self.TestMatrix.ParametersFlagsOptions[0]
        # Update the list box
        self.EnableFlags()
        self.FlagsBox.delete(ParamIdx)
        self.FlagsBox.insert(ParamIdx, Flag)
        self.DisableFlags()
        if Error == 0:
            self.Status.SetStatus('PARAMETERS:Flag set.\n','Normal')
        return None


    def Export(self):
        # Save the list to the testmatrix
        ParamsList = self.ParameterBox.get(0, tk.END)
        ParamFlagList = self.FlagsBox.get(0, tk.END)
        # Combine the parameters and flags
        CombinedList = []
        for i in range(len(ParamsList)):
            CombinedList.append(ParamsList[i]+':'+ParamFlagList[i])

        # --- CASE 1 --- No previous test matrix exists
        if self.TestMatrix.CheckExistence() == 0:
            for x in CombinedList:
                temp = [y.strip() for y in x.split(':')]
                if self.ParamsYAML is not None:
                    if temp[0] in self.ParamsYAML:
                        self.TestMatrix.AddParameter(temp[0],temp[1],temp[2],{'FLAG':self.ParamsYAML[temp[0]]['TIMING']['FLAG'],
                                                                              'VALUE':self.ParamsYAML[temp[0]]['TIMING']['VALUE']})
                    else:
                        self.TestMatrix.AddParameter(temp[0],temp[1],temp[2],{'FLAG':'C','VALUE':0})
                else:
                    self.TestMatrix.AddParameter(temp[0],temp[1],temp[2],{'FLAG':'C','VALUE':0})

        # --- CASE 2 --- Previous test matrix exists    
        elif self.TestMatrix.CheckExistence() == 1:
            # 1, check to see if the user added any parameters
            # List for keeping track of parameter order
            ParamsOrder = []
            for x in CombinedList:
                temp = [y.strip() for y in x.split(':')]
                if temp[0] not in self.TestMatrix.Parameters:
                    self.TestMatrix.AddParameter(temp[0],temp[1],temp[2],{'FLAG':'C','VALUE':0})
                # Append parameter name to order list
                ParamsOrder.append(temp[0])
       
            # 2, check to see if user removed any parameters
            RemoveList = []
            for key,value in self.TestMatrix.Parameters.items():
                # If the parameter is in the test matrix but not in the user defined list,
                # add it to the remove list. [Can't remove the parameter from the test
                # matrix here because it will change the the length of the Parameters
                # dictionary]
                if key not in ParamsOrder:
                    RemoveList.append(key)
            # Now remove the parameters from the test matrix
            for x in RemoveList:
                self.TestMatrix.RemoveParameter(x)

            # 3, check to see if the user changed the order of the parameters
            self.TestMatrix.ReorderParameters(ParamsOrder)

            # 4, update all the parameter values and flags
            for x in CombinedList:
                temp = [y.strip() for y in x.split(':')]
                self.TestMatrix.ModifyParameter(temp[0],temp[1],temp[2])        

        self.Status.SetStatus('PARAMETERS:Saved.\n')
        self.Summary.Update()
        # Close the window
        self.Master.destroy()
