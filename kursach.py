import tkinter as tk
from tkinter import messagebox
from tkinter import *
import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://data.gov.ua/dataset/71f900c9-b7e4-429a-8311-0c4b09471e7b/resource/22af9e96-0a45-4649-91d5-a000e95100a5/download/telephonedirectory-2024-03-28.csv'
local_filename = 'telephonedirectory.csv'
response = requests.get(url)
with open(local_filename, 'wb') as f:
    f.write(response.content)
df = pd.read_csv(local_filename, delimiter=';', encoding='utf-8')
pd.options.display.float_format = '{:.0f}'.format

def add_contact():
    messagebox.showinfo(".")
    
def redact():
    messagebox.showinfo(".")

def show_contact():
    messagebox.showinfo(".")

def delete_func():
    messagebox.showinfo(".")    

def help_func():
    messagebox.showinfo(title="saygex", message="довідка")

def find_contact():
    messagebox.showinfo(".")    

root = tk.Tk()
root.title("Телефонний довідник")

menu_bar = tk.Menu(root)

function_menu = tk.Menu(menu_bar, tearoff=0)
function_menu.add_command(label="Додати новий контакт", command=add_contact)
function_menu.add_command(label="Редагувати контакт", command=redact)
function_menu.add_command(label="Перегляд довіднику", command=show_contact)
function_menu.add_command(label="Видалити контакт", command=delete_func)
menu_bar.add_cascade(label="Дії", menu=function_menu)

help_menu = tk.Menu(menu_bar, tearoff = 0)
help_menu.add_command(label="Довідка", command=help_func)
menu_bar.add_cascade(label="Довідка", menu=help_menu)

entry_prof = Entry(root)
entry_prof.grid(row=0, column=1, pady=10, padx=10)

button1 = Button(root, text="Validate", command=find_contact)
button1.grid(row=7, column=1, pady=10, padx=10)

root.config(menu=menu_bar)
root.mainloop()