import bpy


class ADDONNAME_PT_main_panel:
    bl_label = "Face capture panel"
    bl_idname = "ADDONNAME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ADDONNAME Addon"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class ADDONNAME_PT_subpanel_animate_model(
        ADDONNAME_PT_main_panel, bpy.types.Panel):
    bl_idname = "ADDONNAME_PT_subpanel_animate_model"
    bl_label = "Animate from data"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.settings_properties
        layout.prop(settings, 'number_of_fps', text="Number of FPS")
        layout.prop(settings, 'input_data_path', text="Input data")

        layout.operator("addonname.animate_model_operator",
                        icon='RENDER_ANIMATION')


class ADDONNAME_PT_subpanel_face_capture(
        ADDONNAME_PT_main_panel, bpy.types.Panel):
    bl_idname = "ADDONNAME_PT_subpanel_face_capture"
    bl_label = "Face capture"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.settings_properties

        window_settings_layout = layout.box()
        window_settings_layout.label(text="Window display")
        window_settings_layout = window_settings_layout.column(align=True)
        window_settings_layout.separator()
        window_settings_layout = window_settings_layout.row(align=True)
        window_settings_layout.prop(settings, 'window_width')
        window_settings_layout.separator()
        window_settings_layout.prop(settings, 'window_height')

        device_selection_layout = layout.box()
        device_selection_layout.label(text="Capture settings")
        device_selection_layout.prop(
            settings, 'capture_mode', text="Capture mode")

        if settings.capture_mode == 'camera':
            device_selection_layout.prop(
                settings, 'capture_device', text="Capture device")

            device_selection_layout.prop(settings, 'want_to_record')
            if settings.want_to_record:
                device_selection_layout.prop(settings, 'output_video')

        elif settings.capture_mode == 'video':
            device_selection_layout.prop(
                settings, 'input_video', text="Video path")

        device_selection_layout.prop(settings, 'want_to_export_data')
        if settings.want_to_export_data:
            device_selection_layout.prop(settings, 'landmarks_export')

        landmark_layout = layout.box()
        landmark_layout.label(text="Landmark algorithms settings")
        landmark_layout.prop(
            settings, 'landmarks_algorithm_option', text="Algorithm")
        landmark_layout.prop(
            settings, 'landmarks_model_path', text="Model path")

        layout.operator("addonname.addonname_operator",
                        icon='RENDER_ANIMATION')
