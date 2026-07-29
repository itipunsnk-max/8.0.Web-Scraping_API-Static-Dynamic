# Phase 10: Export และ Data Pipeline

Phase นี้เปลี่ยนผลจากการ Extract ให้เป็นข้อมูลที่นำไปใช้ต่อได้ โดยแยก Raw data ออกจาก Processed data, กำหนด Schema เดียวกัน และ Export เป็น JSON, CSV, Excel และ SQLite

## Workflow

```text
Website / API
    ↓
Extract
    ↓
Validate + Normalize
    ↓
Store raw
    ↓
Deduplicate + Transform
    ↓
Store processed
    ↓
JSON / CSV / Excel / SQLite / Power BI
```

## Schema

| Field | ความหมาย |
| --- | --- |
| `source_url` | แหล่งข้อมูลที่ได้รับอนุญาต |
| `scraped_at` | เวลาเก็บข้อมูลแบบ ISO 8601 พร้อม timezone |
| `record_id` | Key สำหรับ deduplicate และ SQLite upsert |
| `name` | ชื่อที่ผ่านการ normalize |
| `value` | ค่าตัวเลขที่แปลงแล้ว หรือ `null` เมื่อไม่มี/ไม่ถูกต้อง |
| `status` | สถานะของ record |
| `raw_value` | ค่าต้นฉบับก่อน numeric conversion |
| `data_quality_flag` | `ok`, `missing_value`, `invalid_value`, `missing_name` หรือ flag ที่เกี่ยวข้อง |

## รันตัวอย่างบน Windows

```powershell
.\.venv\Scripts\python.exe .\examples\10_excel_export\data_pipeline.py
```

ผลลัพธ์อยู่ใน `output/data_pipeline`:

- `raw/records.json` เก็บ input ก่อน transform
- `processed/records.json`
- `processed/records.csv` เป็น UTF-8 with BOM เพื่อเปิดใน Excel บน Windows ได้ง่าย
- `processed/records.xlsx`
- `processed/records.sqlite3`

ตัวอย่างมี duplicate `p10-002` และ missing value เพื่อให้เห็นผลของ `duplicate_count` และ `data_quality_flag`

## SQLite และ Incremental Load

ตาราง `records` ใช้ `record_id` เป็น Primary Key การรัน pipeline ซ้ำจะใช้ `ON CONFLICT(record_id) DO UPDATE` เพื่ออัปเดต record เดิม ไม่เพิ่มแถวซ้ำ และสามารถต่อยอดเป็น watermark หรือ scraped timestamp ได้ในระบบจริง

## Encoding, Date/Time และ Missing Values

- CSV ใช้ UTF-8 with BOM (`utf-8-sig`) เพื่อรองรับ Excel บน Windows
- JSON และ raw data ใช้ UTF-8 พร้อม `ensure_ascii=False`
- เวลาใช้ ISO 8601 และ timezone UTC
- Missing numeric value เก็บเป็น `null` ใน `value` และเก็บค่าต้นฉบับไว้ใน `raw_value`
- ไม่แทน missing ด้วยศูนย์ เพราะศูนย์กับไม่มีข้อมูลมีความหมายต่างกัน

## Raw กับ Processed

Raw data ควรเก็บเท่าที่จำเป็นและอยู่ภายใต้สิทธิ์/retention ที่อนุมัติ ส่วน Processed data ควรผ่าน schema validation, numeric conversion และ duplicate handling แล้ว ก่อนส่งต่อให้ Excel, SQLite หรือ Power BI

## ทดสอบ

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests\test_phase10_pipeline.py -q
```

การทดสอบตรวจทุก output format, duplicate handling, missing value และ incremental upsert โดยใช้ temporary directory

## Checklist จบ Phase 10

- [ ] กำหนด Schema และ field types ชัดเจน
- [ ] แยก Raw และ Processed data
- [ ] Normalize numeric/date/missing values
- [ ] กำหนด Duplicate key และวิธีจัดการ
- [ ] Export JSON, CSV, Excel และ SQLite
- [ ] รองรับ UTF-8 และ timezone
- [ ] ทดสอบ incremental load และตรวจจำนวน record
- [ ] ตรวจสิทธิ์และ retention ก่อนเก็บข้อมูลจริง
