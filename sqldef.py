import pymysql
import datetime
from time import sleep

conn = pymysql.connect(host='localhost', user='root', password='alstlr2!', db='mbt1', charset='utf8mb4')
cursor = conn.cursor()

def sign_up(cur, con, uid, upw):
    try:
        sign_sql = "insert into User values('" + uid + "', '" + upw + "');"
        cur.execute(sign_sql)

        init_sql_s = "insert into Record values('Squat', '" + datetime.date.today().strftime("%y-%m-%d") + "', 0, 0, 0, '" + uid + "', 1111);"
        cur.execute(init_sql_s)

        init_sql_b = "insert into Record values('BenchPress', '" + datetime.date.today().strftime("%y-%m-%d") + "', 0, 0, 0, '" + uid + "', 1111);"
        cur.execute(init_sql_b)

        init_sql_d = "insert into Record values('Deadlift', '" + datetime.date.today().strftime("%y-%m-%d") + "', 0, 0, 0, '" + uid + "', 1111);"
        cur.execute(init_sql_d)
        con.commit()
        print(uid + ":" + upw + " 님 회원가입 성공")
        return 1

    except:
        print("이미 존재하는 아이디 입니다.")
        con.rollback()
        return 0




def log_in(cur, con, uid, upw):
    try:
        log_sql = "select UID from User where UID = '" + str(uid) + "' and UPW = '" + str(upw) + "';"
        cur.execute(log_sql)
        con.commit()

        uname = cur.fetchone()
        print(str(uname[0]) + "님 환영합니다.")
        
        return 1 # success login
    except:
        print("일치하는 ID 또는 PW가 없습니다.")
        con.rollback()

        return 0 # fail login


def saveData(cur, con, event, weight, reps, oneRM, uid):
    try:
        try:
            # Insert Data
            insert_sql = "insert into Record values('" + event + "', '" + datetime.date.today().strftime("%y-%m-%d") + "', " + str(weight) + ", " + str(reps) + ", " + str(oneRM) + ", '" + uid + "', 1111);"
            cur.execute(insert_sql)
            con.commit()
            print(event + ": 새로운 데이터 생성")

        except:
            # Update Data
            update_sql = "update Record set RWeight = " + str(weight) + ", Rreps = " + str(reps) + ", R1rm = " + str(oneRM) + " where UID = '" + uid + "' and REvent = '" + event + "' and RDate = '" + datetime.date.today().strftime("%y-%m-%d") + "';"
            cur.execute(update_sql)
            con.commit()
            print(event + ": 오늘 데이터 최신화")
    except:
        con.rollback()
        print("실패")



def get_userData_s(cur, con, uid):
    try:
        s_sql = "select RDate, RWeight from Record where UID = '" + uid + "' and REvent = 'Squat' order by RDate desc LIMIT 7;"
        cur.execute(s_sql)
        con.commit()

        s_record = cur.fetchall()
        squat_record = {}
        for i in s_record:
            squat_record[str(i[0])] = i[1]
        
        return squat_record


    except:
        print("스쿼트 기록 조회 실패")
        con.rollback()


def get_userData_b(cur, con, uid):
    try:
        b_sql = "select RDate, RWeight from Record where UID = '" + uid + "' and REvent = 'BenchPress' order by RDate desc LIMIT 7;"
        cur.execute(b_sql)
        con.commit()

        b_record = cur.fetchall()
        bench_record = {}
        for i in b_record:
            bench_record[str(i[0])] = i[1]
        
        return bench_record

    except:
        print("벤치 기록 조회 실패")
        con.rollback()


def get_userData_d(cur, con, uid):
    try:
        d_sql = "select RDate, RWeight from Record where UID = '" + uid + "' and REvent = 'Deadlift' order by RDate desc LIMIT 7;"
        cur.execute(d_sql)
        con.commit()

        d_record = cur.fetchall()
        dead_record = {}
        for i in d_record:
            dead_record[str(i[0])] = i[1]
        
        return dead_record

    except:
        print("데드 기록 조회 실패")
        con.rollback()


def get_userData_t(cur, con, uid):
    sleep(1)
    try:
        oneRM = {}
        cur.execute("select MAX(RWeight) from Record where REvent = 'Squat' and UID = '" + uid + "';")
        con.commit()
        best_s = cur.fetchone()

        cur.execute("select MAX(RWeight) from Record where REvent = 'BenchPress' and UID = '" + uid + "';")
        con.commit()
        best_b = cur.fetchone()

        cur.execute("select MAX(RWeight) from Record where REvent = 'Deadlift' and UID = '" + uid + "';")
        con.commit()
        best_d = cur.fetchone()

        best_rm = best_s[0] + best_b[0] + best_d[0]

        oneRM['User'] = uid 
        oneRM['Total'] = best_rm 
        oneRM['S'] = best_s[0]
        oneRM['B'] = best_b[0]
        oneRM['D'] = best_d[0]
        
        return oneRM

    except:
        print("베스트 기록 조회 실패")
        con.rollback()



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

    # print(sign_up(cursor, conn, "kms", "0000"))
    # print(log_in(cursor, conn, "kms", "1234"))

    # print(rank_sys(cursor, conn))

    # print(get_userData_s(cursor, conn, 'kms'))
    # print(get_userData_b(cursor, conn, 'kms'))
    # print(get_userData_d(cursor, conn, 'kms'))

    # print(get_userData_t(cursor, conn, 'kms'))


    # print(type(get_userData_t(cursor, conn, 'kms')))
    # print(type(get_userData_s(cursor, conn, 'kms')))
    # print(type(get_userData_b(cursor, conn, 'kms')))
    # print(type(get_userData_d(cursor, conn, 'kms')))



