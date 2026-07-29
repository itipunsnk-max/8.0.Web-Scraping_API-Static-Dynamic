# Phase 13: Scheduling และ Automation

Phase นี้ทำให้ use case จาก Phase 12 รันแบบ Daily/Weekly บน Windows ได้ โดยมี entry point เดียว, log file, exit code และ lock file ป้องกันงานซ้ำซ้อน

## Entry point และ exit code

ตัวอย่าง entry point คือ `scripts/run_scheduled_job.py` ซึ่งรัน Price Monitor จาก fixture และใช้ `src/web_scraping_course/automation.py` จัดการ lifecycle ของ job:

- `0` ทำงานสำเร็จ
- `1` job ล้มเหลวจาก exception ที่ไม่คาดคิด
- `2` ข้ามรอบนี้เพราะมี lock ของรอบก่อนหน้าอยู่

ทุก job จะเขียน log แบบ UTF-8 และ lock จะเก็บ PID, hostname และเวลาเริ่มต้นไว้เพื่อให้ตรวจสอบได้

ทดลองจาก PowerShell:

```powershell
.\\scripts\\run_scheduled_job.ps1
Get-Content .\\output\\scheduled\\price-monitor.log
Get-Content .\\output\\scheduled\\price_changes.json
```

หากต้องการระบุ path เอง ให้ใช้ `-Previous`, `-Current`, `-Output`, `-Lock` และ `-Log` โดยไม่ใส่ token หรือ password ใน argument

## Windows Task Scheduler: Daily

เปิด PowerShell แบบสิทธิ์ที่เหมาะสมและลงทะเบียน task ด้วยคำสั่งต่อไปนี้:

```powershell
$root = (Resolve-Path .).Path
$action = New-ScheduledTaskAction `
  -Execute "PowerShell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$root\\scripts\\run_scheduled_job.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM
Register-ScheduledTask -TaskName "WebScraping-PriceMonitor-Daily" -Action $action -Trigger $trigger -Description "Run the local price monitor example"
```

ตรวจสอบ task และรันทดลองทันที:

```powershell
Get-ScheduledTask -TaskName "WebScraping-PriceMonitor-Daily"
Start-ScheduledTask -TaskName "WebScraping-PriceMonitor-Daily"
```

## Windows Task Scheduler: Weekly

เปลี่ยน trigger เป็นรายสัปดาห์ได้ดังนี้:

```powershell
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 6:00AM
Register-ScheduledTask -TaskName "WebScraping-PriceMonitor-Weekly" -Action $action -Trigger $trigger -Description "Run the local price monitor example weekly"
```

ในงาน production ควรกำหนด working directory ให้ชัดเจน, ใช้ service account ที่มีสิทธิ์เท่าที่จำเป็น และตรวจ Event Viewer/ไฟล์ log หลังตั้ง task

## Lock และการกู้คืน

หาก process ถูกหยุดกะทันหัน lock อาจค้างอยู่ ผู้ดูแลควรตรวจ PID/hostname/เวลาใน lock ก่อนลบด้วยตนเอง ห้ามตั้งค่าให้ลบ lock อัตโนมัติโดยไม่ตรวจอายุ เพราะอาจทำให้ job สองรอบเขียน output ทับกัน

## Security checklist

- ไม่เก็บ secret ใน script, command line หรือ Task Scheduler argument
- ใช้ `.env`/environment variable สำหรับค่า configuration ที่เป็นความลับ
- จำกัดสิทธิ์ของ account และโฟลเดอร์ output
- ตั้ง timeout, retry, rate limit และเคารพ Terms/`robots.txt` ก่อนใช้ endpoint จริง
- ให้ task แจ้งเตือนจาก exit code และ log แทนการพยายามหลบระบบป้องกันของเว็บไซต์

## การทดสอบ

```powershell
.\\.venv\\Scripts\\python.exe -m pytest .\\tests\\test_phase13_automation.py -q
.\\.venv\\Scripts\\python.exe -m ruff check .\\src .\\scripts .\\tests
```
