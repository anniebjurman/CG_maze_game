from random import randint
from OpenGL.GL import *
from OpenGL.GLU import *

import math
import random

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def to_string(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.zf * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def to_string(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"

class Cube:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]

    def draw(self, shader):

        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)

class Pyramid:
    def __init__(self):
        self.position_array = [0.0, 1.0, 0.0,
                               -1.0, -1.0, 1.0,
                               1.0, -1.0, 1.0,
                               0.0, 1.0, 0.0,
                               1.0, -1.0, 1.0,
                               1.0, -1.0, -1.0,
                               0.0, 1.0, 0.0,
                               1.0, -1.0, -1.0,
                               -1.0, -1.0, -1.0,
                               0.0, 1.0, 0.0,
                               -1.0,-1.0,-1.0,
                               -1.0,-1.0, 1.0]
        self.normal_array = []
        self.width = 1.5
        self.height = 3
        self.color = [0.8, 0.1, 0.1]
        self.taken = False

    def draw(self, shader):
        shader.set_position_attribute(self.position_array)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDrawArrays(GL_TRIANGLES, 3, 3)
        glDrawArrays(GL_TRIANGLES, 6, 3)
        glDrawArrays(GL_TRIANGLES, 9, 3)

    def set_gradient_color(self):
        speed = 0.005
        new_r = self.color[0] + speed
        new_g = self.color[1] + speed
        new_b = self.color[2] + speed

        if new_r > 1:
            new_r = 0.2
        if new_g > 1:
            new_g = 0.2
        if new_b > 1:
            new_b = 0.2

        self.color = [new_r, new_g, new_b]

    def set_taken(self):
        self.color = [0.1, 0.8, 0.1]
        self.taken = True
    def set_not_taken(self):
        self.color = [0.8, 0.1, 0.1]
        self.taken = False
