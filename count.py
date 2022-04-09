import cv2
import mediapipe as mp
import numpy as np
import math


def get_angle(top, mid, bottom):
    top = np.array(top)
    mid = np.array(mid)
    bottom = np.array(bottom)
    
    radians = np.arctan2(bottom[1]-mid[1], bottom[0]-mid[0]) - np.arctan2(top[1]-mid[1], top[0]-mid[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


def squat(hipAngle, kneeAngle, ankleAngle, reps, status):
    """
        서있을때 최대치
        hip : 176.6430509727502
        knee : 172.7119943786289
        ankle : 97.29720263433197

        앉았을떄 최저치
        hip : 51.8688295282371
        knee : 28.861298582203872
        ankle : 55.830331312741734

        스쿼트 자세인 하이바, 로우바의 서있을때 관절의 각도는 거의 동일하다.
        하지만 앉았을때 각도는 로우바가 하이바보다 고관절의 각도가 더 작지만, 무릎과 발목의 각도는 하이바가 더 작다.

        예시 영상은 하이바, 풀스쾃 이에 따라 각도를 참조하여 여유를 두었다. 
    """
    if (hipAngle > 40 and hipAngle < 60) and (kneeAngle > 25 and kneeAngle < 70) and (ankleAngle > 50 and ankleAngle < 70):
        status = "SQUAT"
    if (hipAngle > 170  and hipAngle < 180) and (kneeAngle < 180 and kneeAngle > 160) and (ankleAngle > 90) and status == 'SQUAT':
        status = "  UP "
        reps +=1
    
    # print(hipAngle, kneeAngle)
    return reps, status


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