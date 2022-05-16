import pymysql
import datetime

conn = pymysql.connect(host='localhost', user='root', password='', db='mbt1', charset='utf8mb4')
cursor = conn.cursor()

def saveData(cur, con, event, weight, reps, oneRM):
    # Change Pk Key RDate -> REvent, RDate
    try:
        try:
            # Insert Data
            insert_sql = "insert into Record values('" + event + "', '" + datetime.date.today().strftime("%y-%m-%d") + "', " + str(weight) + ", " + str(reps) + ", " + str(oneRM) + ", 'kms', 1111);"
            cur.execute(insert_sql)
            con.commit()
            print(event + ": 새로운 데이터 생성")

        except:
            # Update Data
            update_sql = "update Record set RWeight = " + str(weight) + ", Rreps = " + str(reps) + ", R1rm = " + str(oneRM) + " where REvent = '" + event + "' and RDate = '" + datetime.date.today().strftime("%y-%m-%d") + "';"
            cur.execute(update_sql)
            con.commit()
            print(event + ": 오늘 데이터 최신화")
    except:
        con.rollback()
        print("실패")


def getData(cur, con, event):
    try:
        # ssql = "select * from Record where R1rm = (select max(R1rm) from Record where REvent = 'Squat' and UID = 'kms');"
        # cur.execute(ssql)
        # s1rm = cur.fetchone()
        # print(s1rm)

        ssql = "select * from Record where REvent = 'Squat' and UID = 'kms' order by RDate desc LIMIT 7;"
        cur.execute(ssql)
        s1rm = cur.fetchall()
        best_s1rm = 0
        s_1rm = {}
        for i in s1rm:
            if i[4] >= best_s1rm:
                best_s1rm = i[4]
            # print(str(i[0]) + " " + str(i[1]) + " " + str(i[4]))
            s_1rm[str(i[1])] = i[4]
            
        bsql = "select * from Record where REvent = 'BenchPress' and UID = 'kms' order by RDate desc LIMIT 7;"
        cur.execute(bsql)
        b1rm = cur.fetchall()
        best_b1rm = 0
        b_1rm = {}
        for j in b1rm:
            if j[4] >= best_b1rm:
                best_b1rm = j[4]
            # print(str(j[0]) + " " + str(j[1]) + " " + str(j[4]))
            b_1rm[str(j[1])] = j[4]

        dsql = "select * from Record where REvent = 'Deadlift' and UID = 'kms' order by RDate desc LIMIT 7;"
        cur.execute(dsql)
        d1rm = cur.fetchall()
        best_d1rm = 0
        d_1rm = {}
        for k in d1rm:
            if k[4] >= best_d1rm:
                best_d1rm = k[4]
            # print(str(k[0]) + " " + str(k[1]) + " " + str(k[4]))
            d_1rm[str(k[1])] = k[4]
        
        total = best_s1rm + best_b1rm + best_d1rm
        # print("Total : " + str(total) + ", S : " + str(best_s1rm) + ", B : " + str(best_b1rm) + ", D : " + str(best_d1rm))
        oneRM = {'Total':total, 'S':best_s1rm, 'B':best_b1rm, 'D':best_d1rm}

        # print(oneRM)
        # print("Squat : " + str(s_1rm))
        # print("BenchPress : " + str(b_1rm))
        # print("Deadlift : " + str(d_1rm))


        con.commit()
        if event == "Total":
            return oneRM
        elif event == "Squat":
            return s_1rm
        elif event == "BenchPress":
            return b_1rm
        elif event == "Deadlift":
            return d_1rm

    except:
        print("실패")
        con.rollback()


def deleteData(cur, con, reps):
    try:
        str2 = input("삭제할 인덱스 속성을 입력하시오 : ")
        sql = "drop index ix_" + str2 + " on employee"
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()



if __name__ == '__main__':
    print(getData(cursor, conn, "Total"))
    print(getData(cursor, conn, "Squat"))
    print(getData(cursor, conn, "BenchPress"))
    print(getData(cursor, conn, "Deadlift"))