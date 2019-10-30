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
        self.sides.append(LineObstacle(self.corner_4, self.corner_3))
        self.sides.append(LineObstacle(self.corner_1, self.corner_4))

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
        # for i,side in enumerate(self.sides):
        #     if side.collision(c_position, radius, c_motion, delta_time):
        #         self.collision_side = i
        #         return True
        if self.sides[3].collision(c_position, radius, c_motion, delta_time):
            self.collision_side = 3
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

    def collision(self, ball, delta_time):
        distX = self.point_1.x - self.point_2.x
        distY = self.point_1.y - self.point_2.y
        
        length = sqrt(distX**2 + distY**2)
        # print(f"point1: ({self.point_1}), point2: ({self.point_2}), length: {length}")
        
        dotproduct = ( ((ball.pos.x - self.point_1.x) * (self.point_2.x - self.point_1.x))
                     + ((ball.pos.y - self.point_1.y) * (self.point_2.y - self.point_1.y)) ) / length**2
        # print(f"dotproduct: {dotproduct}")

        closestPointOnLine = Point(self.point_1.x + dotproduct * (self.point_2.x - self.point_1.x), 
                                   self.point_1.y + dotproduct * (self.point_2.y - self.point_1.y), 0)
        # print(f"closest point on line: {closestPointOnLine}")

        vector = Vector(ball.pos.x - closestPointOnLine.x, ball.pos.y - closestPointOnLine.y, 0)
        vector.normalize()

        traversal = vector * ball.radius
        closestPointOnCircle = Point(ball.pos.x - traversal.x, ball.pos.y - traversal.y, 0)
        # print(f"Closest point on Circle: {closestPointOnCircle}")
        # if c_position.x > 0.49 and c_position.x < 0.51:
        #     print(f"closest point on line: {closestPointOnLine}")
        #     print(f"Closest point on Circle: {closestPointOnCircle}")
       
        normalDot = self.normal_vector.dot(ball.motion)
        if(normalDot == 0):
            t_hit = 0
        else:    
            t_hit = self.normal_vector.dot(self.point_2 - closestPointOnCircle) / normalDot

        if t_hit > 0 and t_hit <= delta_time:
            p_hit = closestPointOnCircle + ball.motion * t_hit
            # print(f"tHit: {t_hit}")
            # print(f"pHit: cirlceP({closestPointOnCircle}) + Cmotion({c_motion.x}, {c_motion.y}, {c_motion.z}) * tHit({t_hit}) = {p_hit}")
            print(f"pHit")
            print(f"closest point on circ: {closestPointOnCircle}")
            print(f"closest point on line: {closestPointOnLine}")

            if self.point_1.x < self.point_2.x:
                x_min, x_max = self.point_1.x, self.point_2.x
            else:
                x_min, x_max = self.point_2.x, self.point_1.x

            if self.point_1.y < self.point_2.y:
                y_min, y_max = self.point_1.y, self.point_2.y
            else:
                y_min, y_max = self.point_2.y, self.point_1.y

            if p_hit.x >= x_min and p_hit.x <= x_max and p_hit.y >= y_min and p_hit.y <= y_max:
                ball.pos = p_hit
                ball.motion = self.reflection(ball.motion)
                return ball
        return ball
    
    def reflection(self, c_motion):
        return c_motion - self.normal_vector * (c_motion.dot(self.normal_vector) / (self.normal_vector.dot(self.normal_vector))) * 2
