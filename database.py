import pymysql


conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="root",            
    database="school",    
    port=3306  
)