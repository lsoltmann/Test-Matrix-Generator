import tkinter as tk
import yaml
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


class TimingWindow:
    def __init__(self,Master,TestMatrix,Status):
        self.Master = Master
        self.TestMatrix = TestMatrix
        self.Status = Status
        
        # Window size
        WinWidth  = 330
        WinHeight = 575

        # Parameter list box size
        defaultWidth  = 31
        defaultHeight = 25

        MainWindow = tk.Frame(self.Master, width=WinWidth, height=WinHeight)
        self.Master.title('TIMING')
        MainWindow.pack()
        
        # Window location
        xpos = 5
        ypos = 5
        
        # Create the subframe
        Subframe = tk.Frame(self.Master, relief=tk.GROOVE, borderwidth=0)

        # Add list box
        self.TimingBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)
        self.FlagsBox  = tk.Listbox(Subframe,width=3,height=defaultHeight)

        # Add input fields
        self.TimingInput    = tk.StringVar(Subframe, value = '')
        TimingInputField = tk.Entry(Subframe, width=defaultWidth, textvariable=self.TimingInput)

        # Add buttons
        SaveCloseButton       = tk.Button(Subframe, text='SAVE AND CLOSE',justify=tk.CENTER, command=self.Export, width = defaultWidth)
        UpdateTimingButton     = tk.Button(Subframe, text='UPDATE',justify=tk.CENTER, command=self.Update, width = int(defaultWidth/2))
        FlagButton            = tk.Button(Subframe, text='SET FLAG',justify=tk.CENTER, command=self.SetFlag, width = int(defaultWidth/2))

        # Grid the items
        self.TimingBox.grid(     row=0, column=0, columnspan=2)
        self.FlagsBox.grid(      row=0, column=2)
        TimingInputField.grid(   row=1, column=0, columnspan=2)
        UpdateTimingButton.grid( row=2, column=0)
        FlagButton.grid(         row=2, column=1)
        SaveCloseButton.grid(    row=3, column=0, columnspan=2)

        # Disable flags listbox
        self.DisableFlags()
        
        # Place frame
        Subframe.place(x=xpos, y=ypos)

        # Check to to see if a test matrix already exists
        self.CheckForExistingTestMatrix()


    def CheckForExistingTestMatrix(self):
        # If test matrix does exist, populate the timing box if the correct flag is set
        if self.TestMatrix.CheckExistence() == 1:
            for key,value in self.TestMatrix.Parameters.items():
                if 'T' in value['FLAG']:
                    self.TimingBox.insert(tk.END, key+':'+str(self.TestMatrix.Parameters[key]['TIMING']['VALUE']))
                    self.EnableFlags()
                    self.FlagsBox.insert(tk.END, str(self.TestMatrix.Parameters[key]['TIMING']['FLAG']))
                    self.DisableFlags()
                else:
                    pass
        else:
            # If one doesn't exist, don't add anything
            pass
        return None
    

    def Update(self):
        # Get current selection
        Selection = self.TimingBox.curselection()
        if Selection == ():
            self.Status.SetStatus('TIMING:No parameter selected.\n','Error')
            return None
        TimingIdx = Selection[0]
        # Get the parameter name
        TimingName = self.TimingBox.get(TimingIdx).split(':')[0]
        # Get parameter input field data
        Val = self.TimingInput.get()
        # Make sure input string is formatted correctly
        if not Val.isnumeric():
            self.Status.SetStatus('TIMING:Input syntax not recognized. Input must be a int/float.\n','Error')
        else:
            # Remove the old parameter
            self.TimingBox.delete(TimingIdx)
            # Combine and add parameter back to listbox
            self.TimingBox.insert(TimingIdx, TimingName+':'+str(Val))
            self.Status.SetStatus('TIMING:Timing value updated.\n')
        return None


    def EnableFlags(self):
        self.FlagsBox.configure(state="normal")
        return None


    def DisableFlags(self):
        self.FlagsBox.configure(state="disabled")
        return None


    def SetFlag(self):
        # Get highlighted selection in listbox
        Selection = self.TimingBox.curselection()
        if Selection == ():
            self.Status.SetStatus('TIMING:No parameter selected.\n','Error')
            return None
        # Get the parameter index
        ParamIdx = Selection[0]
        # Get input field
        Flag = self.TimingInput.get()
        # Check validity of input
        Error = 0
        if Flag == '':
            Flag = self.TestMatrix.TimingFlagOptions[0]
        else:
            for i in Flag:
                if i not in self.TestMatrix.TimingFlagOptions:
                   self.Status.SetStatus('TIMING:Flag \'{0}\' not recognized. Constant flag set.\n'.format(i),'Error')
                   Error = 1
            if Error == 1:
                Flag = self.TestMatrix.TimingFlagOptions[0]
        # Update the list box
        self.EnableFlags()
        self.FlagsBox.delete(ParamIdx)
        self.FlagsBox.insert(ParamIdx, Flag)
        self.DisableFlags()
        if Error == 0:
            self.Status.SetStatus('TIMING:Flag set.\n','Normal')
        return None


    def Export(self):
        # Save the timing parameters to the testmatrix
        TimingList = self.TimingBox.get(0, tk.END)
        TimingFlagList = self.FlagsBox.get(0, tk.END)
        for i in range(len(TimingList)):
            temp = TimingList[i].split(':')
            self.TestMatrix.UpdateTiming(temp[0],float(temp[1]),TimingFlagList[i])            
        self.Status.SetStatus('TIMING:Saved.\n')
        # Close the window
        self.Master.destroy()
