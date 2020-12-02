import bpy
from addon.manage_animation import manage_animation


class ADDONNAME_OT_face_animation_operator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    # TODO change name of opencv_operator
    bl_idname = "wm.opencv_operator"
    bl_label = "OpenCV Animation Operator"

    _timer = None
    want_to_record_data_from_video = False
    mg = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC', 'Q'}:
            self.cancel(context)
            return {'CANCELLED'}

        # TODO Remove o try except
        if event.type == 'TIMER':
            try:
                has_frame = self.mg.main()
                if not has_frame:
                    raise NameError('Frame is None')
            except Exception as e:
                self.cancel(context)
                print('ERROR', str(e))
                return {'CANCELLED'}

        if event.type == 'R' and event.value == 'PRESS':
            self.mg.recording = not self.mg.recording
            if not self.mg.recording:
                self.mg.save_data()

        return {'PASS_THROUGH'}

    def stop_playback(self, scene):
        if scene.frame_current == scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=False)

    def execute(self, context):
        # bpy.app.handlers.frame_change_pre.append(self.stop_playback)

        self.mg = manage_animation(context.scene.settings_properties)
        self.want_to_record_data_from_video = (
            context.scene.settings_properties.want_to_export_data and
            context.scene.settings_properties.capture_mode == 'video'
        )
        self.mg.init_camera()

        wm = context.window_manager
        ''' 0.033 = 30 fps '''
        self._timer = wm.event_timer_add(0.033, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self.want_to_record_data_from_video:
            self.mg.save_data()

        context.window_manager.event_timer_remove(self._timer)
        self.mg.close_camera()
