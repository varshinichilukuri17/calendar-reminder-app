import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("reminders.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    task TEXT
)
""")
conn.commit()

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Calendar Reminder App")
root.geometry("650x550")
root.config(bg="white")

# ---------------- TITLE ----------------
title = tk.Label(root, text="Calendar Reminder App",
                 font=("Arial", 18, "bold"), bg="white")
title.pack(pady=10)

# ---------------- CALENDAR ----------------
cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.pack(pady=10)

# ---------------- LISTBOX ----------------
listbox = tk.Listbox(root, width=70, height=12, font=("Arial", 11))
listbox.pack(pady=15)

# ---------------- LOAD DATA ----------------
def load_reminders():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT id, date, task FROM reminders")
    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(tk.END, f"{row[0]} | {row[1]} - {row[2]}")

# ---------------- ADD ----------------
def add_reminder():
    date = cal.get_date()

    task = simpledialog.askstring("Reminder", "Enter reminder:")

    if task:
        cursor.execute(
            "INSERT INTO reminders (date, task) VALUES (?, ?)",
            (date, task)
        )
        conn.commit()
        load_reminders()
        messagebox.showinfo("Success", "Reminder Added!")

# ---------------- DELETE ----------------
def delete_reminder():
    selected = listbox.curselection()

    if selected:
        item = listbox.get(selected[0])
        reminder_id = item.split("|")[0].strip()

        cursor.execute(
            "DELETE FROM reminders WHERE id=?",
            (reminder_id,)
        )
        conn.commit()
        load_reminders()

    else:
        messagebox.showwarning("Warning", "Select reminder first")

# ---------------- BUTTONS ----------------
frame = tk.Frame(root, bg="white")
frame.pack()

add_btn = tk.Button(frame, text="Add Reminder",
                    width=18, bg="lightblue",
                    command=add_reminder)
add_btn.grid(row=0, column=0, padx=10)

delete_btn = tk.Button(frame, text="Delete Reminder",
                       width=18, bg="lightcoral",
                       command=delete_reminder)
delete_btn.grid(row=0, column=1, padx=10)

# Load Existing Data
load_reminders()

# Run App
root.mainloop()

# Close DB
conn.close()