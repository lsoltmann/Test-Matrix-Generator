import tkinter as tk
from GUI.ParametersWindow import ParametersWindow
from GUI.DefinitionsWindow import DefinitionsWindow
from GUI.PlotWindow import PlotWindow
from Core.LoadTestMatrix import LoadTestMatrix
from Core.SaveTestMatrix_Raw import SaveTestMatrix_Raw
from GUI.OverwriteCheckWindow import OverwriteCheckWindow
from tkinter.filedialog import askopenfilename
import datetime
import ntpath
import importlib as il
import os

class IOFrame:
    def __init__(self,Master,TestMatrix,Summary,Status):
        self.TestMatrix = TestMatrix
        self.Master = Master
        self.Summary = Summary
        self.Status = Status
        # Variables tracked by observers
        self.TMLoaded = tk.IntVar(0)
        
        # Default column width
        defaultWidth = 10
        # Default box height
        defaultHeight = 20
        
        # Window location
        xpos = 5
        ypos = 5
        
        # Create the subframe
        Subframe = tk.Frame(Master, relief=tk.GROOVE, borderwidth=0)

        # Create labels
        TestNameLabel = tk.Label(Subframe, text='TEST NAME:')
        FormattedOuputLabel = tk.Label(Subframe, text='FORMATTED OUTPUT')

        # Create buttons
        ParamsButton = tk.Button(Subframe, text='PARAMETERS',justify=tk.CENTER, command=self.OpenParams, width = defaultWidth)
        DefButton    = tk.Button(Subframe, text='DEFINITONS',justify=tk.CENTER, command=self.OpenDefs, width = defaultWidth)
        LoadButton   = tk.Button(Subframe, text='LOAD',justify=tk.CENTER, command=self.LoadMatrix, width = defaultWidth)
        SaveButton   = tk.Button(Subframe, text='SAVE',justify=tk.CENTER, command=self.SaveMatrix, width = defaultWidth)
        PlotButton   = tk.Button(Subframe, text='PLOT',justify=tk.CENTER, command=self.Plot, width = defaultWidth)
        TimingButton = tk.Button(Subframe, text='TIMING',justify=tk.CENTER, command=self.Timing, width = defaultWidth)

        # Add input fields
        self.TestNameInput = tk.StringVar(Subframe, value = '')
        TestNameInputField = tk.Entry(Subframe, width=defaultWidth, textvariable=self.TestNameInput)

        # Option menu
        # Get all files in the 'OutputScipts' folder
        OutputFiles = ['NONE']

        # Get OutputScripts Path
        current_working_directory = os.getcwd()
        outscript_path = os.path.join(current_working_directory, 'OutputScripts')

        for file in os.listdir(outscript_path):
            if '.py' in file:
                temp = file.split('.')
                OutputFiles.append(temp[0])

        self.FormattedOutputType = tk.StringVar()
        self.FormattedOutputType.set('NONE') # default value
        FormattedOutputMenu = tk.OptionMenu(Subframe, self.FormattedOutputType,*OutputFiles)
        FormattedOutputMenu.configure(width=17)

        # Grid the items
        ParamsButton.grid(       row=1, column=0)
        DefButton.grid(          row=1, column=1)
        LoadButton.grid(         row=0, column=3)
        SaveButton.grid(         row=1, column=3)
        PlotButton.grid(         row=0, column=2)
        TimingButton.grid(       row=1, column=2)
        FormattedOutputMenu.grid(row=1, column=4)
        FormattedOuputLabel.grid(row=0,column=4)
        TestNameLabel.grid(      row=0, column=0)
        TestNameInputField.grid( row=0, column=1)

        # Place frame
        Subframe.place(x=xpos, y=ypos)

    def OpenParams(self):
        ParamWin = tk.Toplevel()
        ParamWin.resizable(width=tk.FALSE,height=tk.FALSE)
        ParametersWindow(ParamWin,self.TestMatrix,self.Summary,self.Status)
        return None

    def OpenDefs(self):
        DefsWin = tk.Toplevel()
        DefsWin.resizable(width=tk.FALSE,height=tk.FALSE)
        DefinitionsWindow(DefsWin,self.TestMatrix,self.Summary,self.Status)
        return None

    def LoadMatrix(self):
        # Check if a matrix already exists
        if self.TestMatrix.Parameters != {}:
            # Ask user if they want to overwrite
            OverwriteCheckWin = tk.Toplevel()
            OverwriteCheckWin.resizable(width=tk.FALSE,height=tk.FALSE)
            Check = OverwriteCheckWindow(OverwriteCheckWin).Show()
        else :
            # If not matrix was loaded, set 'overwrite check' to 1
            Check = 1
        # Load matrix
        if Check == 1:
            # Get full file path
            FullFilePath = askopenfilename(multiple=False)
            if FullFilePath != '':
                LoadTestMatrix(FullFilePath,self.TestMatrix)
                self.Status.SetStatus('Test matrix loaded.\n')
                self.TestNameInput.set(ntpath.basename(FullFilePath).split('.')[0])
                self.TMLoaded.set(1)
        else:
            self.Status.SetStatus('Load canceled.\n')
        return None


    def SaveMatrix(self):
        # Get test name from input field
        TestName = self.TestNameInput.get()
        if TestName == '':
            Now = datetime.datetime.now()
            TestName = Now.strftime("%d%m%Y_%H%M%S")
        # Save raw matrix
        SaveTestMatrix_Raw(TestName,self.TestMatrix)
        # Save pretty formatted matrix based on the users menu selection
        if self.FormattedOutputType.get() != 'NONE':
            Script = il.import_module('OutputScripts.'+self.FormattedOutputType.get())
            Script = getattr(Script, self.FormattedOutputType.get())
            Script(TestName,self.TestMatrix)
        else:
            pass
        self.Status.SetStatus('Test matrix saved.\n')
        return None


    def Plot(self):
        # Open the plot window only if a test matrix exists
        if self.TestMatrix.CheckExistence():
            PlotWin = tk.Toplevel()
            PlotWin.resizable(width=tk.FALSE,height=tk.FALSE)
            PlotWindow(PlotWin,self.TestMatrix,self.Status)
        else:
           self.Status.SetStatus('Unable to open plot window. No groups exist.\n','Error')
        return None


    def Timing(self):
        self.Status.SetStatus('Feature not yet implemented.\n','Warning')
        return None
