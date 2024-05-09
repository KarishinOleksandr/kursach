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
df = pd.read_csv(local_filename, delimiter=';', encoding='utf-8', dtype={'phone': 'str'})
df = df.astype({"phone": "str"})
if 'nameSet' in df.columns and 'keyWords' in df.columns:
    df.drop(['nameSet', 'keyWords'], axis=1, inplace=True)
df.to_csv(local_filename, sep=';', encoding='utf-8', index=False)
contact_found = False


def add_contact():
    root.withdraw()
    global new_window
    new_window = NewWindow()
    new_window.title("Додавання контакту")

    def add1():
        df = pd.read_csv(local_filename, delimiter=';', encoding='utf-8', dtype={'phone': 'str'})
        pattern2 = re.compile(r'\b[A-Za-z]\w*@[A-Za-z]+\.[A-Za-z]{2,}\b')
        data_to_append = [
            entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get()
        ]
        for i in range(len(data_to_append)):
            if data_to_append[i] == '':
                data_to_append[i] = "Інформація відсутня"
        if not data_to_append[3]:
            messagebox.showerror("Помилка", "Обов'язково введіть ім'я")
            return
        if data_to_append[3] in df["fullName"].values:
            messagebox.showerror("Помилка", "Контак з таким ім'ям вже існує")
            return
        if data_to_append[4] in df["phone"].values:
            messagebox.showerror("Помилка", "Контак з таким номером вже існує")
            return
        if data_to_append[5] in df["email"].values:
            messagebox.showerror("Помилка", "Контак з такою поштою вже існує")
            return

        existing_data = []
        entry5_value = entry5.get()
        phone_numbers = entry5_value.split(", ")
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

        messagebox.showinfo("Успіх!", "Контакт додано!")

    label1 = Label(new_window, text="Назва організації:")
    label1.place(x=150, y=5)
    entry1 = Entry(new_window)
    entry1.place(x=275, y=5)
    label2 = Label(new_window, text="Відділ:")
    label2.place(x=150, y=50)
    entry2 = Entry(new_window)
    entry2.place(x=275, y=50)
    label3 = Label(new_window, text="Посада:")
    label3.place(x=150, y=95)
    entry3 = Entry(new_window)
    entry3.place(x=275, y=95)
    label4 = Label(new_window, text="Прізвище та ім'я:")
    label4.place(x=150, y=140)
    entry4 = Entry(new_window)
    entry4.place(x=275, y=140)
    label5 = Label(new_window, text="Номер телефону:")
    label5.place(x=150, y=185)
    entry5 = Entry(new_window)
    entry5.place(x=275, y=185)
    label6 = Label(new_window, text="Ел-пошта:")
    label6.place(x=150, y=230)
    entry6 = Entry(new_window)
    entry6.place(x=275, y=230)
    bitn1 = Button(new_window, text="Додати", command=add1)
    bitn1.place(x=250, y=275)


def show_contact():
    root.withdraw()
    global new_window
    new_window = NewWindow()
    new_window.title("Список контактів")
    df = pd.read_csv(local_filename, delimiter=';', encoding='utf-8', dtype={'phone': 'str'})
    
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
    new_window.title("Видалення контакту")

    def delete1():
        data_to_search = entry2.get()
        if data_to_search:
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

    label42 = Label(new_window, text="Введіть прізвизе з ім'ям/номер/ел-пошту")
    label42.place(x=175, y=70)

    entry2 = Entry(new_window)
    entry2.place(x=225, y=40)

    btn1 = Button(new_window, text="Видалити контакт", command=delete1)
    btn1.place(x=230, y=100)

    label3 = Label(new_window, text="")
    label3.place(x=100, y=150)
    

def help_func():
    messagebox.showinfo(title="Довідка по додатку", message="Вітаю тебе, користувач!! \n"
                        "\n"
                        "Цей додаток призначається для побудови зручного введення корпоративної бази данних, а саме телефонного довіднику. \n"
                        "\n"
                        "Довідник має функції пошуку, додавання, видалення та редагування контактів. Звичайно, є функція перегляду всієї бази даннихю \n"
                        "\n"
                        "Головне меню це функція нашого пошуку, вам необхідно ввести прізвище з ім'ям/номер телефону/ел-пошту користувача для того щоб знайти його данні. \n"
                        "\n"
                        "ЗВЕРНІТЬ УВАГУ, НЕОБХІДНО ВВОДИТИ ПОВНІСТЮ ІМ'Я ТА ПРІЗВИЩЕ, ЯКЩО Є 'ПО-БАТЬКОВІ', ЙОГО ТАКОЖ ТРЕБА ВВЕСТИ ДОТРИМУЮЧИСЬ КОРЕКТНОГО РЕГІСТРУ!!! \n"
                        "\n"
                        "Для виклику всіх інших функцій необхідно вибрати пункт меню 'дії' та прослідувати підказкам на екрані. \n"
                        "\n"
                        "Не хвивлюйтесь, для повернення в головне меню просто необхідно знову нажати 'Дії' та вибрати повернутись до пошуку.")
    

def find_contact():
    global contact_found, contact_info
    df = pd.read_csv(local_filename, delimiter=';', encoding='utf-8', dtype={'phone': 'str'})
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
        contact_found = True
        update()
    else:
        label4.config(text="Введіть дані для пошуку")

