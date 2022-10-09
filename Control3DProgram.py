import math
from pickle import FALSE
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import Matrices
import Shaders
import Maze
import Base3DObjects

# TODO: Fix pitch

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shaders.Shader3D()
        self.shader.use()

        self.model_matrix = Matrices.ModelMatrix()

        self.projection_matrix = Matrices.ProjectionMatrix()
        self.projection_matrix.set_perspective(60, 1920/1080, 0.2, 40)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix = Matrices.ViewMatrix()
        self.cube = Base3DObjects.Cube()
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.light_pos = Base3DObjects.Point(0, 5, 5)

        # Camera controll
        self.UP_key_right = False
        self.UP_key_left = False
        self.UP_key_up = False
        self.UP_key_down = False

        self.UP_key_w = False
        self.UP_key_s = False
        self.UP_key_a = False
        self.UP_key_d = False

        #light
        self.UP_key_l = False
        self.UP_key_k = False

        # init maze
        self.maze = Maze.Maze(11)
        self.maze.set_10_maze()

        #init pyramid
        self.pyramid = Base3DObjects.Pyramid()

        self.set_camera_at_entrance()
        # self.set_camera_overview()

    def set_camera_at_entrance(self):
        self.view_matrix.eye = Base3DObjects.Point(-self.maze.cell_width, 0.5, self.maze.cell_width * 2.5)
        self.view_matrix.yaw(-90)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

    def set_camera_overview(self):
        self.view_matrix.eye = Base3DObjects.Point(self.maze.cell_width * self.maze.size / 2, 20, self.maze.size + 4)
        self.view_matrix.pitch(80)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.angle += math.pi * delta_time
        if self.angle > 2 * math.pi:
            self.angle -= (2 * math.pi)

        # look up/down/left/right
        new_angle = self.angle * 0.5   #controll the speed, better way of doing it?
        if self.UP_key_right:
            self.view_matrix.yaw(-new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_left:
            self.view_matrix.yaw(new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_up:
            self.view_matrix.pitch(-new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_down:
            self.view_matrix.pitch(new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # Walk forward/backwards/lef/right
        walk_speed = 3 * delta_time
        if self.UP_key_w:
            self.view_matrix.walk(0, 0, -walk_speed)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_s:
            self.view_matrix.walk(0, 0, walk_speed)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_a:
            self.view_matrix.walk(-walk_speed, 0, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_d:
            self.view_matrix.walk(walk_speed, 0, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # move light
        if self.UP_key_k:
            self.light_pos.x -= 0.2 * delta_time
        if self.UP_key_l:
            self.light_pos.x += 0.2 * delta_time

        if self.check_if_in_maze():
            self.check_collision()

    def check_if_in_maze(self):
        cell_in_space = self.get_current_cell_cord()
        if 0 <= cell_in_space[0] < self.maze.size and \
           0 <= cell_in_space[1] < self.maze.size:
           return True
        else:
            return False

    def check_collision(self):
        collision_radius = 0.5
        curr_cell_cord = self.get_current_cell_cord()
        curr_cell = self.maze.maze[curr_cell_cord[0]][curr_cell_cord[1]]

        # wall to the right
        if curr_cell.cord.col + 1 < self.maze.size:
            right_cell = self.maze.maze[curr_cell.cord.row][curr_cell.cord.col + 1]
            if right_cell.wall_west:
                wall_x_value = right_cell.cord.col * self.maze.cell_width - self.maze.wall_thickness / 2
                if self.view_matrix.eye.x + collision_radius > wall_x_value:
                    self.view_matrix.eye.x = wall_x_value - collision_radius
                    self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # wall to the left (own wall)
        if curr_cell.wall_west:
            wall_x_value = curr_cell.cord.col * self.maze.cell_width + self.maze.wall_thickness / 2
            if self.view_matrix.eye.x - collision_radius < wall_x_value:
                self.view_matrix.eye.x = wall_x_value + collision_radius
                self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # wall above
        if curr_cell.cord.row - 1 >= 0:
            cell_above = self.maze.maze[curr_cell.cord.row - 1][curr_cell.cord.col]
            if cell_above.wall_south:
                wall_z_value = curr_cell.cord.row * self.maze.cell_width + self.maze.wall_thickness / 2
                if self.view_matrix.eye.z - collision_radius < wall_z_value:
                    self.view_matrix.eye.z = wall_z_value + collision_radius
                    self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # wall below (own wall)
        if curr_cell.wall_south:
            wall_z_value = (curr_cell.cord.row + 1) * self.maze.cell_width - self.maze.wall_thickness / 2
            if self.view_matrix.eye.z + collision_radius > wall_z_value:
                self.view_matrix.eye.z = wall_z_value - collision_radius
                self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # object inside cell
        if curr_cell.object:
            print("OBJECT")


    def get_current_cell_cord(self): # TODO: because trunc round to 0, the negative values get rounded the wrong direction
        x = math.trunc(self.view_matrix.eye.x) // self.maze.cell_width
        z = math.trunc(self.view_matrix.eye.z) // self.maze.cell_width
        return [z, x]

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.shader.set_light_position(self.light_pos)
        self.shader.set_light_color(1, 1, 1)

        self.draw_maze_base()
        self.draw_maze_walls()
        self.draw_pyramid(Maze.CellCord(2, 9))
        self.draw_pyramid(Maze.CellCord(1, 3))
        # self.draw_pyramid(self.maze.cell_width * 8.5, self.maze.cell_width * 3)
        # self.draw_pyramid(self.maze.cell_width * 2, self.maze.cell_width * 9)

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        pygame.display.flip()

    def draw_pyramid(self, cell_cord):
        color = [0.9, 0.3, 0.3]
        self.maze.maze[cell_cord.row][cell_cord.col].object = Maze.Object.PYRAMID

        self.model_matrix.push_matrix()

        trans_x = self.maze.cell_width * (cell_cord.col + 0.5)
        trans_z = self.maze.cell_width * (cell_cord.row + 0.5)
        self.model_matrix.add_translation(trans_x, self.pyramid.height, trans_z)
        self.model_matrix.add_scale(self.pyramid.width, self.pyramid.height, self.pyramid.width)

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(color[0], color[1], color[2])

        self.pyramid.draw(self.shader)

        self.model_matrix.pop_matrix()

    def draw_maze_base(self):
        base_color = [0.4, 0.4, 0.4]
        base_thickness = 0.1

        self.model_matrix.push_matrix()

        trans_x_z = self.maze.cell_width * self.maze.size / 2
        self.model_matrix.add_translation(trans_x_z, -base_thickness / 2, trans_x_z)

        scale_x_z = (self.maze.cell_width * self.maze.size) + self.maze.wall_thickness
        self.model_matrix.add_scale(scale_x_z, base_thickness, scale_x_z)

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(base_color[0], base_color[1], base_color[2])
        self.cube.draw(self.shader)

        self.model_matrix.pop_matrix()

    def draw_maze_walls(self):
        wall_color = [0.7, 0.4, 0.1]

        for row in self.maze.maze:
            for cell in row:
                if cell.wall_west:
                    self.model_matrix.push_matrix()

                    trans_x = cell.cord.col * self.maze.cell_width
                    trans_y = self.maze.wall_height / 2
                    trans_z = cell.cord.row * self.maze.cell_width + self.maze.cell_width / 2

                    self.model_matrix.add_translation(trans_x, trans_y, trans_z)
                    self.model_matrix.add_scale(self.maze.wall_thickness,
                                                self.maze.wall_height,
                                                self.maze.cell_width + self.maze.wall_thickness)

                    self.shader.set_model_matrix(self.model_matrix.matrix)
                    self.shader.set_material_diffuse(wall_color[0], wall_color[1], wall_color[2])

                    self.cube.draw(self.shader)

                    self.model_matrix.pop_matrix()

                if cell.wall_south:
                    self.model_matrix.push_matrix()

                    trans_x = cell.cord.col * self.maze.cell_width + self.maze.cell_width / 2
                    trans_y = self.maze.wall_height / 2
                    trans_z = (cell.cord.row + 1) * self.maze.cell_width

                    self.model_matrix.add_translation(trans_x, trans_y, trans_z)
                    self.model_matrix.add_scale(self.maze.cell_width + self.maze.wall_thickness,
                                                self.maze.wall_height,
                                                self.maze.wall_thickness)

                    self.shader.set_model_matrix(self.model_matrix.matrix)
                    self.shader.set_material_diffuse(wall_color[0], wall_color[1], wall_color[2])

                    self.cube.draw(self.shader)

                    self.model_matrix.pop_matrix()


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
                    elif event.key == K_RIGHT:
                        self.UP_key_right = True
                    elif event.key == K_LEFT:
                        self.UP_key_left = True
                    elif event.key == K_UP:
                        self.UP_key_up = True
                    elif event.key == K_DOWN:
                        self.UP_key_down = True

                    elif event.key == K_w:
                        self.UP_key_w = True
                    elif event.key == K_s:
                        self.UP_key_s = True
                    elif event.key == K_a:
                        self.UP_key_a = True
                    elif event.key == K_d:
                        self.UP_key_d = True

                    elif event.key == K_l:
                        self.UP_key_l = True
                    elif event.key == K_k:
                        self.UP_key_k = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_RIGHT:
                        self.UP_key_right = False
                    elif event.key == K_LEFT:
                        self.UP_key_left = False
                    elif event.key == K_UP:
                        self.UP_key_up = False
                    elif event.key == K_DOWN:
                        self.UP_key_down = False

                    elif event.key == K_w:
                        self.UP_key_w = False
                    elif event.key == K_s:
                        self.UP_key_s = False
                    elif event.key == K_a:
                        self.UP_key_a = False
                    elif event.key == K_d:
                        self.UP_key_d = False

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