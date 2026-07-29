# Release Checklist

ใช้รายการนี้ก่อน tag หรือเผยแพร่ release ของ repository

## Code และ CI

- [ ] CI บน pull request ผ่านครบทุก Python version ที่ประกาศไว้
- [ ] `ruff check .` ผ่าน
- [ ] `pytest -q` ผ่าน
- [ ] ไม่มี test ที่ยิงเว็บไซต์จริงโดยไม่จำเป็น
- [ ] ตรวจ Python/OS compatibility และคำสั่ง PowerShell แล้ว

## Documentation

- [ ] README, ROADMAP และ course roadmap ชี้ไปยัง phase ล่าสุด
- [ ] ลิงก์ภายในทั้งหมดใช้งานได้
- [ ] ทุกตัวอย่างมีคำสั่ง run และ troubleshooting
- [ ] CHANGELOG มีรายการเปลี่ยนแปลงและวันที่
- [ ] Release note อธิบาย breaking change, migration และ known limitations ถ้ามี

## Security และข้อมูล

- [ ] Secret scan ผ่าน และไม่มี `.env`, token, cookie หรือ personal data
- [ ] ตรวจ Terms, Privacy, Copyright, `robots.txt`, permission และ rate limit ของแหล่งข้อมูลจริง
- [ ] ไฟล์ output, cache และ temporary files ไม่ถูก commit
- [ ] Security policy และช่องทางรายงานช่องโหว่ใช้งานได้

## GitHub release

- [ ] Merge PR หลัง review และ CI ผ่าน
- [ ] สร้าง annotated tag ตาม versioning policy
- [ ] ตรวจไฟล์ที่แนบใน release ไม่รวมข้อมูลลับ
- [ ] ประกาศ release พร้อมลิงก์เอกสารและข้อจำกัด
