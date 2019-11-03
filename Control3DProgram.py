
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
from Objects.GameBricks import *
from Objects.Base3DObjects import *
from texture_loading import *
from Objects.Environment import *

import ojb_3D_loading

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.sprite_shader = SpriteShader()
        self.sprite_shader.use()

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0.0, 0.0, 3), Point(0.0, 0.0, 0), Vector(0, 1, 0))
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

        self.texture_id01 = load_texture("/crack1.png")
        self.texture_id02 = load_texture("/crack2.png")
        self.texture_id03 = load_texture("/crack3.png")
        self.textures = [self.texture_id01, self.texture_id02, self.texture_id03]
        self.texture_galaxy = load_texture("/skydome.jpeg")
        
        # self.brick2 = OneHitBrick(Point(-2, 8, 0), 3, 1, Color(1.0, 0.0, 0.0), self.textures)
        self.brickArray = []
        for i in range(5):
            brick = ThreeHitBrick(Point(i * 3, 11, 0), 3, 1, self.textures)
            self.brickArray.append(brick)
            brick = TwoHitBrick(Point(i * 3, 5, 0), 3, 1, self.textures)
            self.brickArray.append(brick)

        for i in range(1, 5):
            brick = OneHitBrick(Point(-i * 3, 11, 0), 3, 1, self.textures)
            self.brickArray.append(brick)
            brick = ThreeHitBrick(Point(-i * 3, 5, 0), 3, 1, self.textures)
            self.brickArray.append(brick)
        # self.brick3 = Brick(Point(1.5, 5, 0), 3, 1, Color(1.0, 0.0, 0.0))
        self.ballArray = []
        self.ball = Ball(Point(18.0, 5, 0.0), 0.5)
        self.ball.motion = Vector(-1.5, 1.7, 0)

        self.ball2 = Ball(Point(19.0, 4, 0.0), 0.5)
        self.ball2.motion = Vector(-1.5, 1.7, 0)

        self.ball3 = Ball(Point(20.0, 3, 0.0), 0.5)
        self.ball3.motion = Vector(-1.5, 1.7, 0)

        self.ball4 = Ball(Point(21.0, 2, 0.0), 0.5)
        self.ball4.motion = Vector(-1.5, 1.7, 0)
        
        self.ballArray.append(self.ball)
        self.ballArray.append(self.ball2)
        self.ballArray.append(self.ball3)
        self.ballArray.append(self.ball4)
        self.skydome = Skysphere()
        self.platform = Platform(Point(0, 0, 0))

        # self.obj_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models/obj/", "eyeball.obj")
        # self.obj_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models/", "metallic_sphere.obj")


        self.pauseTime = 0.0

        # check framerate, use for optimizing
        self.fr_ticker = 0.0
        self.fr_sum = 0.0

        ### used for testing here
        self.sphere = Sphere(24, 48)
        self.sprite = Sprite()
        self.texture_leaf_color = load_texture("/test_leaf_01.jpg")
        self.texture_leaf_alpha = load_texture("/test_leaf_01_alpha.jpg")

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        if self.pause_game:
            return

        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0

        self.angle += pi * delta_time
        # #     angle -= (2 * pi)
        
        for ball in self.ballArray:
            ball.update(delta_time)

        tmpList = []
        for brick in self.brickArray:
            for i in range(len(self.ballArray)):
                self.ballArray[i] = brick.collision(self.ballArray[i], delta_time)
                brick.update()
            if not brick.destroy:
                tmpList.append(brick)
        self.brickArray = tmpList

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

        glClear(GL_COLOR_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        self.model_matrix.load_identity()

        #### Skydome
        glDisable(GL_DEPTH_TEST)
        self.sprite_shader.use()
        self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_galaxy)
        self.sprite_shader.set_dif_tex(0)
        self.sprite_shader.set_alpha_tex(None)

        self.sprite_shader.set_opacity(1.0)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)

        self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
        self.skydome.draw(self.sprite_shader)
        self.model_matrix.pop_matrix()

        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)
        ##### Skydome ends

        self.shader.use()

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)

        self.shader.set_view_matrix((self.view_matrix.get_matrix()))
        # self.shader.set_light_position(Point(0.0, 20.0, 10.0))
        self.shader.set_light_position(self.view_matrix.eye)
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)

        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(5.0)
        

        self.platform.display(self.model_matrix, self.shader)
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.014, 0, 0)
        # self.model_matrix.add_rotate_x(-pi/2)
        # self.model_matrix.add_scale(0.00345, 0.00345, 0.00345)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.obj_model.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # self.brickArray[0].set_vertices(self.shader)

        # self.brick.display(self.model_matrix, self.shader)


        self.shader.set_using_tex(1.0)        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        self.shader.set_dif_tex(0)
        for ball in self.ballArray:
            ball.display(self.model_matrix, self.shader)
        self.shader.set_using_tex(0.0)

        self.brickArray[0].set_vertices(self.shader)

        for brick in self.brickArray:
            brick.display(self.model_matrix, self.shader)

        ####################
        # for i in range(8):
        #     self.model_matrix.push_matrix()
        #     self.model_matrix.add_rotate_x(self.angle * 0.74324 + i * pi / 4.0)
        #     self.model_matrix.add_translation(0.0, 5.0, 10.0)
        #     self.model_matrix.add_rotate_x(-(self.angle * 0.74324 + i * pi / 4.0))
        #     self.model_matrix.add_scale(3.0, 3.0, 3.0)
        #     self.shader.set_model_matrix(self.model_matrix.matrix)

        #     self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        #     self.sphere.draw(self.shader)
        #     self.model_matrix.pop_matrix()
        ####################

        ##### Adding to sprite shader how to draw with alpha image #####
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        # self.sprite_shader.use()
        # self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        # self.sprite_shader.set_view_matrix((self.view_matrix.get_matrix()))

        # glActiveTexture(GL_TEXTURE0)
        # glBindTexture(GL_TEXTURE_2D, self.texture_leaf_color)
        # self.sprite_shader.set_dif_tex(0)
        # glActiveTexture(GL_TEXTURE1)
        # glBindTexture(GL_TEXTURE_2D, self.texture_leaf_alpha)
        # self.sprite_shader.set_alpha_tex(1)

        # self.sprite_shader.set_opacity(0.8)

        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(3.0, 6.0, 0.0)
        # self.model_matrix.add_scale(8.0, 8.0, 1.0)
        # self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
        # self.sprite.draw(self.sprite_shader)
        # self.model_matrix.pop_matrix()

        glDisable(GL_BLEND)

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