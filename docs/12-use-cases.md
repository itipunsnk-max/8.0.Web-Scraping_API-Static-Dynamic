# Phase 12: Use Cases

Phase นี้นำแนวคิดจาก Phase 1-11 มาประกอบเป็นโครงการขนาดเล็กที่รันซ้ำได้ โดยใช้ fixture ใน repository เป็นค่าเริ่มต้น จึงไม่ยิงเว็บไซต์ภายนอกระหว่างเรียนหรือระหว่าง test

## โครงการตัวอย่าง

| โครงการ | จุดประสงค์ | ตัวอย่างคำสั่ง |
| --- | --- | --- |
| Price Monitor | เปรียบเทียบราคาเดิม/ใหม่และหา item ที่เพิ่มเข้ามา | `python .\\use_cases\\price_monitor\\app.py --previous .\\use_cases\\price_monitor\\previous.json --current .\\use_cases\\price_monitor\\current.json` |
| Public Announcement Tracker | อ่านประกาศจาก HTML และกรองด้วย keyword/date | `python .\\use_cases\\public_announcements\\app.py --input .\\use_cases\\public_announcements\\announcements.html --keyword road` |
| Document Downloader | ค้นหาเฉพาะ PDF/DOCX/XLSX และสร้าง download plan | `python .\\use_cases\\document_downloader\\app.py --input .\\use_cases\\document_downloader\\documents.html` |
| Location Directory | แปลง directory เป็น record พร้อมตรวจพิกัด | `python .\\use_cases\\location_directory\\app.py --input .\\use_cases\\location_directory\\locations.html` |
| Weather API | Normalize forecast JSON และสรุปอุณหภูมิ/ฝน | `python .\\use_cases\\weather_api\\app.py --input .\\use_cases\\weather_api\\forecast.json` |
| Solar Datasheet Catalog | สร้าง catalog สินค้าและ link datasheet | `python .\\use_cases\\solar_datasheet_catalog\\app.py --input .\\use_cases\\solar_datasheet_catalog\\catalog.html --minimum-w 400` |
| Power BI Data Pipeline | ส่ง raw records เข้า Phase 10 schema และ export หลายรูปแบบ | `python .\\use_cases\\power_bi_pipeline\\app.py --input .\\use_cases\\power_bi_pipeline\\input.json --output-dir .\\output\\phase12-power-bi` |

## รูปแบบการออกแบบร่วม

1. แยก `load/parse`, `transform/filter`, `validate` และ `main` ออกจากกันเพื่อให้ unit test ได้
2. ใช้ข้อมูลจำลองที่ commit ได้แทนการพึ่งพาเว็บจริง
3. ใช้ absolute URL และจำกัด extension ก่อนดาวน์โหลดเอกสาร
4. ตรวจพิกัด, วันที่, ตัวเลข และ schema ก่อนส่งต่อ
5. โครงการ Power BI ใช้ `run_pipeline()` จาก Phase 10 เพื่อให้ schema, raw data และ export มีมาตรฐานเดียวกัน

## การนำไปใช้กับแหล่งข้อมูลจริง

ก่อนเปลี่ยน fixture เป็น URL จริง ให้ตรวจ Terms, `robots.txt`, API และสิทธิ์การใช้ข้อมูลก่อน เพิ่ม timeout, retry, rate limit และ logging จาก Phase 8 และเก็บ endpoint/token ใน environment variable เท่านั้น การดาวน์โหลดเอกสารควรกำหนด allow-list ของ host และตรวจชนิดไฟล์เพิ่มเติมในระบบ production

## การทดสอบ

```powershell
.\\.venv\\Scripts\\python.exe -m pytest .\\tests\\test_phase12_use_cases.py -q
.\\.venv\\Scripts\\python.exe -m ruff check .\\use_cases .\\tests\\test_phase12_use_cases.py
```

ชุดทดสอบครอบคลุมทั้ง 7 โครงการ และไม่เรียก network จริง
