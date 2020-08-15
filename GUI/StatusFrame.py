import tkinter as tk

class StatusFrame:
    def __init__(self,Master):
        # Frame location
        xpos = 10
        ypos = 535
        
        # Create the subframe
        Subframe = tk.Frame(Master, relief=tk.GROOVE, borderwidth=0)
        
        # File name label
        StatusLabel      = tk.Label(Subframe, text='STATUS:')

        # Create text box
        self.TextBox=tk.Text(Subframe, width=50, height=7, relief=tk.RIDGE, borderwidth=0)

        # Add a vertical scroll bar to the text area
        #Scroll=tk.Scrollbar(Subframe)
        #self.TextBox.configure(yscrollcommand=Scroll.set)
        #Scroll.configure(command=self.TextBox.yview)

        # Configure tags for normal, warning, and error messages
        self.TextBox.tag_configure('Normal', foreground='#000000')
        self.TextBox.tag_configure('Warning', foreground='#FF6700') #normal orange = FFA500, dark orange = FF8C00
        self.TextBox.tag_configure('Error', foreground='#FF0000')

        # Initialize
        self.TextBox.insert(tk.END, 'Ready\n' ,'Normal')
        self.TextBox.configure(state='disabled')
        
        # Grid the elements
        StatusLabel.grid(    row = 0, column = 0, sticky='W')
        self.TextBox.grid(   row = 1, column = 0)
        #Scroll.grid(         row = 1, column = 1, sticky='NS')
        
        # Place the subframe
        Subframe.place(x=xpos, y=ypos)


    def SetStatus(self,Status,Tag='Normal'):
        # Enable text box to add to it
        self.Enable()
        self.TextBox.insert(tk.END, Status, Tag)
        # Disable box to prevent user from editing
        self.Disable()
        # Auto scroll to the bottom
        self.TextBox.see(tk.END)

    def Enable(self):
        self.TextBox.configure(state='normal')

    def Disable(self):
        self.TextBox.configure(state='disabled')
