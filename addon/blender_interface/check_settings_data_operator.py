import bpy
import cv2


class CRIVEL_OT_check_settings_data_operator(bpy.types.Operator):
    bl_label = "Start face capture"
    bl_idname = "crivel.check_settings_data_operator"

    def is_device_available(self, device_id=0):
        if device_id.isdigit():
            device_id = int(device_id)

        cap = cv2.VideoCapture(device_id)

        available = False
        if cap.read()[0]:
            available = True
            cap.release()

        return available

    def execute(self, context):
        has_error = False
        settings = context.scene.settings_properties
        settings.landmarks_model_path = bpy.path.abspath(
            settings.landmarks_model_path)
        settings.landmarks_export = bpy.path.abspath(
            settings.landmarks_export)
        settings.output_video = bpy.path.abspath(settings.output_video)

        if settings.capture_mode == "camera":
            settings.capture_device_result = settings.capture_device
            if settings.want_to_record and len(settings.output_video) == 0:
                has_error = True
                self.report(
                    {"ERROR"}, "Please insert a output video path. Ex: /home/workspace/videoname.avi")
        else:
            settings.input_video = bpy.path.abspath(settings.input_video)
            settings.capture_device_result = settings.input_video

            if len(settings.input_video) == 0:
                has_error = True
                self.report(
                    {"ERROR"}, "Please insert a input video path. Ex: /home/workspace/videoname.avi")

        if len(settings.landmarks_model_path) == 0:
            has_error = True
            self.report({"ERROR"}, "Please select a landmark model path")

        try:
            bpy.data.objects[settings.character_name].pose.bones
        except:
            has_error = True
            self.report({"ERROR"}, "Please insert a character that is in the scene")

        if not self.is_device_available(settings.capture_device_result):
            has_error = True
            self.report({"ERROR"}, "Device or video not available.")

        if not has_error:
            bpy.ops.wm.face_animation_operator()

        return {"FINISHED"}
