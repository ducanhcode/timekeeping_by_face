import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import StringVar
from pymongo import MongoClient
import datetime

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["leave_requests"]
collection = db["requests"]

def submit_data():
    name = name_var.get()
    leave_type = leave_type_var.get()
    date = date_var.get()
    reason = reason_text.get("1.0", "end").strip()

    if not name or not leave_type or not date or not reason:
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
        return

    # Kiểm tra và chuyển đổi ngày sang kiểu datetime
    try:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Lỗi", "Ngày không hợp lệ! Định dạng: YYYY-MM-DD")
        return

    data = {
        "name": name,
        "leave_type": leave_type,
        "date": parsed_date,  # Lưu dưới dạng datetime
        "reason": reason
    }
    collection.insert_one(data)
    messagebox.showinfo("Thành công", "Đã gửi thông tin nghỉ phép!")
    clear_fields()


# Clear all fields
def clear_fields():
    name_var.set("")
    leave_type_var.set("")
    date_var.set("")
    reason_text.delete("1.0", "end")

# Create GUI
app = tk.Tk()
app.title("Đăng ký nghỉ phép")
app.geometry("400x400")

# Name
tk.Label(app, text="Họ Tên").pack(pady=5)
name_var = StringVar()
tk.Entry(app, textvariable=name_var).pack(pady=5)

# Leave Type
tk.Label(app, text="Loại").pack(pady=5)
leave_type_var = StringVar()
leave_type_combobox = ttk.Combobox(app, textvariable=leave_type_var)
leave_type_combobox['values'] = ("Nghỉ phép", "Đi trễ", "Về sớm")
leave_type_combobox.pack(pady=5)

# Date
tk.Label(app, text="Ngày (YYYY-MM-DD)").pack(pady=5)
date_var = StringVar()
tk.Entry(app, textvariable=date_var).pack(pady=5)

# Reason
tk.Label(app, text="Lý do").pack(pady=5)
reason_text = tk.Text(app, height=5, width=40)
reason_text.pack(pady=5)

# Submit Button
tk.Button(app, text="Gửi", command=submit_data).pack(pady=10)

app.mainloop()
