bl_info = {
    "name": "Addon name",
    "description": "Addon description",
    "author": "Eduardo Nunes",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Add > Mesh (Add aqui o caminho)",
    "warning": "",
    "support": "COMMUNITY",
    "category": "3D View",
    "wiki_url": "github_link",
    "tracker_url": "github_link_issues"
}
 
import sys
import os
import bpy
import importlib

from addon.blender_interface import settings_properties
from addon.blender_interface import panel_blender
from addon.blender_interface import operator_blender
from addon.blender_interface import animate_model_from_data_operator 
from addon.blender_interface import face_animation_operator

importlib.reload(settings_properties)
importlib.reload(panel_blender)
importlib.reload(operator_blender)
importlib.reload(face_animation_operator)

CLASSES = [
    settings_properties.SettingsProperties,
    panel_blender.ADDONNAME_PT_subpanel_face_capture,
    panel_blender.ADDONNAME_PT_subpanel_animate_model,
    operator_blender.ADDONNAME_OT_fcoperator,
    animate_model_from_data_operator.ADDONNAME_OT_animate_model_operator,
    face_animation_operator.ADDONNAME_OT_face_animation_operator
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
    blend_dir = os.path.dirname(bpy.data.filepath)
    if blend_dir not in sys.path:
       sys.path.append(blend_dir)
