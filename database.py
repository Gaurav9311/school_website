
import os
from pathlib import Path

from dotenv import load_dotenv
import pymysql

load_dotenv(Path(__file__).resolve().parent / ".env")

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"),
    user=os.getenv("DB_USER", "43T7tx6v7QgmbxN.root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "school"),
    port=int(os.getenv("DB_PORT", 4000))

)



