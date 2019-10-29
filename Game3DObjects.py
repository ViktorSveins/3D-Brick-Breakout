from Base3DObjects import *

class Brick(Cube):
    def __init__(self, position, width, height, color):
        super().__init__()
        self.pos = position
        self.w = width
        self.h = height
        self.l = 5
        self.color = color

        self.corner_1 = Point(self.pos.x - self.w / 2, self.pos.y - self.h /2, 0)
        self.corner_2 = Point(self.pos.x - self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_3 = Point(self.pos.x + self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_4 = Point(self.pos.x + self.w / 2, self.pos.y - self.h /2, 0)

        self.sides = []
        self.sides.append(LineObstacle(self.corner_1, self.corner_2))
        self.sides.append(LineObstacle(self.corner_2, self.corner_3))
        self.sides.append(LineObstacle(self.corner_3, self.corner_4))
        self.sides.append(LineObstacle(self.corner_4, self.corner_1))

        self.collision_side = 0


    def display(self, model_matrix, shader):
        shader.set_mat_diffuse(self.color.r, self.color.g, self.color.b)
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        model_matrix.add_scale(self.w, self.h, self.l)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader)
        model_matrix.pop_matrix()
        
    def collision(self, c_position, radius, c_motion, delta_time):
        for i,side in enumerate(self.sides):
            if side.collision(c_position, radius, c_motion, delta_time):
                self.collision_side = i
                return True
        return False

    def reflection(self, c_motion):
        return self.sides[self.collision_side].reflection(c_motion)



class Ball(Sphere):
    def __init__(self, position, size, color=Color(1.0, 0.874, 0.0)):
        super().__init__(12, 24)
        self.pos = position
        self.size = size
        self.color = color
        self.shininess = 50.0
        self.radius = (self.size / 2) + 0.5
        self.shot = True
        self.motion = Vector(0,0,0)

    def display(self, model_matrix, shader):
        shader.set_mat_diffuse(self.color.r, self.color.g, self.color.b)
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        model_matrix.add_scale(self.size, self.size, self.size)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader)
        model_matrix.pop_matrix()

    # def update(self, platform_motion, shooting, delta_time):
    #     if shooting and not self.shot:
    #         self.motion = Vector(platform_motion.x, 1) * self.speed # Find way to affect ball if shot of moving platform
    #         self.shot = True
        
    #     if self.shot:
    #         self.position += self.motion * delta_time

    def update(self, delta_time):
        self.pos += self.motion * delta_time
        
class LineObstacle(Line):
    def __init__(self, point_1, point_2):
        Line.__init__(self, point_1, point_2)
        self.normal_vector = Vector(-(self.point_2.y - self.point_1.y), self.point_2.x - self.point_1.x, 0)

    def collision(self, c_position, radius, c_motion, delta_time):
        distX = self.point_1.x - self.point_2.x
        distY = self.point_1.y - self.point_2.y
        
        length = sqrt(distX**2 + distY**2)
        
        dotproduct = ( ((c_position.x - self.point_1.x) * (self.point_2.x - self.point_1.x))
                     + ((c_position.y - self.point_1.y) * (self.point_2.y - self.point_1.y)) ) / length**2

        closestPointOnLine = Point(self.point_1.x + dotproduct * (self.point_2.x - self.point_1.x), 
                                   self.point_1.y + dotproduct * (self.point_2.y - self.point_1.y), 0)

        vector = Vector(c_position.x - closestPointOnLine.x, c_position.y - closestPointOnLine.y, 0)
        vector.normalize()

        traversal = vector * radius
        closestPointOnCircle = Point(c_position.x - traversal.x, c_position.y - traversal.y, 0) 
       
        normalDot = self.normal_vector.dot(c_motion)
        if(normalDot == 0):
            t_hit = 0
        else:    
            t_hit = self.normal_vector.dot(self.point_2 - closestPointOnCircle) / normalDot

        if t_hit > 0 and t_hit <= delta_time:
            print("THIT")
            p_hit = closestPointOnCircle + c_motion * t_hit

            if self.point_1.x < self.point_2.x:
                x_min, x_max = self.point_1.x, self.point_2.x
            else:
                x_min, x_max = self.point_2.x, self.point_1.x

            if self.point_1.y < self.point_2.y:
                y_min, y_max = self.point_1.y, self.point_2.y
            else:
                y_min, y_max = self.point_2.y, self.point_1.y

            return p_hit.x >= x_min and p_hit.x <= x_max and p_hit.y >= y_min and p_hit.y <= y_max
        else:    
            return False
    
    def reflection(self, c_motion):
        return c_motion - self.normal_vector * (c_motion.dot(self.normal_vector) / (self.normal_vector.dot(self.normal_vector))) * 2
