import bpy,pathlib,json,math
from mathutils import Vector
P=pathlib.Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(P/'assets/Northern_Vietnam_1972.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=760;s.render.resolution_percentage=100
cam=s.camera
for ob in s.objects:
 if ob.type=='LIGHT': ob.hide_render=True
for loc,energy,size in [((30,35,60),85000,40),((-35,-15,30),50000,35)]:
 bpy.ops.object.light_add(type='AREA',location=loc);ob=bpy.context.object;ob.data.energy=energy;ob.data.size=size;ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
world=s.world; bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND'); bg.inputs[0].default_value=(.35,.39,.43,1);bg.inputs[1].default_value=.7
assets=list(json.loads((P/'assets/recipe.json').read_text())['assets'])
for name,loc,target,ortho,tag in [('b52',(48,62,33),(0,0,1),75,'aircraft_hero'),('b52',(0,0,95),(0,0,0),84,'aircraft_top'),('b52',(95,0,5),(0,0,3),61,'aircraft_side'),('house0',(18,-23,16),(0,0,3),22,'house'),('hospital',(23,-34,20),(0,0,4),35,'hospital'),('wreck',(15,-21,13),(0,0,1),24,'wreck')]:
 for c in s.collection.children:
  if c.name in assets: c.hide_render=c.name!=name
 off=Vector(((assets.index(name)%5)*65,(assets.index(name)//5)*65,0))
 for ob in bpy.data.collections[name].objects: ob.location-=off
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=ortho
 s.render.filepath=str(P/'qa'/('blender_'+tag+'.png'));bpy.ops.render.render(write_still=True)
 for ob in bpy.data.collections[name].objects:ob.location+=off
print('RENDER_COMPLETE')
