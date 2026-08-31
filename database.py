
import os
import pymysql

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "mysql-19172a6e-gkg603348-5e56.c.aivencloud.com"),
    user=os.getenv("DB_USER", "avnadmin"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "school"),
    port=int(os.getenv("DB_PORT", 28680))
)