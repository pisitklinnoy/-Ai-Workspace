"""
Script สำหรับ Snapshot API List จาก FastAPI openapi.json แปลงเป็น CSV
ตามข้อกำหนดงาน WTN-A06 (ข้อ 4)
"""

import json
import csv
from app.main import app

def export_openapi_to_csv():
    # 1. ดึง OpenAPI Schema จาก FastAPI Application Instance โดยตรง
    openapi_schema = app.openapi()
    
    # 2. บันทึก openapi.json เก็บไว้เป็น Snapshot
    with open("openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, ensure_ascii=False, indent=2)
    print("[SUCCESS] openapi.json saved successfully.")

    # 3. สกัดข้อมูล Endpoints ออกมาจาก OpenAPI Schema
    api_list = []
    paths = openapi_schema.get("paths", {})
    
    for path, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            description = details.get("description", "").strip().replace("\n", " ")
            tags = ", ".join(details.get("tags", []))
            
            # การดึง Request Body / Parameters (ถ้ามี)
            request_body = "Yes" if "requestBody" in details else "No"
            
            # การสรุป Response status codes
            responses = ", ".join(details.get("responses", {}).keys())

            api_list.append({
                "Method": method.upper(),
                "Path": path,
                "Summary": summary,
                "Tags": tags,
                "Request Body": request_body,
                "Response Codes": responses,
                "Description": description
            })

    # 4. เขียนข้อมูลลงไฟล์ CSV (สามารถเปิดด้วย Microsoft Excel ได้)
    csv_filename = "api_list.csv"
    headers = ["Method", "Path", "Summary", "Tags", "Request Body", "Response Codes", "Description"]

    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(api_list)

    print(f"[SUCCESS] Exported API List to CSV: {csv_filename}")

if __name__ == "__main__":
    export_openapi_to_csv()
