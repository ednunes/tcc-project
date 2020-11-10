import bpy
from addon.manager_animation import manager_animation

class ADDONNAME_OT_face_animation_operator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    # TODO change name of opencv_operator
    bl_idname = "wm.opencv_operator"
    bl_label = "OpenCV Animation Operator"
    
    _timer = None
    stop = False
    mg = None
    
    def modal(self, context, event):
        if (event.type in {'RIGHTMOUSE', 'ESC', 'Q'}) or self.stop == True:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            try:
                self.mg.main()
            except Exception as e:
                self.cancel(context)
                print('DEU RUIM no TRY', str(e))
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
        bpy.app.handlers.frame_change_pre.append(self.stop_playback)

        self.mg = manager_animation(context.scene.settings_properties)
        self.mg.init_camera()

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        self.mg.close_camera()