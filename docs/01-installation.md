# การติดตั้งสำหรับผู้เริ่มต้น

## เป้าหมายการเรียนรู้

เมื่อจบบทนี้ ผู้เรียนจะสามารถ:

- ตรวจสอบว่าเครื่องมี Python 3.11 หรือใหม่กว่า
- สร้างและเปิดใช้งาน Virtual Environment บน Windows PowerShell
- ติดตั้งและตรวจสอบ Python Packages ด้วย `python -m pip`
- เปิดโครงการด้วย VS Code และเลือก Python Interpreter ที่ถูกต้อง
- สร้างและรัน Python File แรก
- เข้าใจข้อควรระวังของ PowerShell Execution Policy

## สิ่งที่ต้องเตรียม

- Windows 10 หรือ Windows 11
- VS Code
- Python 3.11 หรือใหม่กว่า จาก [python.org](https://www.python.org/downloads/)
- โฟลเดอร์ Repository นี้บนเครื่อง

คำสั่งในบทนี้ใช้กับ **Windows PowerShell** หรือ VS Code Terminal ที่เลือก Profile เป็น PowerShell เว้นแต่จะระบุเป็นอย่างอื่น

## คำศัพท์

- **Python Interpreter**: โปรแกรมที่ใช้แปลและรันโค้ด Python
- **Package**: ชุดโค้ดที่ติดตั้งเพิ่มเพื่อใช้งาน เช่น `requests`
- **Virtual Environment**: พื้นที่ติดตั้ง Package แยกเฉพาะโครงการ เพื่อลดปัญหา Package ชนกัน
- **pip**: เครื่องมือจัดการ Package ของ Python
- **Execution Policy**: นโยบายของ PowerShell ที่กำหนดว่าจะอนุญาตให้รัน Script ได้หรือไม่

## ตรวจสอบ Python

เปิด PowerShell แล้วรัน:

```powershell
python --version
```

ผลลัพธ์ควรเป็น Python 3.11 หรือใหม่กว่า เช่น `Python 3.14.0` หาก Windows มี Python Launcher ให้ตรวจสอบเพิ่มเติมได้ด้วย:

```powershell
py --version
py -3 --version
```

ถ้าไม่พบคำสั่ง `python` ให้ติดตั้ง Python จาก python.org แล้วเลือกตัวเลือก **Add python.exe to PATH** ระหว่างติดตั้ง จากนั้นปิดและเปิด PowerShell ใหม่

## เปิดโครงการด้วย VS Code

ใน PowerShell ให้เปลี่ยนไปยังโฟลเดอร์โครงการ แล้วเปิด VS Code:

```powershell
Set-Location -LiteralPath 'D:\path\to\0.Web-Scrapping-101'
code .
```

ถ้า `code` ไม่ใช่คำสั่งที่รู้จัก ให้เปิด VS Code จากเมนู Start แล้วเลือก **File > Open Folder** จากนั้นเลือกโฟลเดอร์ Repository

## สร้าง Virtual Environment

จากโฟลเดอร์ Repository ให้รัน:

```powershell
python -m venv .venv
```

คำสั่งนี้สร้างโฟลเดอร์ `.venv` ซึ่งไม่ควร Commit เข้า Git ตามที่กำหนดไว้ใน `.gitignore`

## Activate บน PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

ถ้าสำเร็จ จะเห็นคำว่า `(.venv)` ขึ้นหน้าบรรทัดคำสั่ง ตรวจสอบว่าใช้ Interpreter จาก Virtual Environment ด้วย:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

การออกจาก Virtual Environment ทำได้ด้วย:

```powershell
deactivate
```

## ถ้า PowerShell ไม่อนุญาตให้ Activate

อาจพบข้อความเกี่ยวกับการรัน Script ถูกปิดใช้งาน ปรับใช้เฉพาะ PowerShell Session ปัจจุบันได้ดังนี้:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

การตั้งค่า `Process` มีผลเฉพาะหน้าต่าง PowerShell นี้ เมื่อปิดหน้าต่าง ค่าจะหายไปและไม่เปลี่ยนนโยบายถาวรของเครื่อง หลีกเลี่ยงการใช้ `Unrestricted` หรือการลดนโยบายในระดับเครื่องโดยไม่เข้าใจผลกระทบ

ถ้าต้องการตั้งค่าสำหรับผู้ใช้ปัจจุบัน อาจใช้ `RemoteSigned` ได้ แต่ควรทำตามนโยบาย IT ขององค์กรก่อน:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

ตรวจสอบค่าปัจจุบันได้ด้วย:

```powershell
Get-ExecutionPolicy -List
```

## ติดตั้ง Dependencies

ให้ Activate `.venv` ก่อน แล้วอัปเดต `pip`:

```powershell
python -m pip install --upgrade pip
```

ติดตั้ง Runtime และ Development Dependencies จาก `pyproject.toml`:

```powershell
python -m pip install -e ".[dev]"
```

หากต้องการติดตั้งเครื่องมือ Browser Automation ใน Phase ที่เกี่ยวข้อง ให้ติดตั้งเพิ่ม:

```powershell
python -m pip install -e ".[dev,browser]"
python -m playwright install chromium
```

คำสั่งติดตั้งต้องใช้อินเทอร์เน็ตและอาจถูกจำกัดโดย Firewall ขององค์กร หากติดตั้งไม่ได้ ให้เก็บ Error message ไว้เพื่อแก้ไขตามสภาพแวดล้อมจริง

## pip และ `python -m pip`

คำสั่ง `pip` อาจชี้ไปยัง Python คนละตัวกับโครงการ จึงแนะนำให้ใช้รูปแบบนี้:

```powershell
python -m pip --version
python -m pip list
python -m pip show requests
python -m pip check
```

ตรวจสอบ Package ที่ติดตั้งใน Environment ปัจจุบัน:

```powershell
python -c "import requests, bs4, lxml, pandas, openpyxl, dotenv, tenacity; print('Runtime packages: OK')"
```

ถ้าใช้คำสั่งโดยไม่ Activate ให้เรียก Python ใน `.venv` โดยตรง:

```powershell
.\.venv\Scripts\python.exe -m pip list
```

## เลือก Python Interpreter ใน VS Code

1. เปิดโฟลเดอร์ Repository ใน VS Code
2. กด `Ctrl+Shift+P`
3. เลือก `Python: Select Interpreter`
4. เลือก `.venv\Scripts\python.exe`
5. เปิด Terminal ใหม่ แล้วตรวจสอบ `python -c "import sys; print(sys.executable)"`

ถ้าไม่พบรายการ ให้ติดตั้งส่วนขยาย **Python** ของ Microsoft และตรวจสอบว่าเปิดโฟลเดอร์ระดับ Repository ไม่ใช่เปิดเฉพาะไฟล์เดี่ยว

## รัน Python File แรก

ไฟล์ตัวอย่างอยู่ที่ [examples/00_first_script/hello.py](../examples/00_first_script/hello.py) เปิดไฟล์แล้วกดปุ่ม Run หรือใช้ PowerShell:

```powershell
python .\examples\00_first_script\hello.py
```

ผลลัพธ์ที่คาดหวัง:

```text
สวัสดีจาก Web Scraping Zero to Practical
Python interpreter พร้อมใช้งาน
```

## ใช้ Script ตั้งค่าโครงการ

จากโฟลเดอร์ Repository ให้รัน:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup_windows.ps1
```

Script จะตรวจสอบ Python, สร้าง `.venv` ถ้ายังไม่มี, อัปเดต `pip` และติดตั้ง Dependencies กลุ่ม `dev` หากต้องการติดตั้ง Chromium สำหรับ Playwright ให้เพิ่ม `-InstallBrowser`:

```powershell
.\scripts\setup_windows.ps1 -InstallBrowser
```

## ตรวจสอบโครงการ

หลังตั้งค่าเสร็จ ให้รัน:

```powershell
.\scripts\run_checks.ps1
```

Script จะตรวจสอบ Python, `pip check`, Runtime Packages และเรียก Test/Lint เฉพาะเมื่อมีไฟล์ที่เกี่ยวข้องใน Repository

## ข้อผิดพลาดที่พบบ่อย

### `python` ไม่พบคำสั่ง

ติดตั้ง Python ใหม่โดยเลือก Add to PATH หรือใช้ Python Launcher:

```powershell
py -3 -m venv .venv
```

### ใช้ Python ผิดตัวหลัง Activate

ตรวจสอบด้วย:

```powershell
Get-Command python
python -c "import sys; print(sys.executable)"
```

ควรชี้ไปยัง `.venv\Scripts\python.exe`

### ติดตั้ง Package ไม่ได้

ตรวจสอบอินเทอร์เน็ต, Proxy, Certificate และสิทธิ์ขององค์กรก่อน อย่าฝัง Username, Password หรือ Token ลงในคำสั่งหรือไฟล์ Repository

### `code` ไม่พบคำสั่ง

เปิดโฟลเดอร์ผ่าน VS Code โดยตรง หรือเปิด Command Palette แล้วใช้ `File: Open Folder`

## แบบฝึกหัด

1. สร้าง Virtual Environment ชื่อ `.venv` และแสดง Path ของ Interpreter
2. ใช้ `python -m pip list` บันทึกชื่อ Package ที่ติดตั้งไว้
3. รัน `hello.py` ผ่านทั้งปุ่ม Run ใน VS Code และ PowerShell
4. ปิด Environment ด้วย `deactivate` แล้วตรวจสอบความแตกต่างของ `python` ก่อนและหลัง Activate

## Checklist

- [ ] `python --version` เป็น 3.11 หรือใหม่กว่า
- [ ] สร้าง `.venv` สำเร็จ
- [ ] Activate `.venv` ได้บน PowerShell
- [ ] เลือก `.venv` เป็น Python Interpreter ใน VS Code
- [ ] ติดตั้ง Runtime และ Development Dependencies ได้
- [ ] รัน `hello.py` สำเร็จ
- [ ] เข้าใจความเสี่ยงของ Execution Policy
- [ ] รัน `scripts/run_checks.ps1` ได้

## สรุป

Virtual Environment ช่วยแยก Dependencies ของโครงการ การใช้ `python -m pip` ช่วยให้ติดตั้ง Package ให้ตรงกับ Interpreter ที่กำลังใช้ และ Script ของ Phase นี้ช่วยลดขั้นตอนการตั้งค่าบน Windows ขั้นตอนถัดไปจะเริ่มอธิบาย Web, HTML, HTTP และ Developer Tools ใน Phase 2 เมื่อได้รับคำสั่ง
