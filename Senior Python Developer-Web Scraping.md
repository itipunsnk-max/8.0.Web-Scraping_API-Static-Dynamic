คุณทำหน้าที่เป็น Senior Python Developer, Technical Writer และ Instructor ด้าน Web Scraping

## เป้าหมายโครงการ

สร้าง GitHub Repository ชื่อ:

`web-scraping-zero-to-practical`

Repository นี้ต้องเป็นคู่มือภาษาไทยสำหรับผู้เริ่มต้นที่ยังไม่เคยเขียน Web Scraping มาก่อน ให้สามารถเรียนตั้งแต่พื้นฐานจนสร้างระบบ Web Scraping ที่ใช้งานจริงได้อย่างปลอดภัย มีจริยธรรม ดูแลรักษาง่าย และนำข้อมูลไปใช้กับ CSV, Excel, JSON, SQLite และ Power BI ได้

แหล่งเนื้อหาหลักที่ใช้เป็นแนวทาง:

`https://automatetheboringstuff.com/3e/chapter13.html`

ให้เขียนเนื้อหาใหม่ด้วยคำอธิบายของเราเอง ห้ามคัดลอกข้อความยาวจากแหล่งต้นฉบับ และให้ระบุแหล่งอ้างอิงในเอกสาร References

---

# หลักการสำคัญของ Repository

ทุก Use case ต้องดำเนินการตามลำดับนี้:

1. ตรวจสอบก่อนว่าเว็บไซต์มี API หรือไม่
2. ถ้ามี API ให้ใช้ API ก่อน Web Scraping
3. ถ้าเป็น Static Website ให้ใช้ `requests` และ `BeautifulSoup`
4. ถ้าเป็น Dynamic Website ให้ใช้ `Playwright` เป็นตัวเลือกหลัก และอธิบาย `Selenium` เป็นทางเลือก
5. ตรวจสอบ Terms of Service, Privacy Policy, Copyright และ `robots.txt`
6. จำกัดความถี่ในการส่ง Request และไม่สร้างภาระต่อ Server
7. เตรียมระบบรับมือเมื่อ HTML, CSS Selector หรือหน้าเว็บไซต์เปลี่ยนโครงสร้าง
8. ห้ามทำตัวอย่างที่หลบ CAPTCHA, Authentication, Access Control หรือระบบป้องกัน Bot
9. ห้ามเก็บ Password, Token, Cookie หรือ Secret ลง GitHub
10. ตัวอย่างทั้งหมดต้องใช้เว็บไซต์สาธารณะ เว็บไซต์ทดลอง หรือ Local Mock Website ที่อนุญาตให้ฝึกได้

---

# กลุ่มเป้าหมาย

ผู้เรียนมีพื้นฐานดังนี้:

* ใช้ Windows
* ใช้ VS Code
* ใช้ Python ได้เล็กน้อยหรือไม่เคยใช้
* ยังไม่เข้าใจ HTML, CSS Selector, HTTP หรือ API
* ต้องการคำอธิบายภาษาไทย
* ต้องการตัวอย่างที่คัดลอกไปรันได้จริง
* ต้องการนำผลลัพธ์ไปใช้กับ Excel และ Power BI
* อาจไม่สามารถติดตั้งโปรแกรมเพิ่มเติมนอกเหนือจาก Python ได้

ทุกบทต้องอธิบายคำศัพท์ก่อนใช้งาน และไม่สมมติว่าผู้อ่านรู้เรื่อง Web Development มาก่อน

---

# รูปแบบการทำงานของคุณ

ห้ามสร้าง Repository ทั้งหมดในครั้งเดียว

ให้ทำงานเป็น Phase และหยุดหลังจบแต่ละ Phase เพื่อให้ผู้ใช้ตรวจสอบก่อนดำเนินการต่อ

ในแต่ละ Phase ให้ทำดังนี้:

