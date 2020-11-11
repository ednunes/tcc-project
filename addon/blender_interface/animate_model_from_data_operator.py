import bpy
import codecs
import json
import numpy as np
from addon.model_animation import ModelAnimation


class ADDONNAME_OT_animate_model_operator(bpy.types.Operator):
    bl_label = "Animate from json data"
    bl_idname = "addonname.animate_model_operator"

    model_animation = None
    shape_index = 0
    shapes_len = 0

    data = {}
    _timer = None

    def stop_playback(self, scene):
        if scene.frame_current == scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=False)

    def execute(self, context):
        # bpy.app.handlers.frame_change_pre.append(self.stop_playback)
        self.model_animation = ModelAnimation()

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.016, window=context.window)
        wm.modal_handler_add(self)

        return {'FINISHED'}

    def modal(self, context, event):
        if self.shape_index == (self.shapes_len - 1):
            return {'CANCELLED'}

        nd_shape = np.asarray(
            self.data['shapes'][self.shape_index],
            dtype=np.float32
        )

        self.model_animation.set_animation(nd_shape)
        self.shape_index += 1

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        settings = context.scene.settings_properties
        settings.input_json_path = bpy.path.abspath(
            settings.input_json_path
        )

        json_data = codecs.open(
            settings.input_json_path, 'r', encoding='utf-8'
        ).read()
        self.data = json.loads(json_data)
        self.shapes_len = len(self.data['shapes'])

        self.execute(context)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
