import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Dropdown tagTypes
tagTypes = [
    "Select one", "Biotech/Medical", "Chemistry", "Diagnostics & Drug Delivery", "Education", 
    "Electronics & Instrumentation", "Energy / Environment / Resources", 
    "Engineered Structures & Materials", "Engineering", "Food / Agriculture", 
    "Life Sciences", "Microfluidics", "Mechanical Devices & Processes", 
    "Pharmaceuticals / Nutraceuticals", "Physics", "Software"
]

# Dictionary to hold user selections
tagTypeSelections = {}

def get_user_selections(pdf_folder):
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    pdf_prefixes = [f[:8] for f in pdf_files]

    def get_dropdown_selection(index, prefix):
        def submit():
            tagTypeSelections[prefix] = selection_var.get()
            root.destroy()

        root = tk.Tk()
        root.title(f"Select Tag Type for {prefix}")
        root.geometry("400x150+600+300")  # fixed size and position

        selection_var = tk.StringVar(value=tagTypes[0])

        ttk.Label(root, text=f"Tag Type for PDF: {prefix}").pack(pady=10)
        ttk.OptionMenu(root, selection_var, *tagTypes).pack()
        ttk.Button(root, text="Submit", command=submit).pack(pady=10)

        root.mainloop()

    for i, prefix in enumerate(pdf_prefixes):
        get_dropdown_selection(i, prefix)

    return tagTypeSelections


def confirm_images_uploaded():
    """
    Pops up a Yes/No dialog to ask if the user has uploaded all images.
    Exits the program if the user selects 'No'.
    """
    root = tk.Tk()
    root.withdraw()  # Hide main window
    confirmed = messagebox.askyesno("Image Upload Check", f"Have you uploaded all the images to the correct folder in the correct format? \nex:'2025-001 image'")

    if not confirmed:
        messagebox.showinfo("Reminder", "Please upload the images properly before continuing.")
        root.destroy()
        exit()  # Exits the entire script

    root.destroy()
