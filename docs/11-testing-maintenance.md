# Phase 11: Testing และ Maintenance

Phase นี้ทำให้ Scraper ตรวจสอบซ้ำได้โดยไม่ต้องยิงเว็บไซต์จริงทุกครั้ง และเตรียมรับมือเมื่อ HTML, Selector, API Schema หรือจำนวน Record เปลี่ยน

## Test Pyramid สำหรับ Web Scraping

1. Unit test ของ clean/normalize/validate function
2. Parser test ด้วย HTML/JSON fixture ที่ commit ได้
3. Mock HTTP response สำหรับ status, timeout และ response body
4. Export test ตรวจ schema, encoding และไฟล์ปลายทาง
5. Regression test เก็บ behavior ที่เคยถูกต้องไว้
6. End-to-end test กับ Local Mock Website เฉพาะจุดที่จำเป็น

หลักสำคัญคือ **ไม่ยิงเว็บไซต์จริงทุกครั้งที่รัน test** เพราะผลลัพธ์อาจเปลี่ยน ช้า จำกัดความถี่ และสร้างภาระให้เจ้าของระบบ

## Fixtures และ Mock

ไฟล์ใน `tests/fixtures` เป็นข้อมูลสังเคราะห์สำหรับทดสอบ:

- `static_products.html` สำหรับ parser และ inventory table
- `api_todos.json` สำหรับ JSON schema
- `responses` ใช้จำลอง HTTP 200 และ Timeout โดยไม่ออกอินเทอร์เน็ต

## รัน Test

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

หาก Windows มี permission จำกัดที่ pytest temporary directory ให้ใช้ terminal ที่ได้รับสิทธิ์เหมาะสม หรือกำหนด `--basetemp` ไปยัง temporary directory ที่ผู้ใช้เขียนได้

## Maintenance Utilities

`src/web_scraping_course/maintenance.py` มี helper สำหรับ:

- `first_matching()` — selector fallback แบบกำหนดลำดับชัดเจน
- `validate_record_count()` — fail fast เมื่อจำนวน record ต่ำ/สูงผิดปกติ
- `schema_issues()` — รายงาน required field ที่หายไป
- `snapshot_digest()` และ `compare_snapshots()` — ตรวจ HTML/JSON เปลี่ยนโดยไม่เก็บ payload ลง log

## กรณีที่ต้องทำให้ Test Fail

- Selector หายหรือเปลี่ยนจนไม่มี product card
- ราคากลายเป็นค่าว่างหรือแปลง numeric ไม่ได้
- จำนวน Record ลดลง/เพิ่มขึ้นผิดปกติ
- API เปลี่ยน field ที่จำเป็น
- HTTP status เป็น `401`, `403`, `429` หรือ `5xx` ตาม policy
- Export schema เปลี่ยนโดยไม่มีการปรับ downstream

## Fail Fast กับ Graceful Degradation

- **Fail fast** เมื่อข้อมูลไม่มี key สำคัญ, สิทธิ์ผิดปกติ หรือ schema ใช้ต่อไม่ได้
- **Graceful degradation** เมื่อ field ที่ไม่สำคัญหาย โดยเก็บ `data_quality_flag`, log และแจ้งเตือน
- อย่าปล่อยข้อมูลเสียเข้า downstream โดยไม่ติดธงคุณภาพ

## Change Detection และ Alert

เมื่อพบความเปลี่ยนแปลง ให้บันทึกเฉพาะ metadata ที่จำเป็น เช่น digest เดิม/ใหม่, จำนวน record, schema issue และเวลา แล้วแจ้งผู้ดูแลให้ตรวจ snapshot อย่างเหมาะสม หลีกเลี่ยงการส่งข้อมูลส่วนบุคคลหรือ payload ทั้งก้อนไปใน Alert

## Checklist Maintenance

- [ ] มี fixture สำหรับ HTML และ JSON ที่สำคัญ
- [ ] มี mock response สำหรับ success, timeout และ status ผิดปกติ
- [ ] Parser มี test เมื่อ selector หาย
- [ ] Validation มี test เมื่อ required field หรือ record count ผิด
- [ ] Export มี test เรื่อง schema, encoding และจำนวนแถว
- [ ] มี regression test สำหรับ bug ที่เคยเกิด
- [ ] มี selector fallback ที่จำกัดและมีเจ้าของดูแล
- [ ] มี snapshot/change detection โดยไม่เก็บข้อมูลลับใน log
- [ ] ตั้งขั้นตอน review เมื่อ Terms, Schema หรือ Website เปลี่ยน
