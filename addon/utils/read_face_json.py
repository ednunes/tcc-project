import numpy as np
import cv2
import codecs
import json
import time

file_path = "../data/data_json_fc.json"
print('OPEN JSON FILE:', file_path)
json_data = codecs.open(file_path, 'r', encoding='utf-8').read()
print('LOAD JSON DATA...')
data = json.loads(json_data)

print('SHOW DATA...')
while True:
    if len(data['shapes']) == 0:
        print('SHAPES IS EMPTY')
        break
    else:
        for shape in data['shapes']:
            frame = np.zeros((500,500,3), np.uint8)
            for (x, y) in shape:
                cv2.circle(frame, (round(x), round(y)), 2, (0, 255, 255), -1)

            cv2.imshow("Read face from json", frame)
            time.sleep(0.016)

            if(cv2.waitKey(1) == 27):
                exit()