1. ตรวจสอบไฟล์เดิมใน Repository ก่อนแก้ไข
2. สรุปสิ่งที่จะสร้างหรือแก้ไข
3. สร้างไฟล์เฉพาะที่อยู่ในขอบเขตของ Phase ปัจจุบัน
4. รันคำสั่งตรวจสอบเท่าที่ Environment อนุญาต
5. แก้ Error ที่พบ
6. สรุปไฟล์ที่เพิ่มหรือเปลี่ยน
7. ระบุวิธีทดสอบสำหรับผู้ใช้
8. เสนอ Commit message ที่เหมาะสม
9. หยุดและรอคำสั่งให้ทำ Phase ต่อไป

ห้ามลบหรือเขียนทับงานเดิมโดยไม่ตรวจสอบก่อน

ห้ามใช้ Placeholder เช่น:

* TODO
* Coming soon
* Add content here
* Implement later

ยกเว้นอยู่ในไฟล์ Roadmap และต้องระบุ Phase ที่จะดำเนินการอย่างชัดเจน

---

# Technology Stack

ใช้เครื่องมือหลักดังนี้:

* Python 3.11 หรือใหม่กว่า
* `requests`
* `beautifulsoup4`
* `lxml`
* `pandas`
* `openpyxl`
* `python-dotenv`
* `tenacity`
* `playwright`
* `selenium` สำหรับบทเปรียบเทียบ
* `pytest`
* `responses` หรือ `requests-mock`
* `ruff`
* `mypy` เฉพาะส่วนที่เหมาะสม
* `pre-commit`
* SQLite จาก Python Standard Library

ให้แยก Dependencies เป็นอย่างน้อย:

* Runtime dependencies
* Development dependencies
* Browser automation dependencies

เลือกใช้ `pyproject.toml` เป็นไฟล์ตั้งค่าหลัก

---

# โครงสร้าง Repository เป้าหมาย

สร้าง Repository ให้มีโครงสร้างประมาณนี้ และปรับได้เมื่อมีเหตุผลที่เหมาะสม:

