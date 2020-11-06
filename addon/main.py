bl_info = {
    "name": "Addon name",
    "description": "Addon description",
    "author": "Eduardo Nunes",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Add > Mesh",
    "warning": "",
    "support": "COMMUNITY",
    "category": "3D View",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/My_Script",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
}
 
import sys
import os
import bpy
import importlib

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

from addon.blender_interface import settings_properties
from addon.blender_interface import panel_blender
from addon.blender_interface import operator_blender
from addon.blender_interface import face_animation_operator

importlib.reload(settings_properties)
importlib.reload(panel_blender)
importlib.reload(operator_blender)
importlib.reload(face_animation_operator)

CLASSES = [
    settings_properties.SettingsProperties,
    panel_blender.ADDONNAME_PT_main_panel,
    operator_blender.ADDONNAME_OT_fcoperator,
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
