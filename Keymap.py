bl_info = {
    "name": "Arrow Key Remap",
    "author": "паника",
    "version": (1, 21, 0),
    "blender": (4, 5, 0),
    "location": "3D View",
    "description": "Alt + L/R/U/D arrow keys snaps the 3D view to front, back, left, or right. Shift + U/D arrow keys snaps to top or bottom view. Regular . acts as numpad .",
    "category": "3D View",
}

import bpy

addon_keymaps = []

class VIEW3D_OT_snap_axis(bpy.types.Operator):
    bl_idname = "view3d.snap_axis"
    bl_label = "Snap View Axis"
    view_type: bpy.props.StringProperty()

    def execute(self, context):
        area = next((a for a in context.screen.areas if a.type == 'VIEW_3D'), None)
        if not area:
            return {'CANCELLED'}
        region_3d = next((s.region_3d for s in area.spaces if s.type == 'VIEW_3D'), None)
        if not region_3d:
            return {'CANCELLED'}

        region_3d.view_perspective = 'ORTHO'
        bpy.ops.view3d.view_axis(type=self.view_type)

        return {'FINISHED'}

class VIEW3D_OT_view_selected_safe(bpy.types.Operator):
    bl_idname = "view3d.view_selected_safe"
    bl_label = "View Selected Safe"

    def execute(self, context):
        if context.area and context.area.type == 'VIEW_3D':
            bpy.ops.view3d.view_selected()
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

def remove_timeline_arrows():
    for keymap_name in ['Screen', 'Animation']:
        km = bpy.context.window_manager.keyconfigs.user.keymaps.get(keymap_name)
        if km:
            for kmi in list(km.keymap_items):
                if kmi.type in {'LEFT_ARROW', 'RIGHT_ARROW', 'UP_ARROW', 'DOWN_ARROW'}:
                    if kmi.idname in {'screen.frame_offset', 'screen.frame_jump'}:
                        km.keymap_items.remove(kmi)

def register_shortcuts():
    global addon_keymaps
    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return
    remove_timeline_arrows()
    km = kc.keymaps.get('3D View')
    if not km:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    for kmi in list(km.keymap_items):
        if kmi.type in {'UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW', 'PERIOD'}:
            km.keymap_items.remove(kmi)
    def add_key(key, alt=False, shift=False, view_type='FRONT'):
        kmi = km.keymap_items.new(
            idname='view3d.snap_axis',
            type=key,
            value='PRESS',
            alt=alt,
            shift=shift
        )
        kmi.properties.view_type = view_type
        addon_keymaps.append((km, kmi))
    add_key('UP_ARROW', alt=True, view_type='BACK')
    add_key('DOWN_ARROW', alt=True, view_type='FRONT')
    add_key('LEFT_ARROW', alt=True, view_type='LEFT')
    add_key('RIGHT_ARROW', alt=True, view_type='RIGHT')
    add_key('UP_ARROW', shift=True, view_type='TOP')
    add_key('DOWN_ARROW', shift=True, view_type='BOTTOM')
    for kmi in list(km.keymap_items):
        if kmi.type == 'PERIOD' and kmi.idname in {'wm.call_menu', 'wm.call_menu_pie'}:
            km.keymap_items.remove(kmi)
    kmi = km.keymap_items.new(
        idname='view3d.view_selected_safe',
        type='PERIOD',
        value='PRESS'
    )
    addon_keymaps.append((km, kmi))

def unregister_shortcuts():
    global addon_keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    bpy.utils.register_class(VIEW3D_OT_snap_axis)
    bpy.utils.register_class(VIEW3D_OT_view_selected_safe)
    register_shortcuts()

def unregister():
    unregister_shortcuts()
    bpy.utils.unregister_class(VIEW3D_OT_snap_axis)
    bpy.utils.unregister_class(VIEW3D_OT_view_selected_safe)

if __name__ == "__main__":
    register()
