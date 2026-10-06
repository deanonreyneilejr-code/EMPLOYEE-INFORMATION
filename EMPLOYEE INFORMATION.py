import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# DATABASE

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    position TEXT NOT NULL
)
""")

conn.commit()



# MAIN WINDOW

window = tk.Tk()
window.title("Employee Profile")
window.geometry("650x500")
window.resizable(False, False)



# COLORS

BG_COLOR = "#87CEEB"       # Sky Blue
TITLE_COLOR = "#154360"
BUTTON_COLOR = "#3498DB"
TEXT_COLOR = "#FFFFFF"

window.configure(bg=BG_COLOR)


# VARIABLES

name_var = tk.StringVar()
age_var = tk.StringVar()
position_var = tk.StringVar()



# FUNCTIONS


def clear_fields():
    """Clear all input fields and remove table selection."""

    name_var.set("")
    age_var.set("")
    position_var.set("")

    selected = employee_table.selection()

    if selected:
        employee_table.selection_remove(selected)


def display_employees():
    """Display all employees from the database."""

    # Clear current table
    for item in employee_table.get_children():
        employee_table.delete(item)

    # Get employees from database
    cursor.execute("""
        SELECT id, name, age, position
        FROM employees
        ORDER BY id
    """)

    employees = cursor.fetchall()

    # Add employees to table
    for employee in employees:
        employee_table.insert(
            "",
            tk.END,
            values=employee
        )


def add_employee():
    """Add a new employee to the database."""

    name = name_var.get().strip()
    age = age_var.get().strip()
    position = position_var.get().strip()

    # Check empty fields
    if name == "" or age == "" or position == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    # Check age
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    # Insert employee into database
    cursor.execute("""
        INSERT INTO employees (name, age, position)
        VALUES (?, ?, ?)
    """, (name, age, position))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Employee added successfully!"
    )

    clear_fields()
    display_employees()


def select_employee(event):
    """Load selected employee information into the input fields."""

    selected = employee_table.selection()

    if selected:
        item = employee_table.item(selected[0])
        values = item["values"]

        # Values:
        # 0 = ID
        # 1 = Name
        # 2 = Age
        # 3 = Position

        name_var.set(values[1])
        age_var.set(values[2])
        position_var.set(values[3])


def update_employee():
    """Update the selected employee in the database."""

    selected = employee_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an employee to update."
        )
        return

    # Get employee ID from table
    item = employee_table.item(selected[0])
    employee_id = item["values"][0]

    name = name_var.get().strip()
    age = age_var.get().strip()
    position = position_var.get().strip()

    # Check empty fields
    if name == "" or age == "" or position == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    # Check age
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    # Update employee in database
    cursor.execute("""
        UPDATE employees
        SET name = ?, age = ?, position = ?
        WHERE id = ?
    """, (name, age, position, employee_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Employee updated successfully!"
    )

    clear_fields()
    display_employees()


def delete_employee():
    """Delete the selected employee from the database."""

    selected = employee_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an employee to delete."
        )
        return

    # Get employee ID
    item = employee_table.item(selected[0])
    employee_id = item["values"][0]

    # Confirmation
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this employee?"
    )

    if confirm:

        # Delete from database
        cursor.execute(
            "DELETE FROM employees WHERE id = ?",
            (employee_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Employee deleted successfully!"
        )

        clear_fields()
        display_employees()


def exit_program():
    """Close database connection and exit the program."""

    confirm = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if confirm:
        conn.close()
        window.destroy()



# TITLE


title_label = tk.Label(
    window,
    text="Employee Profile",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack(pady=15)



# INPUT FRAME

input_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

input_frame.pack(pady=5)



# EMPLOYEE NAME

tk.Label(
    input_frame,
    text="Employee Name:",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=TITLE_COLOR
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

name_entry = tk.Entry(
    input_frame,
    textvariable=name_var,
    width=35
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)



# AGE

tk.Label(
    input_frame,
    text="Age:",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=TITLE_COLOR
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

age_entry = tk.Entry(
    input_frame,
    textvariable=age_var,
    width=35
)

age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)



# POSITION

tk.Label(
    input_frame,
    text="Position:",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=TITLE_COLOR
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

position_entry = tk.Entry(
    input_frame,
    textvariable=position_var,
    width=35
)

position_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# BUTTON FRAME

button_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

button_frame.pack(pady=10)


# ADD BUTTON

add_button = tk.Button(
    button_frame,
    text="Add",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    command=add_employee
)

add_button.grid(
    row=0,
    column=0,
    padx=5
)


# UPDATE BUTTON

update_button = tk.Button(
    button_frame,
    text="Update",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    command=update_employee
)

update_button.grid(
    row=0,
    column=1,
    padx=5
)


# DELETE BUTTON

delete_button = tk.Button(
    button_frame,
    text="Delete",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    command=delete_employee
)

delete_button.grid(
    row=0,
    column=2,
    padx=5
)


# CLEAR BUTTON

clear_button = tk.Button(
    button_frame,
    text="Clear",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    command=clear_fields
)

clear_button.grid(
    row=0,
    column=3,
    padx=5
)


# EXIT BUTTON

exit_button = tk.Button(
    button_frame,
    text="Exit",
    width=10,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    command=exit_program
)

exit_button.grid(
    row=0,
    column=4,
    padx=5
)



# EMPLOYEE INFORMATION

info_label = tk.Label(
    window,
    text="Employee Information",
    font=("Arial", 14, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

info_label.pack(pady=(10, 5))



# EMPLOYEE TABLE

table_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

table_frame.pack(pady=5)


employee_table = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Age", "Position"),
    show="headings",
    height=8
)



# TABLE HEADINGS

employee_table.heading(
    "ID",
    text="ID"
)

employee_table.heading(
    "Name",
    text="Name"
)

employee_table.heading(
    "Age",
    text="Age"
)

employee_table.heading(
    "Position",
    text="Position"
)


# TABLE COLUMNS

employee_table.column(
    "ID",
    width=50,
    anchor="center"
)

employee_table.column(
    "Name",
    width=180
)

employee_table.column(
    "Age",
    width=70,
    anchor="center"
)

employee_table.column(
    "Position",
    width=180
)


employee_table.pack()



# EVENT HANDLING

employee_table.bind(
    "<<TreeviewSelect>>",
    select_employee
)



# DISPLAY DATABASE RECORDS

display_employees()



# RUN APPLICATION

window.mainloop()
