# Pagination และการดาวน์โหลดไฟล์

## เป้าหมายการเรียนรู้

เมื่อจบบทนี้ ผู้เรียนจะสามารถ:

- วนอ่านข้อมูลจาก Next Page Link โดยมีขีดจำกัดชัดเจน
- เข้าใจ Page Number, Offset และ Limit
- หยุดเมื่อไม่มีข้อมูลหรือไม่มีหน้าถัดไป
- ป้องกัน Infinite Loop และข้อมูลซ้ำ
- ดาวน์โหลด PDF และรูปภาพด้วย Streaming Request
- ตรวจสอบ Content-Type และขนาดไฟล์
- ตั้งชื่อไฟล์อย่างปลอดภัยและไม่เขียนทับไฟล์เดิม
- คำนวณ SHA-256 Checksum เพื่อยืนยันไฟล์ที่ได้

## สิ่งที่ต้องเตรียม

- Python 3.11 หรือใหม่กว่า
- Dependencies จาก [Phase 1](01-installation.md)
- ความเข้าใจ Requests และ BeautifulSoup จาก [Phase 4](04-static-scraping.md)
- Local Mock Website ใน Repository นี้

## แนวคิดสำคัญ

### Pagination คืออะไร

Pagination คือการแบ่งข้อมูลจำนวนมากออกเป็นหลายหน้า เพื่อไม่ให้ Server ต้องส่งข้อมูลทั้งหมดในครั้งเดียว รูปแบบที่พบบ่อยมีดังนี้:

| รูปแบบ | ตัวอย่าง | จุดที่ต้องตรวจ |
| --- | --- | --- |
| Next Link | `page-1.html` มีลิงก์ไป `page-2.html` | ลิงก์ซ้ำหรือวนกลับหน้าก่อนหรือไม่ |
| Page Number | `?page=2&page_size=20` | จำนวนหน้าสูงสุดและค่าที่รับได้ |
| Offset/Limit | `?offset=40&limit=20` | Offset เพิ่มตามจำนวนที่ได้จริงหรือไม่ |
| Cursor | `next_cursor` ใน JSON | Cursor ใหม่และจุดหยุดเมื่อไม่มี Cursor |

ตัวอย่างนี้ใช้ Next Page Link ใน Local Mock Site และกำหนด `--max-pages` เพื่อป้องกันการวนไม่สิ้นสุด

### ลำดับการทำงาน

```text
หน้าเริ่มต้น
    ↓
อ่านรายการและบันทึก Record ID
    ↓
ตรวจ Next Link
    ├── ไม่มี → จบ
    ├── ซ้ำ → หยุดด้วย Error
    └── มี → ไปหน้าถัดไปจนถึง max-pages
    ↓
ดาวน์โหลดไฟล์แบบ Streaming
    ↓
ตรวจ Content-Type / ขนาด / Checksum
    ↓
เขียน Manifest
```

## เปิด Local Mock Website

จากโฟลเดอร์ Repository ใช้ **Windows PowerShell**:

```powershell
python -m http.server 8000 --directory mock_site/static
```

หน้า Pagination เริ่มต้นที่:

```text
http://127.0.0.1:8000/pagination/page-1.html
```

หน้า Download อยู่ที่:

```text
http://127.0.0.1:8000/downloads.html
```

## ขั้นตอนปฏิบัติ

เปิด PowerShell อีกหน้าต่างหนึ่ง แล้วรัน:

```powershell
python .\examples\05_pagination\pagination_and_downloads.py
```

Script จะอ่านทั้ง 3 หน้า, ตัด Record ซ้ำ, ดาวน์โหลด PDF/SVG ลงในโฟลเดอร์ที่กำหนด และสร้าง:

```text
output/pagination_downloads/items.csv
output/pagination_downloads/download_manifest.csv
output/pagination_downloads/files/sample-guide.pdf
output/pagination_downloads/files/course-logo.svg
```

กำหนดขีดจำกัดเองได้:

```powershell
python .\examples\05_pagination\pagination_and_downloads.py `
  --start-url http://127.0.0.1:8000/pagination/page-1.html `
  --downloads-url http://127.0.0.1:8000/downloads.html `
  --max-pages 5 `
  --max-file-bytes 1048576
```

## การป้องกัน Infinite Loop และข้อมูลซ้ำ

ตัวอย่างตรวจสอบ 3 ชั้น:

1. `seen_pages` ป้องกันการเปิด URL เดิมซ้ำ
2. `max-pages` จำกัดจำนวนหน้าสูงสุด
3. `seen_record_ids` ป้องกัน Record เดิมซ้ำเมื่อข้อมูลทับซ้อนระหว่างหน้า

หากพบ Next Link หลังถึง `max-pages` Script จะหยุดด้วย Error เพื่อไม่ให้ผู้ใช้เข้าใจว่าได้ข้อมูลครบโดยไม่รู้ตัว

## การดาวน์โหลดไฟล์อย่างปลอดภัย

