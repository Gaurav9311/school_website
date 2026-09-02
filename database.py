
import os
import pymysql

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"),
    user=os.getenv("DB_USER", "43T7tx6v7QgmbxN.root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "school"),
    port=int(os.getenv("DB_PORT", 4000))
    
)

