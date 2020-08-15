import tkinter as tk
from GUI.MainFrame import MainFrame
#from GUI.IOFrame import IOFrame
from GUI.StatusFrame import StatusFrame
from Core.TestMatrix import TestMatrix
from GUI.SummaryFrame import SummaryFrame

class Main:
    def __init__(self,Master,Version):
        WinWidth  = 785
        WinHeight = 680

        MainWindow = tk.Frame(Master, width=WinWidth, height=WinHeight)
        Master.title('TEST MATRIX GENERATOR v'+Version)
        MainWindow.pack()

        TM   = TestMatrix()
        STAT = StatusFrame(Master)
        SUM  = SummaryFrame(Master,TM)
        MF   = MainFrame(Master,TM,SUM,STAT)
