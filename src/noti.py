import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["leave_requests"]
collection = db["requests"]

# Fetch and display data
def fetch_data(date=None):
    # Use the provided date or default to today's date
    if not date:
        date = date_var.get()

    # Validate and convert the date
    try:
        query_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Lỗi", "Ngày không hợp lệ! Định dạng: YYYY-MM-DD")
        return

    # Define the start and end of the day
    start_of_day = datetime(query_date.year, query_date.month, query_date.day)
    end_of_day = start_of_day + timedelta(days=1)

    # Fetch records from MongoDB based on the date range
    records = list(collection.find({"date": {"$gte": start_of_day, "$lt": end_of_day}}))
    results.delete(*results.get_children())  # Clear the table

    if not records:
        messagebox.showinfo("Kết quả", f"Không có dữ liệu nào cho ngày {date}!")
        return

    # Display records in the table
    for record in records:
        results.insert("", "end", values=(record["name"], record["leave_type"], record["reason"]))

# Create GUI
app = tk.Tk()
app.title("Xem danh sách xin phép")
app.geometry("600x400")

# Date
tk.Label(app, text="Ngày (YYYY-MM-DD)").pack(pady=5)
date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))  # Default to today's date
tk.Entry(app, textvariable=date_var).pack(pady=5)

# Fetch Button
tk.Button(app, text="Xem", command=lambda: fetch_data(date_var.get())).pack(pady=10)

# Results Table
columns = ("name", "leave_type", "reason")
results = ttk.Treeview(app, columns=columns, show="headings")
results.heading("name", text="Họ Tên")
results.heading("leave_type", text="Loại")
results.heading("reason", text="Lý do")
results.pack(fill=tk.BOTH, expand=True, pady=10)

# Automatically display today's data
fetch_data(datetime.now().strftime("%Y-%m-%d"))

app.mainloop()
