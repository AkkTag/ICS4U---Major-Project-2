import pygame

pygame.init()

from attacks import Attack
from sprites import Wizard, Warrior, Archer # Cleaned up unused sprite imports for now 
from question import QuestionScreen
import random

qa_options_list = [QuestionScreen("FAVOURITE ANIMAL?", [["A. LERNAEAN HYDRA", "REGENERATES HEADS"],
                                                      ["B. GRIFFIN", "HALF EAGLE, HALF LION"],
                                                      ["C. CHIMERA", "LION, GOAT, SNAKE PARTS"],
                                                      ["D. CERBERUS", "GUARD OF THE UNDERWORLD"]], 2),

                QuestionScreen("FAVOURITE GAME?", [["A. LERNAEAN Htrd", "REGENERATES HEADS"],
                                                      ["B. GRIFFIN", "HALF LION"],
                                                      ["C. gg", "LION, SNAKE PARTS"],
                                                      ["D. CC", "OF THE UNDERWORLD"]], 2),

                QuestionScreen("FAVOURITE SPORT?", [["A. SOCCER", "FOOTING"],
                                                      ["B. BASKETBALL", "EXPENSIVE BASKETS"],
                                                      ["C. CRICKET", "LION, WICKET OUT"],
                                                      ["D. BASEBALL", "HOME-RUN STEALERS"]], 1),

                ]
