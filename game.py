import pygame
import pytmx
import sys
from battle import Battle
from scenes import Map_Stage
from sprites import Player, Enemy, Object, Wizard, Warrior, Archer  # Cleaned up unused sprite imports for now
from loading import LoadingScreen

# Temporary test toggle: set to True to start directly on the battle screen.
TEST_BATTLE_ONLY = True


def run_game(user_info):
    # user_info is never actually used in this function, but it can be used to customize the game based on the user

    pygame.init()
    screen = pygame.display.set_mode((896, 640))
    pygame.display.set_caption("Game")
    
    # player1 = Warrior((stage1.entry_x_range[0] + stage1.entry_x_range[1]) // 2, (stage1.entry_y_range[0] + stage1.entry_y_range[1]) // 2) 
    player1 = Warrior(0, 0) # placeholder for player initialization, will be set to entry point of each level during transitions
    
    enemy1 = Enemy(400, 300) # placeholder for enemy initialization, will be set based on each level's design and enemy placements in the future

    # stage1 = Map_Stage("maps/1_level_map.tmx", entry_x_range=[0, 96], entry_y_range=[224, 288], exit_x_range=[832, 928], exit_y_range=[480, 544])
    stage1 = Map_Stage("maps/1_level_map.tmx", player1, screen, enemy=None) # placeholder for multiple levels/players
    stage2 = Map_Stage("maps/2_level_map.tmx", player1, screen, enemy=None) # placeholder for multiple levels/players
    stage3 = Map_Stage("maps/3_battle_map.tmx", player1, screen, enemy=enemy1) # placeholder for battle map, will be used for combat encounters with enemies in the future
    stage4 = Map_Stage("maps/4_level_map.tmx", player1, screen, enemy=None)
    stage5 = Map_Stage("maps/5_level_map.tmx", player1, screen, enemy=None)
    #level3 = 
    phealth_meter = pygame.image.load("game_assets/Player HP bar PNG.png") # placeholder for health meter, will be used to display player health during combat encounters in the future
    #phealth_meter = pygame.transform.scale(phealth_meter, (440, 150))
    #stage3 = Battle(player1, enemy1, screen) # placeholder for battle map, will be used for combat encounters with enemies in the future

    ehealth_meter = pygame.image.load("game_assets/Enemy HP bar PNG.png") # placeholder for enemy health meter, will be used to display enemy health during combat encounters in the future
    ehealth_meter = pygame.transform.scale(ehealth_meter, (440, 148))
    #**player and enemy health meters will be slighly different in desigh**
    
    if TEST_BATTLE_ONLY:
        current_scrn = stage3
        maps_list = [stage3]
        stages_list = [stage3]
        battles_list = [stage3]
        level_surface, tmx_data = current_scrn.load_level()
    else:
        current_scrn = stage1
        maps_list = [stage1, stage2, stage3, stage5]
        stages_list = [stage1, stage2, stage3, stage5]
        battles_list = [stage3]
        level_surface, tmx_data = stage1.load_level()

    
    clock = pygame.time.Clock()
    
    

    gameActive = True
    logout_requested = False
    
    # Initialize loading screen
    loading_screen = LoadingScreen(screen_width=896, screen_height=640)
    
    # Transition variables
    is_transitioning = False
    transition_timer = 0
    transition_duration = 2.0  # 2 seconds for loading screen
    transition_signal_pending = None
    
    #collision_rect = player1.collision_rect
    battle_needs_reset = False
    
    #next_scrn = None
    #prev_scrn = menu_scrn
    
    player_positioned = False # flag to check if player has been positioned at the entry point of the current level
    teleporting_to = None # variable to track which level we're teleporting to for loading screen text

    pygame.mixer.music.load("game_assets/The Last Encounter Collection/The Last Encounter (90s RPG Version) Full Loop.wav")
    pygame.mixer.music.play(loops=0)

    while gameActive:
        # 1. DELTA TIME CALCULATION (Fixed)
        # clock.tick(60) limits the framerate AND returns the milliseconds since the last frame.
        # Dividing by 1000.0 converts it to seconds for smooth, frame-independent movement.
        dt = clock.tick(60) / 1000.0

        # Reset battle state whenever a battle screen is entered during a transition.
        if battle_needs_reset and current_scrn in battles_list:
            current_scrn.current_battle.reset_battle()
            battle_needs_reset = False

        # 2. EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameActive = False

            elif event.type == pygame.KEYDOWN:
                # Ctrl + L to log out
                if event.key == pygame.K_l and (event.mod & pygame.KMOD_CTRL):
                    logout_requested = True
                    gameActive = False

            if current_scrn in battles_list:

                current_scrn.current_battle.handle_event(event) # placeholder for battle system event handling, will be used for combat encounters with enemies in the future

                
                
            
            
        # Position player at entry point if not already positioned (e.g., after a level transition)
        if not player_positioned and current_scrn in maps_list:
            
            if teleporting_to == "next level" or teleporting_to is None: # default to next level teleportation for the first level, can be adjusted as needed
                if current_scrn.entry_portal:
                    portal_center = current_scrn.entry_portal.rect.center
                # Center the player's collision_rect (feet hitbox) on the portal
                # collision_rect is 20x12 with midbottom = rect.midbottom
                # collision_rect.center offset from rect.topleft is (rect.width/2, rect.height - collision_rect.height/2)
                    player1.x = portal_center[0] - player1.rect.width / 2
                    player1.y = portal_center[1] - (player1.rect.height - player1.collision_rect.height / 2)
                    player_positioned = True

            elif teleporting_to == "previous level":
                if current_scrn.exit_portal:
                    portal_center = current_scrn.exit_portal.rect.center
                    player1.x = portal_center[0] - player1.rect.width / 2
                    player1.y = portal_center[1] - (player1.rect.height - player1.collision_rect.height / 2)
                    player_positioned = True

        # 3. TRANSITION HANDLING
        if is_transitioning:
            transition_timer += dt
            
            # Display loading screen
            loading_screen.render(screen, transition_timer)
            pygame.display.update()
            
            # Check if transition is complete
            if transition_timer >= transition_duration:
                is_transitioning = False
                transition_timer = 0
                
                # Handle the actual level transition based on pending signal
                if transition_signal_pending == "transition_to_next":
                    print("Loaded next level")
                    # TODO: Implement level switching when you have multiple levels
                    player_positioned = False # reset player positioned flag for the new level
                    teleporting_to = "next level"

                    for i in range(len(maps_list)):
                        if maps_list[i] == current_scrn and i < len(maps_list) - 1:
                            current_scrn = maps_list[i + 1]
                            battle_needs_reset = (current_scrn in battles_list)
                            break

                    level_surface, tmx_data = current_scrn.load_level()
                    
                    # player1.x, player1.y = 100, 100  # Reset to entry point
                    # player1.on_portal_timer = 0
                    
                elif transition_signal_pending == "transition_to_previous":
                    print("Loaded previous level")
                    # TODO: Implement level switching when you have multiple levels
                    player_positioned = False # reset player positioned flag for the new level
                    teleporting_to = "previous level"

                    for i in range(len(maps_list)):
                        if maps_list[i] == current_scrn and i > 0:
                            current_scrn = maps_list[i - 1]
                            battle_needs_reset = (current_scrn in battles_list)
                            break

                    level_surface, tmx_data = current_scrn.load_level()

                    # player1.x, player1.y = 100, 100  # Reset to entry point
                    # player1.on_portal_timer = 0
                
                transition_signal_pending = None
            continue  # Skip to next frame during transition

        # 4. GAME LOGIC UPDATES
        # Disable player movement on battle maps so combat stays turn-based.
        player1.movement_enabled = not (current_scrn in battles_list)

        if current_scrn in maps_list:
            collision_rect, transition_signal = player1.update(dt, tmx_data, current_scrn) 

            # Handle level transitions based on the signal from the player update
            if transition_signal == "transition_to_next":
                print("Transitioning to next level...")
                is_transitioning = True
                transition_timer = 0
                transition_signal_pending = "transition_to_next"
                player1.on_portal_timer = 0  # Reset portal timer

            elif transition_signal == "transition_to_previous":
                print("Transitioning to previous level...")
                is_transitioning = True
                transition_timer = 0
                transition_signal_pending = "transition_to_previous"
                player1.on_portal_timer = 0  # Reset portal timer
        
        # 5. DRAWING / RENDERING (only if not transitioning)
        screen.blit(level_surface, (0, 0)) 
        
        # Debugging collision rect
        pygame.draw.rect(screen, (0, 255, 0), collision_rect, 2) 
        screen.blit(player1.image, player1.rect)

        if current_scrn in battles_list:
            screen.blit(phealth_meter, (10, 10)) # placeholder for health meter drawing, will be used to display player health during combat encounters in the future
            screen.blit(ehealth_meter, (screen.get_width() - ehealth_meter.get_width() - 10, -28)) # keep both bars aligned at the same top edge
            current_scrn.current_battle.update(dt) # placeholder for battle system updates, will be used for combat encounters with enemies in the future
            current_scrn.current_battle.draw(screen) # placeholder for battle system drawing, will be used for combat encounters with enemies in the future
    
        pygame.display.update()

    pygame.quit()
    return logout_requested