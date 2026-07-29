# พื้นฐาน Web, HTML, HTTP และ Developer Tools

## เป้าหมายการเรียนรู้

เมื่อจบบทนี้ ผู้เรียนจะสามารถ:

- อธิบายการทำงานเบื้องต้นระหว่าง Client และ Server ได้
- แยกส่วนประกอบของ URL และเข้าใจ HTTP Request/Response
- อ่าน Status Code, Headers และ Cookies ในระดับพื้นฐาน
- ระบุ Tag, Attribute, Class, ID และโครงสร้าง DOM ได้
- ใช้ CSS Selector เพื่อค้นหา Element ในหน้าเว็บ
- แยก Static Website, Dynamic Website, API และ JSON ได้
- ใช้ Chrome Developer Tools ตรวจสอบหน้าเว็บและค้นหา Request ที่เกี่ยวข้องได้

## สิ่งที่ต้องเตรียม

- Python 3.11 หรือใหม่กว่า
- Google Chrome หรือ Chromium
- VS Code และโฟลเดอร์ Repository นี้
- เปิดใช้งาน Virtual Environment ตาม [Phase 1](01-installation.md) แล้ว

บทนี้ใช้ **Local Mock Website** ที่อยู่ใน Repository จึงไม่ต้องส่ง Request ไปยังเว็บไซต์ภายนอก

## คำศัพท์สำคัญ

| คำศัพท์ | ความหมายแบบสั้น |
| --- | --- |
| Client | โปรแกรมฝั่งผู้ใช้ เช่น Chrome ที่ส่ง Request |
| Server | ระบบที่รับ Request และส่งข้อมูลกลับ |
| URL | ที่อยู่ของ Resource บนเว็บ |
| Domain | ชื่อระบบหรือโฮสต์ เช่น `example.com` |
| Path | เส้นทางของ Resource หลัง Domain |
| Query String | ค่าพารามิเตอร์หลัง `?` เช่น `?topic=http` |
| HTTP Request | ข้อความที่ Client ส่งไปยัง Server |
| HTTP Response | ข้อความที่ Server ตอบกลับมา |
| Status Code | รหัสบอกผลการทำงาน เช่น `200` หรือ `404` |
| Header | ข้อมูลประกอบ Request หรือ Response |
| Cookie | ข้อมูลขนาดเล็กที่เว็บเก็บไว้กับ Browser |
| HTML Tag | หน่วยโครงสร้างเอกสาร เช่น `<p>` หรือ `<table>` |
| Attribute | คุณสมบัติของ Tag เช่น `href`, `id`, `class` |
| DOM | โครงสร้างเอกสารที่ Browser สร้างเพื่อให้โปรแกรมเข้าถึงได้ |
| CSS Selector | รูปแบบคำสั่งสำหรับเลือก Element |
| JavaScript | ภาษาที่ใช้เพิ่มพฤติกรรมหรือเปลี่ยนหน้าเว็บ |
| API | ช่องทางที่ระบบออกแบบให้โปรแกรมอื่นเรียกใช้ข้อมูล |
| JSON | รูปแบบข้อมูลแบบข้อความที่มีโครงสร้างเป็น Object/Array |

## Client และ Server

เมื่อเปิดหน้าเว็บ Browser ทำหน้าที่เป็น Client ส่ง HTTP Request ไปยัง Server จากนั้น Server ประมวลผลและส่ง HTTP Response กลับมา Response อาจมี HTML, CSS, รูปภาพ, JavaScript หรือข้อมูล JSON

```text
Browser (Client)
      │  HTTP Request
      ▼
Web Server
      │  HTTP Response
      ▼
Browser แสดงผลเป็นหน้าเว็บ
```

ในบทนี้ Python จะทำหน้าที่เป็น Local Web Server เพื่อส่งไฟล์ HTML จาก `mock_site/static` ให้ Browser เปิดดูได้

## ส่วนประกอบของ URL

ตัวอย่าง URL:

```text
https://example.com/guide/index.html?topic=http&level=beginner#selectors
```

| ส่วน | ตัวอย่าง | หน้าที่ |
| --- | --- | --- |
| Scheme | `https` | วิธีเชื่อมต่อ |
| Domain | `example.com` | ชื่อ Server |
| Path | `/guide/index.html` | ตำแหน่ง Resource |
| Query String | `?topic=http&level=beginner` | ค่าที่ส่งไปประกอบการค้นหาหรือกรองข้อมูล |
| Fragment | `#selectors` | จุดภายในหน้าเว็บที่ Browser เลื่อนไปหา |

