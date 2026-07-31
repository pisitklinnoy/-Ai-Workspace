# FastAPI Authentication API (Login & Signup Example)

ตัวอย่างการทำ **API สำหรับ Login & Signup (Signin/Register)** ด้วย **FastAPI** ที่ออกแบบโครงสร้างโค้ดตามสถาปัตยกรรมและหลักการที่ระบุไว้ในเอกสาร **รายงานเรื่อง FastAPI (`รายงานFastAPI_6710110294.pdf`)**

---

## 🏛️ โครงสร้างและการออกแบบตามรายงาน (Layer Architecture & Best Practices)

ตามรายงาน การออกแบบ FastAPI ที่มีประสิทธิภาพและรองรับการขยายตัว (Scalability / Maintainability) จะใช้หลักการ **Separation of Concerns (SoC)** โดยแบ่ง Layer การทำงานออกเป็น 4 ชั้นหลัก:

```
[ Client ]
    │
    ▼
[ Presentation Layer ]  ---> app/routers/auth.py (Endpoints & Schemas Validation)
    │
    ▼
[ Application Layer ]   ---> app/core/dependencies.py & config.py (Dependency Injection & Security)
    │
    ▼
[ Business Logic Layer] ---> app/services/auth_service.py (Auth Rules, Hashing, Token Generation)
    │
    ▼
[ Data Layer ]          ---> app/repositories/user_repository.py & db/ (Database Access)
```

---

## 📂 โครงสร้างโฟลเดอร์ในโปรเจกต์ (Project Structure)

```
Assignment5-fastApi/
├── app/
│   ├── core/
│   │   ├── config.py         # Application Layer: โหลดการตั้งค่าระบบจาก .env (Secret Key, Expiration)
│   │   ├── security.py       # Application Layer: การ Hash รหัสผ่านด้วย Bcrypt และการสร้าง JWT Token
│   │   └── dependencies.py   # Application Layer: กลไก Dependency Injection (Depends()) สำหรับยืนยันตัวตน
│   ├── db/
│   │   └── database.py       # Data Layer: ระบบจัดเก็บข้อมูล / การเชื่อมต่อฐานข้อมูล
│   ├── repositories/
│   │   └── user_repository.py# Data Layer: การค้นหาและบันทึกข้อมูลผู้ใช้ (เช่น get_user_by_username)
│   ├── schemas/
│   │   ├── user.py           # Data Validation: Request Models (Input) และ Response Models (คัดกรอง sensitive data)
│   │   └── token.py          # Data Validation: Response Model สำหรับ JWT Access Token
│   ├── services/
│   │   └── auth_service.py   # Business Logic Layer: กฎการทำงานหลัก (ตรวจสอบบัญชีซ้ำ, ยืนยันรหัสผ่าน)
│   ├── routers/
│   │   └── auth.py           # Presentation Layer: เส้นทาง API (POST /signup, POST /login, GET /me)
│   └── main.py               # Application Instance: ประกาศ FastAPI(), ลงทะเบียน Router, เปิดใช้งาน Swagger UI
├── .env                      # ไฟล์เก็บ Environment Variables (เช่น SECRET_KEY)
├── .env.example              # ตัวอย่างไฟล์ตั้งค่า .env
├── requirements.txt          # รายการแพ็กเกจ Python ที่ต้องใช้งาน
├── test_auth_api.py          # สคริปต์สำหรับทดสอบการทำงานของ API อัตโนมัติ
└── README.md                 # เอกสารอธิบายการใช้งาน
```

---

## 🔑 จุดเด่นของโค้ดชุดนี้ตามเนื้อหาในรายงาน

1. **Application Instance & Automatic Docs (หัวข้อ 1 & 8 หน้า 2, 3)**
   - ประกาศ `FastAPI()` ใน [`app/main.py`](file:///C:/Ai-workspace/Assignment5-fastApi/app/main.py)
   - มีระบบสร้าง API Documentation อัตโนมัติด้วย **Swagger UI** ที่ URL `/docs`

2. **Data Validation & Schemas (หัวข้อ 4 หน้า 2)**
   - ใช้ **Pydantic Schemas** ตรวจสอบ Input ขาเข้า (`UserRegisterRequest`, `UserLoginRequest`)
   - ใช้ **Response Model** (`UserResponse`) ป้องกันไม่ให้ส่งรหัสผ่าน (`password` / `hashed_password`) ออกไปทาง API

3. **Dependency Injection & Security (หัวข้อ 5 หน้า 2 & หัวข้อ 3.1 หน้า 8)**
   - ใช้ `Depends()` ใน [`app/core/dependencies.py`](file:///C:/Ai-workspace/Assignment5-fastApi/app/core/dependencies.py) เพื่อดึงข้อมูลผู้ใช้ปัจจุบันและยืนยัน **JWT Token**
   - รหัสผ่านจะถูก **Hash ด้วย Bcrypt** ก่อนบันทึกเสมอ (ไม่เก็บเป็น Plaintext)

4. **Separation of Concerns & Loose Coupling (หัวข้อ 4.1 หน้า 10)**
   - **Presentation Layer** (`auth.py`) ทำหน้าที่รับส่ง Request/Response เท่านั้น ไม่เขียน Business Logic รวมใน Endpoint
   - **Business Logic Layer** (`auth_service.py`) ดูแลกฎของระบบ
   - **Data Layer** (`user_repository.py`) มีฟังก์ชันค้นหาข้อมูลเฉพาะ เช่น `get_user_by_username(username)` ตรงตามตัวอย่างในรายงานหน้า 7

---

## 🚀 วิธีการติดตั้งและสั่งรัน API

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. สั่งรัน FastAPI Server

```bash
uvicorn app.main:app --reload
```

หรือรันผ่าน Python โดยตรง:

```bash
python -m app.main
```

### 3. เข้าใช้งาน Swagger UI (Automatic Docs)

เปิดเว็บเบราว์เซอร์ไปที่:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🧪 วิธีการทดสอบระบบ (Automated Testing)

สามารถรันไฟล์ทดสอบอัตโนมัติเพื่อตรวจสอบการ Signup, Login และการยิง API ด้วย JWT Token ได้ทันที:

```bash
python test_auth_api.py
```

---

## 📡 รายละเอียด API Endpoints

| HTTP Method | Path | ความอธิบาย | Authorization | Status Code |
|---|---|---|---|---|
| `POST` | `/api/v1/auth/signup` | สมัครสมาชิกใหม่ (Register) | ไม่ต้องระบุ | `201 Created` |
| `POST` | `/api/v1/auth/login` | เข้าสู่ระบบ (Signin) รับ JWT Token | ไม่ต้องระบุ | `200 OK` |
| `GET` | `/api/v1/auth/me` | ดูข้อมูลผู้ใช้ปัจจุบันที่ล็อกอินอยู่ | `Bearer <Token>` | `200 OK` |
