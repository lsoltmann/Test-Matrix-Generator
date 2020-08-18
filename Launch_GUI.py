'''
    Description: Test matrix generator tool used to make test matrices
                 for any kind of testing.
    
    Revision History
    18 AUG 2020 - Created and debugged
    
    Author: Lars Soltmann
    
    NOTES:
    - Written for python3
    - Requires: Pandas, Pyyaml
    
    TODO:
    - None
    
    '''

Version = '1.0'

import tkinter as tk
from GUI.Main import Main

if __name__ == "__main__":
    root = tk.Tk()
    GUI = Main(root,Version)
    root.resizable(width=tk.FALSE,height=tk.FALSE)
    #root.mainloop()
    
    # This is a work around to catch the UnicodeDecodeError ...
    #
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
    #
    # that appears to be a Mac specific issue related to scrolling in tkinter

    while True:
        try:
            root.mainloop()
            break
        except UnicodeDecodeError:
            pass
