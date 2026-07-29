# Answer Guide

1. API มี schema ชัดกว่า ลดการตีความ HTML และมักลด request ที่ไม่จำเป็น
2. Timeout ป้องกันงานค้าง ส่วน rate limit ลดภาระต่อระบบปลายทางและช่วยให้ทำงานตาม policy
3. ทำให้ test deterministic, เร็ว และไม่ขึ้นกับ network หรือการเปลี่ยนแปลงของเว็บจริง
4. command line อาจปรากฏใน process list หรือ task history; ใช้ environment/secret store แทน
5. มี lock ของรอบอื่นอยู่ จึงข้ามการทำงานเพื่อป้องกัน output ชนกัน
6. Raw เก็บ input ใกล้ต้นฉบับเพื่อ audit; processed เก็บ schema ที่ normalize และพร้อมใช้งาน
7. Terms, `robots.txt`, permission, content type, extension, host allow-list และ rate limit
8. ให้สิทธิ์เท่าที่จำเป็น เช่น `contents: read` สำหรับ test/lint
9. ใช้เผยแพร่ static documentation/learning landing page ไม่ใช่รัน Windows scraper หรือ Task Scheduler บน Vercel
10. Fail fast เมื่อข้อมูลผิดจนเสี่ยงสร้างผลลัพธ์ผิด; graceful degradation เมื่อมี fallback ที่ตรวจสอบได้และส่งสัญญาณเตือนชัดเจน
