# Data Access Layer (Repositories)

ส่วนนี้ทำหน้าที่เป็น **Data Access Layer** หรือ **Repository Pattern** สำหรับติดต่อกับส่วนจัดเก็บข้อมูล

## หน้าที่หลัก
- เป็นตัวกลางระหว่าง Business Logic (Services) กับระบบจัดการฐานข้อมูล (Database)
- ทำหน้าที่จัดการคำสั่ง CRUD (Create, Read, Update, Delete) เฉพาะของแต่ละ Entity
- ซ่อนรายละเอียดการ query ข้อมูล ไม่ให้กระทบกับตรรกะในส่วนอื่น

## ไฟล์ในไดเรกทอรีนี้
- `user_repository.py`: ฟังก์ชันค้นหาและจัดการข้อมูลผู้ใช้ เช่น `get_by_username()`, `get_by_email()`, `create()`
