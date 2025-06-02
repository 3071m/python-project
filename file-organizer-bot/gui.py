import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import shutil
from file_types import FILE_TYPES

def organize_folder(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        return [f"❌ โฟลเดอร์ {folder} ไม่พบ"]

    logs = []
    for file in folder.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            moved = False
            for category, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_folder = folder / category
                    target_folder.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_folder / file.name))
                    logs.append(f"✔️ ย้าย {file.name} ไป {category}")
                    moved = True
                    break
            if not moved:
                target_folder = folder / "Others"
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_folder / file.name))
                logs.append(f"📦 ย้าย {file.name} ไป Others")
    return logs

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        status_label.config(text=f"เลือกโฟลเดอร์: {folder_selected}")

def start_organize():
    folder = folder_path.get()
    if not folder:
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกโฟลเดอร์ก่อน")
        return

    try:
        logs = organize_folder(folder)
        status_label.config(text="✅ จัดเรียงไฟล์เสร็จแล้ว")
        log_text.delete(1.0, tk.END)
        for log in logs:
            log_text.insert(tk.END, log + "\n")
    except Exception as e:
        messagebox.showerror("เกิดข้อผิดพลาด", str(e))
        status_label.config(text="❌ เกิดข้อผิดพลาดในการจัดเรียงไฟล์")

# ตั้งค่าหน้าต่างหลัก
root = tk.Tk()
root.title("File Organizer Bot")
root.geometry("600x500")

folder_path = tk.StringVar()

# ส่วนบน: ปุ่มเลือกโฟลเดอร์และแสดง path
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

btn_select = tk.Button(frame_top, text="เลือกโฟลเดอร์", command=select_folder, width=20)
btn_select.pack(side=tk.LEFT, padx=5)

label_path = tk.Label(frame_top, textvariable=folder_path, width=50, anchor="w", relief=tk.SUNKEN)
label_path.pack(side=tk.LEFT, padx=5)

# ปุ่มเริ่มจัดเรียงไฟล์
btn_start = tk.Button(root, text="เริ่มจัดเรียงไฟล์", command=start_organize, width=30)
btn_start.pack(pady=10)

# แสดงสถานะการทำงาน
status_label = tk.Label(root, text="สถานะ: รอการเลือกโฟลเดอร์", fg="blue")
status_label.pack()

# Text box สำหรับแสดง log
log_text = tk.Text(root, height=20, width=70)
log_text.pack(pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar ของ log_text
scrollbar = tk.Scrollbar(root, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
