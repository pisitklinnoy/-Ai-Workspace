# Application Layer & Infrastructure (Core)

ส่วนนี้ทำหน้าที่เก็บ **Infrastructure Configuration** และ **Core Utilities** ของระบบ

## หน้าที่หลัก
- โหลดการตั้งค่าจาก Environment Variables (`.env`) เช่น `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- ให้บริการฟังก์ชันระบบความปลอดภัย เช่น การทำ Password Hashing ด้วย Bcrypt และการสร้าง/แกะ JWT Token
- ให้บริการ Dependency Injection (`Depends()`) สำหรับการตรวจสอบยืนยันตัวตนผู้ใช้ใน Routers

## ไฟล์ในไดเรกทอรีนี้
- `config.py`: โหลดและจัดเก็บการตั้งค่าระบบผ่าน Pydantic BaseSettings
- `security.py`: ฟังก์ชันเกี่ยวกับความปลอดภัย (Hash Password & JWT Token)
- `dependencies.py`: Dependency functions สำหรับใช้ร่วมกับ FastAPI `Depends()`
