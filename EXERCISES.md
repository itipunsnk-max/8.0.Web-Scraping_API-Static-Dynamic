# Exercises

## Exercise 1: Add a source adapter

เพิ่ม parser สำหรับ fixture ใหม่ โดยคืนค่า schema เดียวกับ Phase 10 และเพิ่ม test เมื่อ field สำคัญหาย

## Exercise 2: Add an anomaly rule

ใช้ `validate_record_count()` หรือ helper ใหม่ตรวจ record count เปลี่ยนเกิน 30% จาก snapshot ก่อนหน้า แล้วเขียน test ทั้งกรณีผ่านและ fail

## Exercise 3: Scheduled export

เปลี่ยน scheduled entry point ให้รัน use case ที่เลือกได้จาก `--job` และยังคง exit code/lock/log contract เดิม

## Exercise 4: CI hardening

เพิ่ม job แยกสำหรับตรวจ Markdown links และอธิบายเหตุผลที่ใช้ least-privilege permissions

## Exercise 5: Vercel documentation

เพิ่มหน้า static ใน `site/` สำหรับ capstone แล้วทดสอบด้วย `vercel deploy` แบบ preview โดยไม่ใส่ token ใน repository
