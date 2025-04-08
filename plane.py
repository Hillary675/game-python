import pygame

class Plane(pygame.sprite.Sprite):
    def __init__(self, scale_factor):
        super().__init__()
        
        #image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #rect
        self.rect = self.image.get_rect(midleft = (480 / 20, 800 / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #movement
        self.gravity = 600
        self.direction = 0

        #control flag
        self.update_on = False

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(f'assets/images/plane{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self,dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
        
    def flap(self):
        self.direction = -400

    def animate(self,dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)    
        self.image = rotated_plane

    def update(self, dt):
        if self.update_on:
            self.apply_gravity(dt)
            self.animate(dt)
            self.rotate()