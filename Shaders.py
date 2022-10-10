
from OpenGL.GL import *
import sys
from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)
        ## ADD CODE HERE ##
        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        # Matrices
        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")

        # Light1
        self.lightPosLoc1 = glGetUniformLocation(self.renderingProgramID, "u_light_position_1")
        self.lightColLoc1 = glGetUniformLocation(self.renderingProgramID, "u_light_color_1")

        # Light2
        self.lightPosLoc2 = glGetUniformLocation(self.renderingProgramID, "u_light_position_2")
        self.lightColLoc2 = glGetUniformLocation(self.renderingProgramID, "u_light_color_2")

        # general lights
        self.matDifLoc = glGetUniformLocation(self.renderingProgramID, "u_material_diffuse")
        self.matSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_material_specular")
        self.matShineLoc = glGetUniformLocation(self.renderingProgramID, "u_material_shininess")

        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        self.globalAmbLoc = glGetUniformLocation(self.renderingProgramID, "u_global_ambient")


    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    # Matrices
    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    # Position and normal
    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    # Light1
    def set_light_position_1(self, pos):
        glUniform4f(self.lightPosLoc1, pos.x, pos.y, pos.z, 1.0)

    def set_light_color_1(self, r, g, b):
        glUniform4f(self.lightColLoc1, r, g, b, 1.0)

    # Light2
    def set_light_position_2(self, pos):
        glUniform4f(self.lightPosLoc2, pos.x, pos.y, pos.z, 1.0)

    def set_light_color_2(self, r, g, b):
        glUniform4f(self.lightColLoc2, r, g, b, 1.0)

    # general lights
    def set_material_diffuse(self, r, g, b):
        glUniform4f(self.matDifLoc, r, g, b, 1.0)

    def set_material_specular(self, r, g, b):
        glUniform4f(self.matSpecLoc, r, g, b, 1.0)

    def set_material_shine(self, s):
        glUniform1f(self.matShineLoc, s)


    def set_eye_location(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_global_ambient_location(self, r, g, b):
        glUniform4f(self.globalAmbLoc, r, g, b, 1.0)