```text
web-scraping-zero-to-practical/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── CHANGELOG.md
├── ROADMAP.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── docs/
│   ├── index.md
│   ├── 00-course-roadmap.md
│   ├── 01-installation.md
│   ├── 02-python-basics.md
│   ├── 03-web-basics.md
│   ├── 04-http-and-requests.md
│   ├── 05-api-first.md
│   ├── 06-static-scraping.md
│   ├── 07-css-selectors.md
│   ├── 08-pagination.md
│   ├── 09-dynamic-websites.md
│   ├── 10-playwright.md
│   ├── 11-selenium.md
│   ├── 12-data-cleaning.md
│   ├── 13-export-data.md
│   ├── 14-error-handling.md
│   ├── 15-rate-limiting.md
│   ├── 16-robots-and-terms.md
│   ├── 17-testing.md
│   ├── 18-maintenance.md
│   ├── 19-scheduling.md
│   ├── 20-power-bi-workflow.md
│   ├── 21-troubleshooting.md
│   ├── glossary.md
│   └── references.md
├── src/
│   └── web_scraping_course/
│       ├── __init__.py
│       ├── config.py
│       ├── http_client.py
│       ├── rate_limiter.py
│       ├── retry.py
│       ├── validators.py
│       ├── exporters.py
│       ├── logging_config.py
│       └── utils.py
├── examples/
│   ├── 01_open_url/
│   ├── 02_download_page/
│   ├── 03_api_first/
│   ├── 04_static_page/
│   ├── 05_tables/
│   ├── 06_pagination/
│   ├── 07_files_and_images/
│   ├── 08_playwright/
│   ├── 09_selenium/
│   ├── 10_excel_export/
│   ├── 11_sqlite/
│   └── 12_change_detection/
├── use_cases/
│   ├── price_monitor/
│   ├── public_announcements/
│   ├── document_downloader/
│   ├── location_directory/
│   ├── weather_api/
│   ├── solar_datasheet_catalog/
│   └── power_bi_pipeline/
├── mock_site/
│   ├── static/
│   ├── dynamic/
│   └── README.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
├── output/
│   └── .gitkeep
├── tests/
│   ├── fixtures/
│   ├── test_http_client.py
│   ├── test_parsers.py
│   ├── test_exporters.py
│   └── test_validators.py
├── scripts/
│   ├── setup_windows.ps1
│   ├── run_checks.ps1
│   └── clean_output.py
└── .github/
    ├── workflows/
    │   └── python-tests.yml
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

---

# ลำดับ Phase

## Phase 0: วิเคราะห์และออกแบบ

ยังไม่เขียนเนื้อหาทั้งหมด

ให้สร้างเฉพาะ:

* `README.md` ฉบับโครงร่าง
* `ROADMAP.md`
* `docs/00-course-roadmap.md`
* โครงสร้าง Folder
* `.gitignore`
* `LICENSE`
* `pyproject.toml` ขั้นต้น

README ต้องอธิบาย:

* Web Scraping คืออะไร
* Repository นี้เหมาะกับใคร
* สิ่งที่จะได้เรียน
* API First คืออะไร
* Static กับ Dynamic ต่างกันอย่างไร
* ข้อควรระวัง
* Course Roadmap
* Quick Start แบบย่อ

หลัง Phase 0 ให้หยุด

---

## Phase 1: การติดตั้งสำหรับผู้เริ่มต้น

สร้างคู่มือ:

* ติดตั้งหรือตรวจสอบ Python
* ตรวจสอบ `python --version`
* สร้าง Virtual Environment
* Activate บน PowerShell
* ติดตั้ง Dependencies
* เปิด Project ด้วย VS Code
* เลือก Python Interpreter
* รัน Python File แรก
* วิธีแก้ Execution Policy บน PowerShell โดยอธิบายความเสี่ยง
* วิธีใช้ `pip`, `python -m pip`
* วิธีตรวจสอบ Package ที่ติดตั้ง
* วิธีออกจาก Virtual Environment

ต้องมีคำสั่ง Windows PowerShell แบบคัดลอกไปใช้ได้จริง

เพิ่ม Script:

* `scripts/setup_windows.ps1`
* `scripts/run_checks.ps1`

หลัง Phase 1 ให้หยุด

---

## Phase 2: พื้นฐาน Web, HTML, HTTP และ Developer Tools

อธิบาย:

* Client และ Server
* URL
* Domain
* Path
* Query String
* HTTP Request
* HTTP Response
* Status Code
* Headers
* Cookies
* HTML Tag
* Attribute
* Class
* ID
* DOM
* CSS Selector
* JavaScript
* Static Website
* Dynamic Website
* API
* JSON

เพิ่มตัวอย่าง HTML แบบ Local เพื่อให้ผู้เรียนฝึก:

* Tag selector
* Class selector
* ID selector
* Descendant selector
* Attribute selector
* ตาราง
* ลิงก์
* รูปภาพ

อธิบายการใช้ Chrome Developer Tools:

1. เปิดหน้าเว็บ
2. กด F12
3. ใช้ Elements
4. ใช้ Inspect
5. ใช้ Network
6. เลือก Fetch/XHR
7. ดู Headers
8. ดู Payload
9. ดู Preview
10. ดู Response
11. ค้นหาว่าหน้าเว็บเรียก API หรือไม่

หลัง Phase 2 ให้หยุด

---

## Phase 3: API First

สร้าง Decision Tree:

```text
ต้องการข้อมูลจากเว็บไซต์
├── มี Official API
│   └── ใช้ API
├── ไม่มี Official API แต่หน้าเว็บเรียก Public JSON Endpoint
│   └── ตรวจสอบสิทธิ์ก่อนใช้
├── ข้อมูลอยู่ใน HTML
│   └── requests + BeautifulSoup
└── ข้อมูลเกิดหลัง JavaScript ทำงาน
    └── Playwright หรือ Selenium
