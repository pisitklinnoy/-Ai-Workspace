import logging
import os
from datetime import datetime

def setup_custom_logger(name: str = "MinIO_Project_Logger", log_dir: str = "logs", log_file: str = "app.log"):
    """
    สร้างและตั้งค่า Custom Logger สำหรับโปรเจกต์
    - บันทึก Log ออกทั้งทาง Console (Stdout) และไฟล์ (File Log)
    - รองรับ Log Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Format: Timestamp | Level | Logger Name | File:Line | Message
    """
    # สร้างโฟลเดอร์สำหรับเก็บ logs หากยังไม่มี
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filepath = os.path.join(log_dir, log_file)

    # สร้าง Logger Instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # บันทึกระดับ DEBUG ขึ้นไปทั้งหมด

    # ป้องกัน Handler ซ้ำซ้อนกรณีเรียกใช้หลายครั้ง
    if logger.hasHandlers():
        logger.handlers.clear()

    # รูปแบบข้อความ Log (Formatter)
    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console Handler (สำหรับแสดงผลหน้าจอ Terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 2. File Handler (สำหรับบันทึกลงไฟล์ logs/app.log)
    file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    # ทดสอบการทำงานของ Custom Logger
    logger = setup_custom_logger()
    logger.info("Custom Logger เริ่มต้นทำงานสำเร็จ!")
    logger.debug("นี่คือข้อความระดับ DEBUG (ถูกบันทึกลงไฟล์)")
    logger.warning("เตือนสติ: นี่คือข้อความระดับ WARNING")
    logger.error("ข้อผิดพลาดทดสอบ: นี่คือข้อความระดับ ERROR")