สำหรับ Local Mock Website จะใช้ URL ลักษณะนี้:

```text
http://127.0.0.1:8000/index.html
```

`127.0.0.1` หมายถึงเครื่องของเราเอง และ Port `8000` คือช่องทางที่ Local Server เปิดรอรับ Request

## HTTP Request และ HTTP Response

Request โดยทั่วไปมี Method, URL, Headers และอาจมี Body ส่วน Response มี Status Code, Headers และ Body:

```text
Request:
  GET /index.html HTTP/1.1
  Host: 127.0.0.1:8000

Response:
  HTTP/1.0 200 OK
  Content-Type: text/html
  Body: HTML ของหน้าเว็บ
```

### HTTP Method ที่ควรรู้จัก

- `GET`: ขออ่านข้อมูล ไม่ควรใช้เพื่อแก้ไขข้อมูล
- `POST`: ส่งข้อมูลเพื่อสร้างหรือประมวลผลข้อมูล
- `PUT`/`PATCH`: แก้ไขข้อมูล
- `DELETE`: ลบข้อมูล

บทนี้ใช้ `GET` กับไฟล์ Local เท่านั้น และยังไม่ส่งข้อมูลส่วนตัวหรือข้อมูลรับรองใด ๆ

### Status Code

| กลุ่ม | ความหมาย | ตัวอย่าง |
| --- | --- | --- |
| 2xx | สำเร็จ | `200 OK`, `201 Created` |
| 3xx | เปลี่ยนเส้นทาง | `301`, `302`, `304` |
| 4xx | Request หรือสิทธิ์มีปัญหา | `400`, `401`, `403`, `404` |
| 5xx | Server ประมวลผลผิดพลาด | `500`, `502`, `503` |

Status Code ไม่ได้บอกเนื้อหาทั้งหมด เช่น `200` แปลว่า Server ส่ง Response สำเร็จ แต่ไม่ได้รับประกันว่าข้อมูลมีครบหรือมีรูปแบบตามที่เราต้องการ

### Headers

Headers คือข้อมูลกำกับการสื่อสาร เช่น:

- `Content-Type`: ประเภทข้อมูล เช่น `text/html` หรือ `application/json`
- `Content-Length`: ขนาดข้อมูล
- `User-Agent`: โปรแกรมที่ส่ง Request
- `Accept`: ประเภทข้อมูลที่ Client ยอมรับ
- `Location`: ปลายทางใหม่เมื่อเกิด Redirect

ห้ามคัดลอก Header ที่มี Token, Cookie หรือข้อมูลรับรองจากระบบจริงไปใส่ใน Source Code หรือ Git

### Cookies

Cookie คือข้อมูลที่ Browser เก็บไว้และอาจส่งกลับไปยัง Domain เดิมใน Request ถัดไป ใช้ได้กับการจดจำการตั้งค่า Session หรือสถานะบางอย่าง แต่ Cookie อาจมีข้อมูลสำคัญ ห้ามนำ Cookie ของผู้ใช้หรือระบบจริงไปเผยแพร่หรือใช้หลบระบบควบคุมการเข้าถึง

## HTML และ DOM

HTML เป็นภาษาสำหรับอธิบายโครงสร้างเอกสาร ตัวอย่าง:

```html
<article class="lesson-card" data-topic="html">
  <h2 id="html-heading">HTML Structure</h2>
  <p class="summary">โครงสร้างของหน้าเว็บ</p>
</article>
```

- `article`, `h2`, `p` คือ **Tag**
- `class`, `id`, `data-topic` คือ **Attribute**
- `lesson-card` และ `summary` คือค่า **Class**
- `html-heading` คือค่า **ID**
- Browser จะเปลี่ยน HTML เป็นต้นไม้ของ Node เรียกว่า **DOM (Document Object Model)**

HTML ที่ส่งมาจาก Server กับ DOM ที่เห็นใน Developer Tools อาจต่างกันได้ หาก JavaScript เพิ่ม ลบ หรือแก้ Element หลังโหลดหน้าเว็บ

## CSS Selector

CSS Selector ใช้บอกว่าเราต้องการเลือก Element ใดใน HTML ตัวอย่างทั้งหมดนี้ทดลองได้กับ [Local Mock Page](../mock_site/static/index.html):

