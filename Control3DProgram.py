
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

from Maze import Cell, Maze

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(60, 1920/1080, 0.1, 10)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix = ViewMatrix()
        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.light_pos = Point(0, 5, 5)

        # scene
        self.scene_base = [10, 10, 0.2]

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

        #light
        self.UP_key_l = False
        self.UP_key_k = False

        # init maze
        self.maze = Maze(3)
        self.maze.set_cell([0,0], 'west')
        self.maze.set_cell([0,0], 'south')
        self.maze.set_cell([1,1], 'south')
        self.maze.set_cell([0,1], 'west')
        self.maze.set_cell([0,2], 'south')
        self.maze.set_cell([2,1], 'south')
        print(self.maze.to_string())

        # set camera relative to maze base
        self.view_matrix.eye = Point(self.maze.cell_width * self.maze.size / 2, 0.2, 0)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # set camera to see the maze from above
        # self.view_matrix.eye = Point(self.maze.cell_width * self.maze.size / 2, 5, -2)
        # self.view_matrix.pitch(90)
        # self.shader.set_view_matrix(self.view_matrix.get_matrix())

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
        
        # Remove these if player is walking on a floor
        if self.UP_key_r:
            self.view_matrix.slide(0, tmp2, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_f:
            self.view_matrix.slide(0, -tmp2, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        
        # move light
        if self.UP_key_k:
            self.light_pos.x -= 0.2 * delta_time
        if self.UP_key_l:
            self.light_pos.x += 0.2 * delta_time


    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        glClearColor(0.1, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        self.shader.set_light_position(self.light_pos)
        self.shader.set_light_diffuse(1, 1, 1)

        self.draw_maze_base()
        self.draw_maze_walls()

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        pygame.display.flip()
    
    def draw_maze_base(self):
        self.model_matrix.push_matrix()
        trans_x_z = (self.maze.cell_width * self.maze.size / 2) - (self.maze.wall_thickness / 4)
        self.model_matrix.add_translation(trans_x_z, -0.1 / 2, - trans_x_z)
        scale_x_z = (self.maze.cell_width * self.maze.size) + (self.maze.wall_thickness / 2)
        self.model_matrix.add_scale(scale_x_z, 0.1, scale_x_z)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(0.4, 0.9, 0.8)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()
    
    def draw_maze_walls(self):
        row_num = 0
        col_num = 0
        tot_depth = self.maze.size * self.maze.cell_width

        for row in self.maze.maze:
            for cell in row:
                if cell.wall_west:
                    self.model_matrix.push_matrix()
                    self.model_matrix.add_translation(col_num * self.maze.cell_width, self.maze.wall_height / 2,
                                                      - (tot_depth - (row_num * self.maze.cell_width) - self.maze.cell_width / 2))
                    self.model_matrix.add_scale(self.maze.wall_thickness, self.maze.wall_height, self.maze.cell_width)
                    self.shader.set_model_matrix(self.model_matrix.matrix)
                    self.shader.set_material_diffuse(0.4, 0.8, 0.9)
                    self.cube.draw(self.shader)
                    self.model_matrix.pop_matrix()
                if cell.wall_south:
                    self.model_matrix.push_matrix()
                    self.model_matrix.add_translation((col_num + 1) * self.maze.cell_width - self.maze.cell_width / 2, self.maze.wall_height / 2,
                                                      - (tot_depth - (row_num + 1) * self.maze.cell_width))
                    self.model_matrix.add_scale(self.maze.cell_width, self.maze.wall_height, self.maze.wall_thickness)
                    self.shader.set_model_matrix(self.model_matrix.matrix)
                    self.shader.set_material_diffuse(0.4, 0.8, 0.9)
                    self.cube.draw(self.shader)
                    self.model_matrix.pop_matrix()
                col_num += 1
            row_num += 1
            col_num = 0

        
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
                    
                    elif event.key == K_l:
                        self.UP_key_l = True
                    elif event.key == K_k:
                        self.UP_key_k = True

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
                    
                    elif event.key == K_l:
                        self.UP_key_l = False
                    elif event.key == K_k:
                        self.UP_key_k = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()