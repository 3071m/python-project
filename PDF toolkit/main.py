from tkinter import *
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfMerger
from tkinter import messagebox
from PyPDF2 import PdfReader, PdfWriter
from tkinter import simpledialog
from pdf2image import convert_from_path
import os

class PDFToolkitApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Toolkit by มอมแมม")
        self.geometry("600x400")
        self.configure(bg="#f8f8f8")
        
        self.pdf_files = []

        Label(self, text="📄 Drag & Drop PDF Files", font=("Segoe UI", 16), bg="#f8f8f8").pack(pady=10)

        self.drop_area = Listbox(self, selectmode=MULTIPLE, width=60, height=10)
        self.drop_area.pack(pady=10)
        self.drop_area.insert(END, "📥 วางไฟล์ PDF ที่นี่...")

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)

        # 🔽 Scrollable Button Area
        canvas = Canvas(self, height=200, bg="#f8f8f8")
        scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#f8f8f8")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 🔘 Buttons (inside scrollable frame)
        ttk.Button(scrollable_frame, text="เลือกไฟล์ PDF ด้วยปุ่ม", command=self.select_files).pack(pady=5)
        ttk.Button(scrollable_frame, text="🧩 รวมไฟล์ PDF", command=self.merge_pdfs).pack(pady=5)
        ttk.Button(scrollable_frame, text="🔪 แยกหน้า PDF", command=self.split_pdf).pack(pady=5)
        ttk.Button(scrollable_frame, text="🗑️ ลบหน้า PDF", command=self.delete_pages).pack(pady=5)
        ttk.Button(self, text="🖼️ แปลง PDF เป็นรูปภาพ", command=self.pdf_to_images).pack(pady=5)



    def on_drop(self, event):
        files = self.tk.splitlist(event.data)
        self.add_files(files)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.add_files(files)

    def add_files(self, files):
        self.pdf_files.clear()
        self.drop_area.delete(0, END)
        for f in files:
            if f.lower().endswith(".pdf"):
                self.pdf_files.append(f)
                self.drop_area.insert(END, os.path.basename(f))
                
    def merge_pdfs(self):
        print("ไฟล์ PDF ที่เลือก:", self.pdf_files)
        if len(self.pdf_files) < 2:
            messagebox.showwarning("เตือน", "กรุณาเลือกอย่างน้อย 2 ไฟล์ PDF")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="บันทึกเป็น..."
        )

        if not output_path:
            return

        merger = PdfMerger()

        try:
            for pdf in self.pdf_files:
                merger.append(pdf)

            merger.write(output_path)
            merger.close()
            messagebox.showinfo("สำเร็จ", f"รวมไฟล์สำเร็จ!\n\n{output_path}")
        except Exception as e:
            messagebox.showerror("ผิดพลาด", f"เกิดข้อผิดพลาด:\n{str(e)}")

    def split_pdf(self):
        if len(self.pdf_files) != 1:
            messagebox.showwarning("เตือน", "กรุณาเลือกไฟล์ PDF เพียง 1 ไฟล์ สำหรับการแยกหน้า")
            return

        pdf_path = self.pdf_files[0]
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        # ขอให้ผู้ใช้กรอกช่วงหน้า เช่น 1-3
        page_range = simpledialog.askstring("แยกหน้า PDF", f"ไฟล์นี้มีทั้งหมด {total_pages} หน้า\nกรุณาใส่ช่วงหน้าที่ต้องการแยก (เช่น 1-3):")

        if not page_range:
            return

        try:
            start, end = map(int, page_range.split('-'))
            if start < 1 or end > total_pages or start > end:
                raise ValueError()
        except:
            messagebox.showerror("ผิดพลาด", "กรุณาใส่ช่วงหน้าในรูปแบบถูกต้อง เช่น 1-3 และอยู่ในช่วงจำนวนหน้าของไฟล์")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="บันทึกไฟล์แยกหน้า PDF เป็น..."
        )

        if not output_path:
            return

        writer = PdfWriter()
        for i in range(start-1, end):
            writer.add_page(reader.pages[i])

        try:
            with open(output_path, "wb") as f_out:
                writer.write(f_out)
            messagebox.showinfo("สำเร็จ", f"แยกหน้า PDF สำเร็จ!\nไฟล์บันทึกที่:\n{output_path}")
        except Exception as e:
            messagebox.showerror("ผิดพลาด", f"เกิดข้อผิดพลาด:\n{str(e)}")

    def delete_pages(self):
        if len(self.pdf_files) != 1:
            messagebox.showwarning("เตือน", "กรุณาเลือกไฟล์ PDF เพียง 1 ไฟล์ สำหรับการลบหน้า")
            return

        pdf_path = self.pdf_files[0]
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        page_input = simpledialog.askstring(
            "ลบหน้า PDF",
            f"ไฟล์นี้มีทั้งหมด {total_pages} หน้า\nกรุณาใส่เลขหน้าที่ต้องการลบ (คั่นด้วย , เช่น 1,3,5):"
        )

        if not page_input:
            return

        try:
            pages_to_delete = sorted(set(int(p.strip()) for p in page_input.split(',') if p.strip().isdigit()))
            if not all(1 <= p <= total_pages for p in pages_to_delete):
                raise ValueError("บางหน้าที่ระบุอยู่นอกขอบเขตของ PDF")
        except Exception as e:
            messagebox.showerror("ผิดพลาด", f"รูปแบบไม่ถูกต้อง:\n{str(e)}")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="บันทึกไฟล์ PDF ที่ลบหน้าแล้ว"
        )
        if not output_path:
            return

        writer = PdfWriter()
        try:
            for i in range(total_pages):
                if (i + 1) not in pages_to_delete:
                    writer.add_page(reader.pages[i])
            with open(output_path, "wb") as f_out:
                writer.write(f_out)
            messagebox.showinfo("สำเร็จ", f"ลบหน้า PDF สำเร็จ!\nไฟล์บันทึกที่:\n{output_path}")
        except Exception as e:
            messagebox.showerror("ผิดพลาด", f"เกิดข้อผิดพลาด:\n{str(e)}")

if __name__ == "__main__":
    app = PDFToolkitApp()
    app.mainloop()
