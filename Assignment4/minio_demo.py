import os
import sys
from minio import Minio
from minio.error import S3Error
from minio.versioningconfig import VersioningConfig, ENABLED
from custom_logger import setup_custom_logger

# ตั้งค่า Custom Logger สำหรับโปรเจกต์
logger = setup_custom_logger(name="MinIO_Sandbox")

# ค่าการกำหนดการเชื่อมต่อ (Configuration)
MINIO_ENDPOINT = "localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadminpassword"
BUCKET_NAME = "my-profile-bucket"

# พาธไฟล์รูปถ่ายจริงในเครื่อง และชื่อ Object ใน MinIO
USER_PHOTO_PATH = r"C:\Ai-workspace\b1e011e2-d21c-49bc-8063-03050c9eb184.jpg"
OBJECT_NAME = "my_profile.jpg"

# ==============================================================================
# 1. Function สำหรับเชื่อมต่อ MinIO Server
# ==============================================================================
def connect_minio(endpoint: str, access_key: str, secret_key: str, secure: bool = False) -> Minio:
    """
    สร้างและคืนค่า MinIO Client วัตถุสำหรับสั่งการ MinIO Server
    """
    client = Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )
    logger.info(f"เชื่อมต่อ MinIO Server ที่ {endpoint} สำเร็จ")
    return client

# ==============================================================================
# 2. Function สำหรับตรวจสอบและสร้าง Bucket
# ==============================================================================
def create_bucket_if_not_exists(client: Minio, bucket_name: str):
    """
    ตรวจสอบว่ามี Bucket อยู่หรือไม่ หากยังไม่มีจะทำการสร้าง Bucket ใหม่
    """
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logger.info(f"สร้าง Bucket '{bucket_name}' สำเร็จ")
    else:
        logger.info(f"Bucket '{bucket_name}' มีอยู่แล้วในระบบ")

# ==============================================================================
# 3. Function สำหรับเปิดใช้งาน Object Versioning
# ==============================================================================
def enable_bucket_versioning(client: Minio, bucket_name: str):
    """
    เปิดใช้งาน Object Versioning บน Bucket ที่ระบุ
    """
    client.set_bucket_versioning(bucket_name, VersioningConfig(ENABLED))
    logger.info(f"เปิดใช้งาน Versioning บน Bucket '{bucket_name}' เรียบร้อยแล้ว")

# ==============================================================================
# 4. Function สำหรับอัปโหลดไฟล์ (Upload Data)
# ==============================================================================
def upload_file(client: Minio, bucket_name: str, object_name: str, file_path: str):
    """
    อัปโหลดไฟล์จากเครื่อง Local เข้าไปเก็บใน MinIO Bucket
    คืนค่า Object Version ID ที่ถูกสร้างขึ้น
    """
    if not os.path.exists(file_path):
        logger.error(f"ไม่พบไฟล์ที่ต้องการอัปโหลดที่พาธ: {file_path}")
        return None

    upload_result = client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path
    )
    logger.info(f"อัปโหลดไฟล์ '{object_name}' เข้า Bucket '{bucket_name}' สำเร็จ!")
    logger.info(f"Version ID ที่สร้างขึ้น: {upload_result.version_id}")
    return upload_result.version_id

# ==============================================================================
# 5. Function สำหรับดาวน์โหลดไฟล์ (Download Data)
# ==============================================================================
def download_file(client: Minio, bucket_name: str, object_name: str, dest_file_path: str, version_id: str = None):
    """
    ดาวน์โหลดไฟล์จาก MinIO Bucket มาเก็บบนเครื่อง Local
    สามารถระบุ version_id เพื่อดาวน์โหลดไฟล์เฉพาะเวอร์ชันได้
    """
    client.fget_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=dest_file_path,
        version_id=version_id
    )
    version_info = f" (Version: {version_id})" if version_id else " (Latest Version)"
    logger.info(f"ดาวน์โหลดไฟล์ '{object_name}'{version_info} สำเร็จ! บันทึกที่: {dest_file_path}")

# ==============================================================================
# Main Program
# ==============================================================================
def main():
    print("=" * 60)
    print("[+] เริ่มต้นกระบวนการ Sandbox MinIO (Upload & Download)")
    print("=" * 60)

    try:
        # 1. เชื่อมต่อ MinIO
        client = connect_minio(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY)

        # 2. สร้าง Bucket
        create_bucket_if_not_exists(client, BUCKET_NAME)

        # 3. เปิดใช้งาน Versioning
        enable_bucket_versioning(client, BUCKET_NAME)

        # 4. ทดสอบอัปโหลดไฟล์
        print("\n--- [1. ทดสอบ อัปโหลดข้อมูล (Upload)] ---")
        version_id = upload_file(client, BUCKET_NAME, OBJECT_NAME, USER_PHOTO_PATH)

        # 5. ทดสอบดาวน์โหลดไฟล์ (ไม่ระบุ version)
        print("\n--- [2. ทดสอบ ดาวน์โหลดข้อมูล (Download - Latest Version)] ---")
        download_file(client, BUCKET_NAME, OBJECT_NAME, "downloaded_my_profile.jpg")

        # 6. ทดสอบดาวน์โหลดไฟล์ (ระบุ version)
        if version_id:
            print("\n--- [3. ทดสอบ ดาวน์โหลดข้อมูล (Download - Specific Version)] ---")
            download_file(client, BUCKET_NAME, OBJECT_NAME, "downloaded_specific_version.jpg", version_id=version_id)

        print("\n" + "=" * 60)
        print("[OK] ทำรายการทดสอบ MinIO Sandbox เรียบร้อยแล้ว!")
        print("=" * 60)

    except S3Error as err:
        logger.error(f"เกิดข้อผิดพลาด MinIO S3: {err}")
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดระบบ: {e}")

if __name__ == "__main__":
    main()
