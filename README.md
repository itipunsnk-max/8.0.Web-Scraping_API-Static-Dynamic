# Web Scraping Zero to Practical

คู่มือภาษาไทยสำหรับเรียน Web Scraping ด้วย Python ตั้งแต่พื้นฐานจนถึงการสร้างระบบที่นำไปใช้งานจริงได้ โดยเน้นความปลอดภัย จริยธรรม การดูแลรักษา และการส่งต่อข้อมูลไปยัง CSV, Excel, JSON, SQLite และ Power BI

> สถานะปัจจุบัน: **Phase 15 — Final Review (หลักสูตรครบถ้วน)**

## Web Scraping คืออะไร

Web Scraping คือการเขียนโปรแกรมเพื่ออ่านข้อมูลจากเว็บไซต์หรือบริการบนเว็บ แล้วแปลงข้อมูลให้อยู่ในรูปแบบที่นำไปใช้งานต่อได้ เช่น ตาราง รายงาน หรือฐานข้อมูล การดึงข้อมูลควรทำเท่าที่จำเป็น เคารพข้อกำหนดของเว็บไซต์ และไม่พยายามข้ามระบบป้องกันการเข้าถึง

## Repository นี้เหมาะกับใคร

- ผู้เริ่มต้นที่ใช้ Windows, VS Code และต้องการเรียนด้วย Python
- ผู้ที่ยังไม่คุ้นกับ HTML, CSS Selector, HTTP หรือ API
- ผู้ที่ต้องการตัวอย่างภาษาไทยซึ่งคัดลอกไปทดลองได้
- ผู้ที่ต้องการนำผลลัพธ์ไปใช้กับ Excel หรือ Power BI

## สิ่งที่จะได้เรียน

เนื้อหาจะค่อย ๆ พาจากการติดตั้งและพื้นฐานเว็บ ไปสู่การเลือก API ก่อนการ Scrape, การอ่าน Static Website, การใช้ Playwright กับ Dynamic Website, การจัดการ Error, การทดสอบ, การ Export และการทำงานอัตโนมัติบน Windows

หลักการเลือกวิธีทำงานคือ:

1. ตรวจสอบ Official API ก่อนเสมอ
2. ถ้ามี API ที่เหมาะสม ให้ใช้ API ก่อนการอ่าน HTML
3. ใช้ `requests` และ `BeautifulSoup` กับหน้าเว็บแบบ Static
4. ใช้ Playwright เป็นตัวเลือกหลักกับหน้าเว็บแบบ Dynamic
5. ใช้ Local Mock Website ในบทเรียนที่ไม่ควรผูกกับเว็บไซต์ภายนอก

## API First คืออะไร

API First หมายถึงการตรวจสอบก่อนว่าเว็บไซต์มีช่องทาง API ที่เจ้าของระบบจัดเตรียมไว้หรือไม่ หากมีและอนุญาตให้ใช้ API มักจะได้ข้อมูลที่มีโครงสร้างชัดเจน เสถียรกว่า และลดภาระจากการตีความ HTML

## Static กับ Dynamic ต่างกันอย่างไร

- **Static Website**: ข้อมูลหลักอยู่ใน HTML ที่เซิร์ฟเวอร์ส่งกลับมา จึงมักเริ่มด้วย `requests` และ `BeautifulSoup`
- **Dynamic Website**: ข้อมูลถูกสร้างหรือเติมภายหลังด้วย JavaScript จึงอาจต้องตรวจสอบ Network/API หรือใช้ Playwright เพื่อเปิดหน้าเว็บตามพฤติกรรมที่ได้รับอนุญาต

## ความปลอดภัยและจริยธรรม

ก่อนดึงข้อมูลจริงต้องตรวจสอบ Terms of Service, Privacy Policy, Copyright และ `robots.txt` จำกัดความถี่ของ Request ใช้ User-Agent ที่ระบุวัตถุประสงค์อย่างเหมาะสม และเก็บเฉพาะข้อมูลที่จำเป็น ห้ามทำตัวอย่างเพื่อหลบ CAPTCHA, ข้าม Login, ข้าม Access Control หรือเก็บ Secret ลง Git

## Course Roadmap

