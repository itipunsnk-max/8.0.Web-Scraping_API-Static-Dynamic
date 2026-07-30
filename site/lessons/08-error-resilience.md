# Phase 8: ระบบรองรับ Error และ Resilience

Phase นี้รวมแนวทางที่ต้องใช้ซ้ำในงานจริงไว้ใน `src/web_scraping_course` ได้แก่ Timeout, Retry, Exponential Backoff, Rate Limiting, Logging, Validation, Duplicate Handling, Safe Filename, Configuration และ Custom Exceptions

## นโยบาย Retry

ตัวอย่างนี้ Retry เฉพาะความผิดพลาดชั่วคราว:

- Request timeout หรือ connection error
- HTTP `408`, `425`, `429`
- HTTP `500`, `502`, `503`, `504`

จะไม่ Retry ทุก Error แบบเหมารวม เช่น `400`, `401`, `403`, `404`, Parse Error หรือ Validation Error เพราะการ Retry ไม่ได้แก้สาเหตุและอาจเพิ่มภาระให้เว็บไซต์

## โครงสร้าง Utility

| ไฟล์ | หน้าที่ |
| --- | --- |
| `exceptions.py` | แยก Network, HTTP, Parse, Validation และ Export errors |
| `config.py` | Dataclass configuration พร้อม validation และอ่านค่าที่ไม่ใช่ Secret จาก Environment |
| `retry.py` | Retry แบบ bounded และ exponential backoff |
| `rate_limiter.py` | กำหนดช่วงห่างขั้นต่ำระหว่าง Request |
| `http_client.py` | HTTP client ที่รวม timeout, retry, rate limit และ response-size limit |
| `validators.py` | Required fields, unique key, Content-Type และขนาดข้อมูล |
| `utils.py` | Safe filename, unique destination และ duplicate handling |
| `logging_config.py` | Console/file logging โดยไม่เขียน query หรือ Secret ลง Log |

## ตัวอย่างการใช้งาน

เปิด Local Mock Website:

```powershell
python -m http.server 8000 --directory mock_site/static
```

รัน Resilient HTTP Client:

```powershell
.\.venv\Scripts\python.exe .\examples\10_resilience\resilient_http.py
```

ปรับ Timeout, Retry และ Rate Limit:

```powershell
.\.venv\Scripts\python.exe .\examples\10_resilience\resilient_http.py --timeout 5 --max-retries 2 --min-interval 0.5
```

ตัวอย่างจะเขียน log ที่ `output/resilient_http.log` และไม่บันทึก Cookie, Token, Password หรือ query value

## ทดสอบ Utility

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests\test_phase8_resilience.py -q
```

การทดสอบใช้ fake sleep และ mock HTTP response เพื่อไม่ต้องรอจริงหรือยิง Request ไปยังเว็บไซต์ภายนอก

## ข้อควรระวัง

- Retry ต้องมีจำนวนครั้งและเพดาน Backoff เสมอ
- Rate Limit ไม่ใช่สิทธิ์ให้ข้าม Terms, robots.txt หรือ Access Control
- ตรวจ Schema และ Duplicate ก่อน Export
- จำกัดขนาด Response/ไฟล์เพื่อป้องกันการใช้หน่วยความจำหรือพื้นที่เกินคาด
- Log เฉพาะข้อมูลที่จำเป็นและทำให้ URL ปลอดภัยก่อนบันทึก
- แยก Error ที่แก้ได้ด้วย Retry ออกจาก Error ที่ต้องแก้ด้วย Code, Selector หรือสิทธิ์

## Checklist จบ Phase 8

- [ ] ใช้ Custom Exceptions แยกประเภท Error
- [ ] ตั้ง Timeout และ bounded Retry
- [ ] ใช้ Exponential Backoff ที่มีเพดาน
- [ ] ใช้ Rate Limiter
- [ ] ตรวจ Status, Content-Type, ขนาด และ Schema
- [ ] จัดการ Duplicate และ Safe Filename
- [ ] ตั้งค่า Logging โดยไม่เปิดเผย Secret
- [ ] ทดสอบ Error path โดยไม่ยิงเว็บจริง
