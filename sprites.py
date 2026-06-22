import pygame
import pytmx
import sys
import game
# def walking():
#     pass

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
        self.col_positions, self.col_widths = self._find_nontransparent_spans(axis='x')
        self.row_positions, self.row_heights = self._find_nontransparent_spans(axis='y')

    def _find_nontransparent_spans(self, axis):
        
        if axis == 'x':
            length = self.sheet.get_width()
            other = self.sheet.get_height()
            get_pixel = lambda i, j: self.sheet.get_at((i, j)).a
        
        else:
            length = self.sheet.get_height()
            other = self.sheet.get_width()
            get_pixel = lambda i, j: self.sheet.get_at((j, i)).a

        positions = []
        sizes = []
        in_span = False
        span_start = 0
        threshold = 0.05

        for i in range(length):
            opaque_count = 0

            for j in range(other):

                if get_pixel(i, j) != 0:
                    opaque_count += 1

            transparent_line = (opaque_count / other) < threshold

            if not transparent_line:
                if not in_span:
                    in_span = True
                    span_start = i
            else:
                if in_span:
                    positions.append(span_start)
                    sizes.append(i - span_start)
                    in_span = False

        if in_span:
            positions.append(span_start)
            sizes.append(length - span_start)

        return positions, sizes

    def get_image(self, frame, scale):
        frame_x, frame_y = frame
        frame_x = int(frame_x)
        frame_y = int(frame_y)

        if frame_x >= len(self.col_positions) or frame_y >= len(self.row_positions):
            raise IndexError(f"Frame index out of range: {frame} on sheet size {len(self.col_positions)}x{len(self.row_positions)}")

        x = self.col_positions[frame_x]
        frame_width = self.col_widths[frame_x]
        y = self.row_positions[frame_y]
        frame_height = self.row_heights[frame_y]

        image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        image.fill((0, 0, 0, 0))
        image.blit(self.sheet, (0, 0), (x, y, frame_width, frame_height))

        image = pygame.transform.scale(image, (frame_width * scale, frame_height * scale))
        return image

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.images = {}
        #convert_alpha() is used to optimize the image for faster blitting, it also allows for transparency in the image
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA) #might not be necessary, but could be a pfp (?) or a default image for the player

        self.rect = self.image.get_rect(topleft=(x, y)) #will be modified as needed, #collision detection
        self.partial_rect = pygame.Rect(0, 0, self.rect.width, 15) #used for more precise collision detection, will be modified as needed
        self.partial_rect.midbottom = self.rect.midbottom
        
        self.x = x
        self.y = y
        self.state = "idle"
        self.direction = "right"
        #self.velocity = pygame.math.Vector2(0, 0)

        # self.collision_rect = pygame.Rect(0, 0, 20, 12) #used for feet hit box, will be modified as needed
        # self.collision_rect.midbottom = self.rect.midbottom

        #see what the purposes of the below attributes are
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.loop_animations = True

        self.animation_finished = False

        self.reg_animation_locked = False

        self.previous_state = self.state
        self.previous_direction = self.direction

        # self.movement_enabled = True

        # self.on_portal_timer = 0  # Time spent on current portal
        # self.current_portal = None  # Which portal player is on
        # self.portal_threshold = 3.0  # 3 seconds in seconds

        self.health = 2000
        self.energy = 0 #might need to adjust the initial energy value
        self.percent_impact = 0.9 #might need to adjust the initial impact value

    def load_animations(self, cols, scale):
        
        for state in self.animations:

            self.images[state] = {}
            for direction in self.animations[state]:
                self.images[state][direction] = []

                for frame in self.animations[state][direction]:

                    if "left" in direction:
                        sheet = self.left_spritesheet
                    else:
                        sheet = self.right_spritesheet

                    frame_x = frame % cols
                    frame_y = frame // cols

                    image = sheet.get_image(
                        (frame_x, frame_y),
                        scale
                    )

                    self.images[state][direction].append(image)


    def update(self, dt, tmx_data, current_map): #work on this function next
        
        #if current_map in maps_list:
            #self.movement_enabled = False
            
        #moving, collision_rect, transition_signal = self.move(current_map, dt) #move the player and check if they are moving or not, this will be used to determine the animation state
        
        # Animation state
        # if moving:
        #     self.state = "walk"
        # else:
        #     self.state = "idle"

        self.rect.topleft = (self.x, self.y)

        if self.state != self.previous_state or self.direction != self.previous_direction:
            self.frame_index = 0
            self.previous_state = self.state
            self.previous_direction = self.direction

        self.animate(dt)

        #return collision_rect, transition_signal #returning the collision rect for debugging purposes, will be removed later on

    def animate(self, dt):

        animation_list = self.images[self.state].get(self.direction)
        if not animation_list:
            return

        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:

            self.animation_timer = 0

            self.frame_index += 1

            if self.frame_index >= len(animation_list):

                if self.loop_animations:
                    self.frame_index = 0
                else:
                    self.frame_index = len(animation_list) - 1
                    self.animation_finished = True

        # Preserve the player's feet position when changing frame so
        # sprite size changes don't teleport the collision rect.
        midbottom = self.rect.midbottom
        if self.frame_index >= len(animation_list):
            self.frame_index = 0
        self.image = animation_list[self.frame_index]
        self.rect = self.image.get_rect(midbottom=midbottom)
        # Keep self.x/self.y consistent with the rect used for movement
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # self.images = {}
        # #convert_alpha() is used to optimize the image for faster blitting, it also allows for transparency in the image
        # self.image = pygame.Surface((32, 32), pygame.SRCALPHA) #might not be necessary, but could be a pfp (?) or a default image for the player

        # self.rect = self.image.get_rect(topleft=(x, y)) #will be modified as needed, #collision detection
        # self.partial_rect = pygame.Rect(0, 0, self.rect.width, 15) #used for more precise collision detection, will be modified as needed
        # self.partial_rect.midbottom = self.rect.midbottom
        
        # self.x = x
        # self.y = y
        # self.state = "idle"
        # self.direction = "right"
        self.velocity = pygame.math.Vector2(0, 0)

        self.collision_rect = pygame.Rect(0, 0, 20, 12) #used for feet hit box, will be modified as needed
        self.collision_rect.midbottom = self.rect.midbottom

        #see what the purposes of the below attributes are
        # self.frame_index = 0
        # self.animation_speed = 0.1
        # self.animation_timer = 0

        # self.previous_state = self.state
        # self.previous_direction = self.direction

        self.movement_enabled = True

        self.on_portal_timer = 0  # Time spent on current portal
        self.current_portal = None  # Which portal player is on
        self.portal_threshold = 3.0  # 3 seconds in seconds

        # self.health = 2000
        # self.energy = 0 #might need to adjust the initial energy value
        # self.percent_impact = 0.9 #might need to adjust the initial impact value


    # def load_animations(self, cols, scale):
        
    #     for state in self.animations:

    #         self.images[state] = {}
    #         for direction in self.animations[state]:
    #             self.images[state][direction] = []

    #             for frame in self.animations[state][direction]:

    #                 if "left" in direction:
    #                     sheet = self.left_spritesheet
    #                 else:
    #                     sheet = self.right_spritesheet

    #                 frame_x = frame % cols
    #                 frame_y = frame // cols

    #                 image = sheet.get_image(
    #                     (frame_x, frame_y),
    #                     scale
    #                 )

    #                 self.images[state][direction].append(image)

    def update(self, dt, tmx_data, current_map): #work on this function next
        
        #if current_map in maps_list:
            #self.movement_enabled = False
            
        moving, collision_rect, transition_signal = self.move(current_map, dt) #move the player and check if they are moving or not, this will be used to determine the animation state
        
        # Animation state
        if not self.reg_animation_locked:
            if moving:
                self.state = "walk"
            else:
                self.state = "idle"

        self.rect.topleft = (self.x, self.y)

        if self.state != self.previous_state or self.direction != self.previous_direction:
            self.frame_index = 0
            self.previous_state = self.state
            self.previous_direction = self.direction

        self.animate(dt)

        return collision_rect, transition_signal #returning the collision rect for debugging purposes, will be removed later on

    def move(self, current_scrn, dt):
        self.velocity = pygame.math.Vector2(0, 0)
        transition_signal = None  # Initialize transition signal

        keys = pygame.key.get_pressed()

        moving = False

        tmx_data = current_scrn.tmx_data

        boundaries = []
        obj_layer = tmx_data.get_layer_by_name("Boundaries")

        for obj in obj_layer:
            boundaries.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        #self.collision_rect.midbottom = self.rect.midbottom #sync the collision rect with the player's position
        self.rect.midbottom = self.collision_rect.midbottom #sync the player's rect with the collision rect, this will allow for more precise collision detection without affecting the player's position when changing animations with different sprite sizes

        # Portal collision detection (remove the idle/direction requirements)
        if current_scrn.entry_portal and self.collision_rect.colliderect(current_scrn.entry_portal) and self.state == "idle" and self.direction == "left":
            if self.current_portal != "entry":
                self.current_portal = "entry"
                self.on_portal_timer = 0
                print("Entered entry portal")
            self.on_portal_timer += dt  # dt is delta time from game loop
            
            if self.on_portal_timer >= self.portal_threshold:
                transition_signal = "transition_to_previous"
                #print("Portal timer threshold reached, transitioning to previous level")
                #return "transition_to_previous"  # Signal to load previous level

        elif current_scrn.exit_portal and self.collision_rect.colliderect(current_scrn.exit_portal) and self.state == "idle" and self.direction == "right":
            if self.current_portal != "exit":
                self.current_portal = "exit"
                self.on_portal_timer = 0
                print("Entered exit portal")
            self.on_portal_timer += dt
            
            if self.on_portal_timer >= self.portal_threshold:
                transition_signal = "transition_to_next"
                #print("Portal timer threshold reached, transitioning to next level")
                #return "transition_to_next"  # Signal to load next level

        else:
            # Reset timer when leaving portal
            self.on_portal_timer = 0
            self.current_portal = None

        # if self.collision_rect.colliderect(current_scrn.entry_portal) and self.state == "idle" and self.direction == "left":
        #     print("Entered entry portal")
        #     # previous level

        # elif self.collision_rect.colliderect(current_scrn.exit_portal) and self.state == "idle" and self.direction == "right":
        #     print("Entered exit portal")
        #     # next level

        # need to figure out how to access entry_ and exit_portal for each map, since they will be different for each map, maybe they can be attributes of the Map_Stage class and passed into the player update function as needed?

        #if self.x >= '''???''' and '''???''' <= self.y <= '''???''':
            # next_level() - figure out where (which file) to create this function
            #pass

        #write code here (setting velocity to 0 if colliding with a boundary)
        # if self.rect.collidelist(boundaries):
        #     self.velocity = pygame.math.Vector2(0, 0)
        
        #later on:
        #check collisions with boundaries and adjust velocity accordingly, this will allow for smoother movement along walls and corners
        
        # LEFT
        if self.movement_enabled:
            if keys[pygame.K_LEFT]:
                self.velocity.x -= 1
                #self.velocity += pygame.math.Vector2(-1, 0)
                #self.x -= 3
                self.direction = "left"
                moving = True

            # RIGHT
            if keys[pygame.K_RIGHT]:
                self.velocity.x += 1
                #self.velocity += pygame.math.Vector2(1, 0)
                #self.x += 3
                self.direction = "right"
                moving = True

            # UP
            if keys[pygame.K_UP]:
                self.velocity.y -= 1
                #self.velocity += pygame.math.Vector2(0, -1)
                #self.y -= 3
                self.direction = "up"
                moving = True

            # DOWN
            if keys[pygame.K_DOWN]:
                self.velocity.y += 1
                #self.velocity += pygame.math.Vector2(0, 1)
                #self.y += 3
                self.direction = "down"
                moving = True
        
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() # Normalize to maintain consistent speed in all directions

        speed = 3

        can_move_x = True
        can_move_y = True

        if self.velocity.x != 0:
            test_rect = self.collision_rect.move(self.velocity.x * speed, 0)
            for boundary in boundaries:
                if test_rect.colliderect(boundary):
                    can_move_x = False
                    break

        if self.velocity.y != 0:
            test_rect = self.collision_rect.move(0, self.velocity.y * speed)
            for boundary in boundaries:
                if test_rect.colliderect(boundary):
                    can_move_y = False
                    break

        if self.velocity.x != 0 and self.velocity.y != 0 and not can_move_x and can_move_y:
            # If moving diagonally into a tight opening, try the vertical move first.
            self.y += self.velocity.y * speed
            self.rect.y = round(self.y)
            self.collision_rect.midbottom = self.rect.midbottom

            test_rect = self.collision_rect.move(self.velocity.x * speed, 0)
            can_move_x = True
            for boundary in boundaries:
                if test_rect.colliderect(boundary):
                    can_move_x = False
                    break

            if can_move_x:
                self.x += self.velocity.x * speed
                self.rect.x = round(self.x)
        else:
            if can_move_x:
                self.x += self.velocity.x * speed
                self.rect.x = round(self.x)

            self.collision_rect.midbottom = self.rect.midbottom #sync the collision rect with the player's position after horizontal movement

            if can_move_y:
                self.y += self.velocity.y * speed
                self.rect.y = round(self.y)

        self.collision_rect.midbottom = self.rect.midbottom #sync the collision rect with the player's position after vertical movement
        
        #ONE BUG - one point in the map has a collision rect but the player is able to go right through (top branch path)

        
        # ---------------- HORIZONTAL ----------------

        # old_x = self.x

        # self.x += self.velocity.x * speed
        # self.rect.x = round(self.x)

        # collision_rect = pygame.Rect(
        #     self.rect.x + 10,
        #     self.rect.bottom - 12,
        #     self.rect.width - 20,
        #     12
        # )

        # for boundary in boundaries:
        #     if collision_rect.colliderect(boundary):

        #         self.x = old_x
        #         self.rect.x = round(self.x)

        #         break


        # # ---------------- VERTICAL ----------------

        # old_y = self.y

        # self.y += self.velocity.y * speed
        # self.rect.y = round(self.y)

        # collision_rect = pygame.Rect(
        #     self.rect.x + 10,
        #     self.rect.bottom - 12,
        #     self.rect.width - 20,
        #     12
        # )

        # for boundary in boundaries:
        #     if collision_rect.colliderect(boundary):

        #         self.y = old_y
        #         self.rect.y = round(self.y)

        #         break
        
        return moving, self.collision_rect, transition_signal #returning the collision rect for debugging purposes, will be removed later on
        #pygame.draw.rect(game.screen, (0, 255, 0), collision_rect, 2)

        # # ---------- HORIZONTAL ----------
        # self.x += self.velocity.x * speed
        # self.rect.x = round(self.x)

        # for boundary in boundaries:
        #     if self.rect.colliderect(boundary):

        #         # moving right
        #         if self.velocity.x > 0:
        #             self.rect.right = boundary.left

        #         # moving left
        #         elif self.velocity.x < 0:
        #             self.rect.left = boundary.right

        #         # sync float position
        #         self.x = self.rect.x


        # # ---------- VERTICAL ----------
        # self.y += self.velocity.y * speed
        # self.rect.y = round(self.y)

        # for boundary in boundaries:
        #     if self.rect.colliderect(boundary):

        #         # moving down
        #         if self.velocity.y > 0:
        #             self.rect.bottom = boundary.top

        #         # moving up
        #         elif self.velocity.y < 0:
        #             self.rect.top = boundary.bottom

        #         # sync float position
        #         self.y = self.rect.y

        # SECOND IMPLEMENTATION (sliding along walls, no more movement reverting, will be modified later on for more complex collision shapes and multiple types of boundaries)
        # # Test horizontal movement
        # test_rect = self.rect.move(self.velocity.x * speed, 0)
        # horiz_hit = test_rect.collidelist(boundaries)
        
        # # Allow horizontal movement unless moving into a vertical wall
        # allow_horiz = True
        # if horiz_hit != -1 and self.velocity.x != 0:
        #     boundary = boundaries[horiz_hit]
        #     # Only block if boundary is a vertical wall (taller than wide)
        #     # Floors (wider than tall) don't block horizontal movement
        #     if boundary.height > boundary.width:
        #         # It's a wall; check if moving into it
        #         if self.velocity.x > 0 and test_rect.right > boundary.left:
        #             # Moving right into wall's left edge
        #             allow_horiz = False
        #         elif self.velocity.x < 0 and test_rect.left < boundary.right:
        #             # Moving left into wall's right edge
        #             allow_horiz = False
        
        # if allow_horiz:
        #     self.x += self.velocity.x * speed
        #     self.rect.x = round(self.x)
        
        # # Test vertical movement
        # test_rect = self.rect.move(0, self.velocity.y * speed)
        # vert_hit = test_rect.collidelist(boundaries)
        
        # # Allow vertical movement unless moving into a horizontal floor
        # allow_vert = True
        # if vert_hit != -1 and self.velocity.y != 0:
        #     boundary = boundaries[vert_hit]
        #     # Only block if boundary is a horizontal floor (wider than tall)
        #     # Walls (taller than wide) don't block vertical movement
        #     if boundary.width > boundary.height:
        #         # It's a floor; check if moving into it
        #         if self.velocity.y > 0 and test_rect.bottom > boundary.top:
        #             # Moving down into floor's top edge
        #             allow_vert = False
        #         elif self.velocity.y < 0 and test_rect.top < boundary.bottom:
        #             # Moving up into floor's bottom edge
        #             allow_vert = False
        
        # if allow_vert:
        #     self.y += self.velocity.y * speed
        #     self.rect.y = round(self.y)

        #INITIAL IMPLEMENTATION (no sliding along walls, will be modified later on)
        # rect_temp = self.partial_rect.move(self.velocity * speed)
       
        # if rect_temp.collidelist(boundaries) != -1:
        #     self.velocity = pygame.math.Vector2(0, 0)
        # else:
        #     self.x += self.velocity.x * speed
        #     self.y += self.velocity.y * speed
        #     self.rect.topleft = (self.x, self.y)
        #     self.partial_rect.midbottom = self.rect.midbottom

        #HORIZONTAL MOVEMENT AND COLLISION CHECK
        # if self.velocity.x != 0:
        #     self.x += self.velocity.x * speed
        #     self.rect.x = round(self.x)

        #     #self.rect.topleft = (self.x, self.y)

        #     #Next: IMPLEMENT this new function below - do not need midbottom and movement reverting anymore
        #     rect_temp = self.rect.move(self.velocity * speed)
        #     if rect_temp.collidelist(boundaries) != -1:


        #     self.partial_rect.midbottom = self.rect.midbottom

        #     # Check if horizontal move caused a collision
        #     hit = self.partial_rect.collidelist(boundaries)
            
        #     if hit != -1: # -1 means no collision
        #         # Collision found! Undo the movement on the X axis
        #         self.x -= self.velocity.x * speed
        #         self.rect.x = round(self.x)
        #         self.partial_rect.midbottom = self.rect.midbottom
        #         self.velocity.x = 0

        # #VERTICAL MOVEMENT AND COLLISION CHECK
        # if self.velocity.y != 0:
        #     self.y += self.velocity.y * speed
        #     self.rect.y = round(self.y)
            
        #     self.partial_rect.midbottom = self.rect.midbottom

        #     # Check if vertical move caused a collision
        #     hit = self.partial_rect.collidelist(boundaries)
        #     if hit != -1:
        #         # Collision found! Undo the movement on the Y axis
        #         self.y -= self.velocity.y * speed
        #         self.rect.y = round(self.y)
        #         self.partial_rect.midbottom = self.rect.midbottom
        #         self.velocity.y = 0

        # # Final pass: Make sure feet are perfectly snapped to the final position
        # self.partial_rect.midbottom = self.rect.midbottom
        
        #self.rect.topleft = (self.x, self.y)

        #return moving

    # def animate(self, dt):

    #     animation_list = self.images[self.state].get(self.direction)
    #     if not animation_list:
    #         return

    #     self.animation_timer += dt

    #     if self.animation_timer >= self.animation_speed:

    #         self.animation_timer = 0

    #         self.frame_index += 1

    #         if self.frame_index >= len(animation_list):
    #             self.frame_index = 0

    #     # Preserve the player's feet position when changing frame so
    #     # sprite size changes don't teleport the collision rect.
    #     midbottom = self.rect.midbottom
    #     if self.frame_index >= len(animation_list):
    #         self.frame_index = 0
    #     self.image = animation_list[self.frame_index]
    #     self.rect = self.image.get_rect(midbottom=midbottom)
    #     # Keep self.x/self.y consistent with the rect used for movement
    #     self.x = float(self.rect.x)
    #     self.y = float(self.rect.y)
    