ดูรายละเอียดลำดับการเรียนและขอบเขตของแต่ละ Phase ได้ที่ [ROADMAP.md](ROADMAP.md), [Course Roadmap](docs/00-course-roadmap.md), [คู่มือการติดตั้ง](docs/01-installation.md), [พื้นฐาน Web, HTML, HTTP](docs/02-web-basics.md), [API First](docs/03-api-first.md), [Static Scraping](docs/04-static-scraping.md), [Pagination/Downloads](docs/05-pagination-downloads.md), [Dynamic Website ด้วย Playwright](docs/06-dynamic-playwright.md), [Selenium](docs/07-selenium.md), [ระบบรองรับ Error](docs/08-error-resilience.md), [สิทธิ์/จริยธรรม/ความปลอดภัย](docs/09-ethics-security.md), [Export/Data Pipeline](docs/10-data-pipeline.md), [Testing/Maintenance](docs/11-testing-maintenance.md), [Use Cases](docs/12-use-cases.md), [Scheduling/Automation](docs/13-scheduling-automation.md), [GitHub Documentation/CI](docs/14-github-docs-ci.md), [Final Review](docs/15-final-review.md) และ [Vercel Deployment](VERCEL_DEPLOYMENT.md)

## Quick Start แบบย่อ

เริ่มต้นด้วยการเปิด [คู่มือการติดตั้ง](docs/01-installation.md) หรือรันสคริปต์บน Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup_windows.ps1
.\scripts\run_checks.ps1
```

เปิด Local Mock Website เพื่อฝึก Phase 2 ได้ด้วย:

```powershell
python -m http.server 8000 --directory mock_site/static
```

จากนั้นเปิด `http://127.0.0.1:8000/index.html` ใน Chrome และอ่าน [คู่มือพื้นฐาน Web, HTML, HTTP](docs/02-web-basics.md)

ทดลอง API First และ Export ผลลัพธ์ได้ด้วย:

```powershell
Copy-Item .env.example .env
python .\examples\03_api_first\api_first.py --limit 5
```

อ่านรายละเอียดได้ที่ [คู่มือ API First](docs/03-api-first.md)

ทดลอง Static Scraping จาก Local Mock Store ได้ที่ [คู่มือ Static Scraping](docs/04-static-scraping.md)

ทดลอง Pagination และ Safe Download ได้ที่ [คู่มือ Pagination และการดาวน์โหลดไฟล์](docs/05-pagination-downloads.md)

ทดลอง Dynamic Website และ Playwright ได้ที่ [คู่มือ Dynamic Website ด้วย Playwright](docs/06-dynamic-playwright.md)

ทดลอง Selenium และเปรียบเทียบกับ Playwright ได้ที่ [คู่มือ Selenium](docs/07-selenium.md)

ทดลอง Resilient HTTP Client, Retry, Backoff และ Validation ได้ที่ [คู่มือระบบรองรับ Error](docs/08-error-resilience.md)

ตรวจสิทธิ์, Privacy, robots.txt และ Pre-scraping Checklist ได้ที่ [คู่มือสิทธิ์/จริยธรรม/ความปลอดภัย](docs/09-ethics-security.md)

ทดลอง Schema-first Data Pipeline และ Export ได้ที่ [คู่มือ Export และ Data Pipeline](docs/10-data-pipeline.md)

ตรวจ fixture-based tests, mock responses และ maintenance checks ได้ที่ [คู่มือ Testing และ Maintenance](docs/11-testing-maintenance.md)

หากต้องการตรวจสอบโครงสร้างและลำดับการเรียน ให้เปิด [ROADMAP.md](ROADMAP.md)

คู่มือการติดตั้ง, Scripts สำหรับ Windows PowerShell และตัวอย่าง API First ที่ทำเสร็จแล้วจะถูกขยายต่อทีละ Phase ตาม [ROADMAP.md](ROADMAP.md)

## แหล่งอ้างอิงหลัก

แนวทางด้านการทำงานกับเว็บอ้างอิงจาก [Automate the Boring Stuff with Python — Chapter 13](https://automatetheboringstuff.com/3e/chapter13.html) โดยเนื้อหาใน repository นี้จะเรียบเรียงและอธิบายใหม่ ไม่คัดลอกข้อความยาวจากต้นฉบับ

## สถานะการพัฒนา

งานจะดำเนินการทีละ Phase และหยุดให้ตรวจสอบหลังจบแต่ละ Phase ตามข้อกำหนดของโครงการ
