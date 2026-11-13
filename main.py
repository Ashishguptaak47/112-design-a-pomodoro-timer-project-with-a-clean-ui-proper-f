import sys
import tkinter as tk
from pomodoro.ui import PomodoroApp

def main():
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
