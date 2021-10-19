# uv map rendering 
import bpy

ob = bpy.context.object

for loop in ob.data.loops :
    normal = ob.data.vertices[loop.vertex_index].normal
    ob.data.uv_layers["XY"].data[loop.index].uv = (normal.x, normal.y)
    ob.data.uv_layers["ZW"].data[loop.index].uv = (normal.z, 0)