import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date, timedelta, datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, Tk, Button, Label, StringVar, ttk, Entry
from glob import glob
import os
import pandas as pd

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'dokimastikobrouskounia@gmail.com'
EMAIL_PASSWORD = 'gpazzngooaxeelvh'
RECIPIENT_EMAIL = 'nickbini@hotmail.gr'

# Global variables to store expenses and income
code = "8203"
expenses = {}

montly_expenses = {
    'Enoikio': 0,
    'Reyma': 0,
    'Nero': 0,
    'Aerio': 0,
    'Tilefwno': 0,
    'IKA': 0,
    'EFKA': 0,
    'FPA': 0,
    'Else': 0

}

income = {
    'Z': 0,
    'Tziros': 0,
    'Tziros Cash': 0,
    'Tziros Card': 0,
    'Sitted': 0,
    'Standing': 0,
    'Wolt': 0,
    'Delivery': 0,
    'Phone Delivery': 0,
    'Efood Delivery': 0,
    'Efood Paid': 0,
    'Efood Cash': 0
}

misthodosia = {}

#arxikopoihsh tou expenses dictionary me tous suppliers apo to .csv
with open('suppliers.csv', encoding="utf-8") as file:
    reader=csv.reader(file)
    for row in reader:
        supplier = row[0]  
        amount = float(row[1]) 
        
        if supplier in expenses:
            expenses[supplier] += amount
        else:
            expenses[supplier] = amount

print(expenses)

#arxikopoihsh toy misthodosia dictionary me tous ypallilous apo to .csv
with open('misthodosia.csv', encoding="utf-8") as file:
    reader=csv.reader(file)
    for row in reader:
        ypallilos = row[0]  
        amount = float(row[1]) 
        
        if ypallilos in misthodosia:
            misthodosia[ypallilos] += amount
        else:
            misthodosia[ypallilos] = amount

print(misthodosia)

#gia na onomatizw kathe .csv me tin kathimerini imeromhnia
def get_csv_filename():
    current_date = date.today().strftime('%d-%m-%Y')
    return f"{current_date}.csv"


#gia na katharizw to .csv an thelw
def clear_csv_file():
    with open(get_csv_filename(), 'w', newline='', encoding="utf-8") as file:
        pass

        
#gia na grapsw ta expenses kai ta income
def write_expenses_and_income(expenses_dict, misthodosia_dict, montlyExpenses_dict, income_dict):
    file_exists = True if open(get_csv_filename(), 'a', encoding="utf-8").tell() else False
    with open(get_csv_filename(), 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write expenses
        total_expenses = sum(expenses_dict.values())
        for key, value in expenses_dict.items():
            writer.writerow([key, value])
        writer.writerow(['Total Expenses', total_expenses])
        writer.writerow([])

        # Write monthly expenses
        total_monthly_expenses = sum(montlyExpenses_dict.values())
        for key, value in montlyExpenses_dict.items():
            writer.writerow([key, value])
        writer.writerow(['Total Monthly Expenses', total_monthly_expenses])
        writer.writerow([])

        # Write misthodosia
        total_misthodosia = sum(misthodosia_dict.values())
        for key, value in misthodosia_dict.items():
            writer.writerow([key, value])
        writer.writerow(['Total Misthodosia', total_misthodosia])
        writer.writerow([])

        # Write income
        total_income = income['Tziros']
        for key, value in income_dict.items():
            writer.writerow([key, value])
        writer.writerow(['Total Income', total_income])
        writer.writerow([])

         # Write total expenses and total income row
        total_expenses_all = total_expenses + total_monthly_expenses + total_misthodosia
        writer.writerow(['Expenses', total_expenses_all])
        writer.writerow(['Income', total_income])


#apothikeysi data
def save_data():
    clear_csv_file()
    write_expenses_and_income(expenses, misthodosia, montly_expenses, income)
    messagebox.showinfo("Επιτυχία", "Τα δεδομένα αποθηκέυτηκαν!")
    update_totals()

#apostoli email
def send_email():
    filename = f"{get_csv_filename()}.csv"
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = f"Έξοδα Μαγαζιού - {get_csv_filename()}"
    body = "Τα έξοδα για σήμερα είναι:"
    message.attach(MIMEText(body, 'plain'))

    with open(get_csv_filename(), 'r', encoding="utf-8") as file:
        attachment = MIMEText(file.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(attachment)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)

    messagebox.showinfo("Επιτυχία", "Τα email στάλθηκαν επιτυχώς!")

#combined file send mail
def send_email_combined(filename):
    file_path = os.path.join(os.getcwd(), filename)
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = f"Restaurant Finances - {filename}"
    body = "Τα έξοδα για σήμερα είναι:"
    message.attach(MIMEText(body, 'plain'))

    with open(file_path, 'rb', encoding="utf-8") as file:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(attachment)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)

    messagebox.showinfo("Επιτυχία", "Τα email στάλθηκαν επιτυχώς!")

