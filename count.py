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
        status = "UP"
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







if __name__ == '__main__':
    pass
