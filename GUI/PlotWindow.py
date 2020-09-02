import tkinter as tk
import pandas as pd
from matplotlib import figure as mplfig
import matplotlib.backends.backend_tkagg as tkagg
import numpy as np
import scipy.spatial as ss


class PlotWindow:
    def __init__(self,Master,TestMatrix,Status):
        self.Status = Status
        self.TestMatrix = TestMatrix
        self.Status = Status
        self.PlotFrame = pd.DataFrame()

        # Window size
        WinWidth  = 850
        WinHeight = 480


        #********************** PLOT VARIABLES AND CONTROL FRAME **********************
        # List box size
        defaultWidth  = 10
        defaultHeight = 20

        # Create the main window
        MainWindow = tk.Frame(Master, width=WinWidth, height=WinHeight)
        Master.title('PLOT')
        MainWindow.pack()
        
        # Window location
        xpos = 5
        ypos = 5
        
        # Create the subframe
        Subframe = tk.Frame(Master, relief=tk.GROOVE, borderwidth=0)

        # Add labels
        XLabel     = tk.Label(Subframe, text='X')
        YLabel     = tk.Label(Subframe, text='Y')
        ZLabel     = tk.Label(Subframe, text='Z')
        Blank      = tk.Label(Subframe, text='')
        GroupLabel = tk.Label(Subframe, text='GROUP')

        # Add list box
        self.GroupBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0,selectmode=tk.MULTIPLE)
        self.XBox     = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)
        self.YBox     = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)
        self.ZBox     = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)

        # Add buttons
        PlotButton      = tk.Button(Subframe, text='PLOT',justify=tk.CENTER, command=self.Plot, width = int(defaultWidth))
        ClearZSelButton = tk.Button(Subframe, text='CLEAR Z',justify=tk.CENTER, command=self.ClearZSel, width = int(defaultWidth))

        # Add check button
        self.IncludeHull = tk.IntVar()
        self.IncludeHull.set(1)
        HullCheck   = tk.Checkbutton(Subframe, text='CONVEX HULL', variable=self.IncludeHull)

        # Grid the items
        GroupLabel.grid(      row=0, column=0)
        XLabel.grid(          row=0, column=1)
        YLabel.grid(          row=0, column=2)
        ZLabel.grid(          row=0, column=3)
        self.GroupBox.grid(   row=1, column=0)#, sticky='WE')
        self.XBox.grid(       row=1, column=1)#, sticky='WE')
        self.YBox.grid(       row=1, column=2)#, sticky='WE')
        self.ZBox.grid(       row=1, column=3)#, sticky='WE')
        Blank.grid(           row=2, column=0)
        HullCheck.grid(       row=3, column=0)
        PlotButton.grid(      row=4, column=0)
        ClearZSelButton.grid( row=2, column=3)
        
        # Place frame
        Subframe.place(x=xpos, y=ypos)

        #********************** PLOT GRAPH FRAME **********************
        # Frame location
        xpos = 430
        ypos = 10

        # Plot size
        PlotWidth  = 4
        PlotHeight = 4
        
        # Create the subframe
        Subframe = tk.Frame(Master, relief=tk.GROOVE, borderwidth=0)

        # Create figure and canvas
        self.DataFigure = mplfig.Figure(figsize=(PlotWidth,PlotHeight), dpi=100)
        self.PlotCanvas = tkagg.FigureCanvasTkAgg(self.DataFigure,master=Subframe)
        self.PlotCanvas.draw()
        self.DataGraph  = self.DataFigure.add_subplot(111, projection='3d')
        #self.DataGraph.grid(True)
        #self.DataFigure.set_tight_layout(True)
        self.PlotCanvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Place the subframe
        Subframe.place(x=xpos, y=ypos)

        # Load variables
        self.LoadVars()

        # Marker array
        self.Markers   = np.array(['^','s','P','*','D','o'])
        self.MarkersOG = self.Markers # Used to reset the marker array


    def Refresh(self):
        pass

    def LoadVars(self):
        # Clear the list box first
        self.GroupBox.delete(0,tk.END)
        self.XBox.delete(0,tk.END)
        self.YBox.delete(0,tk.END)
        self.ZBox.delete(0,tk.END)
        # Clear the plot
        self.DataGraph.clear()
        self.PlotCanvas.draw()

        # List to keep track of which parameters across the entire matrix only contain lists or values
        ParamPassGlobal = np.array([True]*len(self.TestMatrix.Parameters))
        GroupPass = []
        for i in range(len(self.TestMatrix.GroupNames)):
            # List of parameters in the current dataframe that have passed
            ParamPassLocal = np.array([True]*len(self.TestMatrix.Parameters))
            # Run through all parameters and add that parameter to the list
            # if and only if all values in that column are numeric or list.
            df = self.TestMatrix.GroupTestPoints[i]
            for col in df:
                # For each column, check all rows
                for j in range(df.shape[0]):
                    # Get the row
                    Value = df[col].values[j]
                    # Check if it is a number or list
                    try:
                        # If its not a number or list, it will fail the eval test
                        num = eval(Value)
                        # Check if Value is 'None'
                        if num is None:
                            ParamPassLocal[df.columns.get_loc(col)] = 0
                    except:
                        # However, it may be using a definition so we
                        # need to check the definitions to see if it
                        # is actually defined as a list or number
                        if Value in self.TestMatrix.Definitions:
                            # If the 'Value' is in the defintions, run the check on the its VALUE
                            try:
                                num = eval(self.TestMatrix.Definitions[Value]['VALUE'])
                            except:
                                ParamPassLocal[df.columns.get_loc(col)] = 0
                        else:
                            ParamPassLocal[df.columns.get_loc(col)] = 0
            # If the local parameter pass vector has any passing values in it,
            # add the group to the listbox
            if sum(ParamPassLocal) > 0:
                # Load groups into the listbox
                self.GroupBox.insert(tk.END, self.TestMatrix.GroupNames[i])
                # AND the local global pass list
                ParamPassGlobal = ParamPassGlobal & ParamPassLocal
                # Add group to pass list
                GroupPass.append(i)
            else:
                pass

        # Convert logical list to parameter list
        ParamList = []
        AllParams = list(self.TestMatrix.Parameters.keys())
        for x in range(len(ParamPassGlobal)):
            if ParamPassGlobal[x]:
                ParamList.append(AllParams[x])

        # Make a single dataframe from all the groups that passed
        self.PlotFrame = pd.DataFrame(columns=ParamList)
        GroupNameList = []
        for Idx in GroupPass:
            self.PlotFrame = pd.concat([self.PlotFrame,self.TestMatrix.GroupTestPoints[Idx][ParamList]],axis=0)
            GroupNameList = GroupNameList + [self.TestMatrix.GroupNames[Idx]]*len(self.TestMatrix.GroupTestPoints[Idx])
        # Add a zero column to make plotting 2D plotting easier
        self.PlotFrame.insert(len(self.PlotFrame.columns), 'NULL', ['0']*len(self.PlotFrame))
        # Add a group names column
        self.PlotFrame.insert(0, 'GROUP', GroupNameList)
        # Replace defintions with their values
        for key,value in self.TestMatrix.Definitions.items():
            self.PlotFrame = self.PlotFrame.replace(key,self.TestMatrix.Definitions[key]['VALUE'])

        # Populate the list boxes
        for item in ParamList:
            self.XBox.insert(tk.END, item)
            self.YBox.insert(tk.END, item)
            self.ZBox.insert(tk.END, item)
        
        # Debug
        #print(self.PlotFrame)
        #print('========================')
        return None
                    

    def Plot(self):
        # Reset the marker array
        self.Markers = self.MarkersOG
        # Clear the graph
        self.DataGraph.clear()
        self.PlotCanvas.draw()
        # Get the selection indices
        GSel = self.GroupBox.curselection()
        XSel = self.XBox.curselection()
        YSel = self.YBox.curselection()
        ZSel = self.ZBox.curselection()
        if XSel == ():
            self.Status.SetStatus('PLOT:No ''x'' variable selected.\n','Error')
            return None
        if YSel == ():
            self.Status.SetStatus('PLOT:No ''y'' variable selected.\n','Error')
            return None
        if ZSel == ():
            ZSel = 'NULL'
        # Group name list
        GNames = []
        # If no group is selected, use all of them
        if GSel == ():
            # Highlight all in box
            self.GroupBox.selection_set(0, tk.END)
            # Grab the indices
            GSel = self.GroupBox.curselection()
        # Append group names to a list
        for i in GSel:
            GNames.append(self.GroupBox.get(i))
        # Get the selection names
        XSel = self.XBox.get(XSel[0])
        YSel = self.YBox.get(YSel[0])
        if ZSel != 'NULL':
            ZSel = self.ZBox.get(ZSel[0])

        # Initialize hull array (stores from all selected groups)
        AllPlotData = np.array([[np.nan,np.nan,np.nan]]) 
        for g in range(len(GNames)):
            # Initialize plot array (stores group data)
            PlotData = np.array([[np.nan,np.nan,np.nan]])
            # Extract x,y,z data
            xdata = self.PlotFrame.loc[self.PlotFrame['GROUP'] == GNames[g]][XSel].values
            ydata = self.PlotFrame.loc[self.PlotFrame['GROUP'] == GNames[g]][YSel].values
            zdata = self.PlotFrame.loc[self.PlotFrame['GROUP'] == GNames[g]][ZSel].values
            # Convert from float to numeric
            xdata = [eval(i) for i in xdata]
            ydata = [eval(i) for i in ydata]
            zdata = [eval(i) for i in zdata]
            
            for i in range(len(xdata)):
                # Make an ND grid
                xgrid,ygrid,zgrid = np.meshgrid(xdata[i],ydata[i],zdata[i])
                # Assemble the data
                PlotData    = np.concatenate((PlotData,np.array([xgrid.flatten(),ygrid.flatten(),zgrid.flatten()]).T),axis=0)
                # Plot the data (group)
                AllPlotData = np.concatenate((AllPlotData,np.array([xgrid.flatten(),ygrid.flatten(),zgrid.flatten()]).T),axis=0)
            # Remove the first row (its just nan's)
            PlotData = np.delete(PlotData, 0, axis=0)
            # Plot the data
            self.Markers = np.roll(self.Markers,1)
            self.DataGraph.plot3D(PlotData[:,0], PlotData[:,1], PlotData[:,2],self.Markers[0],label=GNames[g])

        # Check if convex hull should be plotted
        if self.IncludeHull.get():
            # Remove the first row (its just nan's)
            AllPlotData = np.delete(AllPlotData, 0, axis=0)
            # Hull doesn't work when one axis is constant, so first check if the data is truly 3D.
            # If its not, remove the 3rd dimension. We'll add it back after the hull operation.
            Rmv = [0,0,0]
            RmvValue = 0
            if len(np.unique(AllPlotData[:,0]))==1:
                Rmv[0] = 1
                RmvValue = np.unique(AllPlotData[:,0])
            if len(np.unique(AllPlotData[:,1]))==1:
                Rmv[1] = 1
                RmvValue = np.unique(AllPlotData[:,1])
            if len(np.unique(AllPlotData[:,2]))==1:
                Rmv[2] = 1
                RmvValue = np.unique(AllPlotData[:,2])
            if sum(Rmv)>1:
                self.Status.SetStatus('PLOT:Failed to compute convex hull since more than 1 dimension is zero.\n','Warning')
            else:
                # Check if a dimension needs to be removed
                # ---- 2D CASE ----
                if sum(Rmv) != 0:
                    AllPlotData = np.delete(AllPlotData, Rmv.index(1), axis=1)
                    # Check to make sure that the two remaining arrays aren't equal to each other, which would be the case
                    # if the user accidentally selected the same parameter for x and y 
                    if np.array_equal(AllPlotData[:,0], AllPlotData[:,1]):
                        self.Status.SetStatus('PLOT:Failed to compute convex hull since 2 of the dimensions are equal.\n','Warning')
                    else:
                        # Create the hull
                        Hull = ss.ConvexHull(AllPlotData)
                        HullPlot = np.array([AllPlotData[Hull.vertices,0], AllPlotData[Hull.vertices,1]]).T
                        # Add the zero dimension back in
                        if Rmv[0] == 1:
                            HullPlot = np.insert(HullPlot, 0, RmvValue*np.ones((AllPlotData.shape[0],1)), axis=1)
                        elif Rmv[1] == 1:
                            HullPlot = np.insert(HullPlot, 1, RmvValue*np.ones((AllPlotData.shape[0],1)), axis=1)
                        elif Rmv[2] == 1:
                            HullPlot = np.insert(HullPlot, 2, RmvValue*np.ones((AllPlotData.shape[0],1)), axis=1)
                        # Plot the hull
                        self.DataGraph.plot3D(np.concatenate((HullPlot[:,0],HullPlot[0,0]),axis=None),
                                              np.concatenate((HullPlot[:,1],HullPlot[0,1]),axis=None),
                                              np.concatenate((HullPlot[:,2],HullPlot[0,2]),axis=None),':r')
                # ---- 3D CASE ----   
                else:
                    # Create the hull
                    Hull = ss.ConvexHull(AllPlotData)
                    # Plot the hull
                    for s in Hull.simplices:
                        s = np.append(s, s[0])
                        self.DataGraph.plot3D(AllPlotData[s,0], AllPlotData[s,1], AllPlotData[s,2],':r')

        # Add the axis labels
        self.DataGraph.set_xlabel(XSel)
        self.DataGraph.set_ylabel(YSel)
        self.DataGraph.set_zlabel(ZSel)
        # Add legend if more than one group plotted
        if len(GNames)>1:
            self.DataGraph.legend()
        self.PlotCanvas.draw()
        self.Status.SetStatus('PLOT:Plot generated.\n')
        return None

    # Clear the 'z' selection
    def ClearZSel(self):
        self.ZBox.selection_clear(0, tk.END)