#anoigw parathiro expenses
def open_expenses_window():
    global expenses_window
    expenses_window = tk.Toplevel(window)
    expenses_window.configure(bg="#BFACC8")
    expenses_window.resizable(width=False, height=False)
    window_width=200
    button_height=60
    window_height=button_height*len(expenses)
    expenses_window.geometry(f"{window_width}x{window_height+90}")
    expenses_window.title("Έξοδα")

    def save_expenses():
        global expenses

        # Update the expenses dictionary based on the entry fields
        for supplier, entry_field in entry_fields.items():
            expenses[supplier] = float(entry_field.get())

        write_expenses_and_income(expenses, misthodosia, montly_expenses, income)
        expenses_window.destroy()
        messagebox.showinfo("Επιτυχία", "Τα έξοδα αποθηκεύτηκαν επιτυχώς!")
        update_totals()

    #gia na diwxnw supplier kai apo to dictionary kai apo to .csv
    def remove_supplier():
        def remove_selected_supplier():
            selected_supplier = supplier_var.get()
            if selected_supplier in expenses:
                del expenses[selected_supplier]
                write_expenses_and_income(expenses, misthodosia, montly_expenses, income)
                messagebox.showinfo("Επιτυχία", f"Ο προμηθευτής: '{selected_supplier}' διαγράφηκε με επιτυχία.")
                

            #Remove supplier from the suppliers.csv file
            with open('suppliers.csv', 'r', encoding="utf-8") as file:
                lines = file.readlines()

            with open('suppliers.csv', 'w', encoding="utf-8") as file:
                for line in lines:
                    supplier_info = line.strip().split(',')
                    supplier_name = supplier_info[0]
                    if supplier_name != selected_supplier:
                        file.write(line)

            expenses_window.destroy()
            open_expenses_window()
            remove_supplier_window.destroy()


        remove_supplier_window = tk.Toplevel(expenses_window)
        remove_supplier_window.configure(bg="#A1CDF4")
        remove_supplier_window.resizable(width=False, height=False)
        remove_supplier_window.geometry("250x120")
        remove_supplier_window.title("Διαγράφη Προμηθευτή")

        supplier_label = tk.Label(remove_supplier_window, text="Επίλεξε Προμηθευτή:", font=("Arial", 12, "bold"), width=20)
        supplier_label.configure(bg="#A1CDF4")
        supplier_label.pack()

        supplier_var = tk.StringVar()
        supplier_dropdown = ttk.Combobox(remove_supplier_window, textvariable=supplier_var, state="readonly")
        supplier_dropdown['values'] = tuple(expenses.keys())
        supplier_dropdown.pack()

        remove_button = tk.Button(remove_supplier_window, text="Διαγράφη", command=remove_selected_supplier,font=("Arial", 12, "bold"), width=13)
        remove_button.pack(pady=5)

    #gia na prosthetw supplier kai sto dictionary kai sto .csv
    def add_supplier():
        def add_new_supplier():
            new_supplier = supplier_entry.get().strip()
            if new_supplier:
                if new_supplier in expenses:
                    messagebox.showerror("Αποτυχία", "Ο προμηθευτής υπάρχει ήδη.")
                else:
                    # Add the new supplier to the expenses dictionary and suppliers.csv file
                    expenses[new_supplier] = 0.0
                    with open('suppliers.csv', 'a', encoding="utf-8") as file:
                        file.write(f"{new_supplier},0.0\n")
                    messagebox.showinfo("Επιτυχία", f"Ο προμηθευτής: '{new_supplier}' προστέθηκε με επιτυχία.")
                    add_supplier_window.destroy()
                    
                    # Refresh the expenses window to display the new supplier
                    expenses_window.destroy()
                    open_expenses_window()

        add_supplier_window = tk.Toplevel(expenses_window)
        add_supplier_window.configure(bg="#A1CDF4")
        add_supplier_window.resizable(width=False, height=False)
        add_supplier_window.geometry("250x120")
        add_supplier_window.title("Προσθήκη Προμηθευτή")

        supplier_label = tk.Label(add_supplier_window, text="Όνομα Προμηθευτή:", font=("Arial", 12, "bold"), width=20)
        supplier_label.configure(bg="#A1CDF4")
        supplier_label.pack()

        supplier_entry = tk.Entry(add_supplier_window)
        supplier_entry.pack()

        add_button = tk.Button(add_supplier_window, text="Προσθήκη", command=add_new_supplier, font=("Arial", 12, "bold"), width=13)
        add_button.pack(pady=5)


    entry_fields = {}  #Dictionary to store the entry fields apo to suppliers csv

    # Create labels and entry fields dynamically based on expenses dictionary
    for i, (supplier, amount) in enumerate(expenses.items()):
        label_text = f"{supplier}:"
        label = tk.Label(expenses_window, text=label_text, font=("Arial", 12, "bold"), width=13)
        label.configure(bg="#BFACC8")
        label.pack()

        entry_field = tk.Entry(expenses_window)
        entry_field.insert(0, str(amount))
        entry_field.pack()

        entry_fields[supplier] = entry_field  # Add the entry field to the dictionary

    remove_supplier_button = tk.Button(expenses_window, text="Διαγραφή Προμηθευτή", command=remove_supplier, font=("Arial", 12, "bold"), width=18)
    remove_supplier_button.pack(pady=5)
    add_supplier_button = tk.Button(expenses_window, text="Προσθήκη Προμηθευτή", command=add_supplier, font=("Arial", 12, "bold"), width=18)
    add_supplier_button.pack(pady=5)
    save_expenses_button = tk.Button(expenses_window, text="Αποθήκευση", command=save_expenses, font=("Arial", 12, "bold"), width=15)
    save_expenses_button.pack(pady=5)