- ใช้ `stream=True` เพื่ออ่านทีละ Chunk
- ตรวจ Status Code ก่อนเขียนไฟล์
- ตรวจ `Content-Type` ให้ตรงกับนามสกุลที่คาดหวัง
- จำกัดขนาดไฟล์ด้วย `--max-file-bytes`
- ทำความสะอาดชื่อไฟล์และแทนที่อักขระต้องห้ามของ Windows
- ถ้าชื่อซ้ำ ให้เติม `_1`, `_2` แทนการเขียนทับ
- เขียนผ่าน `.part` แล้วเปลี่ยนชื่อเมื่อดาวน์โหลดสำเร็จ
- คำนวณ SHA-256 และบันทึกใน Manifest

ห้ามดาวน์โหลดไฟล์จาก URL ที่ไม่ได้รับอนุญาต และไม่ควรเชื่อ Content-Type เพียงอย่างเดียวในระบบจริงโดยไม่ตรวจข้อกำหนดและชนิดข้อมูลเพิ่มเติม

## อธิบาย Code ทีละส่วน

- `paginate_items()`: วน Next Link, จำกัดหน้า และ Deduplicate Record
- `safe_filename()`: แปลงชื่อจาก URL ให้ใช้ได้บน Windows
- `unique_destination()`: สร้าง Path ใหม่เมื่อชื่อไฟล์มีอยู่แล้ว
- `download_file()`: Streaming, Content-Type, Size Limit และ SHA-256
- `download_assets()`: อ่านลิงก์จากหน้า Download แล้วเรียก Downloader
- `write_manifest()`: เขียนรายการไฟล์, Content-Type, Byte Count และ Checksum เป็น CSV

## ผลลัพธ์ที่คาดหวัง

```text
Fetched 4 unique items from 3 pages
Downloaded sample-guide.pdf (... bytes, application/pdf)
Downloaded course-logo.svg (... bytes, image/svg+xml)
```

ถ้ารันซ้ำในโฟลเดอร์เดิม จะได้ชื่อไฟล์เช่น `sample-guide_1.pdf` แทนการเขียนทับไฟล์เดิม

## ข้อผิดพลาดที่พบบ่อย

### วนหน้าไม่จบ

ตรวจ `seen_pages`, `max-pages` และ Next Link ใน HTML อย่าใช้ `while True` โดยไม่มีเงื่อนไขหยุด

### มี Record ซ้ำในผลลัพธ์

ตรวจว่าใช้ Record ID ที่เสถียรหรือไม่ และอย่าใช้ตำแหน่งในหน้าเป็น ID หากข้อมูลอาจทับซ้อน

### `Content-Type` ไม่ตรง

หยุดการดาวน์โหลดและตรวจว่า URL ชี้ไปยังไฟล์ที่ถูกต้อง อย่าบังคับบันทึกไฟล์ด้วยการเปลี่ยนนามสกุลเพื่อให้ผ่านการตรวจ

### File Size เกินกำหนด

เพิ่ม Limit เฉพาะเมื่อเข้าใจความเสี่ยงและได้รับอนุญาต ไม่ควรตั้งเป็นค่าสูงไม่จำกัด

### เปิดไฟล์ PDF ไม่ได้

ตรวจ Checksum, ขนาดไฟล์ และ Content-Type ใน Manifest ไฟล์ตัวอย่างในบทนี้อยู่ที่ `mock_site/static/files/sample-guide.pdf`

## แบบฝึกหัด

1. เปลี่ยน `--max-pages` เป็น `2` แล้วสังเกต Error ว่าข้อมูลอาจยังไม่ครบ
2. เพิ่ม Record ซ้ำในหน้า Pagination แล้วตรวจว่าผลลัพธ์ยังมี ID เดียว
3. ดาวน์โหลดซ้ำสองครั้งและตรวจชื่อไฟล์ที่เติมเลขต่อท้าย
4. เปลี่ยนลิงก์ Download ให้มีนามสกุล `.txt` แล้วสังเกต Content-Type Validation
5. เปิด Manifest และตรวจว่า SHA-256 ของไฟล์มีความยาว 64 ตัวอักษร Hexadecimal

## Checklist

- [ ] รองรับ Next Page Link หรือ Page Parameter
- [ ] มีเงื่อนไขหยุดเมื่อไม่มีข้อมูล
- [ ] มี Maximum Page Limit
- [ ] ป้องกัน URL ซ้ำและ Record ซ้ำ
- [ ] ดาวน์โหลดแบบ Streaming
- [ ] ตรวจ Content-Type และ File Size
- [ ] ใช้ Safe Filename บน Windows
- [ ] ไม่เขียนทับไฟล์เดิม
- [ ] สร้าง SHA-256 Checksum
- [ ] มี Download Manifest

## สรุป

Pagination และ Download ต้องมีขอบเขตและเงื่อนไขหยุดที่ตรวจสอบได้เสมอ การตรวจ Content-Type, ขนาด, ชื่อไฟล์ และ Checksum ช่วยลดความเสี่ยงจากไฟล์ผิดประเภท ไฟล์เสีย และการเขียนทับข้อมูลเดิม