```

สอน:

* วิธีค้นหา Official API
* วิธีอ่าน API Documentation
* Endpoint
* Method
* Parameter
* Header
* Authentication
* API Key
* Pagination
* Rate limit
* JSON parsing
* Environment variable
* `.env`
* `.env.example`
* ห้าม Commit Secret

สร้างตัวอย่าง Public API ที่ไม่ต้องใช้ข้อมูลส่วนตัว และมี Error Handling

ผลลัพธ์ต้อง Export เป็น:

* JSON
* CSV
* Excel

หลัง Phase 3 ให้หยุด

---

## Phase 4: Static Website ด้วย Requests และ BeautifulSoup

สอนตั้งแต่:

* `requests.get()`
* Timeout
* Status code
* `raise_for_status()`
* Response text
* Response content
* Encoding
* User-Agent
* BeautifulSoup
* `find()`
* `find_all()`
* `select()`
* `select_one()`
* `get_text()`
* Attribute extraction
* Link normalization
* Data cleaning

ให้ใช้ Local Mock Website เป็นหลักเพื่อให้ตัวอย่างไม่เสียเมื่อเว็บไซต์ภายนอกเปลี่ยน

ตัวอย่างต้องมี:

* ดึงชื่อสินค้า
* ดึงราคา
* ดึงสถานะ
* ดึง URL
* ดึงข้อมูลจากตาราง
* ดึงหลายรายการ
* ตรวจสอบ Element ที่หาไม่พบ
* บันทึก CSV และ Excel

หลัง Phase 4 ให้หยุด

---

## Phase 5: Pagination และการดาวน์โหลดไฟล์

สอน:

* Next page link
* Page number parameter
* Offset และ Limit
* การหยุดเมื่อไม่มีข้อมูล
* ป้องกัน Infinite Loop
* ป้องกันข้อมูลซ้ำ
* ดาวน์โหลด PDF
* ดาวน์โหลดรูปภาพ
* ตรวจสอบ Content-Type
* ตั้งชื่อไฟล์อย่างปลอดภัย
* ป้องกันเขียนทับไฟล์
* Streaming download
* File checksum เบื้องต้น

สร้างตัวอย่างดาวน์โหลดเอกสารที่ใช้ Local Mock Website หรือไฟล์ตัวอย่างใน Repository

หลัง Phase 5 ให้หยุด

---

## Phase 6: Dynamic Website ด้วย Playwright

ใช้ Playwright เป็นเครื่องมือหลักสำหรับ Dynamic Website

สอน:

* ติดตั้ง Playwright
* ติดตั้ง Browser
* เปิด Browser
* Headed และ Headless
* Page navigation
* Locator
* Click
* Fill
* Select
* Wait
* Screenshot
* อ่านตารางหลัง JavaScript โหลด
* Pagination
* Download event
* Timeout
* Browser context
* ปิด Browser อย่างถูกต้อง

ต้องอธิบายว่าไม่ควรใช้ `time.sleep()` เป็นวิธีหลัก และควรใช้ Locator หรือ Explicit Wait

สร้าง Dynamic Local Mock Page สำหรับฝึก เช่น:

* ปุ่ม Load More
* ตารางที่โหลดภายหลัง
* Form สำหรับกรองข้อมูล
* ปุ่ม Download

หลัง Phase 6 ให้หยุด

---

## Phase 7: Selenium

อธิบาย Selenium เพื่อให้ผู้เรียนรู้จักและสามารถอ่าน Project เก่าได้

เปรียบเทียบ:

* Selenium
* Playwright
* requests
* BeautifulSoup

สร้างตัวอย่าง Selenium ที่ทำงานเทียบกับตัวอย่าง Playwright เดียวกัน แต่ไม่ต้องสร้างทุก Use case ซ้ำ

อธิบายเรื่อง:

* WebDriver
* Explicit Wait
* Locator
* Browser lifecycle
* ข้อดี
* ข้อจำกัด
* กรณีที่ควรเลือก Selenium

หลัง Phase 7 ให้หยุด

---

## Phase 8: ระบบที่ทนต่อ Error

สร้าง Utility ที่นำกลับมาใช้ซ้ำได้:

* HTTP client
* Timeout
* Retry
* Exponential backoff
* Rate limiting
* Logging
* Validation
* Duplicate handling
* Safe filename
* Configuration
* Custom exceptions

ห้าม Retry ทุก Error แบบไม่จำกัด

แยก Error เป็น:

* Connection error
* Timeout
* 4xx
* 5xx
* Parse error
* Selector not found
* Invalid data
* Export error

บันทึก Log โดยไม่เปิดเผย Token, Cookie หรือข้อมูลลับ

หลัง Phase 8 ให้หยุด

---

## Phase 9: สิทธิ์ กฎหมาย จริยธรรม และความปลอดภัย

สร้างบทอธิบายเชิงปฏิบัติ ไม่ให้คำแนะนำทางกฎหมายแบบรับรองผล

ครอบคลุม:

* Terms of Service
* Copyright
* Privacy
* Personal data
* Authentication
* Access control
* `robots.txt`
* Rate limits
* Public data กับ Authorized data
* การขออนุญาตเจ้าของเว็บไซต์
* การระบุ User-Agent ที่เหมาะสม
* การไม่สร้างภาระต่อ Server
* การไม่หลบ CAPTCHA
* การไม่ข้ามระบบ Login
* การไม่ Scrape ข้อมูลส่วนบุคคลโดยไม่จำเป็น
* การกำหนด Retention ของข้อมูล
* การลบข้อมูลเมื่อหมดวัตถุประสงค์

สร้าง Pre-scraping Checklist ให้ผู้เรียนตอบก่อนเริ่ม Project จริง

ตัวอย่าง Checklist:

```text
[ ] มี Official API หรือไม่
[ ] Terms อนุญาตหรือไม่
[ ] ข้อมูลเป็นข้อมูลส่วนบุคคลหรือไม่
[ ] ต้อง Login หรือไม่
[ ] robots.txt ระบุไว้อย่างไร
[ ] มี Rate limit หรือไม่
[ ] เราจะส่ง Request ถี่เพียงใด
[ ] จะจัดเก็บข้อมูลไว้นานเท่าใด
[ ] ใครมีสิทธิ์เข้าถึงข้อมูล
[ ] มีวิธีหยุดระบบเมื่อเกิดปัญหาหรือไม่
```

หลัง Phase 9 ให้หยุด

---

## Phase 10: Export และ Data Pipeline

สอน Export เป็น:

* CSV
* Excel
* JSON
* SQLite

ต้องมี Schema ที่ชัดเจน เช่น:

* `source_url`
* `scraped_at`
* `record_id`
* `name`
* `value`
* `status`
* `raw_value`
* `data_quality_flag`

อธิบาย:

* Encoding
* UTF-8
* Date and time
* Timezone
* Missing values
* Numeric conversion
* Duplicate records
* Incremental load
* Raw data กับ Processed data

สร้าง Workflow:

```text
Website/API
    ↓
