# //make all quads or ngons on your mesh planar (2d)
# /*Delete one side of the model, luckily this is a symetrical mesh, it is enough to edit half of it, then mirror it for the other side.
# Select all vertices on a quad IN TURN (you have to do this right clicking on each verts instead of using tools like border select or cicle select). This first quad should be around the center of the topology structure (eye in this case, you'll realize why I recommend to do so later). Then click Coplanar by 3 Verts button in Mesh Tools panel in Tool tab. In the option below, set Reference Plane to First, which mean taking the first three selected vertices to define the reference plane.
# Then select two vertices on either edge first, then select one adjacent quad which shares the same edge with this quad, then repeat step 2.
# Repeat it until you finish this operation on every quad. Now, all quads should be "perfectly" planar. (Note that you have to avoid re-touching all polygons that have been tweaked, otherwise the distortion will be distributed back!)
# To check it, there are generally three ways in Edit Mode:

# Select all polygons then use Mesh > Clean up > Split Non-Planar Faces (or find it in Spacebar searcher), set Max Angle to 0.001 in the option panel, which is the smallest accepted value (0 means to split all quads or ngons no matter what). If no quads splitted, then congratulations.

# In Properties sidebar (N panel), toggle Mesh Analysis panel, then set Type to Distortion. set the min angle to 0°, and the second angle to a very small degree like 0.1° (values smaller than that will not that helpful here anyway). If all quads appear as dark blue identically, then congratulations.

# Go to File > User Preferences... > Add-ons, enable 3D Print Toolbox addon. Find 3D Printing tab in tool sidebar (T panel), click Distorted under Checks section, while keepting the degree value 0 as default. If any non-flat polygons found, You'll see the check result in Output Section Below, click that button will select all non-flat faces so you can see where further tweaks needed. If it shows 0, then congratulations. This is the most recommended way for final check.

# However, not all cases can be done by this solution. Your case got some luck because:
# it is an open mesh (not solid);
# it is symetrical (make it more affordable for manual tweaking);
# it has a relatively simple topology;
# there are a few triangles, which can be used to make adjacent quads happy if you have to.
# However, more tweaks have to be taken for fine tuning (mainly for avoiding distortion happening again while mirroring).*/


bl_info = {
    "name": "Coplanar by 3 Verts",
    "author": "NirenYang[BlenderCN]",
    "version": (0, 1),
    "blender": (2, 75, 5),
    "location": "3d view - toolbar",
    "description": "Make vertices coplanar using a plane defined by the first/last three selected verts.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "mesh",
}


import bpy
import bmesh
from mathutils.geometry import intersect_line_plane, distance_point_to_plane, normal



enum_ref = [( 'first', 'First', 'Defined by the first three selected verts' ),
            ( 'last', 'Last', 'Defined by the last three selected verts' )]
class MESH_OT_3points_flat_trim(bpy.types.Operator):
    """
    Manually pick three vertices to define the reference plane
    """
    bl_idname = 'mesh.3points_flat_trim'
    bl_label = 'Coplanar by 3 Verts'
    bl_options = {'REGISTER', 'UNDO'}



ref_order = bpy.props.EnumProperty(name='Refferece Plane', description='Use the first/last three selected vertices to define the reference plane', items=enum_ref, default="last")
filter_distance = bpy.props.FloatProperty(name='Filter Distance', description='Only affects vertices further than this distance', default=0.0, precision=3, min=0.0)


@classmethod
def poll(cls, context):
    obj = context.active_object
    return (obj and obj.type == 'MESH')

def execute(self, context):
    C = context
    D = bpy.data
    ob = C.active_object

    #if bpy.app.debug != True:
    #    bpy.app.debug = True
    #    if C.active_object.show_extra_indices != True:
    #        C.active_object.show_extra_indices = True

    if ob.mode == 'OBJECT':
        me = C.object.data
        bm = bmesh.new()
        bm.from_mesh(me)
    else:
        obj = C.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

    bm.select_history.validate()
    if len(bm.select_history) < 3:
        self.report({'INFO'}, 'Pick three vertices first')
        return {'CANCELLED'}

    points3Index = []
    points3 = []
    _ordering = bm.select_history if self.ref_order=="first" else list(bm.select_history)[::-1]
    for i in _ordering:
        if len(points3) >= 3:
            break
        elif isinstance(i, bmesh.types.BMVert):
            points3.append(i.co)
            points3Index.append(i.index)
    print(points3Index)
    if len(points3) < 3:
        self.report({'INFO'}, 'at least three vertices are needed to be selected')
        return {'CANCELLED'}


    points3Normal = normal(*points3)
    for v in bm.verts:
        if v.select and v.index not in points3Index:
            _move = True
            if self.filter_distance > 0.0:
                _move = abs(distance_point_to_plane(v.co, points3[0], points3Normal)) < self.filter_distance
            if _move == True:
                v.co = intersect_line_plane(v.co, v.co+points3Normal, points3[0], points3Normal)

    if ob.mode == 'OBJECT':
        bm.to_mesh(me)
        bm.free()
    else:
        bmesh.update_edit_mesh(me, True)

    return {'FINISHED'}

def menu_func_MESH_OT_3points_flat_trim(self, context):
    self.layout.operator(MESH_OT_3points_flat_trim.bl_idname,
                        text=MESH_OT_3points_flat_trim.bl_label)

def register():   
    bpy.utils.register_class(MESH_OT_3points_flat_trim) 
    bpy.types.VIEW3D_PT_tools_meshedit.append(menu_func_MESH_OT_3points_flat_trim)

def unregister():
    bpy.types.VIEW3D_PT_tools_meshedit.remove(menu_func_MESH_OT_3points_flat_trim)
    bpy.utils.unregister_class(MESH_OT_3points_flat_trim)

if __name__ == "__main__":
    register()