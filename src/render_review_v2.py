import bpy,pathlib,json,math
from mathutils import Vector
P=pathlib.Path(__file__).resolve().parents[1];Q=P/'qa/v2/blender';Q.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(P/'assets/Northern_Vietnam_1972.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100
cam=s.camera
for ob in s.objects:
 if ob.type=='LIGHT':ob.hide_render=True
for loc,energy,size in [((40,-55,70),105000,45),((-45,25,35),75000,35)]:
 bpy.ops.object.light_add(type='AREA',location=loc);ob=bpy.context.object;ob.data.energy=energy;ob.data.size=size;ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
bg=next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs[0].default_value=(.20,.24,.29,1);bg.inputs[1].default_value=.55
names=list(json.loads((P/'assets/recipe.json').read_text(encoding='utf-8'))['assets'])
def cv(v):return Vector((v[0],-v[2],v[1]))
shots=[('b52',[56,26,-66],[0,1,0],77,'aircraft_hero'),('b52',[0,7,-100],[0,2,0],68,'aircraft_front'),('b52',[0,95,0],[0,0,0],86,'aircraft_top'),('b52',[85,4,0],[0,2,0],62,'aircraft_side'),('bridge',[160,105,260],[0,9,0],425,'bridge_elevation'),('bridge',[-48,11,10],[-53.1,7.7,2.37],12,'bridge_bearing'),('bridge',[-43,3.5,12],[-53.1,7,0],23,'bridge_under'),('bridge',[-19,11,9],[-25.6,11.4,2.37],13,'bridge_suspended_joint'),('house1',[9,8,20],[0,3,4],16,'house_facade'),('house0',[-8,5,18],[0,1.8,4],14,'house_shop')]
for name,p,t,width,tag in shots:
 for c in s.collection.children:
  if c.name in names:c.hide_render=c.name!=name
 offset=Vector(((names.index(name)%5)*65,(names.index(name)//5)*65,0))
 for ob in bpy.data.collections[name].objects:ob.location-=offset
 cam.location=cv(p);cam.rotation_euler=(cv(t)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=width;s.render.filepath=str(Q/(tag+'.png'));bpy.ops.render.render(write_still=True)
 for ob in bpy.data.collections[name].objects:ob.location+=offset
print('V2_BLENDER_REVIEW_RENDERED',len(shots))