| Selector | ความหมาย | ตัวอย่าง |
| --- | --- | --- |
| `h1` | เลือก Tag ชนิด `h1` | `h1` |
| `.lesson-card` | เลือก Element ที่มี Class | `.lesson-card` |
| `#page-title` | เลือก Element ที่มี ID | `#page-title` |
| `main .lesson-card` | เลือก `.lesson-card` ที่อยู่ใต้ `main` | `main .lesson-card` |
| `a[href]` | เลือก `a` ที่มี Attribute `href` | `a[href]` |
| `table tbody tr` | เลือกแถวในตาราง | `table tbody tr` |
| `[data-level="beginner"]` | เลือก Attribute ที่มีค่าตรงกัน | `[data-level="beginner"]` |

หลักสำคัญคือ ID ควรไม่ซ้ำในหน้าเดียวกัน ส่วน Class ใช้ซ้ำได้หลาย Element และ Descendant Selector ใช้เว้นวรรคเพื่อบอกความสัมพันธ์ระหว่าง Element ชั้นนอกกับชั้นใน

## Static Website, Dynamic Website, API และ JSON

### Static Website

ข้อมูลหลักอยู่ใน HTML ที่ Server ส่งกลับมา การดูเมนู **View Source** มักพบข้อมูลนั้นโดยตรง เครื่องมือที่เหมาะสมใน Phase ถัดไปคือ `requests` และ `BeautifulSoup`

### Dynamic Website

หน้าเว็บใช้ JavaScript เรียกข้อมูลหรือสร้าง Element หลังจาก Browser โหลด HTML แล้ว การขอ HTML ครั้งแรกอาจยังไม่มีข้อมูลที่เห็นบนหน้าจอ ต้องตรวจสอบ Network/API หรือใช้ Browser Automation ที่ได้รับอนุญาต

### API

API คือช่องทางสำหรับโปรแกรมเรียกใช้ข้อมูลตามรูปแบบที่ออกแบบไว้ เช่น Endpoint ที่ตอบกลับเป็น JSON ก่อนทำ Web Scraping ควรตรวจสอบว่ามี Official API ที่เหมาะสมหรือไม่

### JSON

JSON เป็นข้อมูลแบบข้อความ เช่น:

```json
{
  "name": "HTML Basics",
  "level": "beginner",
  "tags": ["html", "web"]
}
```

JSON ไม่ใช่หน้าเว็บ และไม่ใช่ HTML แม้ทั้งสองอย่างจะส่งผ่าน HTTP ได้เหมือนกัน

## เปิด Local Mock Website

เปิด PowerShell ที่โฟลเดอร์ Repository แล้วรัน:

```powershell
python -m http.server 8000 --directory mock_site/static
```

จากนั้นเปิด Chrome ไปที่:

```text
http://127.0.0.1:8000/index.html
```

รายละเอียดเพิ่มเติมอยู่ที่ [mock_site/README.md](../mock_site/README.md) หยุด Server ด้วย `Ctrl+C` เมื่อฝึกเสร็จ

## ฝึกใช้ Chrome Developer Tools

### ตรวจสอบ Elements

1. เปิด Local Mock Page
2. กด `F12` หรือ `Ctrl+Shift+I`
3. เลือกแท็บ **Elements**
4. กดปุ่มรูปตัวชี้ **Select an element** แล้วคลิกหัวข้อหรือแถวตาราง
5. สังเกต Tag, Attribute, Class และ ID
6. คลิกขวา Element แล้วเลือก **Copy > Copy selector** เพื่อดู Selector ที่ Chrome สร้างให้

ไม่ควรยึด Selector ที่มี `nth-child` ยาว ๆ โดยไม่จำเป็น เพราะเปลี่ยนง่ายเมื่อหน้าเว็บเพิ่ม Element ใหม่ ให้มองหา ID, Class หรือ Attribute ที่สื่อความหมายก่อน

### ทดลองใน Console

เลือกแท็บ **Console** แล้วรันทีละคำสั่ง:

```javascript
document.querySelector("#page-title").textContent
document.querySelectorAll(".lesson-card").length
document.querySelectorAll("#course-table tbody tr").length
document.querySelector('a[data-topic="html"]').href
document.querySelector("img#course-logo").alt
```

