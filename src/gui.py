import tkinter as tk
from tkinter import messagebox
import csv
from calculations import perform_calculation

def calculate_loan():
    principal = principal_entry.get()
    months = term_entry.get()
    result = perform_calculation(principal, months)
    result_label.config(text=result)

def save_to_csv():
    with open('clients_loans.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([client_name_entry.get(), principal_entry.get(), term_entry.get()])
    messagebox.showinfo("Saved", "Data has been saved to clients_loans.csv.")

root = tk.Tk()
root.title("Loan Calculator")

# Input Fields
tk.Label(root, text="Client Name").grid(row=0, column=0)
client_name_entry = tk.Entry(root)
client_name_entry.grid(row=0, column=1)

tk.Label(root, text="Principal").grid(row=1, column=0)
principal_entry = tk.Entry(root)
principal_entry.grid(row=1, column=1)

tk.Label(root, text="Term (Months)").grid(row=2, column=0)
term_entry = tk.Entry(root)
term_entry.grid(row=2, column=1)

# Buttons
calculate_button = tk.Button(root, text="Calculate", command=calculate_loan)
calculate_button.grid(row=3, column=0)

save_button = tk.Button(root, text="Save", command=save_to_csv)
save_button.grid(row=3, column=1)

# Result Label
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
