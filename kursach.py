import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import Tk, Canvas, Scrollbar, VERTICAL
import pandas as pd
import requests
import csv
import os
import re

url = 'https://data.gov.ua/dataset/71f900c9-b7e4-429a-8311-0c4b09471e7b/resource/22af9e96-0a45-4649-91d5-a000e95100a5/download/telephonedirectory-2024-03-28.csv'
local_filename = 'telephonedirectory.csv'
response = requests.get(url)
if not os.path.exists(local_filename):
    response = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(response.content)
df = pd.read_csv(local_filename, delimiter=';', encoding='utf-8')
df = df.astype({"phone": "str"})
if 'nameSet' in df.columns and 'keyWords' in df.columns:
    df.drop(['nameSet', 'keyWords'], axis=1, inplace=True)
df.to_csv(local_filename, sep=';', encoding='utf-8', index=False)
pd.options.display.float_format = '{:.0f}'.format

def add_contact():
    root.withdraw()
    global new_window
    new_window = NewWindow()
    def add1():
        pattern2 = re.compile(r'\b[A-Za-z]\w*@[A-Za-z]+\.[A-Za-z]{2,}\b')
        data_to_append = [
            entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get()
        ]
        for i in range(len(data_to_append)):
            if data_to_append[i] == '':
                data_to_append[i] = "Інформація відсутня"
        if not data_to_append[3]:
            messagebox.showerror("Помилка", "обов'язково введіть ім'я")
            return
        
        existing_data = []
        entry5_value = entry5.get()  # Отримати значення з Entry5
        phone_numbers = entry5_value.split(",")
        for phone_number in phone_numbers:
            digits_only = re.sub(r'\D', '', phone_number)
            if not len(digits_only) in [10, 12] or (len(digits_only) == 12 and not digits_only.startswith('380')):
                messagebox.showerror("Помилка", "Неправильний формат номеру!")
                return
        if not pattern2.match(data_to_append[5]):
            messagebox.showerror("Помилка", "Неправильний формат електронної пошти!")
            return
        with open(local_filename, "r", encoding="utf-8") as f:
            existing_data = [line.strip().split(';') for line in f.readlines()]

        existing_data.append(data_to_append)

        data_to_append[4] = ",".join(phone_numbers)

        with open(local_filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(existing_data)

    
    entry1 = Entry(new_window)
    entry1.grid(row=0, column=1, pady=10, padx=10)
    entry2 = Entry(new_window)
    entry2.grid(row=1, column=1, pady=10, padx=10)
    entry3 = Entry(new_window)
    entry3.grid(row=2, column=1, pady=10, padx=10)
    entry4 = Entry(new_window)
    entry4.grid(row=3, column=1, pady=10, padx=10)
    entry5 = Entry(new_window)
    entry5.grid(row=4, column=1, pady=10, padx=10)
    entry6 = Entry(new_window)
    entry6.grid(row=5, column=1, pady=10, padx=10)
    bitn1 = Button(new_window, text="Додати", command=add1)
    bitn1.grid(row=7, column=1, pady=10, padx=10)

def redact():
    root.withdraw()
    global new_window
    new_window = NewWindow()


def show_contact():
    root.withdraw()
    global new_window
    new_window = NewWindow()

    sorted_df = df.sort_values("fullName")
    sorted_df = sorted_df.rename(columns={"nameОrganization": "Назва організаціїї", "nameDepartment": "Відділ", "jobTitle": "Посада", "fullName": "Прізвище, Ім`я", "phone": "Номер", "email": "ел-пошта"})

    text_output = ""

    for index, row in sorted_df.iterrows():
        text_output += f"Назва організації: {row['Назва організаціїї']}\n"
        text_output += f"Ім`я та прізвище: {row['Прізвище, Ім`я']}\n"  
        text_output += f"Посада: {row['Посада']}\n"
        text_output += f"Відділ: {row['Відділ']}\n"
        text_output += f"Номер: {row['Номер']}\n"
        text_output += f"Електронна пошта: {row['ел-пошта']}\n"
        text_output += "-" * 50 + "\n"  

    canvas = Canvas(new_window, height=400, width=500)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(new_window, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    for i, line in enumerate(text_output.split('\n')):
        label = Label(frame, text=line)
        label.grid(row=i, column=0, sticky='w')

    frame.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox("all"))

def delete_func():
    root.withdraw()
    global new_window
    new_window = NewWindow()
    
    def delete1():
        data_to_search = entry2.get()
        if data_to_search:
            # Пошук рядків, що відповідають умові
            if data_to_search in df["fullName"].values:
                df.drop(df[df["fullName"] == data_to_search].index, inplace=True)
            elif data_to_search in df["phone"].values:
                df.drop(df[df["phone"] == data_to_search].index, inplace=True)
            elif data_to_search in df["email"].values:
                df.drop(df[df["email"] == data_to_search].index, inplace=True)
            else:
                label3.config(text="Контакт не знайдено")
                return
            
            df.to_csv(local_filename, sep=';', encoding='utf-8', index=False)
        else:
            label3.config(text="Введіть дані для пошуку")


    entry2 = Entry(new_window)
    entry2.grid(row=1, column=0, padx=10, pady=10)

    btn1 = Button(new_window, text="Validate", command=delete1)
    btn1.grid(row=2, column=0, padx=10, pady=10)

    label3 = Label(new_window, text="")
    label3.grid(row=3, column=0, padx=10, pady=10)
    

def help_func():
    messagebox.showinfo(title="saygex", message="довідка")

def find_contact():
    data_to_search = entry_prof.get()
    if data_to_search:
        if data_to_search in df["fullName"].values:
            contact_info = df[df["fullName"] == data_to_search].copy()
        elif data_to_search in df["phone"].values:
            contact_info = df[df["phone"] == data_to_search].copy()
        elif data_to_search in df["email"].values:
            contact_info = df[df["email"] == data_to_search].copy()
        else:
            label4.config(text="Контакт не знайдено")
            return

        contact_info = contact_info.rename(columns={"nameОrganization": "Назва організаціїї", "nameDepartment": "Відділ", "jobTitle": "Посада", "fullName": "Прізвище, Ім'я", "phone": "Номер", "email": "ел-пошта"})
        
        text_output = ""
        for index, row in contact_info.iterrows():
            for column, value in row.items():
                text_output += f"{column}: {value}\n"
            text_output += "\n"

        label4.config(text=text_output)
    else:
        label4.config(text="Введіть дані для пошуку")

def back_to_main():
    new_window.destroy()
    root.deiconify()  

class NewWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Нове вікно")
        self.geometry("800x400") 

        def on_closing():
            self.destroy()
            root.deiconify()

        self.protocol("WM_DELETE_WINDOW", on_closing)
        
        menu_bar = tk.Menu(self)

        function_menu = tk.Menu(menu_bar, tearoff=0)
        function_menu.add_command(label="Додати новий контакт", command=add_contact)
        function_menu.add_command(label="Редагувати контакт", command=redact)
        function_menu.add_command(label="Перегляд довідника", command=show_contact)
        function_menu.add_command(label="Видалити контакт", command=delete_func)
        function_menu.add_separator()
        function_menu.add_command(label="Повернутися до пошуку", command=back_to_main)
        menu_bar.add_cascade(label="Дії", menu=function_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Довідка", command=help_func)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)

        self.config(menu=menu_bar)

root = tk.Tk()
root.title("Телефонний довідник")
root.geometry("300x200")  

menu_bar = tk.Menu(root)

function_menu = tk.Menu(menu_bar, tearoff=0)
function_menu.add_command(label="Додати новий контакт", command=add_contact)
function_menu.add_command(label="Редагувати контакт", command=redact)
function_menu.add_command(label="Перегляд довідника", command=show_contact)
function_menu.add_command(label="Видалити контакт", command=delete_func)
menu_bar.add_cascade(label="Дії", menu=function_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Довідка", command=help_func)
menu_bar.add_cascade(label="Довідка", menu=help_menu)

entry_prof = Entry(root)
entry_prof.grid(row=0, column=1, pady=10, padx=10)

button1 = Button(root, text="Validate", command=find_contact)
button1.grid(row=3, column=1, pady=10, padx=10)

label4 = Label(root, text="")
label4.grid(row=4,column=1, pady=10, padx=10)

root.config(menu=menu_bar)
root.mainloop()
