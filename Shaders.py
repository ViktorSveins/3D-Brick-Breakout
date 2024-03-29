
from OpenGL.GL import *
import OpenGL.GLU

from math import * # trigonometry

import sys

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

        self.normalLoc                  = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.uvLoc                  = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.modelMatrixLoc			    = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc              = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc        = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        
        self.eyePosLoc                  = glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        
        self.lightPosLoc                = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDifLoc                = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecLoc               = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        
        self.matDifLoc                  = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")        
        self.matSpecLoc                 = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.matShinLoc                 = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")

        self.difTexLoc                  = glGetUniformLocation(self.renderingProgramID, "u_tex01")        
        self.specTexLoc                 = glGetUniformLocation(self.renderingProgramID, "u_tex02")

        self.usingTex                 = glGetUniformLocation(self.renderingProgramID, "u_using_texture")

        self.spotLightPosLoc                 = glGetUniformLocation(self.renderingProgramID, "u_spotlight_position")
        self.spotLightDiffLoc                 = glGetUniformLocation(self.renderingProgramID, "u_spotlight_diffuse")
        self.spotLightSpecLoc                 = glGetUniformLocation(self.renderingProgramID, "u_spotlight_specular")
        

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)
    
    # Sets the vertex to buffer (faster load time)
    def set_attribute_buffers(self, vertex_buffer_id):
        glDisableVertexAttribArray(self.uvLoc)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        glEnableVertexAttribArray(self.uvLoc)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))

    def set_uv_attribute(self, vertex_array):
        glEnableVertexAttribArray(self.uvLoc)
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)
    
    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_diffuse(self, r, g, b):
        glUniform4f(self.lightDifLoc, r, g, b, 1.0)
    
    def set_light_specular(self, r, g, b):
        glUniform4f(self.lightSpecLoc, r, g, b, 1.0)
    
    def set_material_diffuse(self, color):
        glUniform4f(self.matDifLoc, color.r, color.g, color.b, 1.0)
    
    def set_material_specular(self, color):
        glUniform4f(self.matSpecLoc, color.r, color.g, color.b, 1.0)
    
    def set_material_shininess(self, shininess):
        glUniform1f(self.matShinLoc, shininess)

    def set_dif_tex(self, num):
        glUniform1i(self.difTexLoc, num)

    def set_spec_tex(self, num):
        glUniform1i(self.specTexLoc, num)

    def set_using_tex(self, num):
        glUniform1f(self.usingTex, num)

    # Spotlight
    def set_spotlight_position(self, pos):
        glUniform4f(self.spotLightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_spotlight_diffuse(self, color):
        glUniform4f(self.spotLightDiffLoc, color.r, color.g, color.b, 1.0)
    
    def set_spotlight_specular(self, color):
        glUniform4f(self.spotLightSpecLoc, color.r, color.g, color.b, 1.0)
    # Spotlight ends

#################
# Sprite shader #
#################

class SpriteShader:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/sprite_shader.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/sprite_shader.frag")
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

        self.uvLoc                  = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.modelMatrixLoc			    = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc              = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc        = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        self.difTexLoc                  = glGetUniformLocation(self.renderingProgramID, "u_tex01")        
        self.alphaTexLoc                 = glGetUniformLocation(self.renderingProgramID, "u_tex02")

        self.usingAlphaTexture          = glGetUniformLocation(self.renderingProgramID, "u_using_alpha_texture")
        self.opacityLoc                 = glGetUniformLocation(self.renderingProgramID, "u_opacity")
        

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_dif_tex(self, num):
        glUniform1i(self.difTexLoc, num)

    def set_alpha_tex(self, num):
        if num == None:
            glUniform1f(self.usingAlphaTexture, 0.0)            
        else:
            glUniform1f(self.usingAlphaTexture, 1.0)
            glUniform1i(self.alphaTexLoc, num)

    def set_opacity(self, opacity):
        glUniform1f(self.opacityLoc, opacity)

    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))