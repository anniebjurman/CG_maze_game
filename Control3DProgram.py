
# from OpenGL.GL import *
# from OpenGL.GLU import *
from array import ArrayType
from math import *
from pyclbr import Function

import pygame
from pygame.locals import *

import sys
import time
import random

from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        # self.projection_view_matrix = ProjectionViewMatrix()
        # self.shader.set_projection_view_matrix(self.projection_view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix = ViewMatrix()
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##

        self.white_background = False

        self.mouse_pos = None

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        if self.UP_key_down:
            self.white_background = True
        else:
            self.white_background = False
    

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.1, 0.2, 0.2, 1.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        self.model_matrix.add_translation(-1,0,-3)
        self.model_matrix.add_rotation(50, 'y')
        self.model_matrix.add_rotation(50, 'x')
        self.draw_cube()

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        pygame.display.flip()

    def draw_cube(self, tx=1, ty=1, tz=1, sx=1, sy=1, sz= 1, angle=0, axis='', color=[1,1,1]):
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(tx,ty,tz)
        self.model_matrix.add_rotation(angle, axis)
        self.model_matrix.add_scale(sx, sy,sz)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_solid_color(color[0], color[1], color[2])
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_pyramide(self, num_bricks_base, color):
        ty = 0
        tz = 0
        tx = 0

        for x in list(range(num_bricks_base, 0, -1)):
            tx = tx - x - 0.5

            for y in range(x):
                self.draw_cube(color = color, tx = tx, ty = ty, tz = tz)
                tx += 1
            ty += 1

    def draw_scene(self):
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-1, -1, -1)
        self.model_matrix.add_rotation(-10, 'y')
        self.draw_cube(sx = 6, sz = 3, sy = 0.1, color = [0.5, 0.5, 0.5])
        self.model_matrix.push_matrix()

        self.model_matrix.add_rotation(90, 'y')
        self.model_matrix.add_translation(z = -1.5, x = 1.5, y = 1.5)
        self.draw_pyramide(3, [0.9, 0.9, 0.9])
        self.model_matrix.pop_matrix()

        self.draw_cube()
        
    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        
                    if event.key == K_UP:
                        self.UP_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False

                # elif event.type == pygame.MOUSEMOTION:
                #     self.mouse_pos = pygame.mouse.get_pos()
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()