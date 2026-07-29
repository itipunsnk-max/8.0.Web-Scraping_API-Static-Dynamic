# Contributing

ขอบคุณที่ช่วยปรับปรุง repository นี้ การเปลี่ยนแปลงควรเหมาะกับเป้าหมายการเรียนรู้ มีตัวอย่างที่รันซ้ำได้ และไม่ทำให้ผู้เรียนต้องข้ามระบบป้องกันหรือเปิดเผยข้อมูลลับ

## เริ่มต้น

```powershell
.\scripts\setup_windows.ps1
.\.venv\Scripts\Activate.ps1
```

ก่อนแก้ไขให้ตรวจ branch และสถานะ working tree:

```powershell
git status -sb
git switch -c agent/<short-description>
```

## มาตรฐานการเปลี่ยนแปลง

- แยก commit ให้สื่อความหมายและใช้ข้อความแบบ imperative เช่น `feat: add ...` หรือ `docs: clarify ...`
- เพิ่มหรือแก้ test เมื่อ behavior เปลี่ยน
- ใช้ fixture/local mock แทนการยิงเว็บไซต์จริงใน test
- ไม่ commit `.env`, token, cookie, ข้อมูลส่วนบุคคล หรือไฟล์ output
- ตรวจ Terms, `robots.txt`, API permission และ rate limit ก่อนเพิ่มแหล่งข้อมูลจริง
- เอกสารที่เพิ่มต้องมีคำสั่งรัน, troubleshooting และข้อจำกัดที่เกี่ยวข้อง

## Checks ก่อนเปิด Pull Request

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest -q
```

ใช้ Pull Request template อธิบาย scope, validation, security และผลกระทบต่อ Windows/CI ทุกครั้ง
