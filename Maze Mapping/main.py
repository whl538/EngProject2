from gui import *

if __name__ == "__main__":
    app = MazeGUI()
    IntroFrame(app.get_intro_tab(), on_start=app.start_maze)
    app.mainloop()