Extract
    ↓
Validate
    ↓
Clean
    ↓
Store raw
    ↓
Transform
    ↓
Store processed
    ↓
Excel / SQLite / Power BI
```

หลัง Phase 10 ให้หยุด

---

## Phase 11: Testing และ Maintenance

สร้าง Tests โดยไม่ยิงเว็บไซต์จริงทุกครั้ง

ใช้:

* Mock HTTP response
* HTML fixtures
* JSON fixtures
* Parser tests
* Export tests
* Validation tests
* Regression tests

สอนการรับมือหน้าเว็บไซต์เปลี่ยน:

* Selector fallback
* Required field validation
* Record count anomaly
* HTML snapshot
* Logging
* Alert
* Versioning
* Change detection
* Fail fast
* Graceful degradation

สร้างตัวอย่าง Test ที่จะ Fail เมื่อ:

* Selector หาย
* ราคากลายเป็นค่าว่าง
* จำนวน Record ลดลงผิดปกติ
* API schema เปลี่ยน
* HTTP status ผิดปกติ

หลัง Phase 11 ให้หยุด

---

## Phase 12: Use Cases

สร้าง Use case ที่สมบูรณ์อย่างน้อย 7 โครงการ

ทุก Use case ต้องมี:

* Problem statement
* Source type
* API availability check
* Permission checklist
* Data schema
* Architecture
* Setup
* Code
* Configuration
* Sample input
* Sample output
* Error handling
* Rate limiting
* Tests
* Troubleshooting
* Maintenance notes
* Extension ideas

### Use case 1: Price Monitor

ใช้ Local Mock Store หรือเว็บไซต์ฝึกที่อนุญาต

เก็บข้อมูล:

* Product
* Current price
* Previous price
* Change amount
* Change percent
* Availability
* Source URL
* Checked time

มีระบบเปรียบเทียบข้อมูลครั้งก่อน และสร้างรายการเฉพาะสินค้าที่ราคาเปลี่ยน

ห้ามทำระบบหลบ Bot หรือ CAPTCHA

### Use case 2: Public Announcement Tracker

ติดตามประกาศจาก Local Mock Site หรือ Open Data Source

เก็บ:

* Announcement ID
* Title
* Published date
* Category
* URL
* First seen
* Last seen
* Is new

ตรวจจับประกาศใหม่โดยไม่บันทึกซ้ำ

### Use case 3: Document Downloader

ดาวน์โหลด:

* PDF
* Datasheet
* Manual
* Image

มี:

* Content-Type validation
* File size validation
* Safe filename
* Duplicate prevention
* Checksum
* Download log

### Use case 4: Location Directory

รวบรวม:

* Location name
* Address
* District
* Province
* Postal code
* Latitude
* Longitude
* Contact
* Source URL

Export เป็น Excel และ CSV เพื่อใช้กับ QGIS หรือ Power BI

ห้ามใช้ข้อมูลส่วนบุคคลที่ไม่จำเป็น

### Use case 5: Weather API

ใช้ API ก่อน Scraping

อธิบาย:

* API endpoint
* Parameters
* JSON
* Error handling
* Rate limits
* Caching

Export ข้อมูลรายวันไป CSV หรือ Excel

### Use case 6: Solar Datasheet Catalog

สร้าง Catalog ตัวอย่างสำหรับ:

* Solar panel
* Inverter
* Model
* Rated power
* Voltage
* Current
* Datasheet URL
* Download status
* Last checked

ใช้ Local Sample Data หรือแหล่งที่อนุญาต และอธิบายว่า Product Specification ต้องตรวจสอบกับเอกสารผู้ผลิตก่อนนำไปออกแบบจริง

### Use case 7: Power BI Data Pipeline

สร้างข้อมูลแบบ Long Table ที่ Power BI ใช้งานง่าย

ผลลัพธ์อย่างน้อย:

* `fact_scraping_result.csv`
* `dim_source.csv`
* `dim_date.csv`

อธิบาย:

* Star schema เบื้องต้น
* Refresh workflow
* Incremental data
* Data quality
* การใช้ Folder เป็น Data Source
* ความเสี่ยงเมื่อ Schema เปลี่ยน

หลัง Phase 12 ให้หยุด

---

## Phase 13: Scheduling และ Automation

สอนการรันอัตโนมัติด้วย:

* Windows Task Scheduler
* PowerShell
* Python entry point
* Log file
* Exit code
* Lock file
* ป้องกันงานซ้อน
* Daily และ Weekly schedule
* ตรวจสอบว่างานสำเร็จหรือไม่

ไม่ฝัง Password หรือ Token ใน Script

อธิบายทางเลือก GitHub Actions แต่ต้องเตือนว่า:

* Secret ต้องเก็บใน GitHub Secrets
* Browser automation อาจต้องตั้งค่าเพิ่มเติม
* ต้องตรวจสอบข้อกำหนดของเว็บไซต์
* ห้ามตั้ง Schedule ถี่เกินไป

หลัง Phase 13 ให้หยุด

---

## Phase 14: GitHub Documentation และ CI

เพิ่ม:

* GitHub Actions สำหรับ Test และ Lint
* Issue templates
* Pull request template
* Contributing guide
* Security policy
* Changelog
* Release checklist

Workflow ต้อง:

* ติดตั้ง Python
* ติดตั้ง Dependencies
* รัน Ruff
* รัน Pytest
* ไม่เรียกเว็บไซต์จริงโดยไม่จำเป็น
* ไม่แสดง Secret ใน Log

หลัง Phase 14 ให้หยุด

---

## Phase 15: Final Review

ตรวจ Repository ทั้งหมดในมุมมองผู้เริ่มต้น

ตรวจสอบ:

* Link ภายใน Markdown
* คำสั่งติดตั้ง
* Import paths
* Dependencies
* Code formatting
* Tests
* Sample outputs
* Windows compatibility
* Thai encoding
* Error messages
* Security
* Secrets
* License
* References
* ตัวอย่างที่อาจเสียในอนาคต

สร้าง:

* Final learning checklist
* Capstone project
* Quiz
* Exercises
* Answer guide
* Troubleshooting index
* Repository release notes

Capstone ต้องให้ผู้เรียนเลือกแหล่งข้อมูลเอง แล้วทำตามขั้นตอน:

```text
1. กำหนดวัตถุประสงค์
2. ตรวจสอบ API
3. ตรวจสอบสิทธิ์
4. จำแนก Static หรือ Dynamic
5. ออกแบบ Schema
6. สร้าง Extractor
7. เพิ่ม Rate limit
8. เพิ่ม Error handling
9. เพิ่ม Validation
10. เพิ่ม Tests
11. Export ข้อมูล
12. เขียน Maintenance plan
```

---

# มาตรฐานการเขียนเอกสาร

ทุกบทต้องมีรูปแบบ:

```markdown
# ชื่อบท