class Battle:
    def __init__(self, player, enemy, screen):
        self.player = player
        self.screen = screen #remove later, for debugging

        self.player_type = None

        if isinstance(self.player, Wizard):
            self.player_type = "Wizard"
        
        elif isinstance(self.player, Warrior):
            self.player_type = "Warrior"

        elif isinstance(self.player, Archer):
            self.player_type = "Archer"

        self.enemy = enemy
        self.battle_state = "DEFAULT"  # or "ENEMY_TURN", "VICTORY", "DEFEAT"
        
        self.intro_timer = 2.0  # 2 seconds for intro animation, can be used for other timed events in the battle system as well
        
        self.background_overlay = pygame.Surface((896, 640))
        self.background_overlay.fill((0, 0, 0))
        self.background_overlay.set_alpha(0)  # fully transparent initially

        self.attack_delay_timer = 0.0
        self.attack_delay_duration = 1.0
        self.attack_effect_applied = False
        self.overlay_alpha = 0
        #self.decision_active = False
        self.player_choice = None
        self.attack_choice = None

        self.decision_rect_1 = pygame.Rect(127, 227, 190, 190) # Attack image rect (37 + 90, 27 + 200, 190, 190)
        self.decision_rect_2 = pygame.Rect(347, 227, 190, 190) # Idle image rect (37 + 310, 27 + 200, 190, 190)
        self.decision_rect_3 = pygame.Rect(567, 227, 190, 190) # Run image rect (37 + 530, 27 + 200, 190, 190)
        
        
        decision_bg = pygame.image.load("game_assets/Battle - Player Decision Menu PNG.png").convert_alpha() # placeholder for decision menu, will be used to allow the player to choose their action during their turn in the future
        decision_bg = pygame.transform.scale(decision_bg, (821, 586)) # Scale the menu to fit the screen, adjust as needed

        decision_item1 = pygame.transform.scale(pygame.image.load("game_assets/Battle - Decision Menu - Attack 2 PNG.png").convert_alpha(), (190, 190)) # placeholder for attack option button, will be used to allow the player to choose their attack during their turn in the future
        decision_item2 = pygame.transform.scale(pygame.image.load("game_assets/Battle - Decision Menu - Idle 2 PNG.png").convert_alpha(), (190, 190)) # placeholder for defend option button, will be used to allow the player to choose their action during their turn in the future
        decision_item3 = pygame.transform.scale(pygame.image.load("game_assets/Battle - Decision Menu - Run 2 PNG.png").convert_alpha(), (190, 190)) # placeholder for item option button, will be used to allow the player to choose their action during their turn in the future

        self.decision_menu = pygame.Surface((821, 586), pygame.SRCALPHA) # Surface for the decision menu, allows for easier management of the menu and its components
        
        self.decision_menu.blit(decision_bg, (0, 0))
        self.decision_menu.blit(decision_item1, (90, 200)) # Position the attack option button on the decision menu, adjust as needed
        self.decision_menu.blit(decision_item2, (310, 200)) # Position the defend option button on the decision menu, adjust as needed
        self.decision_menu.blit(decision_item3, (530, 200)) # Position the item option button on the decision menu, adjust as needed

        # Rects for the follow-up attack menu shown after the player picks a decision.
        self.attchoice_rect_tl = pygame.Rect(128, 0, 320, 320)
        self.attchoice_rect_tr = pygame.Rect(448, 0, 320, 320)
        self.attchoice_rect_bl = pygame.Rect(128, 320, 320, 320)
        self.attchoice_rect_br = pygame.Rect(448, 320, 320, 320)


        self.attack_menu = None
        self.attoptions = None
        
        self.current_qa = qa_options_list[0]
        self.previous_qa = None

        self.exit_victor_button = pygame.Rect(0, 0, 10, 10)
        # if self.player.type == "Wizard":
        #     self.player_turn_menu = pygame.image.load("game_assets/Battle Attack Designs Wizard PNG.png").convert_alpha()

        # elif self.player.type == "Warrior":
        #     self.player_turn_menu = pygame.image.load("game_assets/Battle Attack Designs Warrior PNG.png").convert_alpha()
    
        # elif self.player.type == "Archer":
        #     self.player_turn_menu = pygame.image.load("game_assets/Battle Attack Designs Archer PNG.png").convert_alpha()

        attacks = {
            "Wizard": [Attack("Magic Forecast", 20, 5),
                       Attack("Wizard's Touch", 25, 10),
                       Attack("Stone Cold", 30, 15),
                       Attack("Wobble Gobble", 35, 20)],

            "Warrior": [Attack("Stardom Thunder", 20, 5),
                        Attack("War Machine", 25, 10),
                        Attack("Wax Cylinder", 30, 15),
                        Attack("Wrist Fist", 35, 20)],

            "Archer": [Attack("Golden Bowfire", 20, 5),
                       Attack("Bullet Beast", 25, 10),
                       Attack("Arch Pegasus", 30, 15),
                       Attack("Ranger Danger", 35, 20)]
        }

        menus = {
            "Wizard": "game_assets/Battle Attack Designs Wizard PNG.png",
            "Warrior": "game_assets/Battle Attack Designs Warrior PNG.png",
            "Archer": "game_assets/Battle Attack Designs Archer PNG.png"
        }

        if self.player_type == "Wizard":
            self.attack_menu = pygame.image.load(menus["Wizard"]).convert_alpha()
            self.attoptions = attacks["Wizard"]

        elif self.player_type == "Warrior":
            self.attack_menu = pygame.image.load(menus["Warrior"]).convert_alpha()
            self.attoptions = attacks["Warrior"]

        elif self.player_type == "Archer":
            self.attack_menu = pygame.image.load(menus["Archer"]).convert_alpha()
            self.attoptions = attacks["Archer"]

        self.attack_menu = pygame.transform.scale(self.attack_menu, (640, 640)) # Scale the menu to fit the screen, adjust as needed

    def reset_battle(self):
        """Reset the battle flow so the decision menu can appear again when re-entering this battle."""
        self.battle_state = "DEFAULT"
        self.intro_timer = 2.0
        self.overlay_alpha = 0
        self.background_overlay.set_alpha(0)
        self.attack_effect_applied = False
        self.player_choice = None
        self.attack_delay_timer = 0.0
        #self.decision_active = False

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        
        mouse_pos = pygame.mouse.get_pos()

        if self.battle_state == "QUESTION":
            result = self.current_qa.handle_event(event)
            
            if result is not None:

                action, value_index = result #value is an index of the selected answer in ans_options

                if action == "submit":

                    print("Answer submitted")

                    self.attack_delay_timer = 0.0
                    self.attack_effect_applied = False
                    self.player.state = "idle"
                    self.player.frame_index = 0
                    self.player.animation_timer = 0.0

                    if self.current_qa.is_correct(value_index):
                        self.battle_state = "PLAYER_ATTACK_DELAY"

                    else:
                        self.battle_state = "ENEMY_TURN"
            
            return

        # First menu: only active while the decision screen is visible.
        elif self.battle_state == "PLAYER_TURN":
            if self.decision_rect_1.collidepoint(mouse_pos):
                self.player_choice = "attack"
                self.battle_state = "ATTACK_MENU"
                #self.decision_active = False
                print("Attack selected")
                return

            if self.decision_rect_2.collidepoint(mouse_pos):
                self.player_choice = "idle"
                self.battle_state = "ATTACK_MENU"
                #self.decision_active = False
                print("Idle selected")
                return

            if self.decision_rect_3.collidepoint(mouse_pos):
                self.player_choice = "run"
                self.battle_state = "ATTACK_MENU"
                #self.decision_active = False
                print("Run selected")
                return

        # Second menu: only active after the player has chosen from the first menu.
        elif self.battle_state == "ATTACK_MENU":
            if self.attchoice_rect_tl.collidepoint(mouse_pos):
                print("Second menu option 1 selected")
                self.attack_choice = self.attoptions[0]
                # self.attack_delay_timer = 0.0
                # self.attack_effect_applied = False
                # self.player.state = "idle"
                # self.player.frame_index = 0
                # self.player.animation_timer = 0.0
                #self.battle_state = "PLAYER_ATTACK_DELAY"
                
                self.battle_state = "QUESTION" #!!!

                if self.current_qa is not None:
                    self.previous_qa = self.current_qa

                rand_qa = random.randint(0, len(qa_options_list) - 1)

                while self.previous_qa == qa_options_list[rand_qa]:
                    rand_qa = random.randint(0, len(qa_options_list) - 1)
                
                #if the new qa received is DIFFERENT from the one just before
                self.current_qa = qa_options_list[rand_qa]
                return

            if self.attchoice_rect_tr.collidepoint(mouse_pos):
                print("Second menu option 2 selected")
                self.attack_choice = self.attoptions[1]
                # self.attack_delay_timer = 0.0
                # self.attack_effect_applied = False
                # self.player.state = "idle"
                # self.player.frame_index = 0
                # self.player.animation_timer = 0.0
                #self.battle_state = "PLAYER_ATTACK_DELAY"

                self.battle_state = "QUESTION" #!!!

                if self.current_qa is not None:
                    self.previous_qa = self.current_qa

                rand_qa = random.randint(0, len(qa_options_list) - 1)

                while self.previous_qa == qa_options_list[rand_qa]:
                    rand_qa = random.randint(0, len(qa_options_list) - 1)
                
                #if the new qa received is DIFFERENT from the one just before
                self.current_qa = qa_options_list[rand_qa]
                return

            if self.attchoice_rect_bl.collidepoint(mouse_pos):
                print("Second menu option 3 selected")
                self.attack_choice = self.attoptions[2]
                # self.attack_delay_timer = 0.0
                # self.attack_effect_applied = False
                # self.player.state = "idle"
                # self.player.frame_index = 0
                # self.player.animation_timer = 0.0
                #self.battle_state = "PLAYER_ATTACK_DELAY"
                
                self.battle_state = "QUESTION" #!!!

                if self.current_qa is not None:
                    self.previous_qa = self.current_qa

                rand_qa = random.randint(0, len(qa_options_list) - 1)

                while self.previous_qa == qa_options_list[rand_qa]:
                    rand_qa = random.randint(0, len(qa_options_list) - 1)
                
                #if the new qa received is DIFFERENT from the one just before
                self.current_qa = qa_options_list[rand_qa]
                return

            if self.attchoice_rect_br.collidepoint(mouse_pos):
                print("Second menu option 4 selected")
                self.attack_choice = self.attoptions[3]
                # self.attack_delay_timer = 0.0
                # self.attack_effect_applied = False
                # self.player.state = "idle"
                # self.player.frame_index = 0
                # self.player.animation_timer = 0.0
                #self.battle_state = "PLAYER_ATTACK_DELAY"

                self.battle_state = "QUESTION" #!!!

                if self.current_qa is not None:
                    self.previous_qa = self.current_qa

                rand_qa = random.randint(0, len(qa_options_list) - 1)

                while self.previous_qa == qa_options_list[rand_qa]:
                    rand_qa = random.randint(0, len(qa_options_list) - 1)
                
                #if the new qa received is DIFFERENT from the one just before
                self.current_qa = qa_options_list[rand_qa]
                return

        elif self.battle_state == "VICTORY":

            if self.exit_victory_button.collidepoint(mouse_pos):
                pass #move on to the next map in the list, battle is over
        
        elif self.battle_state == "DEFEAT":

            if self.exit_victory_button.collidepoint(mouse_pos):
                pass #move on to the next map in the list, battle is over
            
    def update(self, dt):
        
        self.decision_active = (self.battle_state == "PLAYER_TURN")

        if self.battle_state == "DEFAULT":

            self.intro_timer -= dt

            self.overlay_alpha = min(self.overlay_alpha + 200 * dt, 150) # Fade in to a max alpha of 150 for the background overlay
            
            self.background_overlay.set_alpha(int(self.overlay_alpha))
            
            if self.intro_timer <= 0:
                self.battle_state = "PLAYER_TURN"
                
                self.intro_timer = 2.0 #reset timer to 2 seconds for the next attack cycle
        
        
        elif self.battle_state == "PLAYER_TURN":

            target_alpha = 150

            self.overlay_alpha += (target_alpha - self.overlay_alpha) * 5 * dt
            # if self.battle_state == "PLAYER_TURN":
            #     pass

        elif self.battle_state == "QUESTION": #??? - FIX NEXT [RESOLVED]
            #print("QUESTION STATE")
            pass
        
        elif self.battle_state == "PLAYER_ATTACK_DELAY":
            print("PLAYER ATTACK DELAY")
            self.attack_delay_timer += dt
            if self.attack_delay_timer >= self.attack_delay_duration:
                self.player.state = "attack"
                self.player.frame_index = 0
                self.player.animation_timer = 0.0
                self.player.loop_animations = False
                self.player.animation_finished = False
                self.player.reg_animation_locked = True

                print("Setting attack state")
                print(self.player.state)

                #self.battle_state = "PLAYER_ATTACK"

                self.battle_state = "PLAYER_ATTACK"

        

        #     if self.current_qa is not None:
        #         self.previous_qa = self.current_qa

        #     rand_qa = random.randint(0, len(qa_options_list) - 1)

        #     while self.previous_qa == qa_options_list[rand_qa]:
        #         rand_qa = random.randint(0, len(qa_options_list) - 1)
            
        #     #if the new qa received is DIFFERENT from the one just before
        #     self.current_qa = qa_options_list[rand_qa]

            #self.current_qa.handle_event() #?



        elif self.battle_state == "PLAYER_ATTACK":
            
            print("PLAYER_ATTACK")

            print(
                "Battle State:",
                self.battle_state,
                "Player State:",
                self.player.state
            )

            if not self.attack_effect_applied:
                self.player_attack(self.attack_choice, dt)
                self.attack_effect_applied = True

            self.player.animate(dt)
            
            #DEBUGGING
            print(
                self.player.state,
                self.player.frame_index,
                self.player.animation_finished
            )

            # if not self.attack_effect_applied:
            #     self.attack_choice.attack_effect(self.player, self.enemy)
            #     self.attack_effect_applied = True
            if self.player.animation_finished:
                
                self.player.state = "idle"
                self.player.loop_animations = True
                self.player.reg_animation_locked = False

                self.battle_state = "ENEMY_TURN"
                # if self.enemy.health <= 0:
                #     self.battle_state = "VICTORY"
                # else:
                #     self.battle_state = "ENEMY_TURN"

        elif self.battle_state == "ENEMY_ATTACK":
            self.enemy_attack()

        # elif self.battle_state == "VICTORY":
        #     self.draw_victory_screen()

        # elif self.battle_state == "DEFEAT":
        #     self.draw_defeat_screen()
        


    
    
    def player_attack(self, attack, dt):

        # self.player.state = "attack"
        # self.player.animate(dt)

        attack.attack_effect(self.player, self.enemy)

        # self.player.state = "idle"

        # if self.enemy.health <= 0:
        #     self.battle_state = "VICTORY"
        # else:
        #     self.battle_state = "ENEMY_TURN"

    # def player_attack(self, attack, screen):
        
    #     self.draw_attack_menu(screen) # placeholder for drawing the player's attack menu, will be used to allow the player to choose their attack during their turn in the future
    #     # Implement attack logic based on the player's chosen attack and the enemy's stats
    #     # For example, calculate damage, apply it to the enemy, and check for victory condition
    
    

    def enemy_attack(self):
        pass

    # def draw(self, screen):
    #     pass

    def draw(self, screen):

        # draw battle background

        # draw player

        # draw enemy
        
        #default bg when the timer is still counting down before the player's menu appears
        if self.battle_state == "DEFAULT":
            pass

        if self.battle_state == "PLAYER_TURN":
            screen.blit(self.background_overlay, (0, 0))
            self.draw_decision_menu(screen)

        elif self.battle_state == "ATTACK_MENU":
            screen.blit(self.background_overlay, (0, 0))
            self.draw_attack_menu(screen)
        
        elif self.battle_state == "QUESTION":
            #print("DRAWING QUESTION")
            self.draw_question_page(screen)

        elif self.battle_state == "VICTORY":
            screen.blit(self.background_overlay, (0, 0))
            self.draw_victory_screen(screen)

        elif self.battle_state == "DEFEAT":
            self.draw_defeat_screen(screen)

    def draw_decision_menu(self, screen):
        screen.blit(self.decision_menu, (37, 27))

        # Syntax: pygame.draw.rect(surface, color, rect, width)
        border_thickness = 3
        pygame.draw.rect(self.screen, (255, 0, 0), self.decision_rect_1, border_thickness)  # Draws a gold border
        pygame.draw.rect(self.screen, (255, 0, 0), self.decision_rect_2, border_thickness)  # Draws a gold border
        pygame.draw.rect(self.screen, (255, 0, 0), self.decision_rect_3, border_thickness)  # Draws a gold border

        
        #self.draw_attack_menu(screen) # placeholder for drawing the player's attack menu, will be used to allow the player to choose their attack during their turn in the future

    def draw_attack_menu(self, screen):
        
        screen.blit(
            self.attack_menu,
            (128, 0)
        )

        #self.draw_victory_screen(screen) # placeholder for drawing the victory screen, will be used to display a victory message and options after defeating an enemy in the future
    
    def draw_question_page(self, screen):
        
        self.current_qa.draw(screen)


    def draw_victory_screen(self, screen):
        panel = pygame.Surface((896, 640), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 220))

        panel_rect = pygame.Rect(0, 0, 896, 640)
        border_rect = panel_rect.inflate(6, 6)

        pygame.draw.rect(screen, (30, 30, 60), panel_rect, border_radius=18)
        pygame.draw.rect(screen, (255, 0, 0), border_rect, 3, border_radius=18)

        font_title = pygame.font.SysFont("Bold", 40)
        font_body = pygame.font.SysFont("Bold", 24)
        font_small = pygame.font.SysFont("Bold", 18)

        title = font_title.render("VICTORY!", True, (255, 215, 0))
        body = font_body.render("You have successfully defeated the enemy.", True, (235, 245, 255))
        hint = font_small.render("Press ESC or return to continue.", True, (200, 220, 255))

        title_rect = title.get_rect()
        title_rect.center = screen.get_rect().center
        title_rect.centery -= 80

        body_rect = body.get_rect()
        body_rect.center = screen.get_rect().center
        body_rect.centery -= 20

        hint_rect = hint.get_rect()
        hint_rect.center = screen.get_rect().center
        hint_rect.centery += 20

        screen.blit(panel, panel_rect.topleft)
        screen.blit(title, title_rect)
        screen.blit(body, body_rect)
        screen.blit(hint, hint_rect)

    def draw_defeat_screen(self, screen):
        pass