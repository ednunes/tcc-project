import bpy
import time
import numpy as np
from addon.model_animation import ModelAnimation
from addon.utils.import_data import import_data 


class ADDONNAME_OT_animate_model_operator(bpy.types.Operator):
    bl_label = "Animate from data"
    bl_idname = "addonname.animate_model_operator"

    model_animation = None
    shape_index = 0
    shapes_len = 0

    data = {}
    fps = 30
    _timer = None

    def stop_playback(self, scene):
        if scene.frame_current == scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=False)

    def execute(self, context):
        # bpy.app.handlers.frame_change_pre.append(self.stop_playback)
        self.model_animation = ModelAnimation()

        wm = context.window_manager
        self._timer = wm.event_timer_add((1/self.fps), window=context.window)
        wm.modal_handler_add(self)

        return {'FINISHED'}

    def modal(self, context, event):
        time_start = time.time()
        if self.shape_index == (self.shapes_len - 1):
            return {'CANCELLED'}

        nd_shape = np.asarray(
            self.data[self.shape_index],
            dtype=np.float32
        )

        self.model_animation.set_animation(nd_shape)
        self.shape_index += 1
        print("TIME: %.4f sec" % (time.time() - time_start))

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        settings = context.scene.settings_properties
        settings.input_data_path = bpy.path.abspath(
            settings.input_data_path
        )
        self.fps = settings.number_of_fps
        self.data = import_data(settings.input_data_path)
        self.shapes_len = len(self.data)

        self.execute(context)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
