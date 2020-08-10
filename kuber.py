#!/usr/local/bin/python3

import tkinter as tk
top = tk.Tk()
top.geometry("500x200")

greeting = tk.Label(text="Welcome to KUBER!!!", 
                    width=25,
                    height=5,)
greeting.pack()


def handle_click():
    window = tk.Tk()
    top.destroy()
    window.geometry('550x450')
    window.title('Kuber')
    rlbl = tk.Label(window, text='\nWork in progress...')
    rlbl.pack()

button = tk.Button(
    text="Lets start!",
    width=7,
    height=1,
    command = handle_click
)

button.pack()

top.mainloop()