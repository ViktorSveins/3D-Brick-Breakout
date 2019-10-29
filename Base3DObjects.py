
import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

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
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

class Cube:
    def __init__(self):
        self.position_array = [
            -0.5, -0.5, -0.5, -0.5, 0.5, -0.5,
            0.5, -0.5, -0.5, 0.5, 0.5, -0.5,
            #// right
            0.5, -0.5, -0.5, 0.5, 0.5, -0.5,
            0.5, -0.5, 0.5, 0.5, 0.5, 0.5,
            #// ront
            0.5, -0.5, 0.5, 0.5, 0.5, 0.5,
            -0.5, -0.5, 0.5, -0.5, 0.5, 0.5,
            #// let
            -0.5, -0.5, 0.5, -0.5, 0.5, 0.5,
            -0.5, -0.5, -0.5, -0.5, 0.5, -0.5,
            #// top
            -0.5, 0.5, -0.5, -0.5, 0.5, 0.5,
            0.5, 0.5, -0.5, 0.5, 0.5, 0.5,
            #// bottom
            -0.5, -0.5, -0.5, -0.5, -0.5, 0.5,
            0.5, -0.5, -0.5, 0.5, -0.5, 0.5]
                            
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0
                            ]
        self.uv_array = [
            #// back
            2/3, 0.0, 2/3, 1/3,
            1.0, 0.0, 1.0, 1/3,
            #// right
            2/3, 1/3, 2/3, 2/3,
            1.0, 1/3, 1.0, 2/3,
            #// ront
            1/3, 1/3, 1/3, 2/3,
            2/3, 1/3, 2/3, 2/3,
            #// let
            1/3, 1/3, 1/3, 2/3,
            0.0, 1/3, 0.0, 2/3,
            #// top
            1/3, 2/3, 1/3, 1.0,
            2/3, 2/3, 2/3, 1.0,
            #// bottom
            1/3, 0.0, 1/3, 1/3,
            2/3, 0.0, 2/3, 1/3]

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):        
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 20, 4)

class Dice(Cube):
    def __init__(self):
        super().__init__()
                        