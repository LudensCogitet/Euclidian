import pygame
import math

class Point:
    num_points = 0
    
    def __init__(self,x,y,color):
        print("New Point "+str(x)+","+str(y))
        Point.num_points = Point.num_points + 1
        self.num = Point.num_points
        self.x = x
        self.y = y
        self.color = color
        self.size = 3

        target_size = 20
        self.target = pygame.Rect(x - target_size/2, y - target_size/2, target_size, target_size)

    def draw(self,surface):
        pygame.draw.circle(surface,self.color,(self.x,self.y),self.size)

class Circle:
    num_circles = 0

    def __init__(self,center,radius,color):
        Circle.num_circles = Circle.num_circles + 1
        self.center = center
        self.radius = radius
        self.color = color

    def draw(self,surface):
        pygame.draw.circle(surface,self.color,(self.center.x,self.center.y),self.radius,1)

points = []
figures = []

tool = "circle"
select_point = None;

pygame.init()
screen = pygame.display.set_mode((1600,900))

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if tool == "circle":
                    hit = False
                    target = None
                    for point in points:
                        if point.target.collidepoint(event.pos[0],event.pos[1]):
                            print("This is point number: " + str(point.num))
                            if select_point == None:
                                select_point = point
                            else:
                                target = (point.x -select_point.x, point.y -select_point.y)
                            hit = True
                            break
                    if hit == False:
                        if select_point == None:
                            select_point = Point(event.pos[0],event.pos[1],(200,0,0))
                            points.append(select_point)
                        elif target == None:
                            target = (event.pos[0] - select_point.x, event.pos[1] - select_point.y)


                    if select_point != None and target != None:
                        radius = int(math.sqrt(target[0]*target[0] + target[1]*target[1])+1)
                    
                        figures.append(Circle(select_point,radius,(200,0,0)))
                        select_point = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                Point.num_points = 0
                points = []
                Circle.num_circles = 0
                figures = []
            
                                
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0,0,0))

    if select_point != None:
        x_dist = event.pos[0] - select_point.x 
        y_dist = event.pos[1] - select_point.y
        radius = int(math.sqrt(x_dist*x_dist + y_dist*y_dist))

        if radius < 2:
            radius = 2
        
        pygame.draw.circle(screen,(200,0,0),(select_point.x,select_point.y),radius,1)
    
    for point in points:
        point.draw(screen)
    for figure in figures:
        figure.draw(screen)

    pygame.display.flip()
    
pygame.quit()
