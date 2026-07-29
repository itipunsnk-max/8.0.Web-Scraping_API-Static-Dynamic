# Static Website ด้วย Requests และ BeautifulSoup

## เป้าหมายการเรียนรู้

เมื่อจบบทนี้ ผู้เรียนจะสามารถ:

- ส่ง `GET` Request ไปยัง Static Website ด้วย `requests`
- กำหนด Timeout, User-Agent และตรวจ Status Code
- ใช้ `raise_for_status()` และจัดการ Error เบื้องต้น
- อ่าน Response Text, Content และ Encoding
- ใช้ `BeautifulSoup` กับ `find()`, `find_all()`, `select()` และ `select_one()`
- ดึง Text, Attribute, URL, ตาราง และหลายรายการ
- ทำความสะอาดราคาและสร้าง Data Quality Flag เมื่อข้อมูลหาย
- Export ผลลัพธ์เป็น CSV และ Excel

## สิ่งที่ต้องเตรียม

- Python 3.11 หรือใหม่กว่า
- Dependencies จาก [Phase 1](01-installation.md)
- ความเข้าใจ CSS Selector จาก [Phase 2](02-web-basics.md)
- เปิด Local Mock Website แทนเว็บไซต์ภายนอก

## แนวคิดสำคัญ

### Static Website คืออะไร

Static Website คือหน้าเว็บที่ข้อมูลหลักอยู่ใน HTML ที่ Server ส่งกลับมาโดยตรง การใช้ `requests` จึงสามารถอ่าน HTML ได้โดยไม่ต้องเปิด Browser Automation ก่อน อย่างไรก็ตามควรตรวจสอบ API และสิทธิ์ของเว็บไซต์ก่อนเสมอ

### ลำดับการทำงาน

```text
URL
  ↓
requests.get(timeout, headers)
  ↓
ตรวจ Status และอ่าน Response
  ↓
BeautifulSoup สร้างโครงสร้าง HTML
  ↓
เลือก Element ด้วย CSS Selector
  ↓
ทำความสะอาดและตรวจข้อมูล
  ↓
Export CSV / Excel
```

## คำศัพท์และ API ที่ใช้

| คำศัพท์/คำสั่ง | หน้าที่ |
| --- | --- |
| `requests.get()` | ส่ง HTTP GET Request |
| `timeout` | จำกัดเวลารอ Response |
| `status_code` | ตรวจผลลัพธ์ HTTP |
| `raise_for_status()` | เปลี่ยน HTTP Error ให้เป็น Exception |
| `response.text` | อ่าน Body เป็นข้อความตาม Encoding |
| `response.content` | อ่าน Body เป็น Bytes |
| `response.encoding` | Encoding ที่ใช้ถอดรหัสข้อความ |
| `BeautifulSoup` | Parser สำหรับอ่านโครงสร้าง HTML |
| `find()` | หา Element แรกที่ตรงเงื่อนไข |
| `find_all()` | หา Element ทุกตัวที่ตรงเงื่อนไข |
| `select()` | เลือกหลาย Element ด้วย CSS Selector |
| `select_one()` | เลือก Element แรกด้วย CSS Selector |
| `get_text()` | อ่าน Text และตัดช่องว่างส่วนเกิน |
| `urljoin()` | รวม URL ต้นทางกับ Relative URL |

## ขั้นตอนปฏิบัติ

### 1. เปิด Local Mock Store

จากโฟลเดอร์ Repository ใช้ **Windows PowerShell**:

```powershell
python -m http.server 8000 --directory mock_site/static
```

เปิดตรวจหน้าเว็บก่อนที่:

```text
http://127.0.0.1:8000/products.html
```

หน้านี้มี Product Card, ชื่อสินค้า, ราคา, Availability, Link และ Inventory Table

### 2. ตรวจ Selector ใน Browser

เปิด Chrome Developer Tools แล้วตรวจ Selector เหล่านี้:

```text
.product-card
.product-name
.product-price
.availability
.product-link
#inventory-table tbody tr
```

Selector ทั้งหมดถูกเก็บรวมไว้ในตัวแปร `SELECTORS` ของ Parser ไม่กระจายอยู่ทั่ว Code

### 3. รัน Static Scraper

เปิด PowerShell อีกหน้าต่างหนึ่ง แล้วรัน:

```powershell
python .\examples\04_static_page\static_scraper.py
```

หรือระบุ URL, Timeout และโฟลเดอร์ผลลัพธ์เอง:

```powershell
python .\examples\04_static_page\static_scraper.py `
  --url http://127.0.0.1:8000/products.html `
  --timeout 10 `
  --output-dir output\static_page
```

## ตัวอย่าง Code

ส่วนสำคัญของ Parser มีลักษณะดังนี้:

```python
cards = soup.select(SELECTORS["product_card"])
for card in cards:
    name_element = card.select_one(SELECTORS["product_name"])
    name = name_element.get_text(" ", strip=True) if name_element else None
```

ถ้า Element ไม่พบ ต้องไม่เรียก `.get_text()` กับ `None` โดยตรง ควรบันทึก Warning และเพิ่ม `data_quality_flag` เพื่อให้ผู้ใช้รู้ว่าข้อมูลรายการนั้นไม่สมบูรณ์

## ผลลัพธ์ที่คาดหวัง

Script จะสร้าง:

```text
output/static_page/products.csv
output/static_page/products.xlsx
output/static_page/inventory.csv
output/static_page/inventory.xlsx
```

ตัวอย่างข้อมูล Product:

