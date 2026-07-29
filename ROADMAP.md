# Roadmap: Web Scraping Zero to Practical

เอกสารนี้เป็นแผนงานระดับ Repository สำหรับคู่มือภาษาไทยที่สอน Web Scraping อย่างปลอดภัยและลงมือทำได้จริง งานจะทำทีละ Phase และจะไม่เริ่ม Phase ถัดไปจนกว่าจะได้รับคำสั่ง

## สถานะ

| Phase | หัวข้อ | สถานะ |
| --- | --- | --- |
| 0 | วิเคราะห์และออกแบบ Repository | เสร็จแล้ว |
| 1 | การติดตั้งสำหรับผู้เริ่มต้น | เสร็จแล้ว |
| 2 | พื้นฐาน Web, HTML, HTTP และ Developer Tools | เสร็จแล้ว |
| 3 | API First | เสร็จแล้ว |
| 4 | Static Website ด้วย Requests และ BeautifulSoup | เสร็จแล้ว |
| 5 | Pagination และการดาวน์โหลดไฟล์ | เสร็จแล้ว |
| 6 | Dynamic Website ด้วย Playwright | รอคำสั่ง |
| 7 | Selenium | รอคำสั่ง |
| 8 | ระบบที่ทนต่อ Error | รอคำสั่ง |
| 9 | สิทธิ์ กฎหมาย จริยธรรม และความปลอดภัย | รอคำสั่ง |
| 10 | Export และ Data Pipeline | รอคำสั่ง |
| 11 | Testing และ Maintenance | รอคำสั่ง |
| 12 | Use Cases | รอคำสั่ง |
| 13 | Scheduling และ Automation | รอคำสั่ง |
| 14 | GitHub Documentation และ CI | รอคำสั่ง |
| 15 | Final Review | รอคำสั่ง |

## หลักการร่วมทุก Phase

- ตรวจสอบไฟล์เดิมก่อนแก้ไข และรักษางานเดิมไว้
- ตรวจสอบ API ก่อนเลือกการ Scraping
- ใช้ข้อมูลสาธารณะ แหล่งทดลอง หรือ Local Mock Website ที่ได้รับอนุญาต
- มี Timeout, Error Handling, Rate Limiting และการตรวจสอบข้อมูลตามความเหมาะสม
- ไม่หลบ CAPTCHA, Authentication, Access Control หรือระบบป้องกัน Bot
- ไม่เก็บ Password, Token, Cookie หรือ Secret ใน Repository
- แยก Logic การดึงข้อมูลออกจาก Logic การแปลงและ Export
- มีตัวอย่างผลลัพธ์ วิธีทดสอบ และ Troubleshooting ที่ผู้ใช้ Windows ทำตามได้

## ขอบเขตแต่ละ Phase

### Phase 0: วิเคราะห์และออกแบบ Repository

จัดทำ README โครงร่าง, Roadmap, Course Roadmap, โครงสร้างโฟลเดอร์, `.gitignore`, ใบอนุญาต และ `pyproject.toml` ขั้นต้น โดยยังไม่สร้างเนื้อหาบทเรียนหรือ Feature ของระบบ

### Phase 1: การติดตั้งสำหรับผู้เริ่มต้น

สอนตรวจสอบ Python, สร้างและเปิดใช้งาน Virtual Environment, ติดตั้ง Dependencies, ใช้ VS Code และเพิ่ม Script สำหรับตั้งค่าและตรวจสอบบน Windows PowerShell

### Phase 2: พื้นฐาน Web, HTML, HTTP และ Developer Tools

อธิบายคำศัพท์พื้นฐานและสร้าง Local HTML สำหรับฝึก Selector, ตาราง, ลิงก์, รูปภาพ รวมถึงการดู API จาก Chrome Developer Tools

### Phase 3: API First

สอนตัดสินใจเลือก API, อ่านเอกสาร API, จัดการ JSON, Pagination, Rate Limit และ Environment Variable พร้อมตัวอย่าง Public API ที่ไม่ใช้ข้อมูลส่วนตัว และ Export เป็น JSON, CSV, Excel

### Phase 4: Static Website ด้วย Requests และ BeautifulSoup

