import customtkinter as ctk
from tkinter import filedialog, messagebox
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
                            f"Interes y Servicio: Q{payment['Interes y Servicio']}\n"
                            f"Abono a Capital: Q{payment['Abono a Capital']}\n"
                            f"Total Cancelar: Q{payment['Total Cancelar']}\n"
                            f"Capital Restante: Q{payment['Capital Restante']}\n\n")
        
        # Update the scrollable text area
        result_text_area.configure(state=ctk.NORMAL)
        result_text_area.delete(1.0, ctk.END)
        result_text_area.insert(ctk.END, result_text.strip())
        result_text_area.configure(state=ctk.DISABLED)

        # Save schedule to instance variable for later use
        global current_schedule
        current_schedule = schedule
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

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
                logo_path="src/turbo.png",  # Adjust if your logo path is different
                template_path="src/template.pdf"  # Path to your PDF template
            )
            messagebox.showinfo("Guardado", f"El PDF ha sido guardado como {filename}.")
    else:
        messagebox.showwarning("Sin Datos", "Por favor, calcule el préstamo primero.")

# Initialize Tkinter root
root = ctk.CTk()
root.title("Calculadora de Prestamos")
root.geometry("800x600")  # Set the default size of the window
ctk.set_appearance_mode("light")

# Load and display logo
logo_image = Image.open("src/turbo.png")
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = ctk.CTkLabel(root, image=logo_photo)
logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Create a frame to hold the widgets
frame = ctk.CTkFrame(root)
frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Input Fields
ctk.CTkLabel(frame, text="Nombre Cliente").grid(row=0, column=0, padx=10, pady=10, sticky="e")
client_name_entry = ctk.CTkEntry(frame)
client_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

ctk.CTkLabel(frame, text="Monto de Credito").grid(row=1, column=0, padx=10, pady=10, sticky="e")
principal_entry = ctk.CTkEntry(frame)
principal_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

ctk.CTkLabel(frame, text="Plazo de Pagos").grid(row=2, column=0, padx=10, pady=10, sticky="e")
term_entry = ctk.CTkEntry(frame)
term_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Buttons
calculate_button = ctk.CTkButton(frame, text="Calcular", command=calculate_loan)
calculate_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

save_pdf_button = ctk.CTkButton(frame, text="Exportar a PDF", command=save_to_pdf)
save_pdf_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Result Text Area
result_text_area = ctk.CTkTextbox(frame, wrap="word")
result_text_area.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
result_text_area.configure(state=ctk.DISABLED)  # Use configure instead of config

# Adjust grid weights to make the frame responsive
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

frame.grid_rowconfigure(4, weight=1)  # Make the result area expand
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

root.mainloop()
