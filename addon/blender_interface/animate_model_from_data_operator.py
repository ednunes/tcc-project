import bpy
import time
import numpy as np
from addon.manage_animation import get_character 
from addon.utils.import_data import import_data 


class ADDONNAME_OT_animate_model_operator(bpy.types.Operator):
    bl_label = "Animate from data"
    bl_idname = "addonname.animate_model_operator"

    character_animation = None
    shape_index = 0
    shapes_len = 0
    input_data_path = ""

    data = {}
    fps = 30
    _timer = None

    def stop_playback(self, scene):
        if scene.frame_current == scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=False)

    def execute(self, context):
        # bpy.app.handlers.frame_change_pre.append(self.stop_playback)
        if len(self.input_data_path) == 0:
            self.report({"ERROR"}, "Please insert a input data")
        else:
            self.data = import_data(self.input_data_path)
            if len(self.data) == 0:
                self.report({"ERROR"}, "Please insert a valid input data")
            else:
                self.shapes_len = len(self.data)

                self.character_animation = get_character('vincent')

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

        self.character_animation.set_animation(nd_shape)
        self.shape_index += 1
        # print("TIME: %.4f sec" % (time.time() - time_start))

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        settings = context.scene.settings_properties
        settings.input_data_path = bpy.path.abspath(
            settings.input_data_path
        )
        self.input_data_path = settings.input_data_path
        self.fps = settings.number_of_fps
        self.execute(context)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