class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        #convert_alpha() is used to optimize the image for faster blitting, it also allows for transparency in the image
        # self.images = {}
        # self.image = pygame.Surface((32, 32), pygame.SRCALPHA) #might not be necessary, but could be a default image for the enemy
        # self.rect = self.image.get_rect(topleft=(x, y)) #will be modified as needed, #collision detection
        # self.x = x
        # self.y = y

        # self.state = "idle"
        # self.direction = "right"

        # self.frame_index = 0
        # self.animation_speed = 0.1
        # self.animation_timer = 0

        # self.previous_state = self.state
        # self.previous_direction = self.direction
        
    #def update(self, dt): #work on this function next
        
        #moving, collision_rect, transition_signal = self.move(current_map, dt) #move the player and check if they are moving or not, this will be used to determine the animation state
        
        # Animation state
        # if moving:
        #     self.state = "walk"
        # else:
        #     self.state = "idle"

        # self.rect.topleft = (self.x, self.y)

        # if self.state != self.previous_state or self.direction != self.previous_direction:
        #     self.frame_index = 0
        #     self.previous_state = self.state
        #     self.previous_direction = self.direction

        # self.animate(dt)

        #return collision_rect, transition_signal #returning the collision rect for debugging purposes, will be removed later on

    # def load_animations(self, cols, scale):
        
    #     for state in self.animations:

    #         self.images[state] = {}
    #         for direction in self.animations[state]:
    #             self.images[state][direction] = []

    #             for frame in self.animations[state][direction]:

    #                 if "left" in direction:
    #                     sheet = self.left_spritesheet
    #                 else:
    #                     sheet = self.right_spritesheet

    #                 frame_x = frame % cols
    #                 frame_y = frame // cols

    #                 image = sheet.get_image(
    #                     (frame_x, frame_y),
    #                     scale
    #                 )

    #                 self.images[state][direction].append(image)

    # def animate(self, dt):

    #     animation_list = self.images[self.state].get(self.direction)
    #     if not animation_list:
    #         return

    #     self.animation_timer += dt

    #     if self.animation_timer >= self.animation_speed:

    #         self.animation_timer = 0

    #         self.frame_index += 1

    #         if self.frame_index >= len(animation_list):
    #             self.frame_index = 0

    #     # Preserve the player's feet position when changing frame so
    #     # sprite size changes don't teleport the collision rect.
    #     midbottom = self.rect.midbottom
    #     if self.frame_index >= len(animation_list):
    #         self.frame_index = 0
    #     self.image = animation_list[self.frame_index]
    #     self.rect = self.image.get_rect(midbottom=midbottom)
    #     # Keep self.x/self.y consistent with the rect used for movement
    #     self.x = float(self.rect.x)
    #     self.y = float(self.rect.y)
    

