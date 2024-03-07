import pygame 



class PhysicsEntity: # Generic Physics Entity object

    def __init__(self,game, e_type, pos, size): # Initializes the entity object

        self.game = game
        self.type = e_type # Entity types will be Player, Enemies, NPCs
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = { 'up': False, 'down': False, 'right': False, 'left':False }

    def rect(self):  # Rect object creator for entity class

        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


    def update(self,tilemap, movement=(0, 0)): # Updates the entity movement

        self.collisions = { 'up': False, 'down': False, 'right': False, 'left':False }
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Pretty complex way to do object collisions, 
        # The physics entity looks in a 3x3 space around it for collision entities of interest 
        # in the tilemap, this is why keeping the tilemap as a dictionary is an advantage

        
        self.pos[0] += frame_movement[0] 
        
        entity_rect = self.rect()   # Responsible for snapping the entity object and the collider object
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left 
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True 
                
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                
                self.pos[1] = entity_rect.y

        if self.collisions['up'] or self.collisions['down']:

            self.velocity[1] = 0


    def render(self,surf, offset=(0, 0)): # Renders the entity on the screen

        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1] ))