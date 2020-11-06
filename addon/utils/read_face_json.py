import numpy as np
import cv2 as cv
import codecs, json
import time

file_path = "../data/data_json_fc.json"
print('OPEN JSON FILE:', file_path)
json_data = codecs.open(file_path, 'r', encoding='utf-8').read()
print('LOAD JSON DATA...')
data = json.loads(json_data)

print('SHOW DATA...')
while(1):
    if len(data['shapes']) == 0:
        print('SHAPES IS EMPTY')
        break
    else:
        for shape in data['shapes']:
            frame = np.zeros((1000,1000,3), np.uint8)
            for (x, y) in shape:
                cv.circle(frame, (round(x), round(y)), 2, (0, 255, 255), -1)

            cv.imshow("Read face from json", frame)
            time.sleep(0.05)

            if(cv.waitKey(1) == 27):
                exit()
