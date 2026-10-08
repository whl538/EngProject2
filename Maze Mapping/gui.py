import tkinter as tk
from tkinter import Menu
import tkinter.font as tkFont
from tkinter import ttk

from maze import Maze
from cell import Cell
from nodes import Node, BranchNode, EndPointNode

class IntroFrame():
    def __init__(self, frame, on_start=None):
        self.on_start = on_start
        self.container = frame

        self.label = tk.Label(frame, text="Maze simulator testing!").pack()

        self.button = tk.Button(frame, text='Get started!')
        self.button['command'] = self.button_clicked
        self.button.pack()

    def button_clicked(self):
        MazeDimensionsSelect(self.container, self.on_start)

class MazeDimensionsSelect(tk.Toplevel):
    def __init__(self, parent, on_start=None):
        super().__init__(parent)
        self.parent = parent
        self.on_start = on_start

        self.title('Select Maze Dimensions')
        self.geometry('600x200')

        options = {'padx': 5, 'pady': 5}

        self.label = ttk.Label(self, text='Enter the maze\'s length!')
        self.label.grid(column=0, row=0, **options)

        self.maze_length = tk.IntVar()
        self.length_entry = ttk.Entry(self, textvariable=self.maze_length)
        self.length_entry.grid(column=1, row=0, **options)
        self.length_entry.focus()


        self.label = ttk.Label(self, text='Enter the maze\'s width!')
        self.label.grid(column=0, row=1, **options)
        
        self.maze_width = tk.IntVar()
        self.width_entry = ttk.Entry(self, textvariable=self.maze_width)
        self.width_entry.grid(column=1, row=1, **options)

        self.label = ttk.Label(self, text='Enter the number of divisions!')
        self.label.grid(column=0, row=2, **options)
                
        self.maze_divisions = tk.IntVar()
        self.divisions_entry = ttk.Entry(self, textvariable=self.maze_divisions)
        self.divisions_entry.grid(column=1, row=2, **options)

        self.enter_button = ttk.Button(self, text='Enter', command=self.enter_button_pressed)
        self.enter_button.place(relx=0.9, rely=0.8, anchor='center')

    def enter_button_pressed(self):
        if self.on_start:
            self.on_start(self.maze_length.get(), self.maze_width.get(), self.maze_divisions.get())
        self.destroy()

class MazeGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Maze!')
        self.geometry('720x720')

        self.notebook = ttk.Notebook(self)
        self.introtab = tk.Frame(self.notebook)
        self.menubar = Menu(self)
        self.tabs: list[tk.Frame] = []
        self.tab_ids = {}

        self.config(menu=self.menubar)

        self.file_menu = Menu(self.menubar)

        self.file_menu.add_command(label='Quit', command=self.destroy)
        self.menubar.add_cascade(label='File', menu=self.file_menu)

        self.notebook.add(self.introtab, text='Welcome!')
        self.notebook.pack(expand=True, fill='both')

    def get_intro_tab(self):
        return self.introtab

    def create_grid(self, event=None):

        w = self.c.winfo_width() 
        h = self.c.winfo_height() 
        self.c.delete('grid_line') 

        w_divider_frequency = w // self.divisions
        h_divider_frequency = h // self.divisions
        
        for i in range(0, w, w_divider_frequency):
            self.c.create_line([(i, 0), (i, h)], tag='grid_line')
        
        for i in range(0, h, h_divider_frequency):
            self.c.create_line([(0, i), (w, i)], tag='grid_line')


    def start_maze(self, x, y, divisions):
        self.divisions = divisions
        self.maze = Maze(x, y, divisions)
        self.notebook.forget(self.introtab)

        maze_gui = tk.Frame(self.notebook)
        self.c = tk.Canvas(maze_gui, height=1000, width=1000, bg='white')
        self.c.pack(fill=tk.BOTH, expand=True)
        self.c.bind('<Configure>', self.create_grid)

        self.tabs.insert(0, maze_gui)
        self.notebook.add(self.tabs[0], text=f'{x} x {y} maze!')
        self.tabs.append(tk.Frame(self.notebook))
        self.notebook.pack(expand=True, fill='both')

        for tab in self.notebook.tabs():
            self.tab_ids[self.notebook.tab(tab, 'text')] = tab

if __name__ == "__main__":
    app = MazeGUI()
    IntroFrame(app.get_intro_tab(), on_start=app.start_maze)
    app.mainloop()