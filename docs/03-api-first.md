# API First

## เป้าหมายการเรียนรู้

เมื่อจบบทนี้ ผู้เรียนจะสามารถ:

- ตัดสินใจว่าเมื่อใดควรใช้ API ก่อนการอ่าน HTML
- อ่าน Endpoint, Method, Parameter, Header และ Response จากเอกสาร API
- ส่ง Request แบบปลอดภัยด้วย Timeout และ User-Agent
- อ่าน JSON และตรวจสอบโครงสร้างข้อมูลเบื้องต้น
- เข้าใจ Authentication, API Key, Pagination และ Rate Limit
- แยก Configuration ออกจาก Code และไม่ Commit Secret
- Export ผลลัพธ์เป็น JSON, CSV และ Excel

## สิ่งที่ต้องเตรียม

- Python 3.11 หรือใหม่กว่า
- ติดตั้ง Dependencies ตาม [Phase 1](01-installation.md)
- ความเข้าใจเรื่อง HTTP และ JSON จาก [Phase 2](02-web-basics.md)
- อินเทอร์เน็ตสำหรับเรียก Public Test API เมื่อทดสอบจริง

ตัวอย่างนี้ใช้ [JSONPlaceholder](https://jsonplaceholder.typicode.com/) ซึ่งเป็นบริการทดสอบสาธารณะ ข้อมูลเป็นข้อมูลสังเคราะห์และตัวอย่างไม่ใช้ข้อมูลส่วนตัวหรือ API Key จริง

## API First คืออะไร

API First คือการตรวจสอบก่อนว่าเจ้าของระบบมีช่องทาง API ที่อนุญาตให้โปรแกรมเรียกใช้ข้อมูลหรือไม่ หากมี API ที่เหมาะสม ควรใช้ API ก่อนการ Scraping HTML เพราะข้อมูลมีโครงสร้างชัดเจน ลดการพึ่งพา CSS Selector และมักกำหนดวิธีใช้กับ Rate Limit ไว้ชัดเจนกว่า

การมี Endpoint ที่เข้าถึงได้จาก Browser ไม่ได้แปลว่าอนุญาตให้ใช้งานได้ทุกกรณี ต้องตรวจเอกสาร Terms, Authentication, Rate Limit และสิทธิ์ของแหล่งข้อมูลก่อนเสมอ

## Decision Tree

```text
ต้องการข้อมูลจากเว็บไซต์
├── มี Official API และอนุญาตให้ใช้
│   └── ใช้ API
├── ไม่มี Official API แต่หน้าเว็บเรียก Public JSON Endpoint
│   └── ตรวจสอบสิทธิ์และข้อกำหนดก่อนใช้
├── ข้อมูลอยู่ใน HTML ที่ Server ส่งมา
│   └── requests + BeautifulSoup
└── ข้อมูลเกิดหลัง JavaScript ทำงาน
    └── ตรวจ API ก่อน แล้วใช้ Playwright หรือ Selenium เมื่อจำเป็น
```

## คำศัพท์ API

| คำศัพท์ | ความหมาย |
| --- | --- |
| API Documentation | เอกสารอธิบายวิธีเรียก API |
| Endpoint | URL สำหรับข้อมูลหรือการทำงานหนึ่งประเภท |
| Method | วิธีดำเนินการ เช่น `GET` หรือ `POST` |
| Parameter | ค่าที่ส่งไปกำหนดหรือกรองผลลัพธ์ |
| Header | ข้อมูลกำกับ Request เช่น `Accept` หรือ `User-Agent` |
| Authentication | การยืนยันตัวตนของผู้เรียก |
| API Key | รหัสที่ระบบออกให้เพื่อระบุหรือจำกัดการใช้งาน |
| Pagination | การแบ่งผลลัพธ์เป็นหลายหน้า |
| Rate Limit | ข้อจำกัดจำนวน Request ในช่วงเวลาหนึ่ง |
| JSON Parsing | การแปลง JSON เป็นโครงสร้างที่โปรแกรมใช้งานได้ |

## อ่าน API Documentation

ก่อนเขียน Code ให้บันทึกข้อมูลต่อไปนี้:

1. **Endpoint**: เช่น `https://jsonplaceholder.typicode.com/todos`
2. **Method**: ตัวอย่างนี้ใช้ `GET` เพื่ออ่านข้อมูล
3. **Parameter**: `_limit=5` ขอข้อมูลจำนวนเล็กน้อยสำหรับการทดลอง
4. **Header**: ใช้ `Accept: application/json` และ User-Agent ที่สื่อความหมาย
5. **Authentication**: ตัวอย่างนี้ไม่ต้องใช้ API Key
6. **Response**: คาดหวัง JSON Array ที่แต่ละรายการมี `userId`, `id`, `title` และ `completed`
7. **Rate Limit**: อ่านข้อกำหนดของ API จริงก่อนตั้ง Schedule หรือเพิ่มจำนวน Request

อย่าคาดเดา Endpoint จาก URL ที่เห็นใน Developer Tools แล้วนำไปใช้กับระบบจริงโดยไม่ตรวจสอบสิทธิ์

## Authentication และ API Key

API บางระบบต้องใช้ API Key, OAuth Token หรือวิธียืนยันตัวตนอื่น หากต้องใช้ Secret:

- เก็บไว้ใน Environment Variable หรือไฟล์ `.env` ที่อยู่ใน `.gitignore`
- เก็บเฉพาะชื่อ Configuration ที่ไม่มีค่า Secret จริงใน `.env.example`
- ห้ามพิมพ์ Token ใน Log, Screenshot, Error message หรือ Commit
- หยุดเมื่อได้รับ `401 Unauthorized` หรือ `403 Forbidden` และตรวจสอบสิทธิ์ ไม่ Retry เพื่อหลบการควบคุม

ตัวอย่างการอ่านค่าแบบไม่เปิดเผย Secret:

```python
import os

api_key = os.getenv("API_KEY")
if api_key:
    headers = {"X-API-Key": api_key}
```

ตัวอย่าง Phase นี้ไม่ต้องใช้ `API_KEY` จึงไม่ควรสร้างค่าปลอมแล้วส่งไปยัง JSONPlaceholder

## Pagination และ Rate Limit

API อาจแบ่งข้อมูลด้วย:

- `page` และ `page_size`
- `offset` และ `limit`
- Cursor เช่น `next_cursor`
- Link ใน Response Header

ควรเริ่มจากจำนวนข้อมูลน้อย ตั้ง Maximum Page/Record Count และหยุดเมื่อไม่มีข้อมูลหรือถึงขีดจำกัดที่กำหนด ปฏิบัติตาม Rate Limit ของ API และเพิ่ม Delay เมื่อเอกสารระบุไว้

ตัวอย่างนี้ใช้ `_limit` เพื่อลดจำนวนข้อมูลที่ขอ ไม่ได้วน Pagination อัตโนมัติ เพราะบท Pagination อยู่ใน Phase 5

## Environment Variables

ไฟล์ `.env.example` แสดงชื่อ Configuration ที่ผู้เรียนสามารถคัดลอกเป็น `.env` ได้:

```powershell
Copy-Item .env.example .env
```

ห้าม Commit `.env` ไฟล์จริง เพราะอาจมี API Key หรือค่าเฉพาะเครื่อง Script จะใช้ค่าใน Environment หรือ `.env` ผ่าน `python-dotenv` และมีค่า Default ที่ปลอดภัยสำหรับ Public Test API

## ขั้นตอนปฏิบัติบน Windows PowerShell

จากโฟลเดอร์ Repository ให้ Activate Environment แล้วรัน:

```powershell
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
python .\examples\03_api_first\api_first.py --limit 5
```

ผลลัพธ์จะอยู่ที่ `output/api_first/`:

```text
output/api_first/todos.json
output/api_first/todos.csv
output/api_first/todos.xlsx
```

หากต้องการเปลี่ยนจำนวนรายการโดยไม่แก้ `.env`:

```powershell
python .\examples\03_api_first\api_first.py --limit 3
```

## ตัวอย่าง Response JSON

ข้อมูลจาก API มีรูปแบบประมาณนี้:

```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
  }
]
```

Script จะทำความสะอาดชื่อ Field เป็น `user_id` และ `record_id` พร้อมเพิ่ม `source_url` กับ `scraped_at` ตอน Export เพื่อให้ตรวจสอบย้อนกลับได้

## อธิบาย Code ทีละส่วน

- `load_dotenv()`: โหลด Configuration จาก `.env` หากมี
- `fetch_todos()`: ส่ง `GET` พร้อม Timeout, Parameter และ Headers
- `validate_records()`: ตรวจว่า Response เป็น List ของ Object และมี Field ที่จำเป็น
- `build_export_records()`: เพิ่ม Metadata และจัด Schema สำหรับผลลัพธ์
- `export_records()`: เขียน JSON, CSV และ Excel แยกจาก Logic การดึงข้อมูล
- `main()`: อ่าน Argument, เรียกขั้นตอนตามลำดับ และแสดงตำแหน่งไฟล์ผลลัพธ์

การแยกส่วนนี้ทำให้สามารถทดสอบ Parser/Exporter ด้วยข้อมูลจำลองได้ โดยไม่ต้องยิง API จริงทุกครั้ง

## การจัดการ Error

ตัวอย่างจัดการกรณีต่อไปนี้:

- Timeout หรือเชื่อมต่อไม่ได้: แสดงคำแนะนำให้ตรวจอินเทอร์เน็ตและ Endpoint
- HTTP `401`/`403`: หยุดและตรวจสิทธิ์ ไม่ Retry เพื่อหลบ Access Control
- HTTP `4xx`/`5xx`: แสดง Status Code และหยุดอย่างชัดเจน
- JSON ไม่ถูกต้อง: แจ้งว่า Response ไม่ใช่ JSON ที่คาดหวัง
- Schema ไม่ตรง: แจ้ง Field ที่จำเป็นหายไป
- Export Error: แจ้ง Path และตรวจสิทธิ์การเขียนไฟล์

ระบบไม่ใช้ Retry แบบไม่จำกัด และไม่ได้เปลี่ยน User-Agent, หมุน Proxy หรือหลบระบบป้องกัน Bot

## ผลลัพธ์ที่คาดหวัง

เมื่อรันสำเร็จจะเห็นข้อความลักษณะนี้:

```text
Fetched 5 records from https://jsonplaceholder.typicode.com/todos
JSON: output\api_first\todos.json
CSV: output\api_first\todos.csv
Excel: output\api_first\todos.xlsx
```

## ข้อผิดพลาดที่พบบ่อย

### `ModuleNotFoundError`

ตรวจสอบว่า Activate `.venv` แล้วและติดตั้ง Dependencies:

```powershell
python -m pip install -e ".[dev]"
```

### API เรียกไม่ได้หรือ Timeout

ตรวจสอบอินเทอร์เน็ต, Proxy, Firewall และค่า `API_BASE_URL` อย่าเพิ่มความถี่ Request เพื่อแก้ Timeout

### ได้ `401` หรือ `403`

หยุดการเรียกและตรวจเอกสาร Authentication/Permission ของ API ห้ามพยายามหลบ Login หรือ Access Control

### เปิด Excel ไม่ได้

ตรวจสอบว่า `openpyxl` ติดตั้งแล้วและไฟล์ `.xlsx` ไม่ได้ถูกเปิดล็อกโดยโปรแกรมอื่น

### `.env` ถูกแสดงใน Git

ตรวจสอบ `.gitignore` และใช้:

```powershell
git status --short --ignored
```

ถ้า Secret เคยถูก Commit แล้ว ต้องยกเลิก/เปลี่ยน Secret ตามขั้นตอนของผู้ให้บริการ ไม่ใช่เพียงลบไฟล์จาก Working Tree

## แบบฝึกหัด

1. เปลี่ยน `API_LIMIT` เป็น `3` แล้วเปรียบเทียบจำนวนแถวใน CSV
2. เปิด `todos.json` แล้วระบุว่า Field ใดมาจาก API และ Field ใดเป็น Metadata
3. ทดลองใช้ `--limit 1` และตรวจว่าทั้งสามไฟล์มีจำนวน Record เท่ากัน
4. อ่าน API Documentation ของบริการสาธารณะอื่น แล้วเขียนตาราง Endpoint/Method/Parameter/Authentication ก่อนใช้
5. อธิบายว่าทำไม `401` และ `403` ไม่ควรถูก Retry แบบไม่จำกัด

## Checklist

- [ ] ตรวจสอบ Official API ก่อนเลือก Scraping
- [ ] ระบุ Endpoint และ Method ได้
- [ ] เข้าใจ Parameter, Header และ JSON Response
- [ ] เข้าใจ Authentication และการเก็บ API Key
- [ ] มี Timeout และ Error Handling
- [ ] ตรวจสอบ Status Code และ Schema
- [ ] จำกัดจำนวนข้อมูลที่ขอ
- [ ] มี `.env.example` แต่ไม่มี Secret จริง
- [ ] Export ผลลัพธ์เป็น JSON, CSV และ Excel
- [ ] ไม่ Retry เมื่อไม่มีสิทธิ์

## สรุป

API First ช่วยให้เริ่มจากช่องทางข้อมูลที่มีโครงสร้างและข้อกำหนดชัดเจน การใช้งานจริงต้องตรวจสิทธิ์, Rate Limit, Schema และความลับก่อนเสมอ หากไม่มี API ที่เหมาะสมจึงค่อยพิจารณา Static Scraping หรือ Browser Automation ตามลักษณะหน้าเว็บ
