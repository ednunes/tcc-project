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

def normalize_landmark(landmarks):
    center = np.mean(landmarks, axis=0)
    # print('CENTER', center)
    landmarks_norm = landmarks - center
    return landmarks_norm + 100
FPS = 10

print('SHOW DATA...')
while True:
    if len(data['shapes']) == 0:
        print('SHAPES IS EMPTY')
        break
    else:
        for shape in data['shapes']:
            frame = np.zeros((500, 500, 3), np.uint8)
            new_shape = normalize_landmark(shape)
            print(new_shape, shape)
            for (x, y) in new_shape:
                cv2.circle(frame, (round(x), round(y)), 2, (0, 255, 255), -1)

            cv2.imshow("Read face from json", frame)
            time.sleep(1/FPS)

            if(cv2.waitKey(1) == 27):
                exit()
