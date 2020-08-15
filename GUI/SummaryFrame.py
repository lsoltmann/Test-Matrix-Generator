import tkinter as tk

class SummaryFrame:
    def __init__(self,Master,TestMatrix):
        self.TestMatrix = TestMatrix
        
        # Frame location
        xpos = 585
        ypos = 65
        
        # Create the subframe
        Subframe = tk.Frame(Master, relief=tk.GROOVE, borderwidth=0)
        
        # File name label
        SummaryLabel      = tk.Label(Subframe, text="SUMMARY:")

        # Create text box
        self.TextBox=tk.Text(Subframe, width=26, height=37, relief=tk.RIDGE, borderwidth=0)

        # Initialize
        #self.TextBox.insert("end", "Summary\n" ,"Normal")
        self.TextBox.configure(state="disabled")
        
        # Grid the elements
        SummaryLabel.grid(   row = 0, column = 0, sticky="W")
        self.TextBox.grid(   row = 1, column = 0)
        
        # Place the subframe
        Subframe.place(x=xpos, y=ypos)


    def Update(self):
        # Get all parameters that should be included in the summary
        SumParams = {}
        for key,value in self.TestMatrix.Parameters.items():
            if 'S' in value['FLAG']:
                SumParams[key] = {}
        # Calculate summary data
        N_tp = 0
        N_g  = 0
        for i in range(len(self.TestMatrix.GroupTestPoints)):
            N_tp += self.TestMatrix.GroupTestPoints[i].shape[0]
            N_g  += 1
            if SumParams != {}:
                for key,value in SumParams.items():
                    # For each test point find the number of occurances of the summary parameters
                    item   = self.TestMatrix.GroupTestPoints[i][key].value_counts().keys().tolist()  #value of the row item
                    counts = self.TestMatrix.GroupTestPoints[i][key].value_counts().tolist()        #number of occurances of the row item
                    for j in range(len(item)):
                        # For each unique item update the count
                        if item[j] in SumParams[key]:
                            SumParams[key][str(item[j])] = SumParams[key][str(item[j])] + counts[j]
                        else:
                            SumParams[key][str(item[j])] = counts[j]
        # Enable text box
        self.Enable()
        # Clear the box
        self.TextBox.delete(1.0, tk.END)
        # Add data
        self.TextBox.insert(tk.END, 'Test Points: {0}\n'.format(N_tp))
        self.TextBox.insert(tk.END, 'Groups:      {0}\n'.format(N_g))
        self.TextBox.insert(tk.END, '--------------------------\n') #26 dashes, equal to the textbox width
        if SumParams != {}:
            for x in SumParams:
                self.TextBox.insert(tk.END, 'Totals:\n')
                for key,value in SumParams[x].items():
                    self.TextBox.insert(tk.END, '    {0} {1} = {2}\n'.format(x,key,value))
        
        # Disable box to prevent user from editing
        self.Disable()
        

    def Enable(self):
        self.TextBox.configure(state='normal')

    def Disable(self):
        self.TextBox.configure(state='disabled')
