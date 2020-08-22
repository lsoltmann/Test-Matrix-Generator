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
        WinWidth  = 800
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
        XLabel = tk.Label(Subframe, text='X')
        YLabel = tk.Label(Subframe, text='Y')
        ZLabel = tk.Label(Subframe, text='Z')
        Blank  = tk.Label(Subframe, text='')
        GroupLabel = tk.Label(Subframe, text='PLOT GROUP:')

        # Add list box
        self.XBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)
        self.YBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)
        self.ZBox = tk.Listbox(Subframe,width=defaultWidth,height=defaultHeight,exportselection=0)

        # Add option menu
        self.PlotGroup = tk.StringVar()
        PlotGroupMenu = tk.OptionMenu(Subframe, self.PlotGroup,*self.TestMatrix.GroupNames, command=lambda x:self.LoadVars())
        self.PlotGroup.set(self.TestMatrix.GroupNames[0]) # default value
        PlotGroupMenu.configure(width=defaultWidth)

        # Add buttons
        PlotButton      = tk.Button(Subframe, text='PLOT',justify=tk.CENTER, command=self.Plot, width = int(defaultWidth))
        ClearZSelButton = tk.Button(Subframe, text='CLEAR Z',justify=tk.CENTER, command=self.ClearZSel, width = int(defaultWidth))

        # Add check button
        self.IncludeHull = tk.IntVar()
        self.IncludeHull.set(1)
        HullCheck   = tk.Checkbutton(Subframe, text='CONVEX HULL', variable=self.IncludeHull)

        # Grid the items
        GroupLabel.grid(      row=0, column=0)
        PlotGroupMenu.grid(   row=0, column=1)
        XLabel.grid(          row=1, column=0)
        YLabel.grid(          row=1, column=1)
        ZLabel.grid(          row=1, column=2)
        self.XBox.grid(       row=2, column=0)#, sticky='WE')
        self.YBox.grid(       row=2, column=1)#, sticky='WE')
        self.ZBox.grid(       row=2, column=2)#, sticky='WE')
        Blank.grid(           row=3, column=0)
        HullCheck.grid(       row=4, column=0)
        PlotButton.grid(      row=5, column=0)
        ClearZSelButton.grid( row=3, column=2)
        
        # Place frame
        Subframe.place(x=xpos, y=ypos)

        #********************** PLOT GRAPH FRAME **********************
        # Frame location
        xpos = 370
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


    def Refresh(self):
        pass

    def LoadVars(self):
        # Clear the list box first
        self.XBox.delete(0,tk.END)
        self.YBox.delete(0,tk.END)
        self.ZBox.delete(0,tk.END)
        # Clear the plot dataframe
        self.PlotFrame = pd.DataFrame()
        # Clear the plot
        self.DataGraph.clear()
        self.PlotCanvas.draw()
        # Get the selected group
        GroupIDX = self.TestMatrix.GroupNames.index(self.PlotGroup.get())
        # Run through all parameters and add that parameter to the list
        # if and only if all values in that column are numeric or list.
        df = self.TestMatrix.GroupTestPoints[GroupIDX]
        ParamList = []
        for col in df:
            PassCheck = 1
            # For each column, check all rows
            RowValList = []
            for i in range(df.shape[0]):
                # Get the row
                Value = df[col].values[i]
                # Check if it is a number or list
                try:
                    # If its not a number or list, it will fail the eval test
                    num = eval(Value)
                    RowValList.append(num)
                except:
                    # However, it may be using a definition so we
                    # need to check the definitions to see if it
                    # is actually defined as a list or number
                    if Value in self.TestMatrix.Definitions:
                        # If the 'Value' is in the defintions, run the check on the its VALUE
                        try:
                            num = eval(self.TestMatrix.Definitions[Value]['VALUE'])
                            RowValList.append(num)
                        except:
                            PassCheck = 0
                    else:
                        PassCheck = 0
            if PassCheck:
                # Append the column name to the listbox list
                ParamList.append(col)
                # Append the column to the plotting dataframe
                self.PlotFrame = pd.concat([self.PlotFrame,df[col]],axis=1)
                self.PlotFrame[col] = RowValList
            else:
                pass
        # Populate the list boxes
        for item in ParamList:
            self.XBox.insert(tk.END, item)
            self.YBox.insert(tk.END, item)
            self.ZBox.insert(tk.END, item)

        # Add a zero column to make plotting 2D plotting easier
        self.PlotFrame.insert(len(self.PlotFrame.columns), 'NULL', [0]*len(self.PlotFrame))
        
        # Debug
        #print(self.PlotFrame)
        #print('========================')
        return None
                    

    def Plot(self):
        # Clear the graph
        self.DataGraph.clear()
        self.PlotCanvas.draw()
        # Initialize plot array
        PlotData = np.array([[np.nan,np.nan,np.nan]])
        # Get the selection indices
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
        # Get the selection names
        XSel = self.XBox.get(XSel[0])
        YSel = self.YBox.get(YSel[0])
        if ZSel != 'NULL':
            ZSel = self.ZBox.get(ZSel[0])

        # Run through each selected variable and make sure they are plot compatible:
        # 1. Each test point contains only a single point for each variable.
        # 2. Each test point contains only a single list in one of the plot variables
        #    and the others are single points.
        # 3. Each test point contains more than one list but each list is the same
        #    length. Plotting will be done elementwise.
        for i in range(self.PlotFrame.shape[0]):
            # Extract x,y,z data
            xdata = self.PlotFrame[XSel].values[i]
            ydata = self.PlotFrame[YSel].values[i]
            zdata = self.PlotFrame[ZSel].values[i]
            # Make them all lists if they aren't already.
            if not isinstance(xdata, list):
                xdata = [xdata]
            if not isinstance(ydata, list):
                ydata = [ydata]
            if not isinstance(zdata, list):
                zdata = [zdata]
            # Check the length of each data segment and
            # lengthen it if it is equal to one. 
            xlen = len(xdata)
            ylen = len(ydata)
            zlen = len(zdata)
            Maxlen = max([len(xdata),len(ydata),len(zdata)])
            
            if (xlen != Maxlen) and (xlen != 1):
                self.Status.SetStatus('PLOT:''x'' data length not compatible.\n','Error')
                return None
            elif xlen == 1:
                xdata = xdata*Maxlen
                
            if (ylen != Maxlen) and (ylen != 1):
                self.Status.SetStatus('PLOT:''y'' data length not compatible.\n','Error')
                return None
            elif ylen == 1:
                ydata = ydata*Maxlen
                
            if (zlen != Maxlen) and (zlen != 1):
                self.Status.SetStatus('PLOT:''z'' data length not compatible.\n','Error')
                return None
            elif zlen == 1:
                zdata = zdata*Maxlen
            # Add to the data array
            PlotData = np.concatenate((PlotData,np.array([xdata,ydata,zdata]).T),axis=0)
        # Remove the first row (its just nan's)
        PlotData = np.delete(PlotData, 0, axis=0)
        # Plot the data
        self.DataGraph.plot3D(PlotData[:,0], PlotData[:,1], PlotData[:,2],'o')
        # Check if convex hull should be plotted
        if self.IncludeHull.get():
            # Hull doesn't work when one axis is constant, so first check if the data is truly 3D.
            # If its not, remove the 3rd dimension. We'll add it back after the hull operation.
            Rmv = [0,0,0]
            RmvValue = 0
            if len(np.unique(PlotData[:,0]))==1:
                Rmv[0] = 1
                RmvValue = np.unique(PlotData[:,0])
            if len(np.unique(PlotData[:,1]))==1:
                Rmv[1] = 1
                RmvValue = np.unique(PlotData[:,1])
            if len(np.unique(PlotData[:,2]))==1:
                Rmv[2] = 1
                RmvValue = np.unique(PlotData[:,2])
            if sum(Rmv)>1:
                self.Status.SetStatus('PLOT:Failed to compute convex hull since more than 1 dimension is zero.\n','Warning')
            else:
                # Check if a dimension needs to be removed
                # ---- 2D CASE ----
                if sum(Rmv) != 0:
                    PlotData = np.delete(PlotData, Rmv.index(1), axis=1)
                    # Check to make sure that the two remaining arrays aren't equal to each other, which would be the case
                    # if the user accidentally selected the same parameter for x and y 
                    if np.array_equal(PlotData[:,0], PlotData[:,1]):
                        self.Status.SetStatus('PLOT:Failed to compute convex hull since 2 of the dimensions are equal.\n','Warning')
                    else:
                        # Create the hull
                        Hull = ss.ConvexHull(PlotData)
                        HullPlot = np.array([PlotData[Hull.vertices,0], PlotData[Hull.vertices,1]]).T
                        # Add the zero dimension back in
                        if Rmv[0] == 1:
                            HullPlot = np.insert(HullPlot, 0, RmvValue*np.ones((PlotData.shape[0],1)), axis=1)
                        elif Rmv[1] == 1:
                            HullPlot = np.insert(HullPlot, 1, RmvValue*np.ones((PlotData.shape[0],1)), axis=1)
                        elif Rmv[2] == 1:
                            HullPlot = np.insert(HullPlot, 2, RmvValue*np.ones((PlotData.shape[0],1)), axis=1)
                        # Plot the hull
                        self.DataGraph.plot3D(np.concatenate((HullPlot[:,0],HullPlot[0,0]),axis=None),
                                              np.concatenate((HullPlot[:,1],HullPlot[0,1]),axis=None),
                                              np.concatenate((HullPlot[:,2],HullPlot[0,2]),axis=None),':r')
                # ---- 3D CASE ----   
                else:
                    # Create the hull
                    Hull = ss.ConvexHull(PlotData)
                    # Plot the hull
                    for s in Hull.simplices:
                        s = np.append(s, s[0])
                        self.DataGraph.plot3D(PlotData[s,0], PlotData[s,1], PlotData[s,2],':r')

        # Add the axis labels
        self.DataGraph.set_xlabel(XSel)
        self.DataGraph.set_ylabel(YSel)
        self.DataGraph.set_zlabel(ZSel)
        self.PlotCanvas.draw()
        self.Status.SetStatus('PLOT:Plot generated.\n')
        return None

    # Clear the 'z' selection
    def ClearZSel(self):
        self.ZBox.selection_clear(0, tk.END)
