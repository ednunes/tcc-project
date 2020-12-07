import cv2


def return_camera_indexes() -> list:
    # Checks the first 10 valid indexes
    available_devices = []
    for i in range(10):
        video_capture = cv2.VideoCapture(i)
        if video_capture.read()[0]:
            available_devices.append(i)
            video_capture.release()
    return available_devices


if __name__ == "__main__":
    available_devices = return_camera_indexes()
    print("The index of available devices:", available_devices)
