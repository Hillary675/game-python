import pygame, sys, time
from plane import Plane
from pipe import Pipe
pygame.init()

class Game:
    def __init__(self):

        self.width =480
        self.height = 800
        self.scale_factor = 1.5
        self.win= pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.move_speed = 300
        self.plane = Plane(self.scale_factor)

        self.is_enter_pressed = False
        self.pipes=[]
        self.pipe_generate_counter = 71
        self.setUpBgAndGround()

        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = time.time() - last_time
            last_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.is_enter_pressed = True
                        self.plane.update_on = True
                    if event.key == pygame.K_SPACE and self.is_enter_pressed:
                        self.plane.flap(dt)

            self.updateEverythong(dt)
            self.checkCollisions()
            self.drawEverything()
            self.clock.tick(60)
            pygame.display.update()

    def checkCollisions(self):
        if len(self.pipes):
            if self.plane.rect.bottom > self.height:
                self.plane.update_on = False
                self.is_enter_pressed = False
            if (self.plane.rect.colliderect(self.pipes[0].rect_down) or self.plane.rect.colliderect(self.pipes[0].rect_up)):
                self.is_enter_pressed = False

    def updateEverythong(self, dt):
        if self.is_enter_pressed:

            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right<0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right<0:
                self.ground2_rect.x = self.ground1_rect.right

            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0

            self.pipe_generate_counter += 1

            for pipe in self.pipes:
                pipe.update(dt)

            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)

        self.plane.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg, (0,-300))
        
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.plane.image, self.plane.rect)

    def setUpBgAndGround(self):
        self.bg = pygame.transform.scale_by(pygame.image.load('assets/images/bg.png').convert(), self.scale_factor)
        self.ground1_img = pygame.transform.scale_by(pygame.image.load('assets/images/ground.png').convert_alpha(), self.scale_factor)
        self.ground2_img = pygame.transform.scale_by(pygame.image.load('assets/images/ground.png').convert_alpha(), self.scale_factor)

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground1_rect.y = self.ground1_rect.right 
        self.ground2_rect.x = 600
        self.ground2_rect.y = 600
        
if __name__ == "__main__":
    game = Game()
    pygame.quit()