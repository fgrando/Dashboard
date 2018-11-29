from tkinter import *
import os

TEXT_EDITOR_PATH="c:\\windows\\system32\\notepad.exe"
FOLDER_TO_MONITOR="C:\\Users\\user\\Desktop\\dashboard_scripts"

# This is a tool to present information gathered by other python scripts.
# It will load several scripts from a folder and present them like:
# label(script_name.py) button(open)
# label(result value  ) button(open)
#
# every python script can do whatever it wants, but in the end it must
# set the variable RESULT with at least one textual element.
# Example:
# hello.py:
#   def mything():
#       return ["hello", "this is my result"]
#   RESULT= mything()
#
# This script then runs hello.py with exec() and globals() to get the RESULT.

RESULT=[] #scripts have this global also
VERSION = "0.0.1"
REFRESH_INTERVAL_MS=2000



# this is the main program
class Dashboard:

    def __init__(self, master):
        self.master = master
        self.refresh_counter = 1
        self.extension = "py"
        self.rootdir = os.path.abspath(FOLDER_TO_MONITOR)
        self.myname = os.path.basename(__file__)
        
        master.title("DASHBOARD - v" + VERSION)
        
        self.build_gui()
        self.master.after(REFRESH_INTERVAL_MS, self.autorefresh) # auto refresh function

        #self.grid_columnconfigure(1,500

    def build_gui(self):
        # layot is like
        #top
        #+-----------------------------------------------------------------+
        #|-----------------------------------------------------------------|
        #|| button | label||             label                            ||
        #|-----------------------------------------------------------------|
        #|-----------------------------------------------------------------|
        #+-----------------------------------------------------------------+
        #|                                                                 |
        #|                     other items in grid                         |
        #|                                                                 |
        #+-----------------------------------------------------------------+
        #bottom

        self.top_frame =  Frame(self.master, bg='blue')
        self.bottom_frame =  Frame(self.master, bg='red')

        #self.top_frame.grid(row=0, column=0, sticky="nsew")
        #self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.top_frame.pack(fill=X, expand=False, anchor="n")
        self.bottom_frame.pack(fill=BOTH, expand=True)
      
        
        self.rootdir_str = StringVar()
        self.rootdir_str.set(self.rootdir)

        self.counter_str = StringVar()
        self.counter_str.set(str(self.refresh_counter))
        
        self.refresh_button = Button(self.top_frame, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side=LEFT, fill=BOTH)
        #self.refresh_button.grid(row = 0, column = 0, sticky="nsew")

        self.counter_entry = Entry(self.top_frame, textvariable=self.counter_str, width=len(self.counter_str.get()))
        self.counter_entry.pack(side=LEFT, fill=BOTH)
        #self.counter_entry.grid(row = 0, column = 1, sticky="nsew")

        self.rootdir_entry = Entry(self.top_frame, textvariable=self.rootdir_str, width=len(self.rootdir_str.get()))
        self.rootdir_entry.pack(side=LEFT, fill=BOTH, expand=True)
        #self.rootdir_entry.grid(row = 0, column = 2, sticky="nsew")

        self.items = []
        self.files = self.file_list()
        col = 1
        row = 1
        max_per_col = 5
        
        for f in self.files:
            i = Item(f, self.bottom_frame, row, col)
            self.items.append(i)

            if (col%max_per_col) == 0:
                col = 1
                row = row + 1
            else:
                col = col + 1
        print("created", len(self.items), "items")
        
    def autorefresh(self):
        self.refresh()
        self.master.after(REFRESH_INTERVAL_MS, self.autorefresh)

    def refresh(self):
        print("refreshing...")
        for i in self.items:
            i.update()
        print("done")
        # update counter
        self.refresh_counter = self.refresh_counter + 1
        self.counter_str.set(str(self.refresh_counter))
        self.counter_entry.config(width=len(str(self.refresh_counter)))

        

    def file_list(self):
        paths = []
        for rootdir, dirs, files in os.walk(self.rootdir):  
            for filename in files:
                if (filename != self.myname) and (filename.split('.')[-1] == self.extension):
                    paths.append(os.path.join(rootdir,filename))

            break # in future versions: look for inside dirs as well.
        print("monitoring ", paths)
        return paths

    def quit(self):
        self.master.quit()
        self.master.destroy()
       






# every file will be represented by an Item
class Item:
    def __init__(self, filepath, window, row, col):
        print("add tile to row:", row," col:", col)
        # item main frame is like:
        #+--------------------------------------------+
        #|          ||           title                |
        #|  button  ||--------------------------------+
        #|          ||          content               |
        #+--------------------------------------------+
        # left frame          right frame
        
        # main frame
        self.main_frame = Frame(window, bg='violet')
        self.main_frame.grid(row=row, column=col, sticky="nsew")
        
        self.left_frame = Frame(self.main_frame, bg='yellow')
        self.right_frame = Frame(self.main_frame, bg='orange')

        #self.left_frame.grid(row=0, column=0, sticky="nsew")
        #self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.left_frame.pack(side=LEFT, fill=BOTH)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.file = filepath
        self.title_str = StringVar()
        self.content_str = StringVar()
        
        # deals with right frame
        self.edit_button = Button(self.left_frame, text="@", command=self.editfile)
        self.edit_button.pack(fill=BOTH, expand=TRUE, side=LEFT, anchor=CENTER)

        # deals with right frame
        self.title_entry = Entry(self.right_frame)
        self.title_entry.config(textvariable=self.title_str)
        self.title_entry.config(width=len(self.title_str.get()))
        self.title_entry.pack(fill=X)
        
        self.content_entry = Entry(self.right_frame)
        self.content_entry.config(textvariable=self.content_str)
        self.content_entry.config(width=len(self.content_str.get()))
        self.content_entry.pack(fill=X)
        
        # run update to load the string values
        self.update()

    def set_title(self, title):
        self.title_str.set(str(title))
        self.title_entry.config(width=len(str(title)))

    def set_content(self, content):
        self.content_str.set(str(content))
        self.content_entry.config(width=len(str(content)))

    def update(self):
        del RESULT[:] # clear global variable
        print("running", self.file)
        exec(open(self.file).read(), globals())
        print(RESULT)

        if len(RESULT) > 1:
            self.set_content(RESULT[0])
            self.set_title(RESULT[1])
        elif len(RESULT) > 0:
            self.set_content(RESULT[0])
            self.set_title(os.path.basename(self.file))            
        else:
            self.set_content("-")
            self.set_title(os.path.basename(self.file))

    def editfile(self):
        os.system('"' + TEXT_EDITOR_PATH + ' ' + self.file + ' &"')
        print("ok")



                    

root = Tk()
my_gui = Dashboard(root)
root.mainloop()
