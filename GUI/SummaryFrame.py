import tkinter as tk
from Core.Timing import Timing

class SummaryFrame:
    def __init__(self,Master,TestMatrix):
        self.TestMatrix = TestMatrix
        self.SumParams  = {}
        self.TimeParam  = None
        
        # Frame location
        xpos = 585
        ypos = 65
        
        # Create the subframe
        Subframe = tk.Frame(Master, relief=tk.GROOVE, borderwidth=0)
        
        # File name label
        SummaryLabel = tk.Label(Subframe, text="SUMMARY:")

        # Create text box
        self.TextBox = tk.Text(Subframe, width=26, height=37, relief=tk.RIDGE, borderwidth=0)

        # Initialize
        #self.TextBox.insert("end", "Summary\n" ,"Normal")
        self.TextBox.configure(state="disabled")
        
        # Grid the elements
        SummaryLabel.grid( row = 0, column = 0, sticky="W")
        self.TextBox.grid( row = 1, column = 0)
        
        # Place the subframe
        Subframe.place(x=xpos, y=ypos)


    def Update(self):
        # Format of SumParams dictionary:
        # {Param1:{Val1:[occurances,totaltime],Val2:[occurances,totaltime],...}}
        # Get all parameters that should be included in the summary
        self.SumParams = {}
        self.TimeParam = None
        for key,value in self.TestMatrix.Parameters.items():
            if 'S' in value['FLAG']:
                self.SumParams[key] = {}
            if 'Z' in value['FLAG']:
                self.TimeParam = key
        # Calculate timing
        Timing(self.TestMatrix)
        # Concatenate all test points
        TM = self.TestMatrix.OneMatrix()
        # Check if a time storage parameter exists, if one doesn't exist, add fake time column with all zeros
        if self.TimeParam is None:
            TM.insert(len(TM.columns)-1,'<TIME>',0)
            self.TimeParam ='<TIME>'  
        # Calculate summary data
        if self.SumParams != {}:
            for key,value in self.SumParams.items():
                # Find the unique values for the given parameter
                UniqueItems = TM[key].value_counts(ascending=True).keys().tolist()
                UniqueItems.sort()
                # For each unique value create a new dataframe using only that value
                for item in UniqueItems:
                    df = TM.loc[TM[key] == item]
                    self.SumParams[key][str(item)] = [df.shape[0],sum([float(x) for x in df[self.TimeParam].values])]
        # Total time
        T_tot = sum([float(x) for x in TM[self.TimeParam].values])

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
        if self.SumParams != {}:
            for x in self.SumParams:
                self.TextBox.insert(tk.END, 'Totals: Count,Time\n')
                for key,value in self.SumParams[x].items():
                    self.TextBox.insert(tk.END, '    {0} {1} = {2}, {3:.3f}\n'.format(x,key,value[0],value[1]))
        
        # Disable box to prevent user from editing
        self.Disable()
        

    def Enable(self):
        self.TextBox.configure(state='normal')


    def Disable(self):
        self.TextBox.configure(state='disabled')


    # Return data for use in file saving
    def ReturnSummary(self):
        if self.TimeParam == '<TIME>':
            return self.SumParams,None
        else:
            return self.SumParams,self.TimeParam
