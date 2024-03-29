import bpy
from typing import List

DEFAULT_WIDTH = 860
DEFAULT_HEIGHT = 640


def get_devices(self, context) -> List:
    devices = []
    MAX_DEVICES_IDS = 10

    for device_id in range(MAX_DEVICES_IDS):
        name = "Device %s" % device_id
        devices.append((str(device_id), name, ""))

    return devices


class SettingsProperties(bpy.types.PropertyGroup):
    window_width: bpy.props.IntProperty(
        name="Width:",
        description="Window display width",
        default=DEFAULT_WIDTH,
        soft_min=1
    )
    window_height: bpy.props.IntProperty(
        name="Height:",
        description="Window display height",
        default=DEFAULT_HEIGHT,
        soft_min=1
    )
    want_to_record: bpy.props.BoolProperty(
        name="Export webcam video",
        description="Option to record captured video",
        default=True
    )
    want_to_export_data: bpy.props.BoolProperty(
        name="Export landmarks in defined format",
        description="Option to export landmarks in format",
        default=True
    )
    capture_device_result: bpy.props.StringProperty(
        name="Capture device",
        description="Can be a int or a input video path",
        default=""
    )
    output_video: bpy.props.StringProperty(
        name="Output video",
        description="Path, name and format of recorded video. Ex: /home/workspace/videoname.avi",
        default="",
        subtype="FILE_PATH"
    )
    capture_mode: bpy.props.EnumProperty(
        name="Capture mode",
        description="Defines the form of input for detecting landmarks",
        default="camera",
        items=[
            ("camera", "Camera", ""),
            ("video", "Video", "")
        ]
    )
    input_video: bpy.props.StringProperty(
        name="Video path",
        description="Input video for landmarks detecction",
        default="",
        subtype="FILE_PATH"
    )
    capture_device: bpy.props.EnumProperty(
        name="Capture device",
        description="Select the device ID",
        default=0,
        items=get_devices
    )
    landmarks_model_path: bpy.props.StringProperty(
        name="Landmarks model path",
        description="Trained landmarks detection model",
        default="",
        subtype="FILE_PATH"
    )
    landmarks_export: bpy.props.StringProperty(
        name="Output landmarks",
        description="Landmarks result in defined export format. Ex: /home/folder/data.json",
        default="",
        subtype="FILE_PATH"
    )
    input_data_path: bpy.props.StringProperty(
        name="Input data path",
        description="Data used to animate 3D model. Ex: /home/folder/data.json",
        default="",
        subtype="FILE_PATH"
    )
    number_of_fps: bpy.props.IntProperty(
        name="Number of fps:",
        description="Number of frames per second",
        default=30,
        soft_min=1
    )
    character_name: bpy.props.EnumProperty(
        name="Character name",
        description="Character name to bones access",
        default="RIG-Vincent",
        items=[
            ("RIG-Vincent", "Vincent", ""),
            ("RIG-rain", "Rain", "")
        ]
    )

    # TODO get the items list from a file
    landmarks_algorithm_option: bpy.props.EnumProperty(
        name="Algorithm",
        description="Landmarks algorithms options",
        default="opencv",
        items=[
            ("opencv", "OpenCV", ""),
            ("dlib", "Dlib", "")
        ]
    )
