# Presentation Layer (Routers)

ส่วนนี้ทำหน้าที่เป็น **Presentation Layer** หรือ **API Endpoints** ของระบบ

## หน้าที่หลัก
- ประกาศ `APIRouter` กำหนด Path Prefix และ Tags สำหรับ OpenAPI / Swagger UI
- รับ HTTP Requests (POST, GET ฯลฯ) และตรวจสอบความถูกต้องของข้อมูลผ่าน Pydantic Schemas
- เรียกใช้งาน Business Logic ผ่าน `AuthService` (โดยใช้ `Depends()`)
- ส่งคืน HTTP Status Codes และ Response JSON แก่ Client

## ไฟล์ในไดเรกทอรีนี้
- `auth.py`: กำหนดเส้นทาง API สำหรับระบบ Authentication (`/signup`, `/login`, `/me`)
