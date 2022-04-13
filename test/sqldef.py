import pymysql
import datetime

conn = pymysql.connect(host='localhost', user='root', password='alstlr2!', db='mbt1', charset='utf8mb4')
cursor = conn.cursor()

def saveData(cur, con, event, reps):
    try:
        # Insert Data
        # Change Pk Key Event -> Date
        insert_sql = "insert into Record values('" + event + "', '" + datetime.date.today().strftime("%y-%m-%d") + "', 0, " + str(reps) + ", 0, 'kms', 1111);"
        cur.execute(insert_sql)
        con.commit()
        print("새로운 데이터 생성")

    except:
        # Update Data
        update_sql = "update Record set Rreps = " + str(reps) + " where REvent = '" + event + "' and RDate = '" + datetime.date.today().strftime("%y-%m-%d") + "';"
        cur.execute(update_sql)
        con.commit()
        print("오늘 데이터 최신화")

def deleteData(cur, con, reps):
    try:
        str2 = input("삭제할 인덱스 속성을 입력하시오 : ")
        sql = "drop index ix_" + str2 + " on employee"
        cur.execute(sql)
        con.commit()
    except:
        conn.rollback()



if __name__ == "main":
    try:
        sql = "update Record set RDate = '22-02-02', RWeight = 12310, R1rm = 113 where REvent = 'squat' and UID = 'kms' and CCODE = 1111;"
        sql = "update Record set RDate = '22-02-02', RWeight = 12310, R1rm = " + str(1) + " where REvent = 'squat' and UID = 'kms' and CCODE = 1111;"
        print(sql)
        cursor.execute(sql)
        conn.commit()
        print("성공")

    except:
        print("실패")
        conn.rollback()
