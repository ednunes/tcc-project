from addon.face_capture import FaceCapture
from addon.algorithms import OpenCVStrategy
from addon.algorithms import DlibOpenCVStrategy

from addon.characters import VincentModel 
from addon.characters import RainModel 

def get_landmarks_algorithm_option(option, params=()):
    algorithm = None
    if option == "opencv":
        algorithm = OpenCVStrategy(*params)
    elif option == "dlib":
        algorithm = DlibOpenCVStrategy(*params)

    return algorithm 

def get_character(option, params=()):
    character = None
    if option == "RIG-Vincent":
        character = VincentModel(*params)
    elif option == "RIG-rain":
        character = RainModel(*params)

    return character 

def manage_animation(settings):
    addon_settings = {
        "width": settings.window_width,
        "height": settings.window_height,
        "input_video": settings.input_video,
        "output_video": settings.output_video,
        "capture_mode": settings.capture_mode,
        "want_to_record": settings.want_to_record,
        "character_name": settings.character_name,
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
        get_character(addon_settings["character_name"]),
        addon_settings
    )

    return face_capture
