from addon.face_capture import FaceCapture
from addon.algorithms import OpenCVStrategy 
from addon.algorithms import DlibOpenCVStrategy

def manager_animation(settings):
    addon_settings = {
        'width': settings.window_width,
        'height': settings.window_height,
        'capture_mode': settings.capture_mode,
        'device_option': settings.capture_device_result,
        'want_to_export_json': settings.want_to_export_json,
        'landmarks_json_export': settings.landmarks_json_export,
        'want_to_record': settings.want_to_record,
        'output_video': settings.output_video,
        'input_video': settings.input_video,
        'landmarks_algorithm_option': settings.landmarks_algorithm_option,
        'landmarks_model_path': settings.landmarks_model_path
    }

    print('ADDON SETTINGS', addon_settings)
    
    face_capture = FaceCapture(
        DlibOpenCVStrategy(
            (addon_settings['width'], addon_settings['height']),
            addon_settings['landmarks_model_path']),
        addon_settings
    )
    
    return face_capture 