สอน Request, Response, Timeout, Status Code, การเลือก Element และการทำความสะอาดข้อมูล โดยใช้ Local Mock Website เป็นแหล่งหลัก และบันทึกผลเป็น CSV กับ Excel

### Phase 5: Pagination และการดาวน์โหลดไฟล์

สอนการวนหน้า การหยุดอย่างปลอดภัย การป้องกันข้อมูลซ้ำ การดาวน์โหลด PDF/รูปภาพ การตรวจ Content-Type, Safe Filename, Streaming และ Checksum เบื้องต้น

### Phase 6: Dynamic Website ด้วย Playwright

สอนติดตั้ง Browser, Navigation, Locator, Interaction, Explicit Wait, Screenshot, ตารางหลัง JavaScript โหลด, Pagination และ Download Event ผ่าน Dynamic Local Mock Page

### Phase 7: Selenium

เปรียบเทียบ Selenium กับ Playwright, Requests และ BeautifulSoup พร้อมตัวอย่างเทียบเคียงหนึ่งชุด เพื่อให้เข้าใจ WebDriver และการดูแลระบบเดิม

### Phase 8: ระบบที่ทนต่อ Error

สร้าง Utility สำหรับ HTTP Client, Retry, Exponential Backoff, Rate Limiting, Logging, Validation, Duplicate Handling, Safe Filename, Configuration และ Custom Exceptions

### Phase 9: สิทธิ์ กฎหมาย จริยธรรม และความปลอดภัย

อธิบาย Terms, Copyright, Privacy, Personal Data, Authentication, `robots.txt`, Rate Limit, Retention และ Pre-scraping Checklist โดยไม่ให้คำรับรองทางกฎหมาย

### Phase 10: Export และ Data Pipeline

ออกแบบ Schema และ Workflow จาก Extract ไปสู่ Validate, Clean, Store และ Export เป็น CSV, Excel, JSON, SQLite รวมถึงแนวทางเตรียมข้อมูลสำหรับ Power BI

### Phase 11: Testing และ Maintenance

สร้าง Mock HTTP Response, Fixtures, Parser/Export/Validation Tests และการตรวจจับโครงสร้างเว็บไซต์เปลี่ยน เช่น Selector หาย, Schema เปลี่ยน หรือจำนวน Record ผิดปกติ

### Phase 12: Use Cases

สร้างตัวอย่างครบวงจรอย่างน้อย 7 โครงการ ได้แก่ Price Monitor, Public Announcement Tracker, Document Downloader, Location Directory, Weather API, Solar Datasheet Catalog และ Power BI Data Pipeline

### Phase 13: Scheduling และ Automation

สอน Windows Task Scheduler, PowerShell, Entry Point, Log, Exit Code, Lock File และการตั้งงานแบบ Daily/Weekly โดยไม่ฝัง Secret ใน Script

### Phase 14: GitHub Documentation และ CI

เพิ่ม GitHub Actions สำหรับ Test/Lint, Issue Template, Pull Request Template, Contributing Guide, Security Policy, Changelog และ Release Checklist

### Phase 15: Final Review

ตรวจสอบลิงก์ คำสั่ง Import Dependencies, Windows Compatibility, Thai Encoding, Security และสร้าง Learning Checklist, Capstone, Quiz, Exercises, Answer Guide และ Release Notes

## เกณฑ์จบแต่ละ Phase

Phase จะถือว่าจบเมื่อไฟล์ตามขอบเขตถูกสร้างครบ โค้ดและคำสั่งที่เกี่ยวข้องตรวจสอบแล้ว ไม่มี Secret หรือลิงก์ภายในที่เสีย มีเอกสารเชื่อมโยง วิธีทดสอบ Troubleshooting และ Commit Message ที่แนะนำ จากนั้นจะหยุดรอคำสั่ง

## ลำดับการทำงานต่อ

หลังตรวจสอบ Phase 5 แล้ว ให้สั่งให้ดำเนินการ **Phase 6** โดยตรง การดำเนินการครั้งถัดไปจะตรวจสอบ Repository ปัจจุบันก่อนเริ่มสร้างไฟล์ของ Phase 6
