bl_info = {
    "name": "Crivel",
    "description": "Crivel ",
    "author": "Eduardo Nunes",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Crivel Addon",
    "support": "COMMUNITY",
    "category": "3D View",
    "wiki_url": "github_link",
    "tracker_url": "github_link_issues"
}


import sys
import os
import bpy
import importlib

from .blender_interface import settings_properties
from .blender_interface import panel_blender
from .blender_interface import check_settings_data_operator
from .blender_interface import animate_model_from_data_operator
from .blender_interface import face_animation_operator

importlib.reload(settings_properties)
importlib.reload(panel_blender)
importlib.reload(check_settings_data_operator)
importlib.reload(face_animation_operator)

CLASSES = [
    settings_properties.SettingsProperties,
    panel_blender.ADDONNAME_PT_subpanel_face_capture,
    panel_blender.ADDONNAME_PT_subpanel_animate_model,
    face_animation_operator.ADDONNAME_OT_face_animation_operator,
    animate_model_from_data_operator.ADDONNAME_OT_animate_model_operator,
    check_settings_data_operator.ADDONNAME_OT_check_settings_data_operator
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.settings_properties = bpy.props.PointerProperty(
        type=settings_properties.SettingsProperties
    )


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.settings_properties

if __name__ == "__main__":
    register()
    # blend_dir = os.path.dirname(bpy.data.filepath)
    addon_path = os.path.expanduser("~/.config/blender/2.90/scripts/addons/addon")
    if addon_path not in sys.path:
       sys.path.append(addon_path)