def open_montly_expenses_window():
    montly_expenses_window = tk.Toplevel(window)
    montly_expenses_window.configure(bg="#BFACC8")
    montly_expenses_window.resizable(width=False, height=False)
    montly_expenses_window.geometry("200x500")
    montly_expenses_window.title("Έξοδα Μήνα")

    def save_montly_expenses():
        montly_expenses['Enoikio']=float(enoikio_entry.get())
        montly_expenses['Reyma']=float(reyma_entry.get())
        montly_expenses['Nero']=float(nero_entry.get())
        montly_expenses['Tilefwno']=float(tilefwno_entry.get())
        montly_expenses['Aerio']=float(aerio_entry.get())
        montly_expenses['FPA']=float(fpa_entry.get())
        montly_expenses['EFKA']=float(efka_entry.get())
        montly_expenses['IKA']=float(ika_entry.get())
        montly_expenses['Else']=float(alloi_entry.get())

        write_expenses_and_income(expenses, misthodosia, montly_expenses, income)
        montly_expenses_window.destroy()
        messagebox.showinfo("Επιτυχία", "Τα έξοδα αποθηκέυτηκαν με επιτυχία.")
        update_totals()

    enoikio_label = tk.Label(montly_expenses_window, text="Ενοίκιο:", font=("Arial", 12, "bold"), width=13)
    enoikio_label.configure(bg="#BFACC8")
    enoikio_label.pack()
    enoikio_entry = tk.Entry(montly_expenses_window)
    enoikio_entry.insert(0, '0')
    enoikio_entry.pack()

    reyma_label = tk.Label(montly_expenses_window, text="Ρεύμα:", font=("Arial", 12, "bold"), width=13)
    reyma_label.configure(bg="#BFACC8")
    reyma_label.pack()
    reyma_entry = tk.Entry(montly_expenses_window)
    reyma_entry.insert(0, '0')
    reyma_entry.pack()

    nero_label = tk.Label(montly_expenses_window, text="Νερό:", font=("Arial", 12, "bold"), width=13)
    nero_label.configure(bg="#BFACC8")
    nero_label.pack()
    nero_entry = tk.Entry(montly_expenses_window)
    nero_entry.insert(0, '0')
    nero_entry.pack()

    tilefwno_label = tk.Label(montly_expenses_window, text="Τηλέφωνο:", font=("Arial", 12, "bold"), width=13)
    tilefwno_label.configure(bg="#BFACC8")
    tilefwno_label.pack()
    tilefwno_entry = tk.Entry(montly_expenses_window)
    tilefwno_entry.insert(0, '0')
    tilefwno_entry.pack()

    aerio_label = tk.Label(montly_expenses_window, text="Αέριο:", font=("Arial", 12, "bold"), width=13)
    aerio_label.configure(bg="#BFACC8")
    aerio_label.pack()
    aerio_entry = tk.Entry(montly_expenses_window)
    aerio_entry.insert(0, '0')
    aerio_entry.pack()

    fpa_label = tk.Label(montly_expenses_window, text="ΦΠΑ:", font=("Arial", 12, "bold"), width=13)
    fpa_label.configure(bg="#BFACC8")
    fpa_label.pack()
    fpa_entry = tk.Entry(montly_expenses_window)
    fpa_entry.insert(0, '0')
    fpa_entry.pack()

    efka_label = tk.Label(montly_expenses_window, text="ΕΦΚΑ:", font=("Arial", 12, "bold"), width=13)
    efka_label.configure(bg="#BFACC8")
    efka_label.pack()
    efka_entry = tk.Entry(montly_expenses_window)
    efka_entry.insert(0, '0')
    efka_entry.pack()

    ika_label = tk.Label(montly_expenses_window, text="ΙΚΑ:", font=("Arial", 12, "bold"), width=13)
    ika_label.configure(bg="#BFACC8")
    ika_label.pack()
    ika_entry = tk.Entry(montly_expenses_window)
    ika_entry.insert(0, '0')
    ika_entry.pack()

    alloi_label = tk.Label(montly_expenses_window, text="Άλλο:", font=("Arial", 12, "bold"), width=13)
    alloi_label.configure(bg="#BFACC8")
    alloi_label.pack()
    alloi_entry = tk.Entry(montly_expenses_window)
    alloi_entry.insert(0, '0')
    alloi_entry.pack()

    save_expenses_button = tk.Button(montly_expenses_window, text="Αποθήκευση", command=save_montly_expenses, font=("Arial", 12, "bold"), width=10)
    save_expenses_button.pack(pady=5)


