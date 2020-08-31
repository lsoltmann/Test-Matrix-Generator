import tkinter as tk
from Core.Timing import Timing

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
        # Format of SumParams dictionary:
        # {Param1:{Val1:[occurances,totaltime],Val2:[occurances,totaltime],...}}
        # Get all parameters that should be included in the summary
        SumParams = {}
        TimeParam = None
        for key,value in self.TestMatrix.Parameters.items():
            if 'S' in value['FLAG']:
                SumParams[key] = {}
            if 'Z' in value['FLAG']:
                TimeParam = key

        # Calculate timing (output is a concatenate matrix of all groups)
        TM = Timing(self.TestMatrix)

        if TM.shape[0] != 0:
            # Check if a time storage parameter exists, if one doesn't exist, add fake time column with all zeros
            if TimeParam is None:
                TM.insert(len(TM)-1,'<TIME>',0)
                TimeParam ='<TIME>'
                
            # Calculate summary data
            if SumParams != {}:
                for key,value in SumParams.items():
                    # Find the unique values for the given parameter
                    UniqueItems = TM[key].value_counts(ascending=True).keys().tolist()
                    UniqueItems.sort()
                    # For each unique value create a new dataframe using only that value
                    for item in UniqueItems:
                        df = TM.loc[TM[key] == item]
                        SumParams[key][str(item)] = [df.shape[0],sum([float(x) for x in df[TimeParam].values])]
            # Total time
            T_tot = sum([float(x) for x in TM[TimeParam].values])
        else:
            T_tot = 0

        # Get the total number of test points and groups
        N_tp = TM.shape[0]
        N_g  = len(self.TestMatrix.GroupTestPoints)
        
        # Enable text box
        self.Enable()
        # Clear the box
        self.TextBox.delete(1.0, tk.END)
        # Add data
        self.TextBox.insert(tk.END, 'Test Points: {0}\n'.format(N_tp))
        self.TextBox.insert(tk.END, 'Groups:      {0}\n'.format(N_g))
        self.TextBox.insert(tk.END, 'Total Time:  {0:.3f}\n'.format(T_tot))
        self.TextBox.insert(tk.END, '--------------------------\n') #26 dashes, equal to the textbox width
        if SumParams != {}:
            for x in SumParams:
                self.TextBox.insert(tk.END, 'Totals: Count,Time\n')
                for key,value in SumParams[x].items():
                    self.TextBox.insert(tk.END, '    {0} {1} = {2}, {3:.3f}\n'.format(x,key,value[0],value[1]))
        
        # Disable box to prevent user from editing
        self.Disable()
        

    def Enable(self):
        self.TextBox.configure(state='normal')


    def Disable(self):
        self.TextBox.configure(state='disabled')
