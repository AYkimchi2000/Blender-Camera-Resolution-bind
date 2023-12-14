bl_info = {
    "name": "Simple save Camera Resolution",
    "author": "AYkimchi2000",
    "version": (1, 0),
    "blender": (4, 0 , 0),
    "location": "View3D > N panel > Camera",
    "description": "Simple tool that saves and loads resolution to specific camera",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Object"
}

import bpy

# Operator to add a new camera
class OBJECT_OT_add_camera(bpy.types.Operator):
    """Operator to add a new camera"""
    bl_idname = "object.add_camera"
    bl_label = "Add Camera"
    
    camera_name: bpy.props.StringProperty(name="Camera Name", default="Camera")

    def execute(self, context):
        bpy.ops.object.camera_add()
        new_camera = context.object
        new_camera.name = self.camera_name
        if "camera_resolution" in new_camera:
            new_camera["camera_resolution"] = "1920x1080"
        context.scene.camera = new_camera
        return {'FINISHED'}

# Operator to set camera resolution
class OBJECT_OT_set_resolution(bpy.types.Operator):
    """Operator to set the resolution of the active camera and rename it"""
    bl_idname = "object.set_resolution"
    bl_label = "Set Camera Resolution"

    def execute(self, context):
        camera = context.scene.camera
        if camera and "camera_resolution" in camera:
            res_string = camera["camera_resolution"]
            resolution = tuple(map(int, res_string.split('x')))
            context.scene.render.resolution_x = resolution[0]
            context.scene.render.resolution_y = resolution[1]
            # Rename the camera object to match the resolution string
            camera.name = f"Camera_{res_string}"
        return {'FINISHED'}


# Operator to remove a camera
class OBJECT_OT_remove_camera(bpy.types.Operator):
    """Operator to remove the active camera"""
    bl_idname = "object.remove_camera"
    bl_label = "Remove Camera"

    def execute(self, context):
        if context.scene.camera:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            # Select and delete the camera
            context.scene.camera.select_set(True)
            bpy.ops.object.delete()
            # Reset active camera to None
            context.scene.camera = None
        return {'FINISHED'}

# UI Panel to control camera settings
class VIEW3D_PT_camera_resolution(bpy.types.Panel):
    """Panel in the 3D Viewport to control camera settings"""
    bl_label = "Camera Resolution Panel"
    bl_idname = "VIEW3D_PT_camera_resolution"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Camera'  # Changed from 'Tool' to 'Camera'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.add_camera")

        if context.scene.camera:
            layout.prop(context.scene.camera, "camera_resolution")
            layout.operator("object.remove_camera")

        layout.operator("object.set_resolution")

# Register function
def register():
    bpy.utils.register_class(OBJECT_OT_add_camera)
    bpy.utils.register_class(OBJECT_OT_set_resolution)
    bpy.utils.register_class(OBJECT_OT_remove_camera)
    bpy.utils.register_class(VIEW3D_PT_camera_resolution)
    bpy.types.Object.camera_resolution = bpy.props.StringProperty(name="Resolution", default="1920x1080")

# Unregister function
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_camera)
    bpy.utils.unregister_class(OBJECT_OT_set_resolution)
    bpy.utils.unregister_class(OBJECT_OT_remove_camera)
    bpy.utils.unregister_class(VIEW3D_PT_camera_resolution)
    del bpy.types.Object.camera_resolution

if __name__ == "__main__":
    register()