ผลที่คาดหวังคือได้ข้อความชื่อหน้า, จำนวน Card, จำนวนแถว, URL ของลิงก์ และข้อความ `alt` ของรูปภาพตามลำดับ ถ้า Selector ไม่พบ Element ผลลัพธ์อาจเป็น `null` หรือจำนวน `0`

### ตรวจสอบ Network

1. เปิดแท็บ **Network**
2. กดปุ่ม Clear เพื่อเคลียร์รายการเดิม
3. Reload หน้าเว็บด้วย `Ctrl+R`
4. คลิก Request ของ `index.html`
5. ดู **Headers**, **Preview** และ **Response**
6. กรองด้วย **Fetch/XHR** เพื่อค้นหา Request ที่มักใช้เรียก API

Local Mock Page ในบทนี้เป็น Static HTML จึงไม่ควรมี Fetch/XHR สำหรับโหลดข้อมูล หากเว็บจริงมีรายการ Fetch/XHR ให้ตรวจสอบ URL, Method, Status Code, Response และข้อกำหนดการใช้งานก่อนนำไปใช้

## ผลลัพธ์ที่คาดหวัง

- เปิด Local Mock Page ได้โดยไม่ต้องใช้อินเทอร์เน็ต
- เห็นหัวข้อ, Card, ตาราง, ลิงก์ และรูปภาพ
- ค้นหา `#page-title`, `.lesson-card`, `#course-table tbody tr` และ `img#course-logo` ได้
- เห็น HTTP Response ของ `index.html` เป็น Status `200`
- เข้าใจว่า Static Mock Page ไม่มี API Request แยกสำหรับข้อมูลในตาราง

## ข้อผิดพลาดที่พบบ่อย

### `localhost refused to connect`

ตรวจสอบว่า PowerShell ที่รัน `python -m http.server` ยังเปิดอยู่ และใช้ Port `8000` ตรงกับ URL ใน Browser

### Port 8000 ถูกใช้งานแล้ว

ใช้ Port อื่น เช่น:

```powershell
python -m http.server 8765 --directory mock_site/static
```

แล้วเปิด `http://127.0.0.1:8765/index.html`

### เห็นหน้า Directory แต่ไม่เห็นหน้าเว็บ

ตรวจสอบว่า URL ลงท้ายด้วย `/index.html` และคำสั่งใช้ `--directory mock_site/static` จากโฟลเดอร์ Repository ถูกต้อง

### `querySelector` ได้ `null`

ตรวจสอบการสะกดตัวพิมพ์เล็ก/ใหญ่และเครื่องหมาย `#`, `.`, หรือ `[attribute]` ให้ตรงกับ HTML ปัจจุบัน

### Copy Selector ยาวและเปราะบาง

เลือก Selector ที่อาศัย ID, Class หรือ Attribute ที่สื่อความหมาย และทดสอบกับ Element หลายรายการก่อนนำไปใช้ใน Parser

## แบบฝึกหัด

1. ใช้ Elements หา ID ของหัวข้อหลักและ Class ของ Card
2. เขียน CSS Selector ที่เลือกเฉพาะแถว `beginner` ในตาราง
3. ใช้ Console หาจำนวนลิงก์ใน `nav`
4. ตรวจสอบ `Content-Type` ของ `index.html` ใน Network
5. เปรียบเทียบ HTML จาก **View Page Source** กับ DOM ใน **Elements**

## Checklist

- [ ] อธิบาย Client และ Server ได้
- [ ] แยก Scheme, Domain, Path, Query String และ Fragment ได้
- [ ] เข้าใจ Request, Response, Status Code และ Header
- [ ] อธิบายความเสี่ยงของ Cookie ได้
- [ ] แยก Tag, Attribute, Class, ID และ DOM ได้
- [ ] ใช้ Tag, Class, ID, Descendant และ Attribute Selector ได้
- [ ] เปิด Local Mock Website ได้
- [ ] ใช้ Elements, Console และ Network ใน Developer Tools ได้
- [ ] รู้ความแตกต่างระหว่าง Static, Dynamic, API และ JSON

## สรุป

การเข้าใจ HTML, HTTP และ Developer Tools เป็นพื้นฐานก่อนเลือกเครื่องมือดึงข้อมูล ในบทถัดไปจะใช้แนวคิดนี้ตัดสินใจว่าเมื่อใดควรใช้ API ก่อนการ Scraping และวิธีอ่าน JSON อย่างปลอดภัย
