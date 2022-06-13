import pymysql
import datetime

conn = pymysql.connect(host='localhost', user='root', password='alstlr2!', db='mbt1', charset='utf8mb4')
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


def get_userData(cur, con, event, uid):
    try:
        # ssql = "select * from Record where R1rm = (select max(R1rm) from Record where REvent = 'Squat' and UID = 'kms');"
        # cur.execute(ssql)
        # s1rm = cur.fetchone()
        # print(s1rm)

        ssql = "select * from Record where REvent = 'Squat' and UID = '" + str(uid) + "' order by RDate desc LIMIT 7;"
        cur.execute(ssql)
        con.commit()
        s1rm = cur.fetchall()
        best_s1rm = 0
        s_1rm = {}
        for i in s1rm:
            if i[4] >= best_s1rm:
                best_s1rm = i[4]
            # print(str(i[0]) + " " + str(i[1]) + " " + str(i[4]))
            s_1rm[str(i[1])] = i[4]
            
        bsql = "select * from Record where REvent = 'BenchPress' and UID = '" + str(uid) + "' order by RDate desc LIMIT 7;"
        cur.execute(bsql)
        con.commit()
        b1rm = cur.fetchall()
        best_b1rm = 0
        b_1rm = {}
        for j in b1rm:
            if j[4] >= best_b1rm:
                best_b1rm = j[4]
            # print(str(j[0]) + " " + str(j[1]) + " " + str(j[4]))
            b_1rm[str(j[1])] = j[4]

        dsql = "select * from Record where REvent = 'Deadlift' and UID = '" + str(uid) + "' order by RDate desc LIMIT 7;"
        cur.execute(dsql)
        con.commit()
        d1rm = cur.fetchall()
        best_d1rm = 0
        d_1rm = {}
        for k in d1rm:
            if k[4] >= best_d1rm:
                best_d1rm = k[4]
            # print(str(k[0]) + " " + str(k[1]) + " " + str(k[4]))
            d_1rm[str(k[1])] = k[4]
            uname = k[5]


        total = best_s1rm + best_b1rm + best_d1rm
        # print("Total : " + str(total) + ", S : " + str(best_s1rm) + ", B : " + str(best_b1rm) + ", D : " + str(best_d1rm))
        oneRM = {'User':uname, 'Total':total, 'S':best_s1rm, 'B':best_b1rm, 'D':best_d1rm}

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


def login(cur, con, uid, upw):
    try:
        log_sql = "select Uname from User where UID = '" + str(uid) + "' and UPW = '" + str(upw) + "';"
        cur.execute(log_sql)
        con.commit()

        uname = cur.fetchone()
        print(str(uname[0]) + "님 환영합니다.")
        
        return 1 # success login
    except:
        print("일치하는 ID 또는 PW가 없습니다.")
        con.rollback()

        return 0 # fail login




def rank_sys(cur, con):
    try:
        rank_list = {}
        query = "select UID from User"
        cur.execute(query)
        conn.commit()

        userID = cur.fetchall()

        for i in userID:
            cur.execute("select MAX(RWeight) from Record where REvent = 'Squat' and UID = '" + i[0] + "';")
            best_s = cur.fetchall()

            cur.execute("select MAX(RWeight) from Record where REvent = 'BenchPress' and UID = '" + i[0] + "';")
            best_b = cur.fetchall()

            cur.execute("select MAX(RWeight) from Record where REvent = 'Deadlift' and UID = '" + i[0] + "';")
            best_d = cur.fetchall()

            best_rm = best_s[0][0] + best_b[0][0] + best_d[0][0]
            rank_list[i[0]] = best_rm

        rank_list = dict(sorted(rank_list.items(), key=lambda x:x[1], reverse=True))

        print("랭크 조회 성공")
        return rank_list

    except:
        print("랭크 조회 실패")
        con.rollback()



if __name__ == '__main__':

    print(login(cursor, conn, "kms", "1234"))

    rank_sys(cursor, conn)




