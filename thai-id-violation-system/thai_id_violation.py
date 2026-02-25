import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import datetime
import random
import os

# ========== VIOLATION DATA ==========
VIOLATIONS = {
    "ไม่สวมหมวกนิรภัย": {
        "fine": 500,
        "points": 1,
        "desc": "ขับขี่รถจักรยานยนต์ไม่สวมหมวกนิรภัย"
    },
    "ขับรถเร็วเกินกำหนด": {
        "fine": 1000,
        "points": 2,
        "desc": "ขับรถด้วยความเร็วเกินกว่าที่กฎหมายกำหนด"
    },
    "ขับรถย้อนศร": {
        "fine": 2000,
        "points": 3,
        "desc": "ขับรถย้อนศรบนทางเดินรถทางเดียว"
    }
}

# ========== MAIN APPLICATION ==========
class ThaiIDViolationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบบันทึกการกระทำผิดจราจร")
        self.root.geometry("700x700")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.id_data = {
            'id_number': '1-2345-67890-12-3',
            'name_th': 'นายสมชาย ใจดี',
            'name_en': 'Mr. Somchai Jaidee',
            'address': '123 ถนนสุขุมวิท กรุงเทพฯ'
        }
        self.current_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="🚦 ระบบบันทึกการกระทำผิดจราจร", 
                        font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333')
        title.pack(pady=20)
        
        # ===== ID CARD SECTION =====
        id_frame = tk.LabelFrame(self.root, text="ข้อมูลบัตรประชาชน", 
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        id_frame.pack(fill='x', padx=20, pady=10)
        
        # Image upload
        btn_upload = tk.Button(id_frame, text="📷 อัปโหลดรูปบัตรประชาชน", 
                              command=self.upload_image, bg='#4CAF50', fg='white',
                              font=('Arial', 10), padx=10, pady=5)
        btn_upload.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Image preview
        self.image_label = tk.Label(id_frame, bg='white', width=40, height=10)
        self.image_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Manual entry button
        btn_manual = tk.Button(id_frame, text="✏️ กรอกข้อมูลด้วยตนเอง", 
                              command=self.manual_entry, bg='#2196F3', fg='white',
                              font=('Arial', 10), padx=10, pady=5)
        btn_manual.grid(row=2, column=0, padx=5, pady=5)
        
        # Use sample button
        btn_sample = tk.Button(id_frame, text="📋 ใช้ข้อมูลตัวอย่าง", 
                              command=self.use_sample, bg='#FF9800', fg='white',
                              font=('Arial', 10), padx=10, pady=5)
        btn_sample.grid(row=2, column=1, padx=5, pady=5)
        
        # ID display
        self.id_display = tk.Text(id_frame, height=5, width=50, font=('Arial', 10))
        self.id_display.grid(row=3, column=0, columnspan=2, pady=5)
        self.update_id_display()
        
        # ===== VIOLATION SECTION =====
        vio_frame = tk.LabelFrame(self.root, text="ข้อมูลการกระทำผิด", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        vio_frame.pack(fill='x', padx=20, pady=10)
        
        # Violation type
        tk.Label(vio_frame, text="เลือกประเภทความผิด:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
        
        self.violation_var = tk.StringVar()
        self.violation_combo = ttk.Combobox(vio_frame, textvariable=self.violation_var,
                                           values=list(VIOLATIONS.keys()), state='readonly',
                                           width=30)
        self.violation_combo.grid(row=0, column=1, pady=5, padx=5)
        self.violation_combo.bind('<<ComboboxSelected>>', self.update_violation_details)
        
        # Location
        tk.Label(vio_frame, text="สถานที่เกิดเหตุ:", bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
        self.location_entry = tk.Entry(vio_frame, width=40)
        self.location_entry.grid(row=1, column=1, pady=5, padx=5)
        self.location_entry.insert(0, "ถนนสุขุมวิท กรุงเทพฯ")
        
        # Officer ID
        tk.Label(vio_frame, text="รหัสเจ้าหน้าที่:", bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
        self.officer_entry = tk.Entry(vio_frame, width=40)
        self.officer_entry.grid(row=2, column=1, pady=5, padx=5)
        self.officer_entry.insert(0, f"OFF{random.randint(1000, 9999)}")
        
        # Violation details
        self.vio_details = tk.Label(vio_frame, text="", bg='#f0f0f0', fg='#666', justify='left')
        self.vio_details.grid(row=3, column=0, columnspan=2, pady=5)
        
        # ===== BUTTONS =====
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        btn_record = tk.Button(btn_frame, text="✅ บันทึกการกระทำผิด", 
                              command=self.record_violation, bg='#f44336', fg='white',
                              font=('Arial', 12, 'bold'), padx=20, pady=10)
        btn_record.pack(side='left', padx=10)
        
        btn_clear = tk.Button(btn_frame, text="🔄 เริ่มใหม่", 
                             command=self.clear_all, bg='#9E9E9E', fg='white',
                             font=('Arial', 10), padx=15, pady=5)
        btn_clear.pack(side='left', padx=10)
        
        # ===== RESULT DISPLAY =====
        self.result_frame = tk.LabelFrame(self.root, text="ผลการบันทึก", 
                                         font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        self.result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.result_text = tk.Text(self.result_frame, height=8, width=60, font=('Arial', 10))
        self.result_text.pack(fill='both', expand=True)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            # Load and display image
            img = Image.open(file_path)
            img.thumbnail((300, 200))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.current_image = file_path
            
            # Simulate OCR (just show demo message)
            messagebox.showinfo("OCR", "ระบบจำลองการอ่านข้อมูลจากบัตร\n(ในการทำงานจริงจะอ่านข้อมูลจากรูป)")
            
            # Demo: Auto-fill with random Thai ID
            demo_id = f"{random.randint(1,9)}-{random.randint(1000,9999)}-{random.randint(10000,99999)}-{random.randint(10,99)}-{random.randint(1,9)}"
            self.id_data['id_number'] = demo_id
            self.id_data['name_th'] = random.choice(['นายสมชาย', 'นางสาวสมหญิง', 'นายวิชัย']) + ' ' + random.choice(['ใจดี', 'รักดี', 'สุขสันต์'])
            self.update_id_display()
    
    def manual_entry(self):
        # Simple dialog for manual entry
        dialog = tk.Toplevel(self.root)
        dialog.title("กรอกข้อมูลบัตรประชาชน")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="เลขบัตรประชาชน (13 หลัก):").pack(pady=5)
        id_entry = tk.Entry(dialog, width=30)
        id_entry.pack(pady=5)
        
        tk.Label(dialog, text="ชื่อ-นามสกุล (ภาษาไทย):").pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        
        def save_manual():
            self.id_data['id_number'] = id_entry.get() or "1-2345-67890-12-3"
            self.id_data['name_th'] = name_entry.get() or "นายสมชาย ใจดี"
            self.update_id_display()
            dialog.destroy()
        
        tk.Button(dialog, text="บันทึก", command=save_manual, bg='#4CAF50', fg='white').pack(pady=10)
    
    def use_sample(self):
        self.id_data = {
            'id_number': '1-2345-67890-12-3',
            'name_th': 'นายสมชาย ใจดี',
            'name_en': 'Mr. Somchai Jaidee',
            'address': '123 ถนนสุขุมวิท กรุงเทพฯ'
        }
        self.update_id_display()
        messagebox.showinfo("สำเร็จ", "ใช้ข้อมูลตัวอย่างเรียบร้อย")
    
    def update_id_display(self):
        self.id_display.delete(1.0, tk.END)
        self.id_display.insert(1.0, f"เลขบัตร: {self.id_data['id_number']}\n")
        self.id_display.insert(tk.END, f"ชื่อ-สกุล: {self.id_data['name_th']}\n")
        self.id_display.insert(tk.END, f"ชื่อ-สกุล (อังกฤษ): {self.id_data['name_en']}\n")
        self.id_display.insert(tk.END, f"ที่อยู่: {self.id_data['address']}")
    
    def update_violation_details(self, event=None):
        vio_type = self.violation_var.get()
        if vio_type in VIOLATIONS:
            details = VIOLATIONS[vio_type]
            self.vio_details.config(
                text=f"ค่าปรับ: {details['fine']} บาท | คะแนน: {details['points']}\n{details['desc']}"
            )
    
    def record_violation(self):
        # Validate
        if not self.violation_var.get():
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกประเภทความผิด")
            return
        
        # Create violation record
        vio_type = self.violation_var.get()
        vio_data = VIOLATIONS[vio_type]
        
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        result = f"""
{'='*50}
🚨 ใบสั่งจราจร / TRAFFIC TICKET
{'='*50}

วันที่-เวลา: {timestamp}
สถานที่: {self.location_entry.get()}
เจ้าหน้าที่: {self.officer_entry.get()}

👤 ข้อมูลผู้กระทำผิด
────────────────
เลขบัตร: {self.id_data['id_number']}
ชื่อ-สกุล: {self.id_data['name_th']}
ที่อยู่: {self.id_data['address']}

🚗 รายละเอียดความผิด
────────────────
ประเภท: {vio_type}
รายละเอียด: {vio_data['desc']}
ค่าปรับ: {vio_data['fine']} บาท
คะแนนความผิด: {vio_data['points']} คะแนน

{'='*50}
ลงชื่อ......................................... เจ้าหน้าที่
        """
        
        # Display result
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result)
        
        messagebox.showinfo("สำเร็จ", "บันทึกการกระทำผิดเรียบร้อย")
    
    def clear_all(self):
        self.violation_var.set('')
        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, "ถนนสุขุมวิท กรุงเทพฯ")
        self.officer_entry.delete(0, tk.END)
        self.officer_entry.insert(0, f"OFF{random.randint(1000, 9999)}")
        self.vio_details.config(text="")
        self.result_text.delete(1.0, tk.END)
        self.image_label.config(image='')
        self.image_label.image = None
        self.use_sample()

# ========== RUN APPLICATION ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = ThaiIDViolationApp(root)
    root.mainloop()