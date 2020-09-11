import tkinter as tk
import yaml
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


class DefinitionsWindow:
    def __init__(self,Master,TestMatrix,Summary,Status):
        self.Master     = Master
        self.TestMatrix = TestMatrix
        self.Status     = Status
        self.Summary    = Summary
        
        # Window size
        WinWidth  = 330
        WinHeight = 575

        # Parameter list box size
        defaultWidth  = 31
        defaultHeight = 25

        MainWindow = tk.Frame(self.Master, width=WinWidth, height=WinHeight)
        self.Master.title('DEFINITIONS')
        MainWindow.pack()
        
        # Window location
        xpos = 5
        ypos = 5
        
        # Create the subframe
        Subframe = tk.Frame(self.Master, relief=tk.GROOVE, borderwidth=0)

        # Add list box
        self.DefinitionsBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)
        self.FlagsBox       = tk.Listbox(Subframe,width=3,height=defaultHeight)
        self.DefinitionsBox.bind('<MouseWheel>',self.MouseScroll)
        self.FlagsBox.bind('<MouseWheel>',self.MouseScroll)
        self.DefinitionsBox.bind('<Up>',self.ArrowScrollUp)
        self.FlagsBox.bind('<Up>',self.ArrowScrollUp)
        self.DefinitionsBox.bind('<Down>',self.ArrowScrollDown)
        self.FlagsBox.bind('<Down>',self.ArrowScrollDown)

        # Add input fields
        self.DefinitionsInput = tk.StringVar(Subframe, value = '')
        Inputfield            = tk.Entry(Subframe, width=defaultWidth, textvariable=self.DefinitionsInput)

        # Add buttons
        LoadTemplateButton    = tk.Button(Subframe, text='LOAD TEMPLATE',justify=tk.CENTER, command=self.LoadTemplate, width = int(defaultWidth/2))
        SaveTemplateButton    = tk.Button(Subframe, text='SAVE TEMPLATE',justify=tk.CENTER, command=self.SaveTemplate, width = int(defaultWidth/2))
        AddButton             = tk.Button(Subframe, text='ADD',justify=tk.CENTER, command=self.Add, width = int(defaultWidth/2))
        RemoveButton          = tk.Button(Subframe, text='REMOVE',justify=tk.CENTER, command=self.Remove, width = int(defaultWidth/2))
        FlagButton            = tk.Button(Subframe, text='UPDATE FLAG',justify=tk.CENTER, command=self.SetFlag, width = int(defaultWidth/2))
        SaveCloseButton       = tk.Button(Subframe, text='SAVE AND CLOSE',justify=tk.CENTER, command=self.Export, width = defaultWidth)
        UpdateButton          = tk.Button(Subframe, text='UPDATE DEF',justify=tk.CENTER, command=self.Update, width = int(defaultWidth/2))

        # Grid the items
        LoadTemplateButton.grid(    row=0, column=0)
        SaveTemplateButton.grid(    row=0, column=1)
        self.DefinitionsBox.grid(   row=1, column=0, columnspan=2)
        Inputfield.grid(            row=2, column=0, columnspan=2)
        AddButton.grid(             row=3, column=0)
        RemoveButton.grid(          row=3, column=1)
        UpdateButton.grid(          row=4, column=0)
        FlagButton.grid(            row=4, column=1)
        SaveCloseButton.grid(       row=5, column=0, columnspan=2)
        self.FlagsBox.grid(         row=1, column=2)

        # Disable flags listbox
        self.DisableFlags()
        
        # Place frame
        Subframe.place(x=xpos, y=ypos)

        # Check to to see if a test matrix already exists
        self.CheckForExistingTestMatrix()


    def CheckForExistingTestMatrix(self):
        # If test matrix does exist, populate the definitions box
        if self.TestMatrix.CheckExistence() == 1:
            for key,value in self.TestMatrix.Definitions.items():
                self.DefinitionsBox.insert(tk.END, key+':'+str(value['VALUE']))
                self.EnableFlags()
                self.FlagsBox.insert(tk.END, str(value['FLAG']))
                self.DisableFlags()
        else:
            # If one doesn't exist, don't add anything else
            pass
        return None
    

    def LoadTemplate(self):
        try:
            # Clear the list box
            self.DefinitionsBox.delete(0,tk.END)
            # Get full file path
            FullFilePath = askopenfilename(multiple=False)
            if FullFilePath != '':
                # Extract the file name
                TemplateDefs = yaml.safe_load(open(FullFilePath,'r'))
                # Add the user definitions to the listbox
                for key,value in TemplateDefs.items():
                    DefText  = key+':'+str(value['VALUE'])
                    FlagText = str(value['FLAG'])
                    for x in FlagText:
                        if x not in self.TestMatrix.DefinitionsFlagsOptions:
                            self.Status.SetStatus('DEFINITIONS:Unknown flag ''{0}''.\n'.format(x),'Error')
                            return None
                    # Definitions box
                    self.DefinitionsBox.insert(tk.END, DefText)
                    # Flags box
                    self.EnableFlags()
                    self.FlagsBox.insert(tk.END, FlagText)
                    self.DisableFlags()
                # Check for duplicates
                temp = [x.split(':')[0] for x in self.DefinitionsBox.get(0,tk.END)]
                if len(temp) != len(set(temp)):
                    self.DefinitionsBox.delete(0,tk.END)
                    self.FlagsBox.delete(0,tk.END)
                    self.Status.SetStatus('DEFINITIONS:Template contains duplicates.\n','Error')
                    return None
                self.Status.SetStatus('DEFINITIONS:Template loaded.\n','Normal')
        except:
            self.Status.SetStatus('DEFINITIONS:Template load error.\n','Error')
        return None


    def SaveTemplate(self):
        # Get full file path
        FullFilePath = asksaveasfilename(defaultextension='.yaml', filetypes={('YAML file', '*.yaml')})
        # Open the target save file
        FID = open(FullFilePath,'w')
        # Convert listbox data to a dictionary
        dataout = {}
        for i in range(self.DefinitionsBox.size()):
            tempdef = self.DefinitionsBox.get(i)
            tempdef = tempdef.split(':')
            tempflag = self.FlagsBox.get(i)
            dataout[tempdef[0].strip()] = {'VALUE':tempdef[1].strip(),'FLAG':tempflag.strip()}
        # Write the dictionary to the yaml file
        yaml.dump(dataout,FID, default_flow_style=False, sort_keys=False)
        self.Status.SetStatus('DEFINITIONS:Template saved.\n','Normal')
        return None


    def Add(self):
        DefInput = self.DefinitionsInput.get()
        # Split input
        # Input format: Name:Value,Flag or Name:Value
        temp = DefInput.split(':')
        # Check if more than one colon exists
        if len(temp) != 2:
            self.Status.SetStatus('DEFINITIONS:Input syntax not recognized. Input format is NAME:VAL or NAME:VAL,FLAG\n','Error')
            return None
        # Extract definition name
        DefName = temp[0]
        # Check if a flag was included
        # but first check if the input was a list or not
        if ('[' in temp[1]) and (']' in temp[1]):
            temp = temp[1].split('],')
            # Add the last bracket back in (removed by split) if the split was successful
            if temp[0][-1] != ']':
                temp[0] = temp[0]+']'
        else:
            temp = temp[1].split(',')        
        DefVal = temp[0]
        if len(temp) == 2:
            DefFlag = temp[1]
        else:
            DefFlag = self.TestMatrix.DefinitionsFlagsOptions[0]
        # Check if definition already exists
        if DefName in [x.split(':')[0] for x in self.DefinitionsBox.get(0,tk.END)]:
            self.Status.SetStatus('DEFINITIONS:Definition ''{0}'' already exists.\n'.format(DefName),'Error')
            return None
        # Check flag
        Error,DefFlag = self.FlagCheck(DefFlag)
        # Add definition to listbox
        self.DefinitionsBox.insert(tk.END, DefName + ':' + DefVal)
        self.EnableFlags()
        self.FlagsBox.insert(tk.END, DefFlag)
        self.DisableFlags()
        self.Status.SetStatus('DEFINITIONS:Definition added.\n','Normal')
        # Move the window view to the bottom
        self.DefinitionsBox.yview_moveto(1.0)
        self.FlagsBox.yview_moveto(1.0)
        return None
        

    def Remove(self):
        # Get the current window view
        ScrollView = self.DefinitionsBox.yview()
        # Get highlighted selections in listbox
        Selection = self.DefinitionsBox.curselection()
        if Selection != ():
            self.DefinitionsBox.delete(Selection[0])
            self.EnableFlags()
            self.FlagsBox.delete(Selection[0])
            self.DisableFlags()
            self.Status.SetStatus('DEFINITIONS:Definition removed.\n','Normal')
             # Set the window view back to what it was
            self.DefinitionsBox.yview_moveto(ScrollView[0])
            self.FlagsBox.yview_moveto(ScrollView[0])
        return None


    def Update(self):
        # Get the current window view
        ScrollView = self.DefinitionsBox.yview()
        # Get current selection
        Selection = self.DefinitionsBox.curselection()
        if Selection != ():
            DefIdx = Selection[0]
            # Get the definition name
            DefName = self.DefinitionsBox.get(DefIdx).split(':')[0]
            # Get definition input field data
            Val = self.DefinitionsInput.get()
            # Make sure input string is formatted  correctly
            if len(Val.split(':')) != 1:
                self.Status.SetStatus('DEFINITIONS:Input syntax not recognized. Input must be a value/string only.\n','Error')
            else:
                # Remove the old definition
                self.DefinitionsBox.delete(DefIdx)
                # Combine and add definition back to listbox
                self.DefinitionsBox.insert(DefIdx, DefName+':'+str(Val))
                # Set the window view back to what it was
                self.DefinitionsBox.yview_moveto(ScrollView[0])
                self.FlagsBox.yview_moveto(ScrollView[0]) 
        return None


    def EnableFlags(self):
        self.FlagsBox.configure(state="normal")
        return None


    def DisableFlags(self):
        self.FlagsBox.configure(state="disabled")
        return None


    def SetFlag(self):
        # Get the current window view
        ScrollView = self.DefinitionsBox.yview()
        # Get highlighted selection in listbox
        Selection = self.DefinitionsBox.curselection()
        if Selection == ():
            self.Status.SetStatus('DEFINITIONS:No parameter selected.\n','Error')
            return None
        # Get the definition index
        DefIdx = Selection[0]
        # Get input field
        Flag = self.DefinitionsInput.get()
        # Check validity of input
        Error,Flag = self.FlagCheck(Flag)
        # Update the list box
        self.EnableFlags()
        self.FlagsBox.delete(DefIdx)
        self.FlagsBox.insert(DefIdx, Flag)
        self.DisableFlags()
        if Error == 0:
            self.Status.SetStatus('DEFINITIONS:Flag set.\n','Normal')
        # Set the window view back to what it was
        self.DefinitionsBox.yview_moveto(ScrollView[0])
        self.FlagsBox.yview_moveto(ScrollView[0]) 
        return None


    def FlagCheck(self,Flag):
        Error = 0
        if Flag == '':
            Flag = self.TestMatrix.DefinitionsFlagsOptions[0]
        elif (self.TestMatrix.DefinitionsFlagsOptions[0] in Flag) and len(Flag)>1:
            Flag = self.TestMatrix.DefinitionsFlagsOptions[0]
            self.Status.SetStatus('DEFINITIONS:Flag input contains null flag and others. Using null flag only.\n','Warning')
            Error = 1
        else:
            for i in Flag:
                if i not in self.TestMatrix.DefinitionsFlagsOptions:
                   self.Status.SetStatus('DEFINITIONS:Flag \'{0}\' not recognized. Null flag set.\n'.format(i),'Error')
                   Error = 1
            if Error == 1:
                Flag = self.TestMatrix.DefinitionsFlagsOptions[0]
        return Error,Flag
    

    def MouseScroll(self,event):
        self.DefinitionsBox.yview('scroll',event.delta,'units')
        self.FlagsBox.yview('scroll',event.delta,'units')
        return 'break'


    def ArrowScrollUp(self,event):
        self.DefinitionsBox.yview('scroll',-1,'units')
        self.FlagsBox.yview('scroll',-1,'units')
        return 'break'


    def ArrowScrollDown(self,event):
        self.DefinitionsBox.yview('scroll',1,'units')
        self.FlagsBox.yview('scroll',1,'units')
        return 'break'

    
    def Export(self):
        # Get the contents of the list boxes
        DefList     = self.DefinitionsBox.get(0, tk.END)
        DefFlagList = self.FlagsBox.get(0, tk.END)
        # Combine the definitions and flags
        CombinedList = []
        for i in range(len(DefList)):
            CombinedList.append(DefList[i]+':'+DefFlagList[i])

        # --- CASE 1 --- No previous test matrix exists
        if self.TestMatrix.CheckExistence() == 0:
            for x in CombinedList:
                temp = [y.strip() for y in x.split(':')]
                self.TestMatrix.AddDefinition(temp[0],temp[1],temp[2])

        # --- CASE 2 --- Previous test matrix exists    
        elif self.TestMatrix.CheckExistence() == 1:
            # 1, check to see if the user added any definitions
            DefNames = []
            for x in CombinedList:
                temp = [y.strip() for y in x.split(':')]
                if temp[0] not in self.TestMatrix.Definitions:
                    self.TestMatrix.AddDefinition(temp[0],temp[1],temp[2])
                DefNames.append(temp[0])
                
            # 2, check to see if user removed any definitions
            RemoveList = []
            for key,value in self.TestMatrix.Definitions.items():
                # If the definition is in the test matrix but not in the user defined list,
                # add it to the remove list. [Can't remove the definition from the test
                # matrix here because it will change the the length of the definitions
                # dictionary]
                if key not in DefNames:
                    RemoveList.append(key)
            # Now remove the definitions from the test matrix
            for x in RemoveList:
                self.TestMatrix.RemoveDefinition(x)

            # 3, update all the definition values and flags
            for x in CombinedList:
                temp = [y.strip() for y in x.split(':')]
                self.TestMatrix.ModifyDefinition(temp[0],temp[1],temp[2])

        self.Status.SetStatus('DEFINITIONS:Saved.\n')
        self.Summary.Update()
        # Close the window
        self.Master.destroy()
