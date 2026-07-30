# Phase 14: GitHub Documentation และ CI

Phase นี้เตรียม repository ให้ทำงานร่วมกันบน GitHub ได้เป็นระบบ โดย CI จะตรวจ Ruff และ pytest ทุกครั้งที่ push ไป `main` หรือเปิด Pull Request

## ไฟล์สำคัญ

- `.github/workflows/ci.yml` — matrix test บน Python 3.11 และ 3.12
- `.github/ISSUE_TEMPLATE/` — แบบฟอร์ม bug, feature และลิงก์รายงาน security
- `.github/pull_request_template.md` — checklist สำหรับ validation, security และ compatibility
- `CONTRIBUTING.md` — วิธี setup, branch, commit และ checks ก่อน PR
- `SECURITY.md` — แนวทางรายงานช่องโหว่และการจัดการ secret
- `CHANGELOG.md` — ประวัติการเปลี่ยนแปลง
- `RELEASE_CHECKLIST.md` — รายการตรวจความพร้อมก่อน release

## Local CI ที่เทียบเท่า

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest -q
```

หาก CI ล้มเหลว ให้เปิด step ที่ล้มเหลวใน GitHub Actions แล้วทำคำสั่งเดียวกันใน local environment รุ่นเดียวกันก่อนแก้ไข

## การออกแบบ workflow

- ใช้ `permissions: contents: read` เป็นค่าเริ่มต้นแบบ least privilege
- ใช้ `actions/checkout` และ `actions/setup-python` ที่ระบุ major version ชัดเจน
- ติดตั้ง dependencies จาก `pyproject.toml` แทนการซ้ำรายการใน workflow
- ใช้ fixture/local mock เพื่อให้ผล CI deterministic และไม่เพิ่มภาระให้เว็บไซต์จริง
- ไม่ส่ง secret ผ่าน command line; หากอนาคตมี deployment ให้ใช้ GitHub Actions Secrets และจำกัด permissions

## Troubleshooting

- ถ้า dependency install ล้มเหลว ให้ตรวจ `requires-python` และ lock/constraint ที่เกี่ยวข้อง
- ถ้า pytest ผ่าน local แต่ไม่ผ่าน CI ให้ตรวจ path separator, encoding และ timezone assumptions
- ถ้า Ruff ต่างกัน ให้ใช้เวอร์ชันจาก dev dependency และรัน `python -m ruff check .`
- ถ้า workflow ไม่ทำงาน ให้ตรวจ YAML indentation, event (`push`/`pull_request`) และ branch target
