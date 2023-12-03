from tkinter import *
import customtkinter as ctk


"""
Example for a simple 1200x400 window with the following widgets:
Frame, Button, Silder and, Entryfield in darkmode.
"""

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("1200x400")
root.update()

plotframe = ctk.CTkFrame(master=root,
                         height= root.winfo_height()*0.95,
                         width = root.winfo_width()*0.66,
                         fg_color="darkblue")
plotframe.place(relx=0.33, rely=0.025)

Button = ctk.CTkButton(master = root,
                       width=300,
                       height=50)
Button.place(relx=0.025,rely=0.025)

TypedInput = ctk.CTkEntry(master=root,
                          width=300,
                          height=50,
                          fg_color="darkblue")
TypedInput.place(relx=0.025,rely=0.5)

Slider = ctk.CTkSlider(master=root,
                       width=300,
                       height=20)
Slider.place(relx= 0.025,rely=0.90)

root.mainloop()