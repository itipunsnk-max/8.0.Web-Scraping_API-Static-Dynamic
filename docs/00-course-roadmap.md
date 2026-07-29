# Course Roadmap

## เป้าหมายการเรียนรู้

เมื่อเรียนครบหลักสูตร ผู้เรียนควรสามารถ:

- อธิบายความแตกต่างระหว่าง API, Static Website และ Dynamic Website ได้
- ตรวจสอบช่องทางข้อมูลและสิทธิ์ก่อนเริ่มดึงข้อมูล
- เลือกเครื่องมือให้เหมาะกับลักษณะข้อมูล
- สร้างงานดึงข้อมูลที่มี Timeout, Rate Limiting, Validation และ Error Handling
- Export ข้อมูลไปยังไฟล์และ SQLite เพื่อใช้งานต่อใน Excel หรือ Power BI
- ทดสอบและดูแลระบบเมื่อ HTML หรือ Schema เปลี่ยน

## เส้นทางการเรียน

```text
ติดตั้งเครื่องมือ
    ↓
พื้นฐาน Web, HTML, HTTP และ JSON
    ↓
ตรวจสอบ API และเลือกวิธีดึงข้อมูล
    ↓
Requests + BeautifulSoup
    ↓
Pagination + Download
    ↓
Playwright และ Selenium
    ↓
Error Handling + Rate Limiting + Validation
    ↓
สิทธิ์ ความปลอดภัย และจริยธรรม
    ↓
Export + SQLite + Power BI
    ↓
Testing + Maintenance + Scheduling + CI
    ↓
Use Cases และ Capstone Project
```

## ตารางบทเรียนตาม Phase

| Phase | สิ่งที่จะเรียน | ผลลัพธ์หลัก |
| --- | --- | --- |
| 0 | วิเคราะห์และออกแบบ Repository | โครงสร้างและเอกสารตั้งต้น |
| 1 | ติดตั้ง Python และเครื่องมือ | Environment ที่พร้อมใช้งานบน Windows — เสร็จแล้ว |
| 2 | Web, HTML, HTTP และ Developer Tools | อ่านโครงสร้างหน้าเว็บและตรวจ API ได้ — เสร็จแล้ว |
| 3 | API First | ดึง JSON และ Export ผลลัพธ์ได้ — เสร็จแล้ว |
| 4 | Static Scraping | อ่าน HTML และทำความสะอาดข้อมูลได้ — เสร็จแล้ว |
| 5 | Pagination และไฟล์ | วนหน้าและดาวน์โหลดไฟล์อย่างปลอดภัยได้ |
| 6 | Playwright | อ่านข้อมูลที่โหลดด้วย JavaScript ได้ |
| 7 | Selenium | อ่านและดูแล Project ที่ใช้ Selenium ได้ |
| 8 | Error Resilience | มี Retry, Logging, Rate Limit และ Validation |
| 9 | Ethics and Security | ประเมินสิทธิ์และความเสี่ยงก่อนทำงานได้ |
| 10 | Data Pipeline | จัดเก็บ Raw/Processed และ Export หลายรูปแบบได้ |
| 11 | Testing and Maintenance | ตรวจจับ Parser เสียหรือ Schema เปลี่ยนได้ |
| 12 | Use Cases | ประกอบระบบจากปัญหาจริงหลายรูปแบบได้ |
| 13 | Scheduling | ตั้งงานอัตโนมัติบน Windows ได้ |
| 14 | Documentation and CI | ตรวจ Test/Lint บน GitHub ได้ |
| 15 | Final Review | ทำ Capstone และตรวจความพร้อมเผยแพร่ได้ |

## กติกาการเรียน

1. เริ่มจาก API ที่เจ้าของระบบจัดเตรียมให้ หากมีและอนุญาตให้ใช้
2. ใช้ Local Mock Website เมื่อเหมาะสม เพื่อให้แบบฝึกหัดทำซ้ำได้
3. อ่าน Terms of Service, Privacy Policy, Copyright และ `robots.txt` ก่อนใช้แหล่งข้อมูลจริง
4. จำกัดความถี่ Request และหยุดเมื่อได้รับสัญญาณว่าไม่มีสิทธิ์ เช่น `401` หรือ `403`
5. ไม่หลบ CAPTCHA, Login, Access Control หรือ Bot Protection
6. ไม่บันทึกข้อมูลลับลงไฟล์หรือ Git
7. ทำแบบฝึกหัดและตรวจผลลัพธ์ก่อนขยับไป Phase ถัดไป

## ผลงานปลายทาง

ผู้เรียนจะต่อยอดเป็น Capstone ได้ตามลำดับ: กำหนดวัตถุประสงค์ ตรวจ API และสิทธิ์ จำแนก Static/Dynamic ออกแบบ Schema สร้าง Extractor เพิ่ม Rate Limit, Error Handling, Validation และ Tests แล้ว Export ข้อมูลพร้อมเขียนแผน Maintenance

## เอกสารที่เกี่ยวข้อง

- [README](../README.md) — ภาพรวม Repository และหลักการใช้งาน
- [ROADMAP](../ROADMAP.md) — ขอบเขตและสถานะของทุก Phase
- [การติดตั้งสำหรับผู้เริ่มต้น](01-installation.md) — คู่มือ Setup บน Windows PowerShell
- [พื้นฐาน Web, HTML, HTTP และ Developer Tools](02-web-basics.md) — คำศัพท์และการฝึกด้วย Local Mock Website
- [API First](03-api-first.md) — ตรวจ API, อ่าน JSON และ Export ผลลัพธ์
- [Static Scraping](04-static-scraping.md) — ใช้ Requests และ BeautifulSoup กับ Local Mock Store
