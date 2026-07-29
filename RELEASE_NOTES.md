# Release Notes

## v0.1.0 — Learning Repository Baseline

หลักสูตรฉบับแรกครอบคลุมตั้งแต่ Python/HTTP พื้นฐานไปจนถึง static/dynamic scraping, resilience, ethics, data pipeline, tests, use cases, Windows scheduling และ GitHub CI

### Highlights

- ตัวอย่าง Python ที่แยก fetch/parse/validate/export
- Fixture และ mock tests ที่ทำงานได้โดยไม่พึ่งเว็บไซต์จริง
- Export JSON, CSV, Excel และ SQLite
- Scheduled runner พร้อม lock, log และ exit code
- GitHub Actions, issue/PR templates และ security/release documentation
- Static learning site ที่เตรียมพร้อมสำหรับ Vercel

### Known limitations

- Vercel ใช้เผยแพร่ static documentation เท่านั้น ไม่ใช่ runtime สำหรับ Windows Task Scheduler
- การเชื่อมต่อเว็บไซต์จริงต้องตรวจ permission, Terms, `robots.txt`, rate limit และ privacy เพิ่มเติม
- ยังไม่มี custom domain, production secret หรือ external monitoring ที่ผูกกับ deployment
