import cv2
import mediapipe as mp
import math


def get_angle(top, mid, bottom):
    angle = math.degrees(math.atan2(bottom[1] - mid[1], bottom[0] - mid[0]) - math.atan2(top[1] - mid[1], top[0] - mid[0]))

    if angle > 180.0:
        angle = 360 - angle

    return angle


def squat(hipAngle, kneeAngle, reps, status):
    if hipAngle < 100 and kneeAngle < 70:
        status = "SQUAT"
    if (hipAngle > 160 and kneeAngle > 160) and status == 'SQUAT':
        status = "  UP "
        reps +=1
    
    # print(hipAngle, kneeAngle)
    return hipAngle, kneeAngle, reps, status


def benchpress(elbowAngle,reps, status):
    if elbowAngle < 100:
        status = "Down"
    if elbowAngle > 160 and status == 'Down':
        status = "UP"
        reps +=1
    
    # print(elbowAngle)
    return elbowAngle, reps, status


def deadlift(hipAngle, kneeAngle, reps, status):
    if hipAngle < 60 and kneeAngle < 120:
        status = "Down"
    if (hipAngle > 170 and kneeAngle > 170) and status == 'Down':
        status = "UP"
        reps +=1
    
    # print(hipAngle, kneeAngle)
    return hipAngle, kneeAngle, reps, status

def onerm(weight, reps):
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

    return best


if __name__ == '__main__':
    
    print(onerm(140, 5))