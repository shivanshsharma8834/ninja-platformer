# Imported Main Game Libraries
import pygame
import sys

# Importing other scripts to the app
from scripts.entities import PhysicsEntity
from scripts.utils import *
from scripts.tilemap import Tilemap 

class Game:

    def __init__(self):

        pygame.init()

        pygame.display.set_caption('Ninja Game')

        self.screen = pygame.display.set_mode((640,480))

        self.display = pygame.Surface((320,240))

        self.clock = pygame.time.Clock()

        self.player = PhysicsEntity(self, 'player',(50,50),(8,15))

        self.movement = [False,False]

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png')
        }

        self.tilemap = Tilemap(self,tile_size=16)

    def run(self):

        while True:
            self.display.fill((14,219,248))
            
            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0)) # Update player variables
            self.player.render(self.display) # Render the player 

            print(self.tilemap.physics_rects_around(self.player.pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

            self.clock.tick(60)

    
Game().run()