def open_payroll_window():
    payroll_window = tk.Toplevel(window)
    payroll_window.configure(bg="#BFACC8")
    payroll_window.resizable(width=False, height=False)
    window_width=200
    button_height=60
    window_height=button_height*len(misthodosia)
    payroll_window.geometry(f"{window_width}x{window_height+140}")
    payroll_window.title("Μισθοδοσία")

    def save_payroll():
        for employee, entry_field in entry_fields.items():
            misthodosia[employee] = float(entry_field.get())

        write_expenses_and_income(expenses, misthodosia, montly_expenses, income)
        payroll_window.destroy()
        messagebox.showinfo("Επιτυχία", "Οι πληρωμές αποθηκεύτηκαν με επιτυχία.")
        update_totals()

    def remove_employee():
        def remove_selected_employee():
            selected_employee = employee_var.get()
            if selected_employee in misthodosia:
                del misthodosia[selected_employee]
                write_expenses_and_income(expenses, misthodosia, montly_expenses, income)
                messagebox.showinfo("Επιτυχία", f"Ο υπάλληλος: '{selected_employee}' διαγράφηκε με επιτυχία.")
            
            with open('misthodosia.csv', 'r', encoding="utf-8") as file:
                lines=file.readlines()
            
            with open('misthodosia.csv', 'w', encoding="utf-8") as file:
                for line in lines:
                    ypallilos_info=line.strip().split(',')
                    ypallilos_name=ypallilos_info[0]
                    if ypallilos_name != selected_employee:
                        file.wrte(line)


            payroll_window.destroy()
            open_payroll_window()
            remove_employee_window.destroy()

        remove_employee_window = tk.Toplevel(payroll_window)
        remove_employee_window.configure(bg="#A1CDF4")
        remove_employee_window.resizable(width=False, height=False)
        remove_employee_window.geometry("250x120")
        remove_employee_window.title("Διαγραφή Υπαλλήλου")

        employee_label = tk.Label(remove_employee_window, text="Επίλεξε Υπάλληλο:", font=("Arial", 12, "bold"), width=17)
        employee_label.configure(bg="#A1CDF4")
        employee_label.pack()

        employee_var = tk.StringVar()
        employee_dropdown = ttk.Combobox(remove_employee_window, textvariable=employee_var, state="readonly")
        employee_dropdown['values'] = tuple(misthodosia.keys())
        employee_dropdown.pack()

        remove_button = tk.Button(remove_employee_window, text="Διαγράφη", command=remove_selected_employee, font=("Arial", 12, "bold"), width=13)
        remove_button.pack(pady=5)

    def add_employee():
        def add_new_employee():
            new_employee = employee_entry.get().strip()
            if new_employee:
                if new_employee in misthodosia:
                    messagebox.showerror("Αποτυχία", "Ο υπάλληλος υπάρχει ήδη.")
                else:
                    misthodosia[new_employee] = 0.0
                    with open('misthodosia.csv', 'a', encoding="utf-8") as file:
                        file.write(f"{new_employee},0.0\n")
                        
                    messagebox.showinfo("Επιτυχία", f"Ο υπάλληλος: '{new_employee}' προστέθηκε με επιτυχία.")

            payroll_window.destroy()
            open_payroll_window()
            add_employee_window.destroy()


        add_employee_window = tk.Toplevel(payroll_window)
        add_employee_window.configure(bg="#A1CDF4")
        add_employee_window.resizable(width=False, height=False)
        add_employee_window.geometry("250x120")
        add_employee_window.title("Προσθήκη Υπαλλήλου")

        employee_label = tk.Label(add_employee_window, text="Όνομα Υπαλλήλου:", font=("Arial", 12, "bold"), width=20)
        employee_label.configure(bg="#A1CDF4")
        employee_label.pack()

        employee_entry = tk.Entry(add_employee_window)
        employee_entry.pack()

        add_button = tk.Button(add_employee_window, text="Προσθήκη", command=add_new_employee, font=("Arial", 12, "bold"), width=13)
        add_button.pack(pady=5)

    entry_fields = {}

    for i, (employee, amount) in enumerate(misthodosia.items()):
        label_text = f"{employee}:"
        label = tk.Label(payroll_window, text=label_text, font=("Arial", 12, "bold"), width=13)
        label.configure(bg="#BFACC8")
        label.pack()

        entry_field = tk.Entry(payroll_window)
        entry_field.insert(0, str(amount))
        entry_field.pack()

        entry_fields[employee] = entry_field

    remove_employee_button = tk.Button(payroll_window, text="Διαγράφη Υπαλλήλου", command=remove_employee, font=("Arial", 12, "bold"), width=17)
    remove_employee_button.pack(pady=5)

    add_employee_button = tk.Button(payroll_window, text="Προσθήκη Υπαλλήλου", command=add_employee, font=("Arial", 12, "bold"), width=17)
    add_employee_button.pack(pady=5)

    save_payroll_button = tk.Button(payroll_window, text="Αποθήκευση", command=save_payroll, font=("Arial", 12, "bold"), width=10)
    save_payroll_button.pack(pady=5)


