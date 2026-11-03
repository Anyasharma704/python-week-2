import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("contacts.json")

def load_contacts():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_contacts():
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

def refresh_table(query=""):
    for item in table.get_children():
        table.delete(item)
    for contact in sorted(contacts, key=lambda c: c["name"].lower()):
        searchable = " ".join(contact.values()).lower()
        if query.lower() in searchable:
            table.insert("", "end", values=(contact["name"], contact["phone"],
                                            contact["email"], contact["address"]))

def clear_fields():
    for field in (name_entry, phone_entry, email_entry, address_entry):
        field.delete(0, tk.END)

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()
    if not name or not phone:
        messagebox.showwarning("Missing information", "Name and phone number are required.")
        return
    if not phone.isdigit() or not 7 <= len(phone) <= 15:
        messagebox.showwarning("Invalid phone", "Enter a phone number containing 7–15 digits.")
        return
    if email and ("@" not in email or "." not in email.split("@")[-1]):
        messagebox.showwarning("Invalid email", "Enter a valid-looking email address.")
        return
    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts()
    refresh_table(search_entry.get())
    clear_fields()
    messagebox.showinfo("Saved", "Contact added successfully.")

def selected_index():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Select contact", "Select a contact from the table first.")
        return None
    values = table.item(selected[0], "values")
    for i, contact in enumerate(contacts):
        if (contact["name"], contact["phone"], contact["email"], contact["address"]) == tuple(values):
            return i
    return None

def fill_from_selection(_event=None):
    idx = selected_index()
    if idx is None:
        return
    contact = contacts[idx]
    clear_fields()
    for field, key in zip((name_entry, phone_entry, email_entry, address_entry),
                          ("name", "phone", "email", "address")):
        field.insert(0, contact[key])

def update_contact():
    idx = selected_index()
    if idx is None:
        return
    name, phone, email, address = (field.get().strip() for field in
                                   (name_entry, phone_entry, email_entry, address_entry))
    if not name or not phone or not phone.isdigit() or not 7 <= len(phone) <= 15:
        messagebox.showwarning("Invalid information", "A name and valid 7–15 digit phone are required.")
        return
    if email and ("@" not in email or "." not in email.split("@")[-1]):
        messagebox.showwarning("Invalid email", "Enter a valid-looking email address.")
        return
    contacts[idx] = {"name": name, "phone": phone, "email": email, "address": address}
    save_contacts()
    refresh_table(search_entry.get())
    clear_fields()
    messagebox.showinfo("Updated", "Contact updated.")

def delete_contact():
    idx = selected_index()
    if idx is None:
        return
    if messagebox.askyesno("Confirm deletion", "Delete this contact?"):
        contacts.pop(idx)
        save_contacts()
        refresh_table(search_entry.get())
        clear_fields()

root = tk.Tk()
root.title("Contact Book")
root.geometry("900x600")
root.configure(bg="#f4f0ff")
contacts = load_contacts()

tk.Label(root, text="Contact Book", font=("Arial", 23, "bold"),
         bg="#f4f0ff", fg="#51427c").pack(pady=12)
form = tk.Frame(root, bg="#f4f0ff")
form.pack(pady=5)
labels = ["Name *", "Phone *", "Email", "Address"]
entries = []
for row, label in enumerate(labels):
    tk.Label(form, text=label, bg="#f4f0ff", width=12, anchor="w").grid(row=row, column=0, padx=5, pady=5)
    entry = tk.Entry(form, width=42)
    entry.grid(row=row, column=1, padx=5, pady=5)
    entries.append(entry)
name_entry, phone_entry, email_entry, address_entry = entries

buttons = tk.Frame(root, bg="#f4f0ff")
buttons.pack(pady=8)
for label, command in (("Add Contact", add_contact), ("Update Selected", update_contact),
                       ("Delete Selected", delete_contact), ("Clear", clear_fields)):
    tk.Button(buttons, text=label, command=command, bg="#8875c7", fg="white",
              padx=10, pady=5).pack(side="left", padx=5)

search_frame = tk.Frame(root, bg="#f4f0ff")
search_frame.pack(pady=8)
tk.Label(search_frame, text="Search:", bg="#f4f0ff").pack(side="left")
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side="left", padx=6)
search_entry.bind("<KeyRelease>", lambda _e: refresh_table(search_entry.get()))

columns = ("name", "phone", "email", "address")
table = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col, width in zip(columns, (180, 130, 200, 300)):
    table.heading(col, text=col.title())
    table.column(col, width=width)
table.pack(padx=15, pady=10, fill="both", expand=True)
table.bind("<<TreeviewSelect>>", fill_from_selection)
refresh_table()
root.mainloop()
