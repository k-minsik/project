import cv2
import mediapipe as mp
import math


def get_angle(top, mid, bottom):
    angle = math.degrees(math.atan2(bottom[1] - mid[1], bottom[0] - mid[0]) - math.atan2(top[1] - mid[1], top[0] - mid[0]))

    if angle > 180.0:
        angle = 360 - angle

    return angle


def squat(angle, reps, status):
    if angle < 70:
            status = "SQUAT"
    if angle > 160 and status == 'SQUAT':
        status = "UP"
        reps +=1
    
    print(angle)
    return angle, reps, status



if __name__ == '__main__':
    pass
