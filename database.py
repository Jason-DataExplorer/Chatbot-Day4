import os
import psycopg2
import datetime
from linebot.models.responses import Content


def prepare_record(msg):
    text_list = msg.split('\n')   

    record_list = []

    for i in text_list[1:]:
        temp_list = i.split(" ")

        name   = temp_list[0]
        weight = temp_list[1]
        height = temp_list[2]
        
        record = (name, weight, height, str(datetime.date.today()))
        record_list.append(record)
        
    return record_list


# 將資料匯入資料庫
def insert_record(record_list):
    DATABASE_URL = os.environ["DATABASE_URL"]
    
    conn   = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = conn.cursor()

    table_columns = "(name, weight, height, date)"
    postgres_insert_query = f"""INSERT INTO test_table {table_columns} VALUES (%s,%s,%s,%s)"""

    try:
        cursor.executemany(postgres_insert_query, record_list)
    except:
        cursor.execute(postgres_insert_query, record_list)
    
    conn.commit()

    # 要回傳的文字
    message = f"{cursor.rowcount}筆資料成功匯入資料庫囉"

    cursor.close()
    conn.close()

    return message


# 查詢資料
def select_record():
    DATABASE_URL = os.environ["DATABASE_URL"]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM test_table ORDER BY id"""

    cursor.execute(postgres_select_query)
    record = str(cursor.fetchall())

    content = ""
    record = record.split("),")

    for number, r in enumerate(record):
        content += f"第{number+1}筆資料\n{r}\n"

    cursor.close()
    conn.close()

    return content


# 刪除資料
def delete_record(msg):
    msg = msg.split(" ")[1]
    DATABASE_URL = os.environ["DATABASE_URL"]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_delete_query = f"""DELETE FROM test_table WHERE id = {msg}"""

    cursor.execute(postgres_delete_query)
    conn.commit()

    content = ""

    count = cursor.rowcount
    content += f"{count}筆資料成功從資料庫移除囉"

    cursor.close()
    conn.close()

    return content


# 更新資料
def update_record(msg):
    DATABASE_URL = os.environ["DATABASE_URL"]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    msg_list = msg.split(" ")
    column   = msg_list[1]
    origin   = msg_list[2]
    new      = msg_list[3]
    
    postgres_update_query = f"""UPDATE test_table set {column} = %s WHERE {column} = %s"""

    cursor.execute(postgres_update_query, (new, origin))
    conn.commit()

    content = ""

    count = cursor.rowcount
    content += f"{count}筆資料成功從資料庫更新囉"

    return content
