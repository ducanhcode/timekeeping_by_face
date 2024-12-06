import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pymongo
import gridfs
import cv2
import numpy as np
from datetime import datetime, timedelta

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Xem Hình Ảnh Theo Ngày")
        self.root.geometry("800x600")

        # Kết nối đến MongoDB
        try:
            self.client = pymongo.MongoClient('localhost', 27017)  # Thay đổi nếu cần
            self.db = self.client['face_recognition']              # Tên cơ sở dữ liệu
            self.collection_name = 'checkins'                      # Tên collection mặc định
            self.fs = gridfs.GridFS(self.db)                       # GridFS (nếu sử dụng)
            print("Kết nối đến MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối đến MongoDB: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi kết nối đến MongoDB: {e}")
            return

        # Tạo giao diện
        self.create_widgets()

    def create_widgets(self):
        # Ô nhập ngày tháng năm
        self.label_date = tk.Label(self.root, text="Nhập ngày (YYYY-MM-DD):")
        self.label_date.pack(pady=5)

        self.entry_date = tk.Entry(self.root, width=20)
        self.entry_date.pack(pady=5)

        # Select box lựa chọn "Toàn bộ" hoặc "Nhân Viên"
        self.label_option = tk.Label(self.root, text="Lựa chọn:")
        self.label_option.pack(pady=5)

        self.option_var = tk.StringVar()
        self.option_var.set("Toàn bộ")  # Giá trị mặc định

        self.option_menu = ttk.Combobox(self.root, textvariable=self.option_var, values=["Toàn bộ", "Nhân Viên"], state='readonly')
        self.option_menu.pack(pady=5)
        self.option_menu.bind("<<ComboboxSelected>>", self.on_option_change)

        # Ô nhập tên (chỉ hiển thị khi chọn "Nhân Viên")
        self.label_name = tk.Label(self.root, text="Nhập tên nhân viên:")
        self.entry_name = tk.Entry(self.root, width=30)

        # Thêm lựa chọn giữa "Check-ins" và "Check-outs"
        self.label_collection = tk.Label(self.root, text="Chọn loại dữ liệu:")
        self.label_collection.pack(pady=5)

        self.collection_var = tk.StringVar()
        self.collection_var.set("checkins")  # Giá trị mặc định

        self.collection_menu = ttk.Combobox(self.root, textvariable=self.collection_var, values=["checkins", "checkouts"], state='readonly')
        self.collection_menu.pack(pady=5)

        # Nút "Xem"
        self.btn_view = tk.Button(self.root, text="Xem", command=self.view_images)
        self.btn_view.pack(pady=5)

        # Khung hiển thị hình ảnh với scrollbar
        self.frame_images = tk.Frame(self.root)
        self.frame_images.pack(fill=tk.BOTH, expand=True)

        # Canvas để chứa các hình ảnh
        self.canvas = tk.Canvas(self.frame_images)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Thanh cuộn (scrollbar)
        self.scrollbar = tk.Scrollbar(self.frame_images, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame bên trong canvas để đặt các hình ảnh
        self.inner_frame = tk.Frame(self.canvas)

        # Thêm frame vào canvas
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # Ràng buộc sự kiện thay đổi kích thước
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.frame_width)

        # Gọi hàm để cập nhật giao diện theo lựa chọn ban đầu
        self.on_option_change()

    def frame_width(self, event):
        # Cập nhật chiều rộng của canvas để phù hợp với frame bên trong
        canvas_width = event.width
        self.canvas.itemconfig("inner_frame", width=canvas_width)

    def on_frame_configure(self, event):
        # Cập nhật vùng cuộn của canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_option_change(self, event=None):
        option = self.option_var.get()
        if option == "Nhân Viên":
            # Hiển thị ô nhập tên
            self.label_name.pack(pady=5)
            self.entry_name.pack(pady=5)
        else:
            # Ẩn ô nhập tên
            self.label_name.pack_forget()
            self.entry_name.pack_forget()

    def view_images(self):
        # Xóa nội dung cũ
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        date_str = self.entry_date.get().strip()
        if not date_str:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ngày.")
            return

        # Kiểm tra định dạng ngày
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # Tạo khoảng thời gian từ đầu ngày đến cuối ngày
            start_date = date
            end_date = date + timedelta(days=1)
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ. Vui lòng nhập theo định dạng YYYY-MM-DD.")
            return

        option = self.option_var.get()

        query = {
            'timestamp': {
                '$gte': start_date,
                '$lt': end_date
            }
        }

        if option == "Nhân Viên":
            name = self.entry_name.get().strip()
            if not name:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên nhân viên.")
                return
            query['name'] = name

        # Lấy tên collection từ lựa chọn của người dùng
        self.collection_name = self.collection_var.get()
        collection = self.db[self.collection_name]

        # Truy vấn MongoDB để lấy các tài liệu phù hợp
        try:
            documents = collection.find(query).sort('timestamp', pymongo.ASCENDING)
            found = False
            row = 0
            col = 0
            max_columns = 3  # Số cột tối đa trong lưới
            for doc in documents:
                found = True
                # Kiểm tra và lấy hình ảnh từ GridFS hoặc từ trường 'image'
                if 'image' in doc:
                    # Lấy hình ảnh từ trường 'image' trong tài liệu
                    img_bytes = doc['image']
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                elif 'image_id' in doc:
                    # Lấy hình ảnh từ GridFS
                    image_id = doc['image_id']
                    grid_out = self.fs.get(image_id)
                    img_bytes = grid_out.read()
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                elif 'image_path' in doc:
                    # Lấy hình ảnh từ hệ thống tệp
                    image_path = doc['image_path']
                    img_cv = cv2.imread(image_path)
                else:
                    continue  # Nếu không có hình ảnh, bỏ qua tài liệu này

                # Chuyển đổi sang RGB cho PIL
                img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

                # Chuyển đổi OpenCV image thành PIL Image
                img_pil = Image.fromarray(img_cv)

                # Thay đổi kích thước hình ảnh nếu cần
                img_pil = img_pil.resize((200, 200), Image.LANCZOS)

                # Chuyển đổi PIL Image thành ImageTk
                imgtk = ImageTk.PhotoImage(image=img_pil)

                # Tạo Frame cho từng hình ảnh và thông tin
                img_frame = tk.Frame(self.inner_frame, bd=2, relief=tk.RIDGE)
                img_frame.grid(row=row, column=col, padx=5, pady=5)

                # Tạo Label để hiển thị hình ảnh
                img_label = tk.Label(img_frame, image=imgtk)
                img_label.image = imgtk  # Giữ tham chiếu để không bị giải phóng
                img_label.pack()

                # Hiển thị tên và thời gian chụp
                timestamp = doc.get('timestamp', None)
                if timestamp:
                    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    timestamp_str = "Không rõ thời gian"

                name = doc.get('name', 'Không rõ tên')

                info_label = tk.Label(img_frame, text=f"{name}\n{timestamp_str}")
                info_label.pack()

                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1  # Tăng hàng khi đạt số cột tối đa

            if not found:
                messagebox.showinfo("Thông báo", "Không tìm thấy hình ảnh phù hợp.")
        except Exception as e:
            print(f"Lỗi khi truy vấn MongoDB: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi truy vấn MongoDB: {e}")

    def on_closing(self):
        self.client.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