| record_id | name | price | availability | data_quality_flag |
| --- | --- | ---: | --- | --- |
| store-001 | Wireless Mouse | 1299.00 | มีสินค้า | ok |
| store-002 | Mechanical Keyboard | 2490.00 | สินค้าหมด | ok |
| store-003 | Desk Lamp | 890.00 | ว่าง | missing_availability |

ราคาใน HTML เช่น `฿1,299.00` จะถูกแปลงเป็นตัวเลข `1299.00` ส่วน URL แบบ `/products/mouse` จะถูกแปลงเป็น URL เต็มโดยอ้างอิงจาก Source URL

## อธิบาย Code ทีละส่วน

- `fetch_html()`: ส่ง Request, ตั้ง Timeout/User-Agent, ตรวจ Status และเลือก Encoding
- `parse_products()`: ใช้ `select()` วน Product Card และใช้ `select_one()` อ่าน Field ภายใน Card
- `parse_inventory_table()`: ใช้ `select()` กับ `tbody tr` และอ่าน Cell ในแต่ละแถว
- `clean_price()`: ลบสัญลักษณ์สกุลเงินและ Comma ก่อนแปลงเป็น `float`
- `absolute_url()`: ใช้ `urljoin()` ป้องกันการต่อ URL ด้วย String แบบเปราะบาง
- `export_records()`: แยก Logic การ Export ออกจาก Logic การดึงข้อมูล
- `data_quality_flag`: ระบุ `ok` หรือชื่อ Field ที่ขาด เช่น `missing_availability`

## Response Text, Content และ Encoding

- `response.text` เหมาะกับการส่งต่อให้ HTML Parser เป็นข้อความ
- `response.content` เป็น Bytes ใช้เมื่อจำเป็นต้องควบคุมการ Decode เอง
- `response.encoding` ระบุ Encoding ที่ Requests ใช้ หากไม่ชัดเจนสามารถพิจารณา `response.apparent_encoding` แต่ควรตรวจผลกับข้อมูลจริง

ห้ามแก้ Encoding แบบเดาสุ่มจนข้อมูลภาษาไทยเสีย ควรตรวจ Header, HTML Meta และผลลัพธ์ที่อ่านได้

## ข้อผิดพลาดที่พบบ่อย

### `ConnectionError` หรือ `Timeout`

ตรวจว่า Local Server ยังทำงานอยู่และ Port ตรงกัน อย่าแก้ด้วยการตัด `timeout` ออก เพราะจะทำให้โปรแกรมค้างได้

### `404 Not Found`

ตรวจ Path ว่าใช้ `products.html` และเปิด Server ด้วย `--directory mock_site/static`

### `403 Forbidden`

หยุดและตรวจสิทธิ์ของเว็บไซต์ ห้ามเปลี่ยน User-Agent เพื่อหลบการตรวจจับหรือพยายามข้าม Access Control

### `select()` ได้รายการว่าง

เปิด Elements ตรวจโครงสร้าง HTML และเปรียบเทียบกับ `SELECTORS` หากหน้าเว็บเปลี่ยน ให้แก้ Selector ในจุดรวมเดียวและเพิ่ม Test/Fixture ใน Phase ที่เกี่ยวข้อง

### ราคาเป็น `None`

ตรวจว่า Element มีจริงและรูปแบบตัวเลขที่ใช้ใน `clean_price()` รองรับหรือไม่ อย่าแปลงค่าที่ไม่แน่ใจเป็นศูนย์ เพราะจะทำให้ข้อมูลผิด

### Excel Export ไม่สำเร็จ

ติดตั้ง `openpyxl` และตรวจสิทธิ์เขียนโฟลเดอร์ผลลัพธ์:

```powershell
python -m pip install openpyxl
```

## แบบฝึกหัด

1. เปลี่ยน Selector ของราคาให้ชี้ไปยัง Element ที่ไม่มีอยู่ แล้วสังเกต Log และ Data Quality Flag
2. เพิ่ม Product Card ใหม่ใน Local Mock Page แล้วตรวจว่าจำนวนแถวใน CSV เพิ่มขึ้น
3. ทดลองเปลี่ยน Link จาก Absolute เป็น Relative แล้วตรวจ URL ในผลลัพธ์
4. เพิ่มคอลัมน์ `category` ใน HTML และปรับ Parser ให้ดึงข้อมูลเพิ่ม
5. เปรียบเทียบ `response.text` กับ `response.content` ใน Python File

## Checklist

- [ ] ใช้ `requests.get()` พร้อม Timeout
- [ ] ตรวจ Status Code และเรียก `raise_for_status()`
- [ ] ระบุ User-Agent ที่เหมาะสม
- [ ] ใช้ BeautifulSoup Parser
- [ ] ทดลอง `find()`, `find_all()`, `select()` และ `select_one()`
- [ ] ดึง Text และ Attribute ได้
- [ ] Normalize Relative URL ได้
- [ ] ทำความสะอาดราคาและ Text ได้
- [ ] ตรวจ Element ที่หายและสร้าง Quality Flag
- [ ] Export CSV และ Excel ได้

## สรุป

Static Scraping เริ่มจากการขอ HTML อย่างสุภาพ ตรวจ Response แล้วใช้ Selector ที่ดูแลได้ง่ายเพื่อแปลงข้อมูลเป็น Schema ที่ชัดเจน การใช้ Local Mock Website ทำให้ฝึกซ้ำได้โดยไม่ผูกกับการเปลี่ยนแปลงของเว็บไซต์ภายนอก
