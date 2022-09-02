import sys
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
grass_texture = load_texture('MineCraft/assets/grass_block.png')
stone_texture = load_texture('MineCraft/assets/stone_block.png')
brick_texture = load_texture('MineCraft/assets/brick_block.png')
dirt_texture  = load_texture('MineCraft/assets/dirt_block.png')
sky_texture   = load_texture('MineCraft/assets/skybox.png')
arm_texture   = load_texture('MineCraft/assets/arm_texture.png')
punch_sound   = Audio('MineCraft/assets/punch_sound', loop=False, autoplay=False)
block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
    global block_pick
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['escape'] or player.y < -80:
        quit()
        sys.exit()

class Voxel(Button):
    def __init__(self, position_=(0,0,0), texture_=grass_texture):
        super().__init__(
            parent=scene,
            position=position_,
            model='MineCraft/assets/block',
            origin_y=0.5,
            texture=texture_,
            color=color.color(0,0,random.uniform(0.9,1)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                #punch_sound.play()
                new_position = self.position + mouse.normal
                if new_position not in player.position:
                    if block_pick == 1: Voxel(position_=new_position, texture_=grass_texture)
                    if block_pick == 2: Voxel(position_=new_position, texture_=stone_texture)
                    if block_pick == 3: Voxel(position_=new_position, texture_=brick_texture)
                    if block_pick == 4: Voxel(position_=new_position, texture_=dirt_texture)
            if key == 'right mouse down':
                #punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        self.init_position = Vec2(0.4,-0.6)
        super().__init__(
            parent=camera.ui,
            model='MineCraft/assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150,-10,0),
            position=self.init_position
        )

    def active(self):
        self.position = Vec2(0.3,-0.5)

    def passive(self):
        self.position = self.init_position

for z in range(20):
    for x in range(20):
        voxel = Voxel((x,0,z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
