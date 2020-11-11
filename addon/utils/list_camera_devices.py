import cv2


def returnCameraIndexes() -> list:
    # checks the first 10 indexes.
    a = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            a.append(i)
            cap.release()
    return a


if __name__ == "__main__":
    returnCameraIndexes()
