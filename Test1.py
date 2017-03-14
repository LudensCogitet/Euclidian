import pygame
import math

class Point:
    num_points = 0
    
    def __init__(self,x,y,color):
        #print("New Point "+str(x)+","+str(y))
        #print("num_points: " + str(Point.num_points))
        Point.num_points = Point.num_points + 1
        self.num = Point.num_points
        self.x = x
        self.y = y
        self.color = color
        self.size = 3

        target_size = 20
        self.target = pygame.Rect(x - target_size/2, y - target_size/2, target_size, target_size)

        collide_size = 5
        self.collide = pygame.Rect(x - collide_size/2, y - collide_size/2, collide_size, collide_size)

    def draw(self,surface):
        pygame.draw.circle(surface,self.color,(self.x,self.y),self.size)

class Line:
    num_lines = 0

    def __init__(self,endPoints,color):
        Line.num_lines = Line.num_lines + 1
        self.num = Line.num_lines
        self.endPoints = endPoints
        self.color = color
        self.size = 2

        self.surf = pygame.Surface((max(self.endPoints[0].x, self.endPoints[1].x),max(self.endPoints[0].y,self.endPoints[1].y)),pygame.SRCALPHA,32)
        self.surf.convert_alpha()

        self.rect = self.surf.get_rect()
        self.rect.y = min(self.endPoints[0].x, self.endPoints[1].x)
        self.rect.x = min(self.endPoints[0].y,self.endPoints[1].y)

        pygame.draw.line(self.surf,self.color,(endPoints[0].x-self.rect.x,endPoints[0].y-self.rect.y),(endPoints[1].x-self.rect.x,endPoints[1].y-self.rect.y),2)

    def draw(self,surface,coords = None):
        if coords == None:
            coords = (self.rect.x,self.rect.y)
        surface.blit(self.surf,coords)

class Circle:
    num_circles = 0

    def __init__(self,center,radius,color):
        Circle.num_circles = Circle.num_circles + 1
        self.center = center
        self.radius = radius
        self.color = color

        self.surf = pygame.Surface((int(radius*2), int(radius*2)),pygame.SRCALPHA,32)
        self.surf.convert_alpha()
        pygame.draw.circle(self.surf,self.color,(int(radius),int(radius)),radius,2)

        self.rect = self.surf.get_rect()
        self.rect.top = self.center.y - radius;
        self.rect.left = self.center.x - radius;

    def draw(self,surface,coords = None):
        if coords == None:
            coords = (self.rect.x,self.rect.y)
        surface.blit(self.surf,coords)
        #pygame.draw.circle(surface,self.color,(self.center.x,self.center.y),self.radius,1)

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
                            #print("This is point number: " + str(point.num))
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

                        newCircle = Circle(select_point,radius,(0,0,0))
                        for figure in figures:
                            if newCircle.rect.colliderect(figure.rect):
                                offset_x = min(newCircle.rect.x, figure.rect.x)
                                offset_y = min(newCircle.rect.y, figure.rect.y)

                                
                                
                                width = max(newCircle.rect.left + newCircle.rect.width, figure.rect.left + figure.rect.width)
                                width = width - offset_x
                                height = max(newCircle.rect.top + newCircle.rect.height, figure.rect.top + figure.rect.height)
                                height = height - offset_y

                                tempSurf1 = pygame.Surface((width,height),pygame.SRCALPHA,32)
                                tempSurf1.convert_alpha()

                                tempSurf2 = tempSurf1.copy()

                                newCircle.draw(tempSurf1,(newCircle.rect.x - offset_x, newCircle.rect.y - offset_y))
                                figure.draw(tempSurf2, (figure.rect.x - offset_x, figure.rect.y - offset_y))

                                overlap = pygame.mask.from_surface(tempSurf1).overlap_mask(pygame.mask.from_surface(tempSurf2),(0,0))
                   
                                size = overlap.get_size()
                                #print("overlap count" + str(overlap.count()))
                                for x in range(size[0]):
                                    for y in range(size[1]):
                                        if overlap.get_at((x,y)) != 0:
                                            newPoint = Point(x+offset_x,y+offset_y,(200,0,0))
                                            collision = False
                                            for point in points:
                                                if newPoint.collide.colliderect(point.collide) or newPoint.collide.contains(point.collide):
                                                    #print("collision")
                                                    collision = True
                                                    break
                                            if collision == False:
                                                points.append(newPoint)
                                            else:
                                                Point.num_points = Point.num_points - 1
                               
                        figures.append(newCircle)
                        select_point = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                Point.num_points = 0
                points = []
                Circle.num_circles = 0
                figures = []
            if event.key == pygame.K_s:
                if event.mod == pygame.KMOD_LCTRL:
                    pygame.image.save(screen,"./save.png")
            
                                
        if event.type == pygame.QUIT:
            done = True

    screen.fill((150,150,150))

    if select_point != None:
        mouse_pos = pygame.mouse.get_pos()
        x_dist = mouse_pos[0] - select_point.x 
        y_dist = mouse_pos[1] - select_point.y
        radius = int(math.sqrt(x_dist*x_dist + y_dist*y_dist))

        if radius < 2:
            radius = 2
        
        pygame.draw.circle(screen,(0,0,0),(select_point.x,select_point.y),radius,2)
    
    for figure in figures:
        figure.draw(screen)

    for point in points:
        point.draw(screen)
 
    pygame.display.flip()
    
pygame.quit()
