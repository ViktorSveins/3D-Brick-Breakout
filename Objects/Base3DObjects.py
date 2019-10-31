
import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *

import numpy


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"
        
class Color:
    def __init__(self, r, g, b, a = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)

    def __sub__(self, other):
        return Color(self.r - other.r, self.g - other.g, self.b - other.b, self.a - other.a)

class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

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
    
    def length(self):
        return self.__len__()

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

class Sphere:
    def __init__(self, stacks = 12, slices = 24):
        self.vertex_array = []
        self.slices = slices
        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                self.vertex_array.append(sin(stack_angle) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle))
                self.vertex_array.append(sin(stack_angle) * sin(slice_angle))
                
                self.vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle + stack_interval))
                self.vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                self.vertex_count += 2
    
    # def set_vertices(self, shader):
    #     shader.set_position_attribute(self.vertex_array)
    #     shader.set_normal_attribute(self.vertex_array)

    def draw(self, shader):
        shader.set_position_attribute(self.vertex_array)
        shader.set_normal_attribute(self.vertex_array)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)


class OptiSphere:
    def __init__(self, stacks = 12, slices = 24):
        vertex_array = []
        self.slices = slices
        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                for _ in range(2):
                    vertex_array.append(sin(stack_angle) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle))
                    vertex_array.append(sin(stack_angle) * sin(slice_angle))
                for _ in range(2):
                    vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle + stack_interval))
                    vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                self.vertex_count += 2
        
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        vertex_array = None
    
    # def set_vertices(self, shader):
    #     shader.set_attribute_buffers(self.vertex_buffer_id)

    def draw(self, shader):
        shader.set_attribute_buffers(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)