## เป้าหมายการเรียนรู้

## สิ่งที่ต้องเตรียม

## แนวคิดสำคัญ

## คำศัพท์

## ขั้นตอนปฏิบัติ

## ตัวอย่าง Code

## ผลลัพธ์ที่คาดหวัง

## อธิบาย Code ทีละส่วน

## ข้อผิดพลาดที่พบบ่อย

## แบบฝึกหัด

## Checklist

## สรุป
```

คำสั่งทุกชุดต้องระบุว่าใช้ใน:

* PowerShell
* Command Prompt
* Python file
* VS Code Terminal

Code ทุกตัวอย่างต้อง:

* รันได้จริง
* มี `main()` เมื่อเหมาะสม
* มี Timeout
* มี Error Handling
* ไม่ใช้ Bare `except`
* ไม่ฝัง Secret
* ไม่ส่ง Request ถี่เกินไป
* ปิด File และ Browser อย่างถูกต้อง
* ใช้ชื่อ Variable ที่สื่อความหมาย
* มี Type Hint ในส่วน Library
* มี Docstring สำหรับ Public function
* แยก Logic การดึงข้อมูลออกจาก Logic การ Export
* ทดสอบได้โดยไม่พึ่งเว็บไซต์จริงเสมอไป

---

# มาตรฐานด้าน Rate Limiting

สร้าง Rate Limiter ที่กำหนดค่าได้ เช่น:

```env
REQUEST_DELAY_SECONDS=2
REQUEST_TIMEOUT_SECONDS=20
MAX_RETRIES=3
USER_AGENT=web-scraping-zero-to-practical/1.0
```

หลักการ:

* ค่าเริ่มต้นต้องสุภาพต่อ Server
* Retry เฉพาะ Error ที่เหมาะสม
* รองรับ `Retry-After`
* ใช้ Exponential Backoff
* มี Maximum retry
* หยุดเมื่อเกิด 401, 403 หรือข้อผิดพลาดที่บ่งชี้ว่าไม่มีสิทธิ์
* ไม่หมุน Proxy
* ไม่เปลี่ยน User-Agent เพื่อหลบการตรวจจับ
* ไม่แก้หรือหลบ CAPTCHA

---

# มาตรฐานรับมือเว็บไซต์เปลี่ยนโครงสร้าง

ทุก Project ต้องเตรียม:

1. Selector แยกอยู่ใน Configuration หรือ Parser module
2. Required field validation
3. Logging เมื่อ Selector หาไม่พบ
4. เก็บ Sample HTML สำหรับ Test
5. Parser unit test
6. Record count sanity check
7. Schema validation
8. วันที่และเวลาที่ดึงข้อมูล
9. Source URL
10. Version ของ Parser
11. Maintenance guide
12. วิธีอัปเดต Selector

ตัวอย่าง Config:

```python
SELECTORS = {
    "product_card": ".product-card",
    "product_name": ".product-name",
    "price": ".product-price",
    "availability": ".availability",
}
```

ห้ามซ่อน Selector กระจายอยู่ทั่ว Code โดยไม่มีโครงสร้าง

---

# Definition of Done

Phase หนึ่งถือว่าเสร็จเมื่อ:

* ไฟล์ตาม Scope ถูกสร้างครบ
* Code รันได้
* Test ผ่านเท่าที่ Environment รองรับ
* ไม่มี Secret
* ไม่มี Dead link ภายในที่ตรวจพบ
* ไม่มี Placeholder ที่ไม่ได้อธิบาย
* README หรือสารบัญเชื่อมถึงบทใหม่
* มีตัวอย่างผลลัพธ์
* มี Troubleshooting
* มี Commit message
* มีคำสั่งสำหรับผู้ใช้ทดสอบเอง

---

# รูปแบบรายงานเมื่อจบแต่ละ Phase

ตอบในรูปแบบนี้:

```markdown
## Phase ที่ดำเนินการ

