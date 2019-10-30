
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time
from random import randint

from Shaders import *
from Matrices import *
from Base3DObjects import *
from Game3DObjects import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0, 9.5, 10), Point(0, 9.5, 0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 4
        
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False  
        self.DOWN_key_down = False
        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.w_key_down = False
        self.s_key_down = False
        self.a_key_down = False
        self.d_key_down = False
        self.t_key_down = False
        self.g_key_down = False
        self.q_key_down = False
        self.e_key_down = False
        self.z_key_down = False
        self.x_key_down = False
        self.pause_game = False

        
        self.brick = Brick(Point(0, 10, 0), 3, 1, Color(1.0, 0.0, 0.0))
        self.ball = Ball(Point(10.0, 0.0, 0.0), 1)
        self.ball.motion = Vector(-1, 0.95, 0)

    def load_texture(self, path_string):
        surface = pygame.image.load(sys.path[0] + path_string)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # #     angle -= (2 * pi)
        
        self.ball.update(delta_time)
        self.ball = self.brick.collision(self.ball, delta_time)

        if self.UP_key_down:
            self.view_matrix.pitch((pi / 2) * delta_time)
        if self.DOWN_key_down:
            self.view_matrix.pitch(-(pi / 2) * delta_time)
        if self.LEFT_key_down:
            self.view_matrix.yaw(-(pi / 2) * delta_time)
        if self.RIGHT_key_down:
            self.view_matrix.yaw((pi / 2) * delta_time)

        if self.w_key_down:
            self.view_matrix.slide(0, 0, -3 * delta_time)
        if self.s_key_down:
            self.view_matrix.slide(0, 0, 3 * delta_time)
        if self.a_key_down:
            self.view_matrix.slide(-3 * delta_time, 0, 0)
        if self.d_key_down:
            self.view_matrix.slide(3 * delta_time, 0, 0)

        if self.q_key_down:
            self.view_matrix.roll((pi / 2) * delta_time)
        if self.e_key_down:
            self.view_matrix.roll(-(pi / 2) * delta_time)

        if self.z_key_down:
            self.view_matrix.slide(0, -1 * delta_time, 0)            
        if self.x_key_down:
            self.view_matrix.slide(0, 1 * delta_time, 0)

        if self.t_key_down:
            self.fov += 0.25 * delta_time
        if self.g_key_down:
            self.fov -= 0.25 * delta_time
            

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        glClearColor(1.0, 1.0, 0.0, 1.0)



        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)

        self.shader.set_view_matrix((self.view_matrix.get_matrix()))
        # self.shader.set_light_position(Point(3.0, 10.0, 6.0))
        self.shader.set_light_position(self.view_matrix.eye)
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)

        self.shader.set_mat_specular(1.0, 1.0, 1.0)
        self.shader.set_mat_shininess(5.0)
        
        self.model_matrix.load_identity()

        # self.shader.set_mat_diffuse(1.0, 1.0, 1.0)
        # self.model_matrix.add_scale(3.0, 3.0, 3.0)
        # cube = Cube()
        # cube.set_vertices(self.shader)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # cube.draw(self.shader)

        
        self.ball.set_vertices(self.shader)
        self.ball.display(self.model_matrix, self.shader)

        self.brick.set_vertices(self.shader)
        self.brick.display(self.model_matrix, self.shader)


        pygame.display.flip()

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
                        
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_DOWN:
                        self.DOWN_key_down = True
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True

                    if event.key == K_w:
                        self.w_key_down = True
                    if event.key == K_s:
                        self.s_key_down = True
                    if event.key == K_a:
                        self.a_key_down = True
                    if event.key == K_d:
                        self.d_key_down = True
                    if event.key == K_t:
                        self.t_key_down = True
                    if event.key == K_g:
                        self.g_key_down = True
                    if event.key == K_q:
                        self.q_key_down = True
                    if event.key == K_e:
                        self.e_key_down = True
                    if event.key == K_z:
                        self.z_key_down = True
                    if event.key == K_x:
                        self.x_key_down = True
                    if event.key == K_p:
                        self.pause_game = not self.pause_game
                        
                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_DOWN:
                        self.DOWN_key_down = False
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    
                    if event.key == K_w:
                        self.w_key_down = False
                    if event.key == K_s:
                        self.s_key_down = False
                    if event.key == K_a:
                        self.a_key_down = False
                    if event.key == K_d:
                        self.d_key_down = False
                    if event.key == K_t:
                        self.t_key_down = False
                    if event.key == K_g:
                        self.g_key_down = False
                    if event.key == K_q:
                        self.q_key_down = False
                    if event.key == K_e:
                        self.e_key_down = False
                    if event.key == K_z:
                        self.z_key_down = False
                    if event.key == K_x:
                        self.x_key_down = False

            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()