def open_income_window():
    income_window = tk.Toplevel(window)
    income_window.configure(bg="#BFACC8")
    income_window.resizable(width=False, height=False)
    income_window.geometry("250x600")
    income_window.title("Εισόδημα")

    def save_income():
        income['Z'] = float(z_entry.get())
        income['Tziros'] = float(tziros_entry.get())
        income['Tziros Cash'] = float(tziros_cash_entry.get())
        income['Tziros Card'] = float(tziros_card_entry.get())
        income['Sitted'] = float(sitted_label_entry.get())
        income['Standing'] = float(standing_label_entry.get())
        income['Wolt'] = float(wolt_label_entry.get())
        income['Delivery'] = float(delivery_label_entry.get())
        income['Phone Delivery'] = float(phone_delivery_label_entry.get())
        income['Efood Delivery'] = float(efood_delivery_label_entry.get())
        income['Efood Paid'] = float(efood_paid_label_entry.get())
        income['Efood Cash'] = float(efood_cash_label_entry.get())

        z=float(z_entry.get())
        tziros = float(tziros_entry.get())
        tziros_cash = float(tziros_cash_entry.get())
        tziros_card = float(tziros_card_entry.get())
        sitted = float(sitted_label_entry.get())
        standing = float(standing_label_entry.get())
        wolt = float(wolt_label_entry.get())
        delivery = float(delivery_label_entry.get())
        phone_delivery = float(phone_delivery_label_entry.get())
        efood_delivery = float(efood_delivery_label_entry.get())
        efood_paid = float(efood_paid_label_entry.get())
        efood_cash = float(efood_cash_label_entry.get())

        sum_values = (tziros_cash+tziros_card+sitted+standing+wolt+delivery)
        sum_delivery = (phone_delivery+efood_delivery+efood_paid+efood_cash)
        sum_card = (wolt+efood_paid)
        efood_del = (efood_paid+efood_cash)

        if sum_values != tziros or sum_delivery != delivery:
            messagebox.showerror("Αποτυχία", "Παρουσιάστηκε κάποιο λάθος στις τιμές.")
            return 
        else:
            messagebox.showinfo("Tick", "Σωστές Τιμές")


        write_expenses_and_income(expenses, misthodosia, montly_expenses, income)
        income_window.destroy()
        messagebox.showinfo("Επιτυχία", "Το εισόδημα αποθηκέυτηκε με επιτυχία.")
        update_totals()

    z_label = tk.Label(income_window, text="Ζ:", font=("Arial", 12, "bold"), width=13)
    z_label.configure(bg="#BFACC8")
    z_label.pack()
    z_entry = tk.Entry(income_window)
    z_entry.insert(0, '0')
    z_entry.pack()

    tziros_label = tk.Label(income_window, text="Τζίρος:", font=("Arial", 12, "bold"), width=16)
    tziros_label.configure(bg="#BFACC8")
    tziros_label.pack()
    tziros_entry = tk.Entry(income_window)
    tziros_entry.insert(0, '0')
    tziros_entry.pack()

    tziros_cash_label = tk.Label(income_window, text="Τζίρος Μετρητά:", font=("Arial", 12, "bold"), width=16)
    tziros_cash_label.configure(bg="#BFACC8")
    tziros_cash_label.pack()
    tziros_cash_entry = tk.Entry(income_window)
    tziros_cash_entry.insert(0, '0')
    tziros_cash_entry.pack()

    tziros_card_label = tk.Label(income_window, text="Τζίρος Κάρτα:", font=("Arial", 12, "bold"), width=16)
    tziros_card_label.configure(bg="#BFACC8")
    tziros_card_label.pack()
    tziros_card_entry = tk.Entry(income_window)
    tziros_card_entry.insert(0, '0')
    tziros_card_entry.pack()

    sitted_label = tk.Label(income_window, text="Καθίμενοι:", font=("Arial", 12, "bold"), width=16)
    sitted_label.configure(bg="#BFACC8")
    sitted_label.pack()
    sitted_label_entry = tk.Entry(income_window)
    sitted_label_entry.insert(0, '0')
    sitted_label_entry.pack()

    standing_label = tk.Label(income_window, text="Όρθιοι:", font=("Arial", 12, "bold"), width=16)
    standing_label.configure(bg="#BFACC8")
    standing_label.pack()
    standing_label_entry = tk.Entry(income_window)
    standing_label_entry.insert(0, '0')
    standing_label_entry.pack()

    wolt_label = tk.Label(income_window, text="Wolt:", font=("Arial", 12, "bold"), width=16)
    wolt_label.configure(bg="#BFACC8")
    wolt_label.pack()
    wolt_label_entry = tk.Entry(income_window)
    wolt_label_entry.insert(0, '0')
    wolt_label_entry.pack()

    delivery_label = tk.Label(income_window, text="Delivery:", font=("Arial", 12, "bold"), width=16)
    delivery_label.configure(bg="#BFACC8")
    delivery_label.pack()
    delivery_label_entry = tk.Entry(income_window)
    delivery_label_entry.insert(0, '0')
    delivery_label_entry.pack()

    phone_delivery_label = tk.Label(income_window, text="Τηλεφωνικό Delivery:", font=("Arial", 12, "bold"), width=19)
    phone_delivery_label.configure(bg="#BFACC8")
    phone_delivery_label.pack()
    phone_delivery_label_entry = tk.Entry(income_window)
    phone_delivery_label_entry.insert(0, '0')
    phone_delivery_label_entry.pack()

    efood_delivery_label = tk.Label(income_window, text="Efood Delivery:", font=("Arial", 12, "bold"), width=16)
    efood_delivery_label.configure(bg="#BFACC8")
    efood_delivery_label.pack()
    efood_delivery_label_entry = tk.Entry(income_window)
    efood_delivery_label_entry.insert(0, '0')
    efood_delivery_label_entry.pack()

    efood_paid_label = tk.Label(income_window, text="Efood Πηρωμένα:", font=("Arial", 12, "bold"), width=16)
    efood_paid_label.configure(bg="#BFACC8")
    efood_paid_label.pack()
    efood_paid_label_entry = tk.Entry(income_window)
    efood_paid_label_entry.insert(0, '0')
    efood_paid_label_entry.pack()

    efood_cash_label = tk.Label(income_window, text="Efood Μετρητά:", font=("Arial", 12, "bold"), width=16)
    efood_cash_label.configure(bg="#BFACC8")
    efood_cash_label.pack()
    efood_cash_label_entry = tk.Entry(income_window)
    efood_cash_label_entry.insert(0, '0')
    efood_cash_label_entry.pack()

    save_income_button = tk.Button(income_window, text="Αποθήκευση", command=save_income, font=("Arial", 12, "bold"), width=13)
    save_income_button.pack(pady=5)

