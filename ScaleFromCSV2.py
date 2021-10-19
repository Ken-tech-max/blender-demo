# //use CSV values to drive object scale
# //

import bpy, csv

fp = "C:/csvs/buses.csv"

with open( fp ) as csvfile:
    rdr = csv.reader( csvfile )
    for i, row in enumerate( rdr ):
        if i == 0: continue # Skip column titles
        lon, lat = row[3:5]

        # Generate UV sphere at x = lon and y = lat (and z = 0 )
        bpy.ops.mesh.primitive_uv_sphere_add( location = ( float(lon), float(lat), 0 ) )

# ///////////////////////////////////        
# import bpy
# bpy.ops.object.game_property_new(type='FLOAT', name="Test")

# obj = bpy.data.objects["Cube.002"]
# cube = obj.data
# print(bpy.types.GameStringProperty.values(cube))