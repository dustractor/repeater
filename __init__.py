# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
        "name":        "repeater",
        "description": "repeater",
        "author":      "Shams Kitz <dustractor@gmail.com>",
        "version":     (1,0),
        "blender":     (2,80,0),
        "location":    "Mesh select menu in during edge mode",
        "warning":     "",
        "tracker_url": "https://github.com/dustractor/repeater",
        "wiki_url":    "",
        "category":    "Mesh"
        }

import bpy

class REPEATER_OT_repeater(bpy.types.Operator):
    bl_idname = "repeater.repeater"
    bl_label = "repeater"
    bl_options = {"REGISTER","UNDO"}
    op: bpy.props.StringProperty(default="tkit.epz")
    detach: bpy.props.BoolProperty(default=False)
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
    def execute(self,context):
        for modop in self.op.split(","):
            modn,opn = modop.split(".")
            module = getattr(bpy.ops,modn)
            op = getattr(module,opn)
            op()
        if self.detach:
            ob = context.active_object
            acname = ob.name
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.duplicate()
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.duplicate()
            bpy.ops.mesh.select_all(action="INVERT")
            bpy.ops.mesh.delete()
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_pattern(pattern=acname,extend=False)
            context.view_layer.objects.active = ob
            bpy.ops.object.mode_set(mode="EDIT")
        return {'FINISHED'}


def draw_menu(self,context):
    self.layout.operator("repeater.repeater")

def register():
    bpy.utils.register_class(REPEATER_OT_repeater)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_select_edit_mesh.remove(draw_menu)
    bpy.utils.unregister_class(REPEATER_OT_repeater)
