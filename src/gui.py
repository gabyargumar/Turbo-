import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from PIL import Image, ImageTk
from calculations import generate_amortization_schedule
from pdf_utils import generate_pdf

def calculate_loan():
    try:
        principal = float(principal_entry.get())
        months = int(term_entry.get())
        schedule = generate_amortization_schedule(principal, 0.14, months)  # Assuming annual rate is 0.14

        # Create a formatted string for the result
        result_text = ""
        for i, payment in enumerate(schedule, start=1):
            result_text += (f"Pago {i}:\n"
                            f"Interes y Servicio: ${payment['Interes y Servicio']}\n"
                            f"Abono a Capital: ${payment['Abono a Capital']}\n"
                            f"Total Cancelar: ${payment['Total Cancelar']}\n"
                            f"Capital Restante: ${payment['Capital Restante']}\n\n")
        
        # Update the scrollable text area
        result_text_area.config(state=tk.NORMAL)
        result_text_area.delete(1.0, tk.END)
        result_text_area.insert(tk.END, result_text.strip())
        result_text_area.config(state=tk.DISABLED)

        # Save schedule to instance variable for later use
        global current_schedule
        current_schedule = schedule
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def save_to_csv():
    with open('clients_loans.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([client_name_entry.get(), principal_entry.get(), term_entry.get()])
    messagebox.showinfo("Saved", "Data has been saved to clients_loans.csv.")

def save_to_pdf():
    if 'current_schedule' in globals():
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            generate_pdf(
                filename,
                current_schedule,
                client_name_entry.get(),
                float(principal_entry.get()),
                int(term_entry.get()),
                logo_path="turbo.png",  # Adjust if your logo path is different
                template_path="template.pdf"  # Path to your PDF template
            )
            messagebox.showinfo("Guardado", f"El PDF ha sido guardado como {filename}.")
    else:
        messagebox.showwarning("Sin Datos", "Por favor, calcule el préstamo primero.")

# Initialize Tkinter root
root = tk.Tk()
root.title("Loan Calculator")
root.geometry("800x600")  # Set the default size of the window

# Load and display logo
logo_image = Image.open("src/turbo.png")
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo)
logo_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Create a canvas for scrolling
canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)
canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
scroll_y.grid(row=1, column=3, sticky="ns")

# Create a frame to hold the widgets
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Update scroll region when the frame size changes
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Input Fields
tk.Label(frame, text="Nombre Cliente").grid(row=0, column=0, padx=10, pady=10, sticky="e")
client_name_entry = tk.Entry(frame)
client_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

tk.Label(frame, text="Monto de Credito").grid(row=1, column=0, padx=10, pady=10, sticky="e")
principal_entry = tk.Entry(frame)
principal_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Label(frame, text="Plazo de Pagos").grid(row=2, column=0, padx=10, pady=10, sticky="e")
term_entry = tk.Entry(frame)
term_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Buttons
calculate_button = tk.Button(frame, text="Calcular", command=calculate_loan)
calculate_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

save_csv_button = tk.Button(frame, text="Guardar a CSV", command=save_to_csv)
save_csv_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

save_pdf_button = tk.Button(frame, text="Exportar a PDF", command=save_to_pdf)
save_pdf_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

# Result Text Area
result_text_area = tk.Text(frame, wrap="word", height=15, width=60)
result_text_area.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
result_text_area.config(state=tk.DISABLED)

# Adjust grid weights to make canvas and scrollbar responsive
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=0)

frame.grid_rowconfigure(4, weight=1)  # Make the result area expand

root.mainloop()
