#!/usr/local/bin/python3

import tkinter as tk
top = tk.Tk()
top.geometry("500x200")
# Code to add widgets will go here...
# def helloCallBack():
#    tkMessageBox.showinfo( "Hello Python", "Hello World")


# B = tkinter.Button(top, text ="Hello", command = helloCallBack)

greeting = tk.Label(text="Welcome to KUBER!!!", 
                    width=25,
                    height=5,)
greeting.pack()


def handle_click(event):
    print("The button was clicked!")

button = tk.Button(
    text="Lets start!",
    width=7,
    height=1,
)

button.pack()

top.mainloop()