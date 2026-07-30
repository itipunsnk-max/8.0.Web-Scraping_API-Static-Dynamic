# Phase 15: Final Review

Phase นี้ตรวจความพร้อมของ repository ก่อนเผยแพร่ โดยรวม code quality, dependency/import, Windows compatibility, Thai UTF-8, security, learning materials และ static documentation deployment

## คำสั่งตรวจหลัก

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe .\scripts\final_review.py
```

`final_review.py` ตรวจ required files, UTF-8, internal Markdown links และ secret pattern แบบ deterministic โดยไม่ส่งข้อมูลออกนอกเครื่อง

## ผลลัพธ์ที่ต้องตรวจด้วยคน

- ตรวจว่า source และ endpoint มี permission, Terms, Privacy, Copyright และ `robots.txt` ที่เหมาะสม
- ตรวจคำสั่ง PowerShell บน Windows เครื่องเป้าหมายและสิทธิ์ของ Task Scheduler account
- ตรวจ generated output, cache, `.env` และข้อมูลส่วนบุคคลไม่อยู่ใน commit
- อ่าน `LEARNING_CHECKLIST.md`, `CAPSTONE.md`, `QUIZ.md`, `EXERCISES.md` และ `ANSWER_GUIDE.md` เพื่อทบทวนหลักสูตร
- ใช้ `RELEASE_CHECKLIST.md` ก่อน tag/release

## Vercel readiness

Vercel ใน repository นี้มีเป้าหมายเป็น static learning site เท่านั้น ไฟล์ `vercel.json` ชี้ `outputDirectory` ไปที่ `site/` และ `VERCEL_DEPLOYMENT.md` อธิบายการ link, preview และ production deploy หลังผู้ใช้เชื่อมต่อ account/team ของตัวเอง

Python scraper และ Windows scheduler ไม่ควรถูกย้ายไปรันบน Vercel โดยอัตโนมัติ เพราะเป็นคนละ runtime และ operational boundary
