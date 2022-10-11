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
        self.projection_matrix.set_perspective(60, 1920/1080, 0.2, 60)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix = Matrices.ViewMatrix()
        self.cube = Base3DObjects.Cube()
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0
        self.collision_radius = 0.5

        # Camera controll
        self.UP_key_right = False
        self.UP_key_left = False
        self.UP_key_up = False
        self.UP_key_down = False

        self.UP_key_w = False
        self.UP_key_s = False
        self.UP_key_a = False
        self.UP_key_d = False

        # Light
        self.UP_key_l = False
        self.UP_key_k = False

        # init maze
        self.maze = Maze.Maze(11)
        self.maze.set_10_maze()

        # Pyramids
        self.add_pyramid(Maze.CellCord(1, 9))
        self.add_pyramid(Maze.CellCord(8, 8))
        self.add_pyramid(Maze.CellCord(7, 5))

        self.light_pos_1 = Base3DObjects.Point(self.maze.size * self.maze.cell_width / 2, 10, 0)
        self.light_pos_2 = Base3DObjects.Point(self.maze.size * self.maze.cell_width / 2, 10, self.maze.size * self.maze.cell_width)

        self.set_camera_at_entrance()
        # self.set_camera_overview()

    def set_camera_at_entrance(self):
        self.view_matrix.eye = Base3DObjects.Point(0, 0.5, self.maze.cell_width * 2.5)
        self.view_matrix.yaw(-90)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

    def set_camera_overview(self):
        self.projection_matrix.set_perspective(60, 1920/1080, 25, 50)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix.eye = Base3DObjects.Point(self.maze.cell_width * self.maze.size / 2, 30, self.maze.size * self.maze.cell_width)
        self.view_matrix.pitch(57)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.angle += math.pi * delta_time
        if self.angle > 2 * math.pi:
            self.angle -= (2 * math.pi)

        # look up/down/left/right
        new_angle = self.angle * 0.6
        if self.UP_key_right:
            self.view_matrix.turn(-new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_left:
            self.view_matrix.turn(new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_up:
            self.view_matrix.pitch(-new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_down:
            self.view_matrix.pitch(new_angle)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # Walk forward/backwards/lef/right
        walk_speed = 4 * delta_time
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
        row, col = self.get_current_cell_cord()
        if 0 <= row < self.maze.size and \
           0 <= col < self.maze.size:
           return True
        else:
            return False

    def check_collision(self):
        self.set_current_cell()

        # wall to the right
        if self.maze.curr_cell.cord.col + 1 < self.maze.size:
            right_cell = self.maze.maze[self.maze.curr_cell.cord.row][self.maze.curr_cell.cord.col + 1]
            if right_cell.wall_west:
                wall_x_value = right_cell.cord.col * self.maze.cell_width - self.maze.wall_thickness / 2
                if self.view_matrix.eye.x + self.collision_radius > wall_x_value:
                    self.view_matrix.eye.x = wall_x_value - self.collision_radius
                    self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # wall to the left (own wall)
        if self.maze.curr_cell.wall_west:
            wall_x_value = self.maze.curr_cell.cord.col * self.maze.cell_width + self.maze.wall_thickness / 2
            if self.view_matrix.eye.x - self.collision_radius < wall_x_value:
                self.view_matrix.eye.x = wall_x_value + self.collision_radius
                self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # wall above
        if self.maze.curr_cell.cord.row - 1 >= 0:
            cell_above = self.maze.maze[self.maze.curr_cell.cord.row - 1][self.maze.curr_cell.cord.col]
            if cell_above.wall_south:
                wall_z_value = self.maze.curr_cell.cord.row * self.maze.cell_width + self.maze.wall_thickness / 2
                if self.view_matrix.eye.z - self.collision_radius < wall_z_value:
                    self.view_matrix.eye.z = wall_z_value + self.collision_radius
                    self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # wall below (own wall)
        if self.maze.curr_cell.wall_south:
            wall_z_value = (self.maze.curr_cell.cord.row + 1) * self.maze.cell_width - self.maze.wall_thickness / 2
            if self.view_matrix.eye.z + self.collision_radius > wall_z_value:
                self.view_matrix.eye.z = wall_z_value - self.collision_radius
                self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # pyramide inside cell
        if self.maze.curr_cell.object:
            bound_z = [self.maze.curr_cell.cord.row * self.maze.cell_width + (self.maze.cell_width - self.maze.curr_cell.object.width * 2) / 2,
                       (self.maze.curr_cell.cord.row + 1) * self.maze.cell_width - (self.maze.cell_width - self.maze.curr_cell.object.width * 2) / 2]
            # left
            if self.maze.prev_cell.cord.col < self.maze.curr_cell.cord.col and \
               bound_z[0] < self.view_matrix.eye.z < bound_z[1]:

                pyr_x_value = self.maze.curr_cell.cord.col * self.maze.cell_width + (self.maze.cell_width - self.maze.curr_cell.object.width * 2) / 2
                if self.view_matrix.eye.x + self.collision_radius > pyr_x_value:
                    self.view_matrix.eye.x = pyr_x_value - self.collision_radius
                    self.shader.set_view_matrix(self.view_matrix.get_matrix())
                    self.maze.curr_cell.object.set_gradient_color()
            # right
            elif self.maze.prev_cell.cord.col > self.maze.curr_cell.cord.col and \
                 bound_z[0] < self.view_matrix.eye.z < bound_z[1]:
                pyr_x_value = (self.maze.curr_cell.cord.col + 1) * self.maze.cell_width - (self.maze.cell_width - self.maze.curr_cell.object.width * 2) / 2
                if self.view_matrix.eye.x - self.collision_radius < pyr_x_value:
                    self.view_matrix.eye.x = pyr_x_value + self.collision_radius
                    self.shader.set_view_matrix(self.view_matrix.get_matrix())
                    self.maze.curr_cell.object.set_gradient_color()

    def get_current_cell_cord(self):
        col = math.trunc(self.view_matrix.eye.x) // self.maze.cell_width
        row = math.trunc(self.view_matrix.eye.z) // self.maze.cell_width
        return row, col

    def set_current_cell(self):
        row, col = self.get_current_cell_cord()

        if self.maze.curr_cell.cord.row != row or self.maze.curr_cell.cord.col != col:
            self.maze.prev_cell = self.maze.curr_cell
            self.maze.curr_cell = self.maze.maze[row][col]

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #light1
        self.shader.set_light_position_1(self.light_pos_1)
        self.shader.set_light_color_1(.7, .7, .7)

        #light2
        self.shader.set_light_position_2(self.light_pos_2)
        self.shader.set_light_color_2(.3, 0, 0)

        self.shader.set_material_specular(0.1, 0.1, 0.1)
        self.shader.set_material_shine(0.1)

        self.draw_maze_base()
        self.draw_maze_walls()
        self.draw_pyramids()

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        pygame.display.flip()

    def add_pyramid(self, cell_cord):
        pyr = Base3DObjects.Pyramid()
        self.maze.maze[cell_cord.row][cell_cord.col].object = pyr

    def draw_pyramids(self):
        for row in self.maze.maze:
            for cell in row:
                if cell.object:
                    self.model_matrix.push_matrix()

                    trans_x = self.maze.cell_width * cell.cord.col + (self.maze.cell_width / 2)
                    trans_z = self.maze.cell_width * cell.cord.row + (self.maze.cell_width / 2)
                    self.model_matrix.add_translation(trans_x, cell.object.height, trans_z)
                    self.model_matrix.add_scale(cell.object.width, cell.object.height, cell.object.width)

                    self.shader.set_model_matrix(self.model_matrix.matrix)
                    self.shader.set_material_diffuse(cell.object.color[0], cell.object.color[1], cell.object.color[2])

                    cell.object.draw(self.shader)

                    self.model_matrix.pop_matrix()

    def draw_maze_base(self):
        base_color = [0, 0.01, 0.01]
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
        wall_color = [0.5, 0.5, 0.5]

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