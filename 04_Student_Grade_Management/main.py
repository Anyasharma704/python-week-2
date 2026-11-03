import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.json")

def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_students():
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)

def calculate_average(marks):
    return sum(marks) / len(marks) if marks else 0

def grade_for(average):
    if average >= 90: return "A+"
    if average >= 80: return "A"
    if average >= 70: return "B"
    if average >= 60: return "C"
    if average >= 50: return "D"
    return "F"

def refresh_table(query=""):
    for item in table.get_children():
        table.delete(item)
    for student in sorted(students, key=lambda s: s["name"].lower()):
        if query.lower() in (student["roll"] + " " + student["name"]).lower():
            avg = calculate_average(student["marks"])
            table.insert("", "end", values=(student["roll"], student["name"],
                                            ", ".join(map(str, student["marks"])),
                                            f"{avg:.2f}", grade_for(avg)))

def clear_fields():
    for field in (roll_entry, name_entry, marks_entry):
        field.delete(0, tk.END)

def read_form():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    raw_marks = marks_entry.get().strip()
    if not roll or not name or not raw_marks:
        raise ValueError("Roll number, name, and marks are required.")
    try:
        marks = [float(x.strip()) for x in raw_marks.split(",")]
    except ValueError:
        raise ValueError("Enter marks as comma-separated numbers, e.g. 78, 85, 91.")
    if not marks or any(mark < 0 or mark > 100 for mark in marks):
        raise ValueError("Each mark must be between 0 and 100.")
    return roll, name, marks

def add_student():
    try:
        roll, name, marks = read_form()
    except ValueError as error:
        messagebox.showwarning("Invalid input", str(error))
        return
    if any(s["roll"] == roll for s in students):
        messagebox.showwarning("Duplicate roll number", "This roll number already exists.")
        return
    students.append({"roll": roll, "name": name, "marks": marks})
    save_students()
    refresh_table(search_entry.get())
    clear_fields()

def selected_index():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Select student", "Select a student from the table first.")
        return None
    roll = table.item(selected[0], "values")[0]
    return next((i for i, s in enumerate(students) if s["roll"] == roll), None)

def fill_form(_event=None):
    idx = selected_index()
    if idx is None: return
    student = students[idx]
    clear_fields()
    roll_entry.insert(0, student["roll"])
    name_entry.insert(0, student["name"])
    marks_entry.insert(0, ", ".join(map(str, student["marks"])))

def update_student():
    idx = selected_index()
    if idx is None: return
    try:
        roll, name, marks = read_form()
    except ValueError as error:
        messagebox.showwarning("Invalid input", str(error))
        return
    if any(i != idx and s["roll"] == roll for i, s in enumerate(students)):
        messagebox.showwarning("Duplicate roll number", "This roll number already exists.")
        return
    students[idx] = {"roll": roll, "name": name, "marks": marks}
    save_students()
    refresh_table(search_entry.get())
    clear_fields()

def delete_student():
    idx = selected_index()
    if idx is None: return
    if messagebox.askyesno("Confirm", "Delete this student record?"):
        students.pop(idx)
        save_students()
        refresh_table(search_entry.get())
        clear_fields()

root = tk.Tk()
root.title("Student Grade Management System")
root.geometry("950x620")
root.configure(bg="#f4f0ff")
students = load_students()

tk.Label(root, text="Student Grade Management", font=("Arial", 22, "bold"),
         bg="#f4f0ff", fg="#51427c").pack(pady=12)
form = tk.Frame(root, bg="#f4f0ff")
form.pack(pady=8)
for row, (label, width) in enumerate((("Roll Number", 25), ("Student Name", 35),
                                      ("Marks (comma-separated)", 45))):
    tk.Label(form, text=label, bg="#f4f0ff", width=23, anchor="w").grid(row=row, column=0, padx=5, pady=6)
    entry = tk.Entry(form, width=width)
    entry.grid(row=row, column=1, padx=5, pady=6)
    if row == 0: roll_entry = entry
    elif row == 1: name_entry = entry
    else: marks_entry = entry

buttons = tk.Frame(root, bg="#f4f0ff")
buttons.pack(pady=8)
for label, command in (("Add Student", add_student), ("Update Selected", update_student),
                       ("Delete Selected", delete_student), ("Clear", clear_fields)):
    tk.Button(buttons, text=label, command=command, bg="#8875c7", fg="white",
              padx=12, pady=6).pack(side="left", padx=5)

search_frame = tk.Frame(root, bg="#f4f0ff")
search_frame.pack(pady=8)
tk.Label(search_frame, text="Search by roll/name:", bg="#f4f0ff").pack(side="left")
search_entry = tk.Entry(search_frame, width=35)
search_entry.pack(side="left", padx=6)
search_entry.bind("<KeyRelease>", lambda _e: refresh_table(search_entry.get()))

columns = ("roll", "name", "marks", "average", "grade")
table = ttk.Treeview(root, columns=columns, show="headings", height=13)
for col, width in zip(columns, (120, 200, 250, 120, 100)):
    table.heading(col, text=col.title())
    table.column(col, width=width)
table.pack(padx=15, pady=12, fill="both", expand=True)
table.bind("<<TreeviewSelect>>", fill_form)
refresh_table()
root.mainloop()
