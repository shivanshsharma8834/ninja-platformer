# Imported Main Game Libraries
import pygame
import sys

# Importing other scripts to the app
from scripts.entities import PhysicsEntity
from scripts.utils import *
from scripts.tilemap import Tilemap 
from scripts.clouds import Clouds

class Game: # Main game

    def __init__(self):

        pygame.init()

        pygame.display.set_caption('Ninja Game')

        self.screen = pygame.display.set_mode((640,480)) # Display Window

        self.display = pygame.Surface((320,240)) # Main background Context

        self.clock = pygame.time.Clock() # Update Clock

         

        self.movement = [False,False] # Movement flag vectors

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'clouds' : load_images('clouds'),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16 )

        self.player = PhysicsEntity(self, 'player',(50,50),(8,15))
        
        self.tilemap = Tilemap(self,tile_size=16)

        self.scroll = [0, 0]

    def run(self):

        while True: # Render tilemap, then player, then other objects 
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/ 2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height()/ 2 - self.scroll[1]) / 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll )

            self.tilemap.render(self.display, offset=render_scroll )

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0)) # Update player variables 
            self.player.render(self.display, offset=render_scroll ) # Render the player 

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
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3 # Temporary jump button

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # Scale the background surface to the window context, then blit it
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

            self.clock.tick(60)

    
Game().run()
