import pygame
import sys

# Initialize Pygame
# pygame.init()

# Constants
SCREEN_WIDTH = 896 #1200 diff: -304
SCREEN_HEIGHT = 640 #675 diff: -35
FPS = 60

# Color Palette (Matching your UI assets)
DARK_BLUE = (6, 18, 36)      # Base background
BOX_BG = (12, 32, 64)         # Option box interior
BORDER_GOLD = (218, 165, 32)  # Normal gold border
HOVER_GOLD = (255, 223, 0)    # Bright gold for interaction
TEXT_WHITE = (240, 240, 240)
TEXT_GOLD = (245, 215, 120)

# Set up screen
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Dynastic - Question Screen")
# clock = pygame.time.Clock()

# Fonts (Using system defaults; substitute with custom .ttf files if needed)
font_title = pygame.font.SysFont("cambria", 40, bold=True)
font_question = pygame.font.SysFont("cambria", 26)
font_option = pygame.font.SysFont("cambria", 22, bold=True)
font_sub = pygame.font.SysFont("cambria", 16, italic=True)

class QuestionScreen:
    def __init__(self, q_text, ans_options, correct_ans): #q_text is the question text, will be randomized from a list of premade questions
        # 1. Top Question Box Layout
        self.question_rect = pygame.Rect(80, 120, 736, 105)
        self.question_text = q_text
        
        # 2. 4 Ans_Options Layout (2x2 Grid)
        # Grid parameters
        start_x = 80
        start_y = 290
        box_w = 353
        box_h = 100
        gap_x = 30
        gap_y = 20
        
        self.ans_options = [
            {"rect": pygame.Rect(start_x, start_y, box_w, box_h), "title": ans_options[0][0], "sub": ans_options[0][1]},
            {"rect": pygame.Rect(start_x + box_w + gap_x, start_y, box_w, box_h), "title": ans_options[1][0], "sub": ans_options[1][1]},
            {"rect": pygame.Rect(start_x, start_y + box_h + gap_y, box_w, box_h), "title": ans_options[2][0], "sub": ans_options[2][1]},
            {"rect": pygame.Rect(start_x + box_w + gap_x, start_y + box_h + gap_y, box_w, box_h), "title": ans_options[3][0], "sub": ans_options[3][1]}
        ]

        self.correct_ans = self.ans_options[0]["title"]
        
        # 3. Bottom Action Buttons
        self.submit_rect = pygame.Rect(233, 560, 200, 50)
        self.back_rect = pygame.Rect(464, 560, 200, 50)
        
        self.selected_option = None
        self.correct_ans_index = correct_ans

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Check if an option box was clicked
            for idx, opt in enumerate(self.ans_options):
                if opt["rect"].collidepoint(mouse_pos):
                    self.selected_option = idx
                    print(f"Selected Option: {opt['title']}")
                    
            # Check Action Buttons
            if self.submit_rect.collidepoint(mouse_pos):

                if self.selected_option is not None:
                    return ("submit", self.selected_option)
                #print(f"Submitting Choice: {self.selected_option}")
                # Add transition logic here

            elif self.back_rect.collidepoint(mouse_pos):
                
                return ("back", None)
                #print("Going Back") 
                # Add scene switching logic here

            return (None, None)
    
    def is_correct(self, selected_index):
        return selected_index == self.correct_ans_index

    def draw(self, screen):
        # Fill deep dark blue background
        # background = pygame.Surface((896, 640), pygame.SRCALPHA)
        # background.fill(DARK_BLUE)
        
        screen.fill(DARK_BLUE)

        mouse_pos = pygame.mouse.get_pos()
        
        # --- DRAW HEADER TEXT ---
        title_surf = font_title.render("CHALLENGE", True, TEXT_GOLD)
        screen.blit(title_surf, (screen.width // 2 - title_surf.get_width() // 2, 40))
        
        # --- DRAW QUESTION BOX ---
        pygame.draw.rect(screen, BOX_BG, self.question_rect)
        pygame.draw.rect(screen, BORDER_GOLD, self.question_rect, 3) # Outer border
        pygame.draw.rect(screen, BORDER_GOLD, self.question_rect.inflate(-10, -10), 1) # Decorative inner thin border
        
        q_text_surf = font_question.render(self.question_text, True, TEXT_GOLD)
        screen.blit(q_text_surf, (self.question_rect.centerx - q_text_surf.get_width() // 2, 
                                   self.question_rect.centery - q_text_surf.get_height() // 2))

        # --- DRAW 2x2 GRID OPTIONS ---
        for index, option in enumerate(self.ans_options):
            rect = option["rect"]
            is_hovered = rect.collidepoint(mouse_pos)
            is_selected = (self.selected_option == index)
            
            # Determine Border Color based on state
            if is_selected:
                border_color = HOVER_GOLD
                bg_color = (20, 50, 95) # Distinct background color if selected
            elif is_hovered:
                border_color = HOVER_GOLD
                bg_color = BOX_BG
            else:
                border_color = BORDER_GOLD
                bg_color = BOX_BG
                
            # Draw option container box
            pygame.draw.rect(screen, bg_color, rect)

            if not is_selected:
                #pygame.draw.rect(surface, border_color, rect, 2 if not is_selected else 4)

                pygame.draw.rect(screen, border_color, rect, 2)
            else:
                pygame.draw.rect(screen, border_color, rect, 4)

            # Render Option Titles and Descriptions
            title_color = HOVER_GOLD if (is_hovered or is_selected) else TEXT_WHITE
            t_surf = font_option.render(option["title"], True, title_color)
            s_surf = font_sub.render(option["sub"], True, TEXT_GOLD)
            
            # Left-align text inside the boxes with some padding
            screen.blit(t_surf, (rect.x + 30, rect.y + 22))
            screen.blit(s_surf, (rect.x + 30, rect.y + 55))

        # --- DRAW UTILITY BUTTONS (SUBMIT / BACK) ---
        for btn_rect, btn_text in [(self.submit_rect, "SUBMIT"), (self.back_rect, "BACK")]:
            btn_hover = btn_rect.collidepoint(mouse_pos)
            btn_border = HOVER_GOLD if btn_hover else BORDER_GOLD
            
            pygame.draw.rect(screen, BOX_BG, btn_rect)
            pygame.draw.rect(screen, btn_border, btn_rect, 2)
            
            btn_surf = font_option.render(btn_text, True, TEXT_GOLD)
            screen.blit(btn_surf, (btn_rect.centerx - btn_surf.get_width() // 2, 
                                    btn_rect.centery - btn_surf.get_height() // 2))

        #screen.blit(background, (0, 0))


# if __name__ == "__main__":
#     # Initialize state handler
#     question_screen = QuestionScreen("FAVOURITE ANIMAL?", [["A. LERNAEAN HYDRA", "REGENERATES HEADS"],
#                                                         ["B. GRIFFIN", "HALF EAGLE, HALF LION"],
#                                                         ["C. CHIMERA", "LION, GOAT, SNAKE PARTS"],
#                                                         ["D. CERBERUS", "GUARD OF THE UNDERWORLD"]], 2)

#     # Game Loop
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
                
#             question_screen.handle_event(event)
            
#         # Render loop
#         question_screen.draw(screen)
#         pygame.display.update()
#         #clock.tick(FPS)