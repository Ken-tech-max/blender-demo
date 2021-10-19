# csv sample
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
I have tried some of the following code in the console window to make sure I can talk to Game properties:

import bpy
bpy.ops.object.game_property_new(type='FLOAT', name="Test")

obj = bpy.data.objects["Cube.002"]
cube = obj.data
print(bpy.types.GameStringProperty.values(cube))