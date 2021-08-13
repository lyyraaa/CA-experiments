"""
Copyright 2019 Richard Feistenauer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import sys
import time


class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self,x,y,z,mult=1):

        X, Y, Z = x+1, y+1, z+1

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        white = [255]*4
        black = [0]*4
        yella = (int(255*mult), int(10*mult), int(218*mult), 120)

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

        start_time = time.time()


        ca = ConwaysCA()
        x = ca.get_cells()
        #print(dir(x))

        rackArr = []
        for evolution in range(60):
            x = ca.get_cells()
            array = []
            for row in range(60):
                rowArr = []
                for column in range(60):
                    rowArr.append(int(x[(row,column)].state[0]))
                array.append(rowArr)

            rackArr.append(array)
            ca.evolve()

        print("time to compute 190x190, 60 steps, more objects: ",str(time.time()-start_time),"s")

        cubeList = self.draw_from_array(rackArr)


        #cube1 = self.add_block(0, 0, -1)
        #cube2 = self.add_block(0, 2, -1)



    def undraw(self, object):
        for vertexList in object:
            vertexList.delete()

    def draw_from_array(self, drawArr):
        rowC = 0
        colC = 0
        rackC = 0
        totalRack = len(drawArr)
        step = 0.5/totalRack
        mult = 1
        cubeList = []
        for row in drawArr:
            colC = 0
            for col in row:
                rackC = 0
                for rack in col:
                    if rack:
                        cube = self.add_block(colC,-rowC,rackC,mult)
                        cubeList.append(cube)
                    rackC += 1
                colC += 1
            rowC += 1
            mult-=step
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

import random
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cellular_automaton import CellularAutomaton, MooreNeighborhood, CAWindow, EdgeRule

ALIVE = [1.0]
DEAD = [0]


class ConwaysCA(CellularAutomaton):
    """ Cellular automaton with the evolution rules of conways game of life """

    def __init__(self):
        super().__init__(dimension=[60, 60],
                         neighborhood=MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS))

    def init_cell_state(self, __):  # pylint: disable=no-self-use

        rand = random.randrange(0, 16, 1)
        init = max(.0, float(rand - 14))
        return [init]

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        alive_neighbours = self.__count_alive_neighbours(neighbors_last_states)
        if last_cell_state == DEAD and alive_neighbours == 3:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours < 2:
            new_cell_state = DEAD
        if last_cell_state == ALIVE and 1 < alive_neighbours < 4:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours > 3:
            new_cell_state = DEAD
        return new_cell_state

    @staticmethod
    def __count_alive_neighbours(neighbours):
        alive_neighbors = []
        for n in neighbours:
            if n == ALIVE:
                alive_neighbors.append(1)
        return len(alive_neighbors)


if __name__ == "__main__":


    window = Window(width=400, height=300, caption='My caption',resizable=True)
    glClearColor(0.2,0.25,0.5,1)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    pyglet.app.run()



    # x[(0,0)] is a cell
