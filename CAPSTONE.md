# Capstone: Maintainable Data Collection Service

สร้างระบบเก็บข้อมูลจากแหล่งข้อมูลที่ได้รับอนุญาตหนึ่งแหล่ง แล้วส่งออกเป็นข้อมูลที่ทีมธุรกิจใช้ต่อได้

## Requirements

1. บันทึก source, timestamp, record id และ schema ที่ชัดเจน
2. ใช้ API เมื่อมี API ที่อนุญาต ถ้าไม่มีให้ใช้ static/dynamic parser ตามความจำเป็น
3. มี timeout, retry, rate limit, structured logging และ validation
4. มี fixture, mock HTTP response, unit/parser/export/regression tests
5. ส่งออก JSON, CSV และ SQLite อย่างน้อย พร้อม data-quality flags
6. มี scheduled entry point, exit code และ lock file
7. มี README, security note, CI และ release checklist

## Acceptance criteria

- `python -m ruff check .` และ `python -m pytest -q` ผ่าน
- ไม่พบ secret, personal data หรือลิงก์ภายในเสีย
- ทดสอบกับ local fixture ได้โดยไม่ยิงเว็บจริง
- อธิบายข้อจำกัด, source permission, retention และวิธีหยุดงานได้
- ผลลัพธ์ถูกนำไปใช้กับ Excel/Power BI หรือระบบ downstream ได้