def redact():
    root.withdraw()
    global new_window
    new_window = NewWindow()
    new_window.title("Редагування контакту")
    global entry_prof, label4, contact_found, contact_info
    
    def redact1():
        pattern2 = re.compile(r'\b[A-Za-z]\w*@[A-Za-z]+\.[A-Za-z]{2,}\b')
        contact_info1 = [
            entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(), entry7.get()
        ]
        for i in range(len(contact_info1)):
            if contact_info1[i] == '':
                contact_info1[i] = "Інформація відсутня"
        if not contact_info1[3]:
            messagebox.showerror("Помилка", "Обов'язково введіть ім'я")
            return
        if contact_info1[3] in df["fullName"].values:
            messagebox.showerror("Помилка", "Контакт з таким ім'ям вже існує")
            return
        
        existing_data = []
        entry6_value = entry6.get()
        phone_numbers = entry6_value.split(",")
        for phone_number in phone_numbers:
            digits_only = re.sub(r'\D', '', phone_number)
            if not len(digits_only) in [10, 12] or (len(digits_only) == 12 and not digits_only.startswith('380')):
                messagebox.showerror("Помилка", "Неправильний формат номеру!")
                return
        if not pattern2.match(contact_info1[5]):
            messagebox.showerror("Помилка", "Неправильний формат електронної пошти!")
            return
        
        with open(local_filename, "r", encoding="utf-8") as f:
            existing_data = [line.strip().split(';') for line in f.readlines()]
        
        row_to_delete = None
        for i, row in enumerate(existing_data):
            if row[:3] == contact_info1[:3]:
                row_to_delete = i
                break
        
        if row_to_delete is not None:
            del existing_data[row_to_delete]
        
        existing_data.append(contact_info1)
        
        with open(local_filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(existing_data)


    if contact_found:
        label1 = Label(new_window, text="Назва організації:")
        label1.place(x=150, y=5)
        entry2 = Entry(new_window)
        entry2.delete(0, tk.END)
        entry2.insert(0, contact_info.iloc[0]["Назва організаціїї"])
        entry2.place(x=275, y=5)

        label2 = Label(new_window, text="Відділ:")
        label2.place(x=150, y=50)
        entry3 = Entry(new_window)
        entry3.delete(0, tk.END)
        entry3.insert(0, contact_info.iloc[0]["Відділ"])
        entry3.place(x=275, y=50)

        label3 = Label(new_window, text="Посада:")
        label3.place(x=150, y=95)
        entry4 = Entry(new_window)
        entry4.delete(0, tk.END)
        entry4.insert(0, contact_info.iloc[0]["Посада"])
        entry4.place(x=275, y=95)

        label4 = Label(new_window, text="Прізвище та ім'я:")
        label4.place(x=150, y=140)
        entry5 = Entry(new_window)
        entry5.delete(0, tk.END)
        entry5.insert(0, contact_info.iloc[0]["Прізвище, Ім'я"])
        entry5.place(x=275, y=140)

        label5 = Label(new_window, text="Номер телефону:")
        label5.place(x=150, y=185)
        entry6 = Entry(new_window)
        entry6.delete(0, tk.END)
        entry6.insert(0, contact_info.iloc[0]["Номер"])
        entry6.place(x=275, y=185)

        label6 = Label(new_window, text="Ел-пошта:")
        label6.place(x=150, y=230)
        entry7 = Entry(new_window)
        entry7.delete(0, tk.END)
        entry7.insert(0, contact_info.iloc[0]["ел-пошта"])
        entry7.place(x=275, y=230)
        
        btn1 = Button(new_window, text="Зберегти зміни", command=redact1)
        btn1.place(x=250, y=275)

def back_to_main():
    new_window.destroy()
    root.deiconify()  

def update():
    global root
    btn1 = Button(root, text="Редагувати контакт", command=redact)
    btn1.place(x=240, y=300)


class NewWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Нове вікно")
        self.geometry("600x400") 
        self.resizable(False, False)

        def on_closing():
            self.destroy()
            root.deiconify()

        self.protocol("WM_DELETE_WINDOW", on_closing)
        
        menu_bar = tk.Menu(self)

        function_menu = tk.Menu(menu_bar, tearoff=0)
        function_menu.add_command(label="Повернутися до пошуку", command=back_to_main)
        menu_bar.add_cascade(label="Дії", menu=function_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Довідка", command=help_func)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)

        self.config(menu=menu_bar)

root = tk.Tk()
root.title("Телефонний довідник")
root.geometry("600x400")
root.resizable(False, False)

menu_bar = tk.Menu(root)

function_menu = tk.Menu(menu_bar, tearoff=0)
function_menu.add_command(label="Додати новий контакт", command=add_contact)
function_menu.add_command(label="Перегляд довідника", command=show_contact)
function_menu.add_command(label="Видалити контакт", command=delete_func)
menu_bar.add_cascade(label="Дії", menu=function_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Довідка", command=help_func)
menu_bar.add_cascade(label="Довідка", menu=help_menu)

label_start = Label(root, text="Вітаю, користувач!")
label_start.place(x=230, y=5)

entry_prof = Entry(root)
entry_prof.place(x=225, y=40)

label41 = Label(root, text="Введіть прізвизе з ім'ям/номер/ел-пошту")
label41.place(x=175, y=70)

button1 = Button(root, text="Знайти контакт", command=find_contact)
button1.place(x=240, y=100)

label4 = Label(root, text="")
label4.place(x=130, y=150)

root.config(menu=menu_bar)
root.mainloop()
