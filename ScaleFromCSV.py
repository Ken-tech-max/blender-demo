#  // use CSV values to drive object scale
#  // distinctly: calling '.scale' instead of '.dimensions'.
#  // https://docs.blender.org/api/blender_python_api_current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.values
#  // https://docs.blender.org/api/blender_python_api_current/bpy.types.GameProperty.html#bpy.types.GameProperty.name

 import bpy, csv

fp = "E:\Data_Viz_Prototype\Data Files\Workcenter_DPPM.csv"

with open( fp ) as csvfile:
    rdr = csv.reader ( csvfile)
    for i, row in enumerate (rdr):
        if i == 0: continue #Skip colum titles
        if row[2:3] != 2018: continue #Skip any rows not from 2018
        if row[3:2] != 1: continue #Skip any rows not from January
        wc, dept, year, month, run, rej, dppm = row[:]

if bpy.data.objects["Cube.002"]['Work_Center'] == '04-LSE200':
    bpy.data.objects["Cube.002"].scale = (.5, .5, dppm)
However I get the following error:

Traceback (most recent call last):
  File "<blender_console>", line 1, in <module>
KeyError: 'bpy_struct[key]: key "Work_Center" not found'