class Object(pygame.sprite.Sprite): #might need a Projectile class, Object class might not be necessary
    def __init__(self, x, y):
        super().__init__()
        #convert_alpha() is used to optimize the image for faster blitting, it also allows for transparency in the image
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA) #might not be necessary, but could be a default image for the object
        self.rect = self.image.get_rect(topleft=(x, y)) #will be modified as needed, #collision detection
        self.x = x
        self.y = y

class Wizard(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        #add wizard specific attributes here
        self.animations = animations["wizard"]
        
        self.left_spritesheet = SpriteSheet(pygame.image.load("game_assets/wizard_left.png").convert_alpha())
        self.right_spritesheet = SpriteSheet(pygame.image.load("game_assets/wizard_right.png").convert_alpha())

        self.load_animations(cols=14, scale=2)

        self.image = self.images["idle"]["right"][0] # Set initial image to the first frame of the idle right animation
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

class Warrior(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        #add warrior specific attributes here
        self.animations = animations["warrior"]
        
        self.left_spritesheet = SpriteSheet(pygame.image.load("game_assets/warrior_left.png").convert_alpha())
        self.right_spritesheet = SpriteSheet(pygame.image.load("game_assets/warrior_right.png").convert_alpha())

        self.load_animations(cols=14, scale=2)

        self.image = self.images["idle"]["right"][0] # Set initial image to the first frame of the idle right animation
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

class Archer(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        #add archer specific attributes here
        self.animations = animations["archer"]
        
        self.left_spritesheet = SpriteSheet(pygame.image.load("game_assets/archer_left.png").convert_alpha())
        self.right_spritesheet = SpriteSheet(pygame.image.load("game_assets/archer_right.png").convert_alpha())

        self.load_animations(cols=14, scale=2)

        self.image = self.images["idle"]["right"][0] # Set initial image to the first frame of the idle right animation
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

#see if animations also must exist as a master dict, delete otherwise

class Portal(Object):
    def __init__(self, x, y, rect):
        super().__init__(x, y)
        #add portal specific attributes here
        #self.image = extract the portal image from the tileset
        self.rect = rect #will be modified as needed, #collision detection
        self.target = None #target is the portal that this portal leads to, this will be used to determine the player's new position when transitioning between levels
        

#each portal object will have its specific rect for collision detection (as generated by Tiled), 
# but the player will also have a reference to the entry and exit portal rects for the current map, which will be used to check for level transitions in the player update function
#portal objects will have a target attribute specifying the target portal that it leads to, which will be used to determine the player's new position when transitioning between levels

#figure out a way to organize the up_left and up_right animations
#need to fix the wizard animation for idle right facing (looks like the sprite is moving when in an idle state)
#need to fix the wizard animation for movement up and down
animations = {
    "wizard": {
        "walk": {
            "left": [0, 1, 2, 3, 4, 5], #from wizard_left.png
            "right": [8, 9, 10, 11, 12, 13], #from wizard_right.png
            "up_left": [10, 11, 12, 13], #from wizard_left.png
            "up_right": [0, 1, 2, 3], #from wizard_right.png
            "down_left": [0, 1, 2, 3, 4, 5], #from wizard_left.png
            "down_right": [8, 9, 10, 11, 12, 13], #from wizard_right.png
        },
        "idle": {
            "left": [6, 7, 8, 9], #from wizard_left.png
            "right": [4, 5, 6, 7], #from wizard_right.png
            "up_left": [10, 11, 12, 13], #from wizard_left.png
            "up_right": [0, 1, 2, 3], #from wizard_right.png
            "down_left": [8, 13, 10, 9, 12, 11, 12, 9, 10, 13, 8], #from wizard_right.png
            "down_right": [5, 0, 3, 4, 1, 2, 1, 4, 3, 0, 5], #from wizard_left.png
        },
        "attack": {
            "left": [20, 19, 18, 21], #from wizard_right.png
            "right": [21, 22, 23, 20], #from wizard_left.png
            "up_left": [14, 15, 16, 17], #from wizard_right.png
            "up_right": [24, 25, 26, 27], #from wizard_left.png
            "down_left": [20, 19, 18, 21], #from wizard_right.png
            "down_right": [21, 22, 23, 20], #from wizard_left.png
        },
    },
    "warrior": {
        "walk": {
            "left": [24, 25], #from warrior_left.png
            "right": [16, 17], #from warrior_right.png
            "up": [27], #from warrior_left.png
            #"up_left": [],
            #"up_right": [],
            "down": [13], #from warrior_left.png
            # "down_left": [],
            # "down_right": [],
        },
        "idle": {
            "left": [5, 6, 19, 20], #from warrior_left.png
            "right": [7, 8, 21, 22], #from warrior_right.png
            "up": [27], #from warrior_left.png
            "down": [23], #from warrior_left.png
        },
        "attack": {
            "left": [10, 25, 24, 23],
            "right": [3, 16, 17, 18],
            #"up": [],
            #"down": [],
        },
    },
    "archer": {
        "walk": {
            "left": [21, 22, 23], #from archer_left.png
            "right": [18, 19, 20], #from archer_right.png
            "up": [25, 26, 27], #from archer_left.png
            "down": [12, 13], #from archer_left.png
        },
        "idle": {
            "left": [10, 11], #from archer_left.png
            "right": [2, 3], #from archer_right.png
            "up_left": [24], #from archer_left.png
            "up_right": [17], #from archer_right.png
            "down_left": [10, 11], #from archer_left.png
            "down_right": [2, 3], #from archer_right.png
        },
        "attack": {
            "left": [0, 1, 2, 3, 4, 5, 6], #from archer_left.png
            "right": [13, 12, 11, 10, 9, 8, 7], #from archer_right.png
            #"up": [],
            #"down": [],
        },
    },
}