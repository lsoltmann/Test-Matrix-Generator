import tkinter as tk

class OverwriteCheckWindow:
    def __init__(self,Master):
        self.Master = Master
        self.Return = -1

        # Window size
        WinWidth  = 270
        WinHeight = 60

        MainWindow = tk.Frame(self.Master, width=WinWidth, height=WinHeight)
        self.Master.title('')
        MainWindow.pack()
        
        # Create the subframe
        Subframe = tk.Frame(self.Master, relief=tk.GROOVE, borderwidth=0)

        # Create label
        TextLabel = tk.Label(Subframe, text='OVERWRITE EXISTING TEST MATRIX?')

        # Create button
        YesButton = tk.Button(Subframe, text='YES',justify=tk.CENTER, command=self.Overwrite, width = 10)
        NoButton  = tk.Button(Subframe, text='NO',justify=tk.CENTER, command=self.Cancel, width = 10)

        # Grid the items
        TextLabel.grid( row=0, column=0, columnspan=2)
        YesButton.grid( row=1, column=0)
        NoButton.grid(  row=1, column=1)

        # Place frame
        Subframe.place(x=5, y=5)


    def Overwrite(self):
        self.Return = 1
        self.Master.destroy()


    def Cancel(self):
        self.Return = 0
        self.Master.destroy()


    def Show(self):
        # Make window blocking
        self.Master.grab_set()
        # Wait for user input
        self.Master.wait_window()
        return self.Return