def update_totals():
    total_expenses = f"Συνολικά Έξοδα: ${sum(expenses.values())+sum(misthodosia.values())+sum(montly_expenses.values()):.2f}"
    total_income = f"Συνολικά Έσοδα: ${income['Tziros']:.2f}"
    totals_label.config(text=f"{total_expenses}\n{total_income}")

#pairnoume ta dates apo ta csv files gia ta combination
def get_existing_dates():
    csv_files = glob("*.csv")
    existing_dates = []
    for csv_file in csv_files:
        date_str = os.path.splitext(csv_file)[0]
        try:
            date = datetime.strptime(date_str, "%d-%m-%Y")
            existing_dates.append(date.strftime("%d-%m-%Y"))
        except ValueError:
            pass
    return existing_dates


#gia na epilegei o xristis range imerominiwn pou thelei combination
def open_date_range_window():
    date_range_window = Tk()
    date_range_window.title("Εύρος Ημερομηνιών")

    csv_dates = get_existing_dates()


    def generate_combined_csv():
        start_date = pd.to_datetime(start_date_entry.get(), format='%d-%m-%Y')
        end_date = pd.to_datetime(end_date_entry.get(), format='%d-%m-%Y')

        output = f'combined_{start_date.strftime("%d-%m-%Y")}_{end_date.strftime("%d-%m-%Y")}.csv'

        combined_data = {}

        # Read the start date CSV and populate the dictionary
        start_csv_path = f'{start_date.strftime("%d-%m-%Y")}.csv'
        start_df = pd.read_csv(start_csv_path, header=None, names=['Name', 'Value'])
        start_df = start_df.dropna(subset=['Name'])  # Exclude rows with NaN values in 'Name' column
        start_df = start_df[start_df['Name'].isin(['Expenses', 'Income'])]  # Filter rows by 'Expenses' and 'Income'
        combined_data = dict(start_df.values)

        # Iterate over the remaining CSV files within the date range
        for date in pd.date_range(start=start_date + pd.DateOffset(days=1), end=end_date):
            csv_path = f'{date.strftime("%d-%m-%Y")}.csv'
            df = pd.read_csv(csv_path, header=None, names=['Name', 'Value'])
            df['Value'] = pd.to_numeric(df['Value'])  # Convert 'Value' column to numeric
            df = df[df['Name'].isin(['Expenses', 'Income'])]  # Filter rows by 'Expenses' and 'Income'
            for index, row in df.iterrows():
                name = row['Name']
                value = row['Value']
                if name in combined_data:
                    combined_data[name] += value
                else:
                    combined_data[name] = value

        combined_df = pd.DataFrame(list(combined_data.items()), columns=['Name', 'Value'])
        combined_df.to_csv(output, index=False)
        send_email_combined(output)


    
    dates_label = Label(date_range_window, text="Υπάρχουσες Ημερομηνίες:")
    dates_label.pack()

    dates_table = ttk.Treeview(date_range_window, columns=("date"))
    dates_table.heading("#0", text="Date")
    dates_table.column("#0", width=100, anchor="center")
    dates_table.pack()

    for date in csv_dates:
        dates_table.insert("", "end", text=date)

    start_date_label = Label(date_range_window, text="Αρχική Ημερομηνία:")
    start_date_label.pack()
    start_date_entry = Entry(date_range_window)
    start_date_entry.pack()

    end_date_label = Label(date_range_window, text="Τελική Ημερομηνία:")
    end_date_label.pack()
    end_date_entry = Entry(date_range_window)
    end_date_entry.pack()

    generate_button = Button(date_range_window, text="Δημιουργία CSV", command=generate_combined_csv)
    generate_button.pack()

    # Adjust window size based on the number of dates
    num_dates = len(csv_dates)
    window_height = 300 + (num_dates * 20)  # Adjust the height based on the number of dates
    window_width = 300

    date_range_window.geometry(f"{window_width}x{window_height}")




