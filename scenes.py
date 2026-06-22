import pygame
import pytmx
import sys

from battle import Battle
from sprites import Portal

# stage1_surf = pygame.Surface((900, 600))
# stage1_surf = stage1_surf.convert_alpha()
# tmx_data = pytmx.load_pygame("1_level_map.tmx")

class Map_Stage:

    def __init__(self, map_file, player, screen, enemy):
        self.tmx_data = pytmx.load_pygame(map_file)
        self.level_surface = None

        self.entry_portal = None
        self.exit_portal = None

        if enemy is not None:
            self.current_battle = Battle(player, enemy, screen) # placeholder for battle system, will be used for combat encounters with enemies in the future

        self.load_endpoints()
        self.load_obj_layers(screen)
        #below attributes need to be initialized based on each map
        # self.entry_x_range = entry_x_range
        # self.entry_y_range = entry_y_range
        # self.exit_x_range = exit_x_range
        # self.exit_y_range = exit_y_range

        # self.entry_portal = portal1
        # self.exit_portal = portal2
        
    def load_endpoints(self):
        
        portal_layer = self.tmx_data.get_layer_by_name("Portal_Rects")

        if portal_layer is not None:

            for obj in portal_layer:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

                portal = Portal(rect.x, rect.y, rect)

                if obj.name == "entry":
                    self.entry_portal = portal

                elif obj.name == "exit":
                    self.exit_portal = portal
        
            print(self.exit_portal)
            print(self.entry_portal)

        #do I need to return the entry and exit rects? Look into this later, maybe they can just be attributes of the Map_Stage class and accessed as needed
    
    def load_obj_layers(self, screen):
        covering_objs = self.tmx_data.get_layer_by_name("Covering_Tiles")

        if covering_objs is not None:

            for obj in covering_objs:
                obj_rect = obj.get_rect()
                screen.blit(obj, obj_rect)

    def load_level(self):

        #check dimensions of the map in Tiled (below line) - should be standard 900x600
        self.level_surface = pygame.Surface((self.tmx_data.width * self.tmx_data.tilewidth, self.tmx_data.height * self.tmx_data.tileheight))
        
        for layer in self.tmx_data.visible_layers:
            # Check if the layer contains actual tiles
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        # Calculate pixel position
                        pos_x = x * self.tmx_data.tilewidth
                        pos_y = y * self.tmx_data.tileheight
                        self.level_surface.blit(tile_image, (pos_x, pos_y))
            
        return self.level_surface, self.tmx_data #tmx_data is returned as a placeholder, see if this is actually needed later on