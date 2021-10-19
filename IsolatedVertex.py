import bpy

context = bpy.context
scene = context.scene
obj = context.object
shape_name = obj.active_shape_key.name

obj.shape_key_add(name=str(shape_name) + "_X", from_mix=True)
obj.shape_key_add(name=str(shape_name) + "_Y", from_mix=True)
obj.shape_key_add(name=str(shape_name) + "_Z", from_mix=True)
bpy.ops.object.shape_key_add(from_mix=False)
bpy.ops.object.shape_key_remove(all=False)   #Hack to select the last shape_key in the list

shape_name = obj.active_shape_key.name #Update the active_shape_key.name

for vert in obj.data.vertices: #Isolate the translation on the Z axis first
    obj.data.shape_keys.key_blocks[shape_name].data[vert.index].co.x = obj.active_shape_key.data[vert.index].co.x
    obj.data.shape_keys.key_blocks[shape_name].data[vert.index].co.y = obj.active_shape_key.data[vert.index].co.y

obj.active_shape_key_index = obj.active_shape_key_index - 2

shape_name = obj.active_shape_key.name

for vert in obj.data.vertices: #Isolate the translation on the X axis
    obj.data.shape_keys.key_blocks[shape_name].data[vert.index].co.y = obj.active_shape_key.data[vert.index].co.y
    obj.data.shape_keys.key_blocks[shape_name].data[vert.index].co.z = obj.active_shape_key.data[vert.index].co.z

obj.active_shape_key_index = obj.active_shape_key_index + 1 

shape_name = obj.active_shape_key.name

for vert in obj.data.vertices: #Isolate the translation on the Y axis
    obj.data.shape_keys.key_blocks[shape_name].data[vert.index].co.x = obj.active_shape_key.data[vert.index].co.x
    obj.data.shape_keys.key_blocks[shape_name].data[vert.index].co.z = obj.active_shape_key.data[vert.index].co.z