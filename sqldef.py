# import pymysql
import datetime

# conn = pymysql.connect(host='localhost', user='root', password='', db='mbt1', charset='utf8mb4')
# cursor = conn.cursor()

def saveData(cur, con, event, reps):
    # Change Pk Key RDate -> REvent, RDate
    try:
        try:
            # Insert Data
            insert_sql = "insert into Record values('" + event + "', '" + datetime.date.today().strftime("%y-%m-%d") + "', 0, " + str(reps) + ", 0, 'kms', 1111);"
            cur.execute(insert_sql)
            con.commit()
            print(event + "새로운 데이터 생성")

        except:
            # Update Data
            update_sql = "update Record set Rreps = " + str(reps) + " where REvent = '" + event + "' and RDate = '" + datetime.date.today().strftime("%y-%m-%d") + "';"
            cur.execute(update_sql)
            con.commit()
            print(event + "오늘 데이터 최신화")
    except:
        con.rollback()
        print("실패")

def deleteData(cur, con, reps):
    try:
        str2 = input("삭제할 인덱스 속성을 입력하시오 : ")
        sql = "drop index ix_" + str2 + " on employee"
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()



if __name__ == "main":
    pass
