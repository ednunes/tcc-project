import cv2
import codecs
import json
import time
import numpy as np

file_path = "../data/data_json_fc.json"
print('OPEN JSON FILE:', file_path)
json_data = codecs.open(file_path, 'r', encoding='utf-8').read()
print('LOAD JSON DATA...')
data = json.loads(json_data)

def normalize_landmark(landmarks: list) -> np.array:
    center = np.mean(landmarks, axis=0)
    landmarks_norm = landmarks - center
    return landmarks_norm + 150

FPS = 10
SECONDS = 1 / FPS

print('SHOW DATA...')
while True:
    if len(data['shapes']) == 0:
        print('SHAPES IS EMPTY')
        break
    else:
        for shape in data['shapes']:
            frame = np.zeros((350, 350, 3), np.uint8)
            new_shape = normalize_landmark(shape)

            for (x, y) in new_shape:
                cv2.circle(frame, (round(x), round(y)), 2, (0, 255, 255), -1)

            cv2.imshow("Read face from json", frame)
            time.sleep(SECONDS)

            if(cv2.waitKey(1) == 27):
                exit()
