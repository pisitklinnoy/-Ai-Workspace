import os
from minio import Minio
from minio.error import S3Error
from minio.versioningconfig import VersioningConfig, ENABLED
from custom_logger import setup_custom_logger

# ตั้งค่า Logger
logger = setup_custom_logger(name="MinIO_Versioning_Demo")

MINIO_ENDPOINT = "localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadminpassword"
BUCKET_NAME = "my-profile-bucket"

# พาธไฟล์รูปถ่าย 2 รูปสำหรับการทดสอบ Versioning
PHOTO_V1_PATH = r"C:\Ai-workspace\b1e011e2-d21c-49bc-8063-03050c9eb184.jpg"  # รูปแรก (v1)
PHOTO_V2_PATH = r"C:\Ai-workspace\372fae08-61a7-42b8-bd34-26761ba020c8.jpg"                                  # รูปที่สอง (v2)
OBJECT_NAME = "my_profile.jpg"

def main():
    print("=" * 70)
    print("[+] การทดสอบ MinIO Object Versioning (3.b)")
    print("=" * 70)

    try:
        # 1. เชื่อมต่อ MinIO
        client = Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False
        )

        # 2. สร้าง Bucket (ถ้ายังไม่มี)
        if not client.bucket_exists(BUCKET_NAME):
            client.make_bucket(BUCKET_NAME)
            logger.info(f"สร้าง Bucket '{BUCKET_NAME}' สำเร็จ")

        # 3. เปิดใช้งาน Versioning
        client.set_bucket_versioning(BUCKET_NAME, VersioningConfig(ENABLED))
        logger.info(f"เปิดใช้งาน Object Versioning บน Bucket '{BUCKET_NAME}' สำเร็จ")

        # 4. อัปโหลดรูปภาพที่ 1 (Version 1)
        print("\n--- [1. อัปโหลดรูปที่ 1 (Photo v1)] ---")
        res1 = client.fput_object(BUCKET_NAME, OBJECT_NAME, PHOTO_V1_PATH)
        v1_id = res1.version_id
        logger.info(f"อัปโหลด รูปที่ 1 สำเร็จ | Version ID (v1): {v1_id}")

        # 5. อัปโหลดรูปภาพที่ 2 ชื่อนามสมมติเดิม (Version 2)
        print("\n--- [2. อัปโหลดรูปที่ 2 (Photo v2 - ชื่อไฟล์เดิม)] ---")
        res2 = client.fput_object(BUCKET_NAME, OBJECT_NAME, PHOTO_V2_PATH)
        v2_id = res2.version_id
        logger.info(f"อัปโหลด รูปที่ 2 สำเร็จ | Version ID (v2): {v2_id}")

        # 6. ทดสอบดึงข้อมูลแบบ 'ไม่ระบุ version_id' (จะได้รูป v2 ล่าสุด)
        print("\n--- [3. ทดสอบดึงข้อมูลแบบ 'ไม่ระบุ version'] ---")
        client.fget_object(BUCKET_NAME, OBJECT_NAME, "result_no_version.jpg")
        logger.info("ผลลัพธ์ (ไม่ระบุ version): ได้ไฟล์รูปภาพล่าสุด (Photo v2)")

        # 7. ทดสอบดึงข้อมูลแบบ 'ระบุ version_id = v1_id' (จะได้รูป v1 ย้อนหลัง)
        print("\n--- [4. ทดสอบดึงข้อมูลแบบ 'ระบุ version_id = v1_id'] ---")
        client.fget_object(BUCKET_NAME, OBJECT_NAME, "result_version_1.jpg", version_id=v1_id)
        logger.info(f"ผลลัพธ์ (ระบุ v1_id): ได้ไฟล์รูปภาพเวอร์ชันแรก (Photo v1) | Version ID: {v1_id}")

        # 8. ทดสอบดึงข้อมูลแบบ 'ระบุ version_id = v2_id' (จะได้รูป v2)
        print("\n--- [5. ทดสอบดึงข้อมูลแบบ 'ระบุ version_id = v2_id'] ---")
        client.fget_object(BUCKET_NAME, OBJECT_NAME, "result_version_2.jpg", version_id=v2_id)
        logger.info(f"ผลลัพธ์ (ระบุ v2_id): ได้ไฟล์รูปภาพเวอร์ชันสอง (Photo v2) | Version ID: {v2_id}")

        print("\n" + "=" * 70)
        print("[OK] ทดสอบ Versioning สำเร็จเรียบร้อยแล้ว!")
        print("=" * 70)

    except S3Error as err:
        logger.error(f"เกิดข้อผิดพลาด MinIO S3: {err}")
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดระบบ: {e}")

if __name__ == "__main__":
    main()
