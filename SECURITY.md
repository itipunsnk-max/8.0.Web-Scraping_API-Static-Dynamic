# Security Policy

## การรายงานช่องโหว่

โปรดอย่าเปิดเผยรายละเอียดช่องโหว่เป็น public issue หากอาจกระทบผู้ใช้งานหรือข้อมูล ให้ใช้ [GitHub private security advisory](https://github.com/itipunsnk-max/8.0.Web-Scraping_API-Static-Dynamic/security/advisories/new) หรือช่องทางส่วนตัวของผู้ดูแล repository

รายงานควรมีผลกระทบ, ขั้นตอนทำซ้ำ, รุ่น/commit ที่เกี่ยวข้อง และหลักฐานที่ลบ secret กับข้อมูลส่วนบุคคลแล้ว

## ขอบเขตความปลอดภัย

- ห้าม commit API key, password, cookie, session, personal data หรือ response ที่มีข้อมูลอ่อนไหว
- ห้ามใช้ตัวอย่างเพื่อหลบ CAPTCHA, authentication, access control หรือ rate limit
- ตรวจสอบ Terms, Privacy Policy, Copyright และ `robots.txt` ก่อน scraping จริง
- ใช้ environment variables สำหรับ configuration ที่เป็นความลับ และจำกัดสิทธิ์ของ account/โฟลเดอร์ output
- ในกรณีที่สงสัยว่า secret หลุด ให้ revoke/rotate ทันที แล้วจึงลบออกจากประวัติด้วยกระบวนการที่เหมาะสม

## Supported versions

โดยปกติให้รายงานปัญหาบน commit ล่าสุดของ `main` และเวอร์ชัน Python ที่ระบุใน `pyproject.toml`
