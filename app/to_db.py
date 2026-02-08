# 录数据到数据库
import psycopg2
from uuid import uuid4
from datetime import datetime

conn = psycopg2.connect(
    host="15.223.161.189",
    port=5488,
    database="dmcomdb_test",
    user="saleor",
    password="saleor"
)

sql = """
INSERT INTO public.user_push_devices (
    user_id,
    platform,
    registration_id,
    alias,
    app_version,
    device_model,
    os_version,
    is_active,
    last_active_at
)
VALUES (
    %(user_id)s,
    %(platform)s,
    %(registration_id)s,
    %(alias)s,
    %(app_version)s,
    %(device_model)s,
    %(os_version)s,
    %(is_active)s,
    %(last_active_at)s
)
RETURNING id;
"""

data = {
    "user_id": str(uuid4()),                 # 必填 UUID
    "platform": "ios",                       # 必填
    "registration_id": "abc123-xyz-token",   # 必填
    "alias": "Rachel-iPhone",                # 必填
    "app_version": "1.2.0",
    "device_model": "iPhone 15",
    "os_version": "iOS 17.2",
    "is_active": True,
    "last_active_at": datetime.utcnow()
}

with conn:
    with conn.cursor() as cur:
        cur.execute(sql, data)
        new_id = cur.fetchone()[0]
        print("Inserted row id =", new_id)

conn.close()
