# Vercel Deployment Preparation

Repository นี้เตรียม Vercel สำหรับ static learning site ใน `site/` เท่านั้น ส่วน Python scraper, Windows Task Scheduler และ local output ยังทำงานใน repository/เครื่องของผู้ใช้

## สิ่งที่เตรียมไว้

- `vercel.json` กำหนด `outputDirectory` เป็น `site`
- `site/index.html`, `site/styles.css` และ `site/robots.txt`
- security headers สำหรับ static response
- ไม่มี environment variable หรือ token ที่ต้องฝังใน source

## เชื่อมต่อครั้งแรก

ติดตั้ง Vercel CLI และ login ด้วย account ของผู้ใช้ จากนั้นรันที่ repository root:

```powershell
npm install -g vercel
vercel login
vercel link
```

ตรวจว่า project ที่ link เป็น project ที่ตั้งใจใช้ แล้วสร้าง preview deployment:

```powershell
vercel deploy
```

เมื่อ preview ผ่านการตรวจสอบจึงค่อย deploy production:

```powershell
vercel deploy --prod
```

## Git integration

ทางเลือกที่แนะนำสำหรับทีมคือ import repository นี้ใน Vercel แล้วตั้ง Production Branch เป็น `main` โดยให้ project root อยู่ที่ repository root และปล่อยให้ `vercel.json` เลือก `site` เป็น output directory

## ข้อจำกัดและความปลอดภัย

- ยังไม่ได้ link project หรือ deploy เพราะต้องใช้ account/team ของผู้ใช้
- ห้าม commit `.vercel/`, `VERCEL_TOKEN`, `VERCEL_ORG_ID` หรือ `VERCEL_PROJECT_ID`
- หากใช้ GitHub Actions deploy ให้เก็บค่าเหล่านี้ใน repository/environment secrets และให้สิทธิ์เท่าที่จำเป็น
- อย่าใช้ Vercel เป็นตัวแทน Windows Task Scheduler หรือรัน scraper ที่ต้องใช้ browser/session แบบ local
