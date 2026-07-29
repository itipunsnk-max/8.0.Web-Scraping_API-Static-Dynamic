# Local Mock Website

โฟลเดอร์นี้เก็บหน้าเว็บภายใน Repository สำหรับฝึกอ่าน HTML และใช้ Chrome Developer Tools โดยไม่ต้องส่ง Request ไปยังเว็บไซต์ภายนอก

## เปิด Static Page

รันคำสั่งจากโฟลเดอร์ Repository ด้วย Windows PowerShell:

```powershell
python -m http.server 8000 --directory mock_site/static
```

เปิดหน้าเว็บที่:

```text
http://127.0.0.1:8000/index.html
```

เมื่อฝึกเสร็จ กด `Ctrl+C` ในหน้าต่าง PowerShell เพื่อหยุด Server

## ไฟล์สำหรับฝึก

- `static/index.html` — หน้า Static ที่มี ID, Class, Attribute, ตาราง, ลิงก์ และรูปภาพ
- `static/products.html` — หน้า Local Mock Store สำหรับฝึก Requests และ BeautifulSoup
- `static/assets/course-logo.svg` — รูปภาพ Local ที่ใช้ฝึก Attribute Selector และตรวจสอบ `alt`

ตัวอย่างนี้ไม่มี Login, CAPTCHA, API Key, Cookie หรือข้อมูลส่วนตัว