## สิ่งที่สร้าง

## ไฟล์ที่เพิ่ม

## ไฟล์ที่แก้ไข

## การตรวจสอบที่รันแล้ว

## ผลการตรวจสอบ

## วิธีทดสอบบน Windows

## ข้อจำกัดหรือสิ่งที่ยังไม่ทำ

## Commit message ที่แนะนำ

## Phase ถัดไป
```

---

# ข้อกำหนดสำคัญ

* อย่าทำทุก Phase พร้อมกัน
* เริ่มเฉพาะ Phase 0 เท่านั้น
* อย่าทำ Phase 1 จนกว่าจะได้รับคำสั่ง
* ตรวจสอบ Repository ปัจจุบันก่อนสร้างไฟล์
* รักษาไฟล์เดิมที่ผู้ใช้มีอยู่
* เน้นการเรียนแบบลงมือทำ
* เนื้อหาหลักเป็นภาษาไทย
* คำศัพท์เทคนิคให้ใส่ภาษาอังกฤษในวงเล็บ
* รองรับ Windows และ VS Code เป็นหลัก
* ตัวอย่างต้องปลอดภัยและไม่ละเมิดสิทธิ์ของเว็บไซต์
* ใช้ API ก่อน Scraping เสมอเมื่อมี API ที่เหมาะสม
* ใช้ Playwright เป็นตัวเลือกหลักสำหรับเว็บ Dynamic
* ใช้ Selenium เพื่อการเปรียบเทียบและรองรับระบบเดิม
* ใช้ Local Mock Site เพื่อให้บทเรียนไม่เสียเมื่อเว็บไซต์ภายนอกเปลี่ยน

ตอนนี้ให้เริ่มดำเนินการเฉพาะ **Phase 0: วิเคราะห์และออกแบบ Repository** เท่านั้น
