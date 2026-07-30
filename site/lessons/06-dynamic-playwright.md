# Phase 6: Dynamic Website ด้วย Playwright

บทนี้ใช้ Playwright เปิด Browser เพื่ออ่านข้อมูลที่ JavaScript สร้างภายหลังการโหลด HTML โดยใช้ Local Mock Page ใน `mock_site/dynamic` เท่านั้น

## สิ่งที่ได้ฝึก

- เปิดและปิด Browser/Context อย่างถูกต้อง
- ใช้ `locator` แทนการพึ่ง CSS ที่เปราะบางหรือการหน่วงด้วย `time.sleep()`
- รอข้อมูลที่ JavaScript สร้างด้วย explicit wait
- เลือกค่าใน Form และกดปุ่ม Apply filter
- กด Load more จนหมด พร้อมตรวจจำนวนแถวหลังแต่ละรอบ
- บันทึก Screenshot ก่อนและหลังการทำงาน
- รอ Download event และบันทึกไฟล์ที่ Browser สร้าง
- แยก Headless และ Headed mode ด้วย `--headed`

## เตรียมเครื่องมือบน Windows

เปิด PowerShell ที่ Root ของ Repository แล้วติดตั้ง Browser dependencies:

```powershell
python -m pip install -e ".[dev,browser]"
python -m playwright install chromium
```

หากใช้ Virtual Environment ของ Repository ให้เรียกผ่าน `.venv`:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev,browser]"
.\.venv\Scripts\python.exe -m playwright install chromium
```

คำสั่งติดตั้ง Chromium อาจใช้เวลานานและต้องใช้อินเทอร์เน็ต หากองค์กรจำกัดการดาวน์โหลด ให้เก็บข้อความ Error ไว้ตรวจสอบกับผู้ดูแลระบบ

## เปิด Local Mock Website

Terminal ที่ 1:

```powershell
python -m http.server 8000 --directory mock_site
```

เปิดดูหน้า Dynamic ได้ที่ `http://127.0.0.1:8000/dynamic/index.html`

หน้า Mock นี้มีข้อมูลว่างใน HTML ตอนเริ่มต้น แล้ว `app.js` จะโหลดตารางทีละหน้า, กรอง Category และสร้าง CSV ผ่าน Blob เมื่อกด Download

## รันตัวอย่าง

Terminal ที่ 2:

```powershell
.\.venv\Scripts\python.exe .\examples\08_playwright\dynamic_playwright.py
```

แสดง Browser เพื่อดูขั้นตอน:

```powershell
.\.venv\Scripts\python.exe .\examples\08_playwright\dynamic_playwright.py --headed
```

ผลลัพธ์จะอยู่ใน `output/playwright_dynamic`:

- `dynamic_items.csv` และ `dynamic_items.json` จากตารางที่ JavaScript โหลด
- `dynamic-catalog-initial.png` และ `dynamic-catalog-final.png`
- `dynamic-catalog.csv` จาก Download event

## ทำไมไม่ใช้ `time.sleep()` เป็นวิธีหลัก

เวลาที่ข้อมูลพร้อมอาจเปลี่ยนตามเครื่องและเครือข่าย การหน่วงแบบคงที่อาจช้าเกินไปหรือสั้นเกินไป ตัวอย่างนี้ใช้ `locator.wait_for()`, `page.wait_for_function()` และ `page.expect_download()` ซึ่งรอเหตุการณ์หรือเงื่อนไขที่ต้องการโดยตรง

## ข้อควรระวัง

- ตรวจ Official API และ Terms/robots/สิทธิ์ก่อนใช้กับเว็บไซต์จริง
- ใช้ Browser Automation เฉพาะเมื่อข้อมูลจำเป็นต้องผ่าน JavaScript และได้รับอนุญาต
- กำหนด Timeout และปิด Context/Browser ใน `finally` เสมอ
- ห้ามเก็บ Cookie, Token, Password หรือข้อมูลส่วนบุคคลลง Repository
- อย่าหลบ CAPTCHA, Login, Access Control หรือ Bot Protection

## แบบฝึกหัด

1. เพิ่ม Category ใหม่ใน `app.js` แล้วตรวจว่า Filter ยังทำงาน
2. เพิ่มคอลัมน์ `stock` และส่งออกใน CSV
3. ปรับตัวอย่างให้รับ URL ผ่าน Command Line แล้วทดสอบ Timeout
4. เพิ่มการตรวจชื่อไฟล์ Download และขนาดไฟล์ก่อนบันทึก

## Checklist จบ Phase 6

- [ ] ติดตั้ง Playwright และ Chromium สำเร็จ
- [ ] เปิด Dynamic Mock Page ได้
- [ ] อ่านตารางหลัง JavaScript โหลด
- [ ] ใช้ Locator และ Explicit Wait
- [ ] ใช้ Form filter และ Load more pagination
- [ ] บันทึก Screenshot
- [ ] รับ Download event และบันทึกไฟล์
- [ ] ปิด Browser อย่างถูกต้อง
