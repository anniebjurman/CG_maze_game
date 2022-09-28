
from math import *
# from turtle import up
# from xml.etree.ElementTree import PI # trigonometry

from Base3DObjects import *

class ModelMatrix:
    def __init__(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]
        self.stack = []
        self.stack_count = 0
        self.stack_capacity = 0

    def load_identity(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]

    def copy_matrix(self):
        new_matrix = [0] * 16
        for i in range(16):
            new_matrix[i] = self.matrix[i]
        return new_matrix

    def add_transformation(self, matrix2):
        counter = 0
        new_matrix = [0] * 16
        for row in range(4):
            for col in range(4):
                for i in range(4):
                    new_matrix[counter] += self.matrix[row*4 + i]*matrix2[col + 4*i]
                counter += 1
        self.matrix = new_matrix

    # OPERATIONS
    def add_scale(self, x = 1, y = 1, z = 1):
        other_matrix = [x, 0, 0, 0,
                        0, y, 0, 0,
                        0, 0, z, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_translation(self, x = 0, y = 0, z = 0):
        other_matrix = [1, 0, 0, x,
                        0, 1, 0, y,
                        0, 0, 1, z,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_rotation(self, angle, axis):
        if axis == 'x':
            other_matrix = [1, 0, 0, 0,
                            0, math.cos(angle * math.pi / 180), -math.sin(angle * math.pi / 180), 0,
                            0, math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180), 0,
                            0, 0, 0, 1]
        elif axis == 'y':
            other_matrix = [math.cos(angle * math.pi / 180), 0, math.sin(angle * math.pi / 180), 0,
                            0, 1, 0, 0,
                            -math.sin(angle * math.pi / 180), 0, math.cos(angle * math.pi / 180), 0,
                            0, 0, 0, 1]
        elif axis == 'z':
            other_matrix = [math.cos(angle * math.pi / 180), -math.sin(angle * math.pi / 180), 0, 0,
                            math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180), 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1]
        else:
            other_matrix = [1, 0, 0, 0,
                            0, 1, 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1]

        self.add_transformation(other_matrix)

    # YOU CAN TRY TO MAKE PUSH AND POP (AND COPY) LESS DEPENDANT ON GARBAGE COLLECTION
    # THAT CAN FIX SMOOTHNESS ISSUES ON SOME COMPUTERS
    def push_matrix(self):
        self.stack.append(self.copy_matrix())

    def pop_matrix(self):
        self.matrix = self.stack.pop()

    # This operation mainly for debugging
    def __str__(self):
        ret_str = ""
        counter = 0
        for _ in range(4):
            ret_str += "["
            for _ in range(4):
                ret_str += " " + str(self.matrix[counter]) + " "
                counter += 1
            ret_str += "]\n"
        return ret_str



# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation

class ViewMatrix:
    def __init__(self):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)

    ## MAKE OPERATIONS TO ADD LOOK, SLIDE, PITCH, YAW and ROLL ##

    def look(self, eye: Vector, center: Vector, up: Vector):
        self.eye = eye
        self.n = Vector(eye[0] - center[0], eye[1] - center[1], eye[2] - center[2])
        self.u = up.cross(self.n)
        self.v = self.n.cross(self.u)
    
    def slide(self, del_u, del_v, del_n): # works!
        self.eye.x += del_u * self.u.x + del_v * self.v.x + del_n * self.n.x
        self.eye.y += del_u * self.u.y + del_v * self.v.y + del_n* self.n.y
        self.eye.z += del_u * self.u.z + del_v * self.v.z + del_n * self.n.z
    
    # not change the or use the y-coordinates of the camera’s coordinate frame.
    def walk(self, del_u, del_v, del_n):
        self.eye.x += del_u * self.u.x + del_v * self.v.x + del_n * self.n.x
        self.eye.z += del_u * self.u.z + del_v * self.v.z + del_n * self.n.z

    # rotate camera about the n-axis
    def roll(self, angle):
        ang_cos = cos(angle * math.pi/180.0)
        ang_sin = sin(angle * math.pi/180.0)
        u_org = self.u # store original u

        self.u = Vector(ang_cos * u_org.x + ang_sin * self.v.x,
                        ang_cos * u_org.y + ang_sin * self.v.y,
                        ang_cos * u_org.z + ang_sin * self.v.z)

        self.v = Vector(- ang_sin * u_org.x + ang_cos * self.v.x,
                        - ang_sin * u_org.y + ang_cos * self.v.y,
                        - ang_sin * u_org.z + ang_cos * self.v.z)

    # rotate camera about the u-axis
    def pitch(self, angle):
        ang_cos = cos(angle * math.pi/180.0)
        ang_sin = sin(angle * math.pi/180.0)
        n_org = self.n # store original n
        
        self.n = Vector(ang_cos * n_org.x + ang_sin * self.v.x,
                        ang_cos * n_org.y + ang_sin * self.v.y,
                        ang_cos * n_org.z + ang_sin * self.v.z)

        self.v = Vector(- ang_sin * n_org.x + ang_cos * self.v.x,
                        - ang_sin * n_org.y + ang_cos * self.v.y,
                        - ang_sin * n_org.z + ang_cos * self.v.z)

    # rotate camera about the v-axis
    def yaw(self, angle):
        ang_cos = cos(angle * math.pi/180.0)
        ang_sin = sin(angle * math.pi/180.0)
        n_org = self.n # store original n
        
        self.n = Vector(ang_cos * n_org.x + ang_sin * self.u.x,
                        ang_cos * n_org.y + ang_sin * self.u.y,
                        ang_cos * n_org.z + ang_sin * self.u.z)

        self.u = Vector(- ang_sin * n_org.x + ang_cos * self.u.x,
                        - ang_sin * n_org.y + ang_cos * self.u.y,
                        - ang_sin * n_org.z + ang_cos * self.u.z)

    # rotate all the vectors (u, v and n) about the base y-axis
    # def turn(self, angle):
    #     ang_cos = cos(angle * math.pi/180.0)
    #     ang_sin = sin(angle * math.pi/180.0)
    #     n_org = self.n # store original n
        
    #     self.n = Vector(ang_cos * n_org.x + ang_sin * self.u.x,
    #                     ang_cos * n_org.y + ang_sin * self.u.y,
    #                     ang_cos * n_org.z + ang_sin * self.u.z)

    #     self.u = Vector(- ang_sin * n_org.x + ang_cos * self.u.x,
    #                     - ang_sin * n_org.y + ang_cos * self.u.y,
    #                     - ang_sin * n_org.z + ang_cos * self.u.z)

    def get_matrix(self):
        minusEye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0,        0,        0,        1]
    
    def to_string(self):
        matrix = self.get_matrix()
        string = "[ " + str(matrix[0]) + ", " + str(matrix[1]) + ", " + str(matrix[2]) + ", " + str(matrix[3]) + ",\n" \
                      + str(matrix[4]) + ", " + str(matrix[5]) + ", " + str(matrix[6]) + ", " + str(matrix[7]) + ",\n" \
                      + str(matrix[8]) + ", " + str(matrix[9]) + ", " + str(matrix[10]) + ", " + str(matrix[11]) + " ]"
        return string
    
    def values_to_string(self):
        return "View matrix:\n" + "\teye: " + self.eye.to_string() + "\n\tu: " + \
                self.u.to_string() + "\n\tn: " + self.n.to_string() + "\n\tv: " + \
                self.v.to_string()


# The ProjectionMatrix class builds transformations concerning
# the camera's "lens"

class ProjectionMatrix:
    def __init__(self):
        self.left = -1
        self.right = 1
        self.bottom = -1
        self.top = 1
        self.near = -1
        self.far = 1

        self.is_orthographic = True

    ## MAKE OPERATION TO SET PERSPECTIVE PROJECTION (don't forget to set is_orthographic to False) ##
    # ---

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.is_orthographic = True

    def get_matrix(self):
        if self.is_orthographic:
            A = 2 / (self.right - self.left)
            B = -(self.right + self.left) / (self.right - self.left)
            C = 2 / (self.top - self.bottom)
            D = -(self.top + self.bottom) / (self.top - self.bottom)
            E = 2 / (self.near - self.far)
            F = (self.near + self.far) / (self.near - self.far)

            return [A,0,0,B,
                    0,C,0,D,
                    0,0,E,F,
                    0,0,0,1]

        else:
            pass
            # Set up a matrix for a Perspective projection
            ###  Remember that it's a non-linear transformation   ###
            ###  so the bottom row is different                   ###



# The ProjectionViewMatrix returns a hardcoded matrix
# that is just used to get something to send to the
# shader before you properly implement the ViewMatrix
# and ProjectionMatrix classes.
# Feel free to throw it away afterwards!

class ProjectionViewMatrix:
    def __init__(self):
        pass

    def get_matrix(self):
        return [ 0.45052942369783683,  0.0,  -0.15017647456594563,  0.0,
                -0.10435451285616304,  0.5217725642808152,  -0.3130635385684891,  0.0,
                -0.2953940042189954,  -0.5907880084379908,  -0.8861820126569863,  3.082884480118567,
                -0.2672612419124244,  -0.5345224838248488,  -0.8017837257372732,  3.7416573867739413 ]


# IDEAS FOR OPERATIONS AND TESTING:
# if __name__ == "__main__":
#     matrix = ModelMatrix()
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_translation(3, 1, 2)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(2, 3, 4)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
#     matrix.add_translation(5, 5, 5)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(3, 2, 3)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
#     matrix.pop_matrix()
#     print(matrix)
        
#     matrix.push_matrix()
#     matrix.add_scale(2, 2, 2)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(3, 3, 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_rotation_y(pi / 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(1, 1, 1)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
