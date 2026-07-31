# คู่มือปฏิบัติงานและเทมเพลตรายงาน Assignment 05: MinIO and System Logging

คู่มือนี้สรุปขั้นตอนการทำงาน โค้ดที่ใช้ จุดที่ต้องแคปหน้าจอ (Screenshot) และโครงร่างรายงานสำหรับส่งอาจารย์ ตามโจทย์ในไฟล์ **Module-AIEcosystem-04 MinIO and System Logging.pdf**

> 💡 **โครงสร้างของโปรเจกต์ (ใน `C:\Ai-workspace`)**:
> - `compose.yml` (หลักด้านนอก): เพิ่ม MinIO Service เรียบร้อยแล้ว
> - `.gitignore` (หลักด้านนอก): ละเว้น `venv/` และ `logs/` เรียบร้อยแล้ว
> - `venv/` (ด้านนอก): Virtual Environment รวมของโปรเจกต์
> - `Assignment4/`: โฟลเดอร์งานนี้ บรรจุ `minio_demo.py` และ `custom_logger.py`

---

## 📋 เช็คลิสต์สิ่งที่ต้องทำและแคปหน้าจอส่ง

| หัวข้อ | สิ่งที่ต้องเตรียม/ทำ | สถานะ |
| :--- | :--- | :---: |
| **1. MinIO Service** | เพิ่ม MinIO ใน `compose.yml` + รัน `docker compose up -d minio` + แคปหน้าจอ MinIO Console | 🟩 พร้อมรัน |
| **2. อัปโหลดรูปภาพตนเอง** | คำสั่ง/สคริปต์อัปโหลดรูปของตัวเองเข้า MinIO + แคปหน้าจอ | 🟩 พร้อมรัน |
| **3. MinIO Sandbox & Script** | สคริปต์ `minio_demo.py` + อธิบาย Library/Function + ทดสอบ Versioning (ระบุ vs ไม่ระบุ Version) | 🟩 พร้อมรัน |
| **4. Custom System Logging** | สคริปต์ `custom_logger.py` + อธิบายหลักการออกแบบและไฟล์ Logs | 🟩 พร้อมรัน |
| **5. Docker Container Logging** | ตั้งค่าบันทึก Log ของแต่ละ Container + แคปหน้าจอ Logs ตอนเริ่ม Service | 🟩 พร้อมรัน |
| **6. Git & GitHub** | `.gitignore` (ข้าม Logs/venv) + Commit โค้ดลง GitHub + แนบลิงก์ | 🟩 พร้อมทำ |

---

## 🚀 ขั้นตอนการปฏิบัติงาน (Step-by-step Guide)

### 📌 ขั้นตอนที่ 1: เตรียม Virtual Environment และติดตั้ง Library
เปิด Terminal (PowerShell) ที่โฟลเดอร์หลัก `C:\Ai-workspace`:

1. **เปิดใช้งาน Virtual Environment** (ใช้ venv รวมที่อยู่ด้านนอก):
   ```powershell
   cd C:\Ai-workspace
   .\venv\Scripts\Activate.ps1
   ```
2. **ติดตั้ง Library ที่ต้องใช้ (`minio`)**:
   ```powershell
   pip install minio
   ```

---