# Create the GUI window
window = tk.Tk()
#window.configure(bg="#A1CDF4")
window.resizable(width=False, height=False)
window.geometry("400x400")
window.title("Έξοδα Μαγαζιού")

backround_image=tk.PhotoImage(file="gradient.png")
backround_label=tk.Label(window, image=backround_image)
backround_label.place(x=0, y=0, relheight=1, relwidth=1)

# Create buttons for expenses, income, save, and send data
expenses_button = tk.Button(window, text="Προμηθευτές", command=open_expenses_window, font=("Arial", 12, "bold"), width=13)
expenses_button.pack(pady=5)

payroll_button=tk.Button(window, text="Μισθοδοσία", command=open_payroll_window, font=("Arial", 12, "bold"), width=13)
payroll_button.pack(pady=5)

montly_expenses_button=tk.Button(window, text="Έξοδα Μήνα", command=open_montly_expenses_window, font=("Arial", 12, "bold"), width=13)
montly_expenses_button.pack(pady=5)

income_button = tk.Button(window, text="Εισόδημα", command=open_income_window, font=("Arial", 12, "bold"), width=13)
income_button.pack(pady=5)

combined_button=tk.Button(window, text="Αρχεία Εύρους", command=open_date_range_window, font=("Arial", 12, "bold"), width=13)
combined_button.pack(pady=5)

save_button = tk.Button(window, text="Αποθήκευση", command=save_data, font=("Arial", 12, "bold"), width=13)
save_button.pack(pady=5)

send_button = tk.Button(window, text="Αποστολή", command=send_email, font=("Arial", 12, "bold"), width=13)
send_button.pack(pady=5)
# Create a label to display the totals
totals_label = tk.Label(window, text="Συνολικά Έξοδα: €0.00\nΣυνολικά Έσοδα: €0.00", font=("Arial", 12, "bold"))
totals_label.configure(bg="#BFACC8")
totals_label.pack(pady=20)

rights_label=tk.Label(window, text="By Georgios Mermigkis", font=("Arial", 7, "bold"))
rights_label.pack()

window.mainloop()
