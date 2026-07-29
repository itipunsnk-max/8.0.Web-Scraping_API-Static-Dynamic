# Phase 7: Selenium

บทนี้แสดง Selenium บน Dynamic Mock Page เดียวกับ Phase 6 เพื่อให้เปรียบเทียบ Browser Automation ได้โดยไม่ต้องสร้าง Use case ซ้ำทั้งหมด

## สิ่งที่ได้ฝึก

- WebDriver และ Browser lifecycle
- `WebDriverWait` และ Expected Conditions
- Locator ด้วย `By.ID`, `By.CSS_SELECTOR` และ `By.TAG_NAME`
- เลือกค่าใน Form ด้วย `Select`
- อ่านตารางที่ JavaScript โหลด, Filter และ Load More
- บันทึก Screenshot
- ตั้งค่า Chrome download directory และรอไฟล์ที่ดาวน์โหลดเสร็จ
- ข้อดี ข้อจำกัด และกรณีที่ควรเลือก Selenium

## เตรียมเครื่องมือบน Windows

ถ้ายังไม่ได้ติดตั้ง Browser extra:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev,browser]"
```

Selenium รุ่นใหม่ใช้ Selenium Manager ช่วยค้นหา WebDriver หากเครื่องมี Google Chrome อยู่แล้ว ในบางองค์กร Selenium Manager อาจต้องดาวน์โหลด driver ผ่านอินเทอร์เน็ต

## เปิด Local Mock Website

Terminal ที่ 1:

```powershell
python -m http.server 8000 --directory mock_site
```

หน้าเดียวกับ Phase 6 อยู่ที่ `http://127.0.0.1:8000/dynamic/index.html`

## รันตัวอย่าง Selenium

Terminal ที่ 2:

```powershell
.\.venv\Scripts\python.exe .\examples\09_selenium\selenium_dynamic.py
```

แสดง Browser:

```powershell
.\.venv\Scripts\python.exe .\examples\09_selenium\selenium_dynamic.py --headed
```

ผลลัพธ์อยู่ใน `output/selenium_dynamic` ได้แก่ CSV/JSON, Screenshot และ `dynamic-catalog.csv` ที่ได้จาก Chrome download

## Selenium เทียบกับ Playwright

| ประเด็น | Selenium | Playwright |
| --- | --- | --- |
| แนวคิดหลัก | WebDriver ควบคุม Browser | Browser automation protocol ที่รวมอยู่ใน package |
| Wait | `WebDriverWait` + Expected Conditions | Locator auto-wait และ `expect_download()` |
| Download | ตั้งค่าโฟลเดอร์ แล้วรอไฟล์เกิดขึ้น | รอ Download event แล้ว `save_as()` |
| Browser lifecycle | สร้าง `webdriver.Chrome()` และ `quit()` | สร้าง Browser/Context และปิดทั้งคู่ |
| จุดแข็ง | รองรับระบบเดิมและภาษา/เครื่องมือหลากหลาย | API ทันสมัยและเหมาะกับงาน E2E ที่ต้องการ auto-wait |
| ข้อจำกัด | ต้องดูแล Driver/Browser compatibility และ wait เองมากขึ้น | ต้องติดตั้ง browser binaries และ package เฉพาะ |

## Selenium, Playwright, Requests และ BeautifulSoup

- ใช้ `Requests` ก่อนเมื่อข้อมูลอยู่ใน API หรือ HTML ที่ Static
- ใช้ `BeautifulSoup` เมื่อได้ HTML แล้วต้อง parse และ clean ข้อมูล
- ใช้ Playwright หรือ Selenium เมื่อข้อมูลต้องผ่าน JavaScript หรือมี Interaction ที่จำเป็น
- เลือก Selenium เมื่อระบบเดิมใช้ WebDriver, ทีมมีมาตรฐาน Selenium หรือจำเป็นต้องรองรับ Browser/ภาษาใน ecosystem เดิม

## ข้อควรระวัง

- ใช้กับเว็บไซต์จริงเมื่อมีสิทธิ์และตรวจ Terms, robots.txt, Rate Limit และ Privacy แล้ว
- ห้ามหลบ CAPTCHA, Login, Access Control หรือ Bot Protection
- ใช้ explicit wait แทน `time.sleep()` เป็นวิธีหลัก
- ตั้ง Timeout และเรียก `driver.quit()` ใน `finally` เสมอ
- ไม่เก็บ Cookie, Token, Password หรือข้อมูลส่วนบุคคลใน Repository

## Checklist จบ Phase 7

- [ ] เปิด Dynamic Mock Page ด้วย Selenium ได้
- [ ] ใช้ WebDriverWait และ Locator
- [ ] ใช้ Form filter และ Load More
- [ ] บันทึก Screenshot
- [ ] ตั้งค่าและตรวจ Download directory
- [ ] ปิด WebDriver อย่างถูกต้อง
- [ ] อธิบายความแตกต่างระหว่าง Selenium กับ Playwright ได้