### 📌 ขั้นตอนที่ 2: รัน MinIO Service ด้วย Docker
MinIO Service ถูกรวมไว้ใน [compose.yml](file:///C:/Ai-workspace/compose.yml) เรียบร้อยแล้ว:

**คำสั่งรันเฉพาะ MinIO Service**:
```powershell
cd C:\Ai-workspace
docker compose up -d minio
```

📸 **จุดที่ต้องแคปหน้าจอ (Screenshot Checkpoint 1)**:
1. หน้าจอ Terminal ที่สั่ง `docker compose up -d minio`
2. หน้าเว็บ MinIO Console เปิดผ่านเบราว์เซอร์ `http://localhost:9001` (Log in ด้วย `minioadmin` / `minioadminpassword`)

---

### 📌 ขั้นตอนที่ 3: บันทึกข้อมูลรูปภาพตนเอง และทดสอบ Sandbox/Versioning
ย้ายเข้าโฟลเดอร์ `Assignment4` แล้วสั่งรันสคริปต์ [minio_demo.py](file:///C:/Ai-workspace/Assignment4/minio_demo.py):

```powershell
cd C:\Ai-workspace\Assignment4
python minio_demo.py
```

> 💡 **หมายเหตุเกี่ยวกับรูปภาพของคุณ**:
> ในสคริปต์ `minio_demo.py` มีการสร้างไฟล์ภาพจำลองเพื่อทดสอบอัตโนมัติ หากต้องการใช้รูปถ่ายของคุณเอง สามารถนำรูปภาพของคุณมาวางในโฟลเดอร์ `Assignment4` ตั้งชื่อเป็น `my_photo_v1.jpg` และ `my_photo_v2.jpg` แล้วรันสคริปต์ใหม่ได้เลยครับ

📸 **จุดที่ต้องแคปหน้าจอ (Screenshot Checkpoint 2)**:
1. หน้าจอ Terminal ผลการรัน `python minio_demo.py` แสดง Log การอัปโหลดและดาวน์โหลดแบบต่างๆ
2. หน้าเว็บ MinIO Console (`http://localhost:9001`) แสดงไฟล์ `my_profile.jpg` ใน Bucket `my-profile-bucket` และแสดงประวัติ Versioning (คลิกดู Versions ใน MinIO Console)

---

### 📌 ขั้นตอนที่ 4: ตรวจสอบ Custom Logger และ System Logs
เราใช้สคริปต์ [custom_logger.py](file:///C:/Ai-workspace/Assignment4/custom_logger.py) เพื่อทำ Logging:
- Log จะแสดงออกทั้ง **Console (Terminal)** และถูกบันทึกลงไฟล์ **`Assignment4/logs/app.log`**
- รูปแบบ Log มี Timestamp, Log Level (`INFO`, `DEBUG`, `WARNING`, `ERROR`), ชื่อไฟล์ และเลขบรรทัด

**คำสั่งตรวจสอบ Log จาก Docker Container**:
```powershell
docker compose logs minio
```

📸 **จุดที่ต้องแคปหน้าจอ (Screenshot Checkpoint 3)**:
1. เนื้อหาภายในไฟล์ `Assignment4/logs/app.log` ที่เกิดจากการรันสคริปต์
2. ผลลัพธ์คำสั่ง `docker compose logs minio` เพื่อแสดง Log ของ MinIO Container

---

### 📌 ขั้นตอนที่ 5: บันทึกงานขึ้น Git & GitHub
ไฟล์ [.gitignore](file:///C:/Ai-workspace/.gitignore) ด้านนอกถูกตั้งค่าข้ามการ commit โฟลเดอร์ `logs/` และ `venv/` ไว้แล้ว

**คำสั่ง Git Commit & Push** (ทำที่ `C:\Ai-workspace`):
```powershell
cd C:\Ai-workspace
git add .
git commit -m "Assignment 04: Add MinIO Service, Custom Logger and Versioning Sandbox"
git push origin main
```

---

## 📝 โครงร่างรายงาน (Report Template) สำหรับนำไปส่งอาจารย์

คุณสามารถคัดลอกส่วนล่างนี้ไปใส่ในไฟล์รายงานของคุณได้เลย:

```markdown
# รายงาน Assignment 05: MinIO and System Logging

**ชื่อ-นามสกุล**: [ใส่ชื่อของคุณ]
**รหัสนักศึกษา**: [ใส่รหัสนักศึกษา]
**GitHub Repository**: [แปะลิงก์ GitHub Repo ของคุณที่นี่]

---

## Part 1: MinIO Service Setup & Image Upload

### 1.1 การสร้าง MinIO Service
- **ไฟล์ Configuration**: `compose.yml`
- **ขั้นตอนการทำงาน**: 
  1. ใช้ Docker Compose ในการสร้าง Container สำหรับ MinIO Service
  2. กำหนด Port `9000` สำหรับ MinIO API และ Port `9001` สำหรับ MinIO Web Console
  3. ตั้งค่า Persistent Volume `minio-data` เพื่อรักษาข้อมูลเมื่อสั่ง Restart Service

[วางภาพ Screenshot 1: ผลการรัน docker compose up -d minio และหน้าเว็บ MinIO Console]

---

### 1.2 การบันทึกรูปภาพตนเองเข้า MinIO
- **คำสั่ง / สคริปต์ที่ใช้**: ใช้ Python Library `minio` สั่งงานผ่านฟังก์ชัน `client.fput_object()` ในสคริปต์ `minio_demo.py`

[วางภาพ Screenshot 2: หน้า MinIO Console แสดงไฟล์รูปภาพที่ถูกอัปโหลดขึ้น Bucket]

---

## Part 2: MinIO Sandbox & Object Versioning

### 2.1 สคริปต์ทดสอบและการอธิบาย Function
- **Library ที่ใช้**: `minio` (Python SDK)
- **ฟังก์ชันสำคัญที่ใช้งาน**:
  - `Minio()`: ใช้สำหรับตั้งค่าการเชื่อมต่อกับ MinIO Server (Endpoint, Access Key, Secret Key)
  - `bucket_exists()` / `make_bucket()`: ตรวจสอบและสร้าง Bucket ใหม่หากยังไม่มี
  - `set_bucket_versioning()`: เปิดใช้งาน Object Versioning บน Bucket ด้วย `VersioningConfig(ENABLED)`
  - `fput_object()`: อัปโหลดไฟล์จากดิสก์เข้าสู่ MinIO Bucket
  - `fget_object()`: ดาวน์โหลดไฟล์จาก MinIO Bucket ลงมายังเครื่อง local (สามารถใส่ parameter `version_id` ได้)

### 2.2 หลักการทำ Versioning และผลการทดสอบ
- **หลักการทำงาน**: 
  เมื่อเปิดใช้งาน Versioning บน Bucket MinIO จะมอบหมาย Unique `version_id` ให้กับทุก Object ที่ถูกอัปโหลด หากมีการอัปโหลดไฟล์ใหม่ทับชื่อเดิม ไฟล์เดิมจะไม่ถูกลบทิ้งแต่จะถูกจัดเก็บเป็น Version เก่า
- **ผลการทดสอบ**:
  1. **ไม่ระบุ Version**: เมื่อสั่ง `fget_object()` โดยไม่ส่ง `version_id` ระบบจะคืนค่าไฟล์เวอร์ชันล่าสุดเสมอ (รูปที่ 2)
  2. **ระบุ Version**: เมื่อสั่ง `fget_object()` พร้อมระบุ `version_id` ของเวอร์ชันแรก ระบบจะคืนค่าไฟล์รูปภาพเวอร์ชันเดิม (รูปที่ 1) ได้อย่างถูกต้อง

[วางภาพ Screenshot 3: Terminal แสดง Log ผลการรัน minio_demo.py และการดึงข้อมูลทั้ง 2 เวอร์ชัน]
[วางภาพ Screenshot 4: หน้า MinIO Console แสดงรายการ Versions ของไฟล์ my_profile.jpg]

---

## Part 3: System Logging

### 3.1 การออกแบบ Custom Logger
- **หลักการออกแบบ**: 
  สร้าง Module `custom_logger.py` เพื่อจัดกลุ่ม Log ออกเป็น 2 ช่องทาง (Dual Stream):
  1. **Console Output (StreamHandler)**: แสดงผลแบบเรียลไทม์บน Terminal สำหรับนักพัฒนา
  2. **File Output (FileHandler)**: บันทึกเหตุการณ์ทั้งหมดลงไฟล์ `logs/app.log` พร้อม Timestamp, Log Level, ชื่อไฟล์ และบรรทัดที่เกิด Log เพื่อใช้ในการวิเคราะห์ย้อนหลัง

[วางภาพ Screenshot 5: เนื้อหาไฟล์ logs/app.log]

### 3.2 การปรับปรุง Docker Logging
- **วิธีทำ**: 
  กำหนด `logging` driver เป็น `json-file` พร้อมจำกัดขนาดไฟล์ใน `compose.yml` และใช้คำสั่ง `docker compose logs minio` ในการดึง Log ของแต่ละ Container

[วางภาพ Screenshot 6: ภาพ Logs จากการสั่ง docker compose logs minio]
```
