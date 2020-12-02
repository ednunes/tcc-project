from addon.face_capture import FaceCapture
from addon.algorithms import OpenCVStrategy
from addon.algorithms import DlibOpenCVStrategy


def get_landmarks_algorithm_option(option, params):
    options = {
        "opencv": OpenCVStrategy(*params),
        "dlib": DlibOpenCVStrategy(*params),
    }

    return options[option]


def manage_animation(settings):
    addon_settings = {
        "width": settings.window_width,
        "height": settings.window_height,
        "input_video": settings.input_video,
        "output_video": settings.output_video,
        "capture_mode": settings.capture_mode,
        "want_to_record": settings.want_to_record,
        "landmarks_export": settings.landmarks_export,
        "device_option": settings.capture_device_result,
        "want_to_export_data": settings.want_to_export_data,
        "landmarks_model_path": settings.landmarks_model_path,
        "landmarks_algorithm_option": settings.landmarks_algorithm_option
    }

    print("ADDON SETTINGS", addon_settings)

    landmarks_algorithm_params = (
        (addon_settings["width"], addon_settings["height"]),
        addon_settings["landmarks_model_path"]
    )

    face_capture = FaceCapture(
        get_landmarks_algorithm_option(
            addon_settings["landmarks_algorithm_option"],
            landmarks_algorithm_params
        ),
        addon_settings
    )

    return face_capture
