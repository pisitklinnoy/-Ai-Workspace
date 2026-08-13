# Data Validation Layer (Schemas)

ส่วนนี้ทำหน้าที่เป็น **Data Validation Layer** กำหนดรูปแบบข้อมูลด้วย **Pydantic Models**

## หน้าที่หลัก
- **Request Models**: ตรวจสอบประเภทข้อมูล ขอบเขต และความถูกต้องของข้อมูลขาเข้า (Input Validation)
- **Response Models**: ควบคุมโครงสร้างข้อมูลขาออก (Output Validation) และซ่อนข้อมูลสุ่มเสี่ยง เช่น `password` / `hashed_password` ไม่ให้ส่งหลุดออกไปทาง API
- กำหนด Metadata และ Example Data เพื่อแสดงบน Swagger UI

## ไฟล์ในไดเรกทอรีนี้
- `user.py`: Schemas สำหรับ User Registration, User Login และ User Profile Response
- `token.py`: Schema สำหรับ JWT Access Token Response
