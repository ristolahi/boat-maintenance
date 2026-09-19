import json
import tkinter as tk
from datetime import date

with open("tasks.json") as f:
    tasks = json.load(f)
    tasks.sort(key=lambda t: t["due"])

BG = "#eaf4fb"
ACCENT = "#013a63"
today = date.today().isoformat()

root = tk.Tk()
root.title("Boat Maintenance")
root.geometry("440x560")
root.configure(bg=BG)

title = tk.Label(root, text="⛵ Boat Maintenance", font=("Segoe UI", 18, "bold"), bg=BG, fg=ACCENT)
title.pack(pady=(15, 5))

progress_canvas = tk.Canvas(root, width=380, height=22, bg="white", highlightthickness=1, highlightbackground=ACCENT)
progress_canvas.pack(pady=(0, 15))
progress_bar = progress_canvas.create_rectangle(0, 0, 0, 22, fill="#2a9d8f", width=0)
progress_text = progress_canvas.create_text(190, 11, text="", font=("Segoe UI", 9, "bold"))

def update_progress():
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    width = int((done / total) * 380) if total else 0
    progress_canvas.coords(progress_bar, 0, 0, width, 22)
    progress_canvas.itemconfig(progress_text, text=f"{done} of {total} tasks done")

check_vars = []
task_frame = tk.Frame(root, bg=BG)
task_frame.pack(pady=5, fill="x", padx=15)

def save():
    for task, var in zip(tasks, check_vars):
        task["done"] = var.get()
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)
    update_progress()
    print("Saved!")

def add_checkbox(task):
    var = tk.BooleanVar(value=task["done"])

    row = tk.Frame(task_frame, bg=BG)
    row.pack(anchor="w", fill="x", pady=3)

    overdue = (not task["done"]) and task["due"] < today
    text_color = "#c1121f" if overdue else "black"
    prefix = "⚠️ " if overdue else ""
    text = f"{prefix}{task['due']} - {task['name']}"

    checkbox = tk.Checkbutton(row, text=text, variable=var, font=("Segoe UI", 12), bg=BG,
                               activebackground=BG, fg=text_color, selectcolor="white", command=save)
    checkbox.pack(side="left")

    def delete_task():
        tasks.remove(task)
        check_vars.remove(var)
        row.destroy()
        save()

    delete_button = tk.Button(row, text="✕", fg="white", bg="#c1121f", font=("Segoe UI", 9, "bold"),
                               relief="flat", command=delete_task)
    delete_button.pack(side="right")

    check_vars.append(var)

def refresh_list():
    for widget in task_frame.winfo_children():
        widget.destroy()
    check_vars.clear()
    for task in tasks:
        add_checkbox(task)
    update_progress()

refresh_list()

def add_task():
    name = name_entry.get()
    due = due_entry.get()
    if name and due:
        new_task = {"name": name, "due": due, "done": False}
        tasks.append(new_task)
        tasks.sort(key=lambda t: t["due"])
        refresh_list()
        save()
        name_entry.delete(0, tk.END)
        due_entry.delete(0, tk.END)

entry_frame = tk.Frame(root, bg=BG)
entry_frame.pack(pady=15)

tk.Label(entry_frame, text="Task:", bg=BG, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=4)
name_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), width=25)
name_entry.grid(row=0, column=1, pady=4)

tk.Label(entry_frame, text="Due (YYYY-MM-DD):", bg=BG, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=4)
due_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), width=25)
due_entry.grid(row=1, column=1, pady=4)

tk.Button(entry_frame, text="+ Add Task", bg="#2a9d8f", fg="white", font=("Segoe UI", 10, "bold"),
          relief="flat", command=add_task).grid(row=2, column=0, columnspan=2, pady=8, ipadx=10, ipady=4)

root.mainloop()