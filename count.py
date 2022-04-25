import numpy as np




def get_angle(top, mid, bottom):
    top = np.array(top)
    mid = np.array(mid)
    bottom = np.array(bottom)
    
    radians = np.arctan2(bottom[1]-mid[1], bottom[0]-mid[0]) - np.arctan2(top[1]-mid[1], top[0]-mid[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


def squat(RhipAngle, RkneeAngle, RankleAngle, LhipAngle, LkneeAngle, LankleAngle, reps, status):
    
    if ((RkneeAngle < 90) and (RhipAngle < 90) and (RankleAngle < 90)) or ((LkneeAngle < 90) and (LhipAngle < 90) and (LankleAngle < 90)):
        status = "SQUAT"
    if (((RhipAngle > 170)  and (RkneeAngle > 160) and (RankleAngle > 90)) or ((LhipAngle > 170)  and (LkneeAngle > 160) and (LankleAngle > 90))) and status == 'SQUAT':
        status = "  UP "
        reps +=1
    
    # print(hipAngle, kneeAngle)
    return reps, status


def benchpress(RelbowAngle, LelbowAngle, reps, status):
    if RelbowAngle < 100 or LelbowAngle < 100:
        status = "Down"
    if (RelbowAngle > 160 or LelbowAngle > 160) and status == 'Down':
        status = "UP"
        reps +=1
    
    # print(elbowAngle)
    return reps, status


def deadlift(RhipAngle, RkneeAngle, LhipAngle, LkneeAngle, reps, status):
    if (RhipAngle < 100 and RkneeAngle < 150) or (LhipAngle < 100 and LkneeAngle < 150):
        status = "Down"
    if ((RhipAngle > 170 and RkneeAngle > 170) or (LhipAngle > 170 and LkneeAngle > 170)) and status == 'Down':
        status = "UP"
        reps +=1
    
    # print(hipAngle, kneeAngle)
    return reps, status

def onerm(weight, reps):
    best = 0
    # NCSA 계산상수 활용
    if reps >= 12:  # 12회 이상은 12회로 계산
        best = weight / (0.7)
    elif reps == 11:
        best = weight / (0.73)
    elif reps == 10:
        best = weight / (0.75)
    elif reps == 9:
        best = weight / (0.77)
    elif reps == 8:
        best = weight / (0.80)
    elif reps == 7:
        best = weight / (0.83)
    elif reps == 6:
        best = weight / (0.85)
    elif reps == 5:
        best = weight / (0.87)
    elif reps == 4:
        best = weight / (0.90)
    elif reps == 3:
        best = weight / (0.93)
    elif reps == 2:
        best = weight / (0.95)
    elif reps == 1:
        best = weight

    return round(best, 1)


if __name__ == '__main__':
    
    print(onerm(100, 10))