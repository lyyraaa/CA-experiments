import cellpylib as cpl
import sys




# code from https://www.youtube.com/watch?v=Hqg4qePJV2U
# Pyglet OpenGL tutorial by DLC ENERGY
# As taught by Aiden Ward
#https://github.com/jjstrydom/pyglet_examples/blob/master/textured_square.py

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import sys

class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self,x,y,z):

        X, Y, Z = x+1, y+1, z+1

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        white = [255]*4
        black = [0]*4
        yella = (255, 10, 218, 255)

        cubeList = (
            self.batch.add(4, GL_QUADS, None, ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), ('c4B', yella * 4)), # back
            self.batch.add(4, GL_QUADS, None, ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), ('c4B', yella * 4)), # front

            self.batch.add(4, GL_QUADS, None, ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), ('c4B', yella * 4)),  # left
            self.batch.add(4, GL_QUADS, None, ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), ('c4B', yella * 4)),  # right

            self.batch.add(4, GL_QUADS, None, ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), ('c4B', yella * 4)),  # bottom
            self.batch.add(4, GL_QUADS, None, ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), ('c4B', yella * 4))) # top

        return cubeList

    def __init__(self):


        self.batch = pyglet.graphics.Batch()
        # Glider
        cellular_automaton = cpl.init_simple2d(60, 60)
        cellular_automaton[:, [28,29,30,30], [30,31,29,31]] = 1

        # Blinker
        cellular_automaton[:, [40,40,40], [15,16,17]] = 1

        # Light Weight Space Ship (LWSS)
        cellular_automaton[:, [18,18,19,20,21,21,21,21,20], [45,48,44,44,44,45,46,47,48]] = 1

        # evolve the cellular automaton for 60 time steps
        cellular_automaton = cpl.evolve2d(cellular_automaton, timesteps=20, neighbourhood='Moore',
                                          apply_rule=cpl.game_of_life_rule)

        cubeList = self.draw_from_array(cellular_automaton)
        #cube1 = self.add_block(0, 0, -1)
        #cube2 = self.add_block(0, 2, -1)



    def undraw(self, object):
        for vertexList in object:
            vertexList.delete()

    def draw_from_array(self, drawArr):
        rowC = 0
        colC = 0
        rackC = 0
        cubeList = []
        for row in drawArr:
            colC = 0
            for col in row:
                rackC = 0
                for rack in col:
                    if rack:
                        cube = self.add_block(colC,-rowC,rackC)
                        cubeList.append(cube)
                    rackC += 1
                colC += 1
            rowC += 1
        return cubeList

    def draw(self):
        self.batch.draw()

class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self, dx, dy):
        dx/= 8
        dy/= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self,dt,keys):
        sens = 0.4
        s = dt*10
        #shiftmod = keys[key.LSHIFT] * 1.5 * sens
        rotY = -self.rot[1]/180*math.pi
        dx, dz = math.sin(rotY), math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE]:
            self.pos[1] += s*sens
        if keys[key.LCTRL]:
            self.pos[1] -= s*sens

class Window(pyglet.window.Window):

    def push(self,pos,rot):
        glPushMatrix()
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.model = Model()
        self.player = Player((0.5,1.5,1.5),(-30,0))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.model.draw()
        glPopMatrix()

if __name__ == '__main__':
    window = Window(width=400, height=300, caption='My caption',resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    pyglet.app.run()
