
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
        self.projection_matrix.set_perspective(60, 1920/1080, 0.1, 10)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        

        self.view_matrix = ViewMatrix()
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        ## --- CONTROLS FOR KEYS TO CONTROL THE CAMERA --- ##
        self.UP_key_down = False
        self.UP_key_up = False
        self.UP_key_right = False
        self.UP_key_left = False

        self.UP_key_w = False
        self.UP_key_s = False
        self.UP_key_a = False
        self.UP_key_d = False

        self.UP_key_q = False
        self.UP_key_e = False
        self.UP_key_r = False
        self.UP_key_f = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        if self.angle > 2 * pi:
            self.angle -= (2 * pi)

        speed = 0.01 # to controll the speed, better way of doing it?
        tmp = self.angle * speed 
         
        # set view_matrix after checking all the ifs? but it's only nessecery to set when something has changed

        # WORKS
        if self.UP_key_up:
            self.view_matrix.pitch(-tmp)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_down:
            self.view_matrix.pitch(tmp)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_right:
            self.view_matrix.yaw(-tmp)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_left:
            self.view_matrix.yaw(tmp)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())

        tmp2 = 0.001
        if self.UP_key_w:
            self.view_matrix.walk(0, 0, -tmp2)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_s:
            self.view_matrix.walk(0, 0, tmp2)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        # WORKS
        if self.UP_key_a:
            self.view_matrix.walk(-tmp2, 0, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_d:
            self.view_matrix.walk(tmp2, 0, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        
        # WORKS
        # Remove these if player is a person walking, roll is not natural
        if self.UP_key_e:
            self.view_matrix.roll(-tmp)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_q:
            self.view_matrix.roll(tmp)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        
        # Remove these if player is walking on a floor
        if self.UP_key_r:
            self.view_matrix.slide(0, tmp2, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_f:
            self.view_matrix.slide(0, -tmp2, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        glClearColor(0.1, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0, 0, -3)
        self.model_matrix.add_rotation(50, 'x')
        self.model_matrix.add_rotation(50, 'y')
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_solid_color(1,1,1)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0, 1, -5)
        self.model_matrix.add_rotation(50, 'x')
        self.model_matrix.add_rotation(50, 'y')
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_solid_color(0,0.5,0.9)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        pygame.display.flip()

    def draw_cube(self, tx=0, ty=0, tz=0, sx=1, sy=1, sz= 1, angle=0, axis='', color=[1,1,1]):
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
                    elif event.key == K_UP:
                        self.UP_key_up = True
                    elif event.key == K_DOWN:
                        self.UP_key_down = True
                    elif event.key == K_RIGHT:
                        self.UP_key_right = True
                    elif event.key == K_LEFT:
                        self.UP_key_left = True

                    elif event.key == K_w:
                        self.UP_key_w = True
                    elif event.key == K_s:
                        self.UP_key_s = True
                    elif event.key == K_a:
                        self.UP_key_a = True
                    elif event.key == K_d:
                        self.UP_key_d = True

                    elif event.key == K_r:
                        self.UP_key_r = True
                    elif event.key == K_f:
                        self.UP_key_f = True
                    elif event.key == K_q:
                        self.UP_key_q = True
                    elif event.key == K_e:
                        self.UP_key_e = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_up = False
                    elif event.key == K_DOWN:
                        self.UP_key_down = False
                    elif event.key == K_RIGHT:
                        self.UP_key_right = False
                    elif event.key == K_LEFT:
                        self.UP_key_left = False
                    
                    elif event.key == K_w:
                        self.UP_key_w = False
                    elif event.key == K_s:
                        self.UP_key_s = False
                    elif event.key == K_a:
                        self.UP_key_a = False
                    elif event.key == K_d:
                        self.UP_key_d = False

                    elif event.key == K_r:
                        self.UP_key_r = False
                    elif event.key == K_f:
                        self.UP_key_f = False
                    elif event.key == K_q:
                        self.UP_key_q = False
                    elif event.key == K_e:
                        self.UP_key_e